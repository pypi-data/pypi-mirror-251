import enum
import json
import logging
import urllib.request
from contextlib import contextmanager
from dataclasses import dataclass
from typing import IO, Any, AnyStr, Generator, Union

from numerous.grpc.spm_pb2 import FilePath, FilePaths
from numerous.grpc.spm_pb2_grpc import FileManagerStub

logger = logging.getLogger(__name__)


@dataclass
class Parameter:  # will be used as a base-class later for implementing specific functionality
    id: str
    uuid: str
    display_name: str
    type: str
    value: Any

    @staticmethod
    def from_document(
        data: dict[str, Any], file_manager_client: FileManagerStub
    ) -> "Parameter":
        return Parameter(
            id=data["id"],
            uuid=data["uuid"],
            display_name=data["displayName"],
            type=data["type"],
            value=parse_value(
                data["value"], data["type"], file_manager_client=file_manager_client
            ),
        )


@dataclass
class FileReference:
    id: str
    path: str
    name: str
    file_manager_client: FileManagerStub

    @staticmethod
    def from_document(
        data: dict[str, Any], file_manager_client: FileManagerStub
    ) -> "FileReference":
        return FileReference(
            data["id"],
            data["path"],
            data["name"],
            file_manager_client=file_manager_client,
        )

    def get_file_url(self) -> str:
        return (
            self.file_manager_client.GetDownloadUrls(
                request=FilePaths(
                    file_paths=[FilePath(path=self.path, content_type="text/plain")]
                )
            )
            .urls[0]
            .url
        )

    @contextmanager
    def open(self) -> Generator[IO, None, None]:
        try:
            url = self.get_file_url()
            filepath, headers = urllib.request.urlretrieve(url)  # nosec

            with open(filepath, "r") as f:
                yield f

        except Exception as e:
            logger.exception(f"Error while downloading file: {e}")
            raise

    def read_json(self) -> Union[dict, list]:
        with self.open() as f:
            return json.load(f)

    def read_text(self) -> AnyStr:
        with self.open() as f:
            return f.read()


class SimTimeUnit(enum.Enum):
    years = "years"
    months = "months"
    days = "days"
    hours = "hours"
    minutes = "minutes"
    seconds = "seconds"

    @classmethod
    def from_string(cls, value_str) -> "SimTimeUnit":
        for member in cls:
            if member.value == value_str:
                return member
        raise ValueError(f"No matching enum member for value: {value_str}")


@dataclass
class Currency:
    name: str
    code: str

    @staticmethod
    def from_document(data: dict[str, Any]) -> "Currency":
        return Currency(data["name"], data["code"])


@dataclass
class Month:
    value: int

    @staticmethod
    def from_document(data: dict[str, Any]) -> "Month":
        return Month(data["value"])


@dataclass
class MapLocation:
    id: str
    name: str
    center: tuple[float, float]

    @staticmethod
    def from_document(data: dict[str, Any]) -> "MapLocation":
        return MapLocation(data["id"], data["name"], data["center"])


@dataclass
class TimeValue:
    value: float
    unit: SimTimeUnit

    @staticmethod
    def from_document(data: dict[str, Any]) -> "TimeValue":
        return TimeValue(float(data["value"]), SimTimeUnit.from_string(data["unit"]))


@dataclass
class Config:
    value: str

    @staticmethod
    def from_document(data: dict[str, Any]) -> "Config":
        return Config(data["value"])


@dataclass
class Selector:
    value: Union[str, float, int]

    @staticmethod
    def from_document(data: dict[str, Any]) -> "Selector":
        return Selector(data["value"])


def parse_value(value: Any, type_: Any, file_manager_client: FileManagerStub) -> Any:
    if type_ == "string":
        return value
    elif type_ == "number":
        return float(value)
    elif type_ == "boolean":
        return value
    elif type_ == "file":
        return FileReference.from_document(value, file_manager_client)
    elif type_ == "json":
        return json.loads(value)
    elif type_ == "time_value":
        return TimeValue.from_document(value)
    elif type_ == "currency":
        return Currency.from_document(value)
    elif type_ == "month":
        return Month.from_document(value)
    elif type_ == "map":
        return MapLocation.from_document(value)
    elif type_ == "config":
        return Config.from_document(value)
    elif type_ == "selecter":
        return Selector.from_document(value)
    raise ValueError(f"Unkwnown parameter type: {type_}")


def get_parameters_dict(
    data: list[dict[str, Any]], file_manager_client: FileManagerStub
) -> dict[str, Parameter]:
    return {
        param.id: param
        for param in get_parameters_list(data, file_manager_client=file_manager_client)
    }


def get_parameters_list(
    data: list[dict[str, Any]], file_manager_client: FileManagerStub
) -> list[Parameter]:
    return [Parameter.from_document(param, file_manager_client) for param in data]

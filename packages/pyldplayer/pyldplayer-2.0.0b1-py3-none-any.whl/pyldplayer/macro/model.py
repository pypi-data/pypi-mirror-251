
from dataclasses import dataclass
from pydantic import BaseModel
import typing
import json

class Point(typing.TypedDict):
    id: int
    x: int
    y: int
    state: int

@dataclass(slots=True)
class PutMultiTouch:
    timing: int
    operationId: str
    points: typing.List[Point]

@dataclass(slots=True)
class PutScanCode:
    timing: int
    operationId: str
    code : int
    down : bool

@dataclass(slots=True)
class RecordInfo:
    loopType: int
    loopTimes: int
    circleDuration: int
    loopInterval: int
    loopDuration: int
    accelerateTimes: int
    accelerateTimesEx: int
    recordName: str
    createTime: str
    playOnBoot: bool
    rebootTiming: int

class LDRecord(BaseModel):
    operations : typing.List[typing.Union[PutMultiTouch, PutScanCode]]
    recordInfo : RecordInfo

    @classmethod
    def fromPath(cls, path : str):
        with open(path, "r") as f:
            rawdata = json.load(f)
        return cls(**rawdata)

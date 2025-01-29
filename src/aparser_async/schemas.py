"""Схемы для валидации данных и генерации json A-Parser"""
import enum
# pylint: disable=missing-class-docstring
from typing import Literal, Optional, Union, Any
from pydantic import BaseModel, Json

__all__ = ('PingRequest', 'BaseRequest', 'OverrideOptions', 'OverrideOptionsAdditional', 'IteratorOptions',
           'ResultsOptions', 'Data', 'AddTaskRequest', 'TaskUidData', 'GetTaskState', 'GetTaskResultFile',
           'DeleteTaskResultFile', 'ResponseParsed', 'StatusState', 'TaskStatus', 'TaskChangeStatus',
           'ProxyCheckerState', 'ChangeProxyCheckerState')


class TaskChangeStatus(str, enum.Enum):
    STARTING = "starting"  # Launching a task
    PAUSING = "pausing"  # Putting the task on pause
    STOPPING = "stopping"  # Stopping the task
    DELETING = "deleting"  # Deleting the task


class BaseRequest(BaseModel):
    password: str
    action: Literal["ping", "oneRequest", "bulkRequest", "addTask", "getTaskState", "getTaskResultsFile",
    "getTasksList", "changeTaskStatus", "moveTask", "changeProxyCheckerState"]


class PingRequest(BaseRequest):
    action: str = "ping"


class OverrideOptions(BaseModel):
    type: Optional[str] = "override"
    id: str
    value: Union[int, bool, str]


class OverrideOptionsAdditional(OverrideOptions):
    additional: Json[Any]


class IteratorOptions(BaseModel):
    onAllLevels: Optional[bool] = False
    queryBuildersAfterIterator: Optional[bool] = False
    queryBuildersOnAllLevels: Optional[bool] = False


class ResultsOptions(BaseModel):
    overwrite: Optional[bool] = False
    writeBOM: Optional[bool] = False


class Data(BaseModel):
    preset: Optional[str] = "default"
    configPreset: Optional[str] = "default"
    parsers: list[list[Union[str, OverrideOptions, OverrideOptionsAdditional]]]
    resultsFormat: Optional[str] = "$p1.preset"
    resultsSaveTo: Optional[str] = "file"
    resultsFileName: Optional[str] = "$datefile.format().txt"
    additionalFormats: Optional[list[str]] = []
    resultsUnique: Optional[Literal["no", "yes"]] = "no"
    queriesFrom: Optional[str] = "text"
    queryFormat: Optional[list[str]] = ["$query"]
    uniqueQueries: Optional[bool] = False
    saveFailedQueries: Optional[bool] = False
    iteratorOptions: Optional[IteratorOptions] = IteratorOptions()
    resultsOptions: Optional[ResultsOptions] = ResultsOptions()
    doLog: Optional[Literal["no", "yes"]] = "no"
    limitLogsCount: Optional[str] = "0"
    keepUnique: Optional[Literal["no", "yes"]] = "no"
    moreOptions: Optional[bool] = False
    resultsPrepend: Optional[str] = ""
    resultsAppend: Optional[str] = ""
    queryBuilders: Optional[list[str]] = []
    resultsBuilders: Optional[list[str]] = []
    configOverrides: Optional[list[str]] = []
    runTaskOnComplete: Optional[int] = None
    useResultsFileAsQueriesFile: Optional[bool] = False
    runTaskOnCompleteConfig: Optional[str] = "default"
    toolsJS: Optional[str] = ""
    prio: Optional[int] = 5
    removeOnComplete: Optional[bool] = False
    callURLOnComplete: Optional[str] = ""
    stopOnError: Optional[bool] = False
    queries: str


class AddTaskRequest(BaseRequest):
    action: str = "addTask"
    data: Data


class TaskUidData(BaseModel):
    taskUid: int


class ToStatus(TaskUidData):
    toStatus: TaskChangeStatus


class GetTaskState(BaseRequest):
    action: str = "getTaskState"
    data: TaskUidData


class ChangeTaskStatus(BaseRequest):
    action: str = "changeTaskStatus"
    data: ToStatus


class GetTaskResultFile(BaseRequest):
    action: str = "getTaskResultsFile"
    data: TaskUidData


class DeleteTaskResultFile(BaseRequest):
    action: str = "deleteTaskResultsFile"
    data: TaskUidData


class ResponseParsed(BaseModel):
    success: int
    data: Optional[Any] = None


class StatusState(BaseModel):
    totalFail: int
    totalWaitProxyThreads: Optional[int] = None
    minimized: int
    queriesDoneCount: int
    avgSpeed: int
    activeThreads: Union[int, Literal['none']] = None
    startTime: int
    changeTime: int
    queriesCount: int
    logExists: int
    runTime: Optional[int] = None
    uniqueResultsCount: Union[int, Literal['none']] = None
    requests: int
    addTime: int
    additionalCount: int
    queriesDoneCountAtStart: Optional[int] = None
    lastQuery: str
    curSpeed: int
    started: int
    resultsCount: int


class TaskStatus(BaseModel):
    status: str
    stats: Any
    state: StatusState


class ProxyCheckerState(BaseModel):
    checker: str
    state: Literal[0, 1]


class ChangeProxyCheckerState(BaseRequest):
    action: str = "changeProxyCheckerState"
    data: ProxyCheckerState

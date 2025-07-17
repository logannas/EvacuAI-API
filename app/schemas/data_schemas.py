from pydantic import BaseModel
from typing import Optional, Dict


class Project(BaseModel):
    project_name: str
    image: str
    nodes: str
    edges: str
    layouts: str


class ListDatas(BaseModel):
    created: str


class Hyperparameters(BaseModel):
    beta: Optional[float] = None
    lr: Optional[float] = None
    batch_size: Optional[int] = None
    buffer_size: Optional[int] = None
    episodes: Optional[int] = None
    gamma: Optional[float] = None
    epsilon: Optional[float] = None
    num_virtual_agents: Optional[int] = None
    reward_exit: Optional[float] = None
    reward_fire: Optional[float] = None
    reward_invalid: Optional[float] = None
    reward_valid: Optional[float] = None
    reward_congestion: Optional[float] = None
    p_random_neighbor: Optional[float] = None
    congestion_threshold: Optional[int] = None


class InfoDatas(BaseModel):
    project: str


class DatasReturn(BaseModel):
    project_id: str


class InferenceTime(BaseModel):
    created: str
    project: str
    createdTime: str
    block: Optional[str] = None
    init_node: Optional[str] = None
    close_nodes_sense: Optional[Dict] = {}
    close_node_wo_sense: Optional[Dict] = {}


class PathModel(BaseModel):
    init_node: int
    last_node: int
    path: list[int]


class InferenceResponseModel(BaseModel):
    predictions: list[PathModel]

from fastapi import APIRouter, Depends, Request, Query
import app.core.grpc.evacuai_rl_pb2 as evacuai_rl_pb2
from typing import List, Optional
from app.core.grpc.grpc_client import get_grpc_stub
from google.protobuf.json_format import MessageToDict
from app.schemas.data_schemas import InferenceResponseModel

router = APIRouter()


@router.get("/")
async def run_inference(
    project_id: str,
    version: str,
    state: Optional[int] = None,
    fire_nodes: List[int] = Query(default=[]),
    congestion_nodes: List[int] = Query(default=[]),
    stub=Depends(get_grpc_stub),
):
    inference_request = evacuai_rl_pb2.InferenceRequest(
        project_id=project_id,
        version=version or "",
        previous_state=state if state is not None else 0,
        fire_nodes=fire_nodes,
        agents_positions=congestion_nodes,
    )

    response = stub.Inference(inference_request)

    response_dict = MessageToDict(
        response,
        preserving_proto_field_name=True,
    )
    for prediction in response_dict.get("predictions", []):
        if "last_node" not in prediction:
            path = prediction.get("path", [])
            if path:
                prediction["last_node"] = path[-1]  # usa o último valor do path
            else:
                prediction["last_node"] = None  # ou trate conforme sua lógica

    return {"predictions": response_dict["predictions"]}

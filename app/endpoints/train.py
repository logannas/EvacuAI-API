from fastapi import APIRouter, Depends

from app.schemas.data_schemas import InfoDatas, Hyperparameters
from app.core.grpc.grpc_client import get_grpc_stub
import app.core.grpc.evacuai_rl_pb2 as evacuai_rl_pb2

router = APIRouter()


@router.post("")
async def train_project(
    info: InfoDatas, hyperparameters: Hyperparameters, stub=Depends(get_grpc_stub)
):
    hyp_dict = hyperparameters.dict(exclude_unset=True)

    hyp_params = evacuai_rl_pb2.HypParams(**hyp_dict)

    print(hyp_params)
    train_request = evacuai_rl_pb2.TrainRequest(
        hyperparameters=hyp_params,
        project_id=info.project,
    )

    response = stub.TrainModel(train_request)
    return {"model_id": response.model_id}

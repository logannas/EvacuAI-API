from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from minio import Minio
from app.core.minio_config import get_minio_client, list_files

router = APIRouter()


@router.get("/{project_id}")
async def list_train_ids(
    project_id: str,
    minio_client: Minio = Depends(get_minio_client),
):
    prefix = f"experiments/{project_id}/"
    objects = await list_files(minio_client, prefix)

    train_ids = set()

    for obj in objects:
        parts = obj.object_name.split("/")
        if len(parts) >= 3:
            train_id = parts[2]
            train_ids.add(train_id)

    return JSONResponse(content=sorted(list(train_ids)))

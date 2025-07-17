from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import base64
from app.db.mongodb import get_mongodb
from app.core.minio_config import get_minio_client
from app.core.minio_config import download_minio
import json

router = APIRouter()


@router.get("")
async def list_projects(
    minio_client=Depends(get_minio_client), mongodb: tuple = Depends(get_mongodb)
):
    _, _, collection = mongodb
    projects = collection.find()

    project_list = []

    for project in projects:
        project_id = project["project_id"]
        project_name = project["project_name"]
        image_path = project.get("image_s3_uri")
        graph_path = project.get("graph_s3_uri")

        # Baixa a imagem do MinIO
        image_bytes = await download_minio(minio_client, image_path)
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        graph_bytes = await download_minio(minio_client, graph_path)
        graph_str = graph_bytes.decode("utf-8")
        graph = json.loads(graph_str)

        project_list.append(
            {
                "project_id": project_id,
                "project_name": project_name,
                "graph_nodes": graph["nodes"],
                "image_base64": f"data:image/svg+xml;base64,{image_base64}",
            }
        )

    return JSONResponse(content=project_list)

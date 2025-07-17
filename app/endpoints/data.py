from fastapi import APIRouter, Depends
import json
import re
import base64
import random
import string
import hashlib
import datetime
import io

from app.schemas.data_schemas import Project, DatasReturn
from app.db.mongodb import get_mongodb
from app.core.minio_config import get_minio_client
from app.core.minio_config import upload_minio
from app.utils.calculate_distance import calculate_distance

router = APIRouter()


@router.post("")
async def add_data(
    Project: Project,
    minio_client=Depends(get_minio_client),
    mongodb: tuple = Depends(get_mongodb),
):
    _, _, collection = mongodb
    # Decodifica a imagem
    image_data = re.sub("^data:image/.+;base64,", "", Project.image)
    im_bytes = base64.b64decode(image_data)

    # Converte strings JSON em dicionários
    nodes = json.loads(Project.nodes)
    edges = json.loads(Project.edges)
    layouts = json.loads(Project.layouts)

    graph_dict = {"nodes": nodes, "edges": edges, "layouts": layouts}

    graph_dict = calculate_distance(graph_dict)

    # Gera um identificador único
    random_str = "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(6)
    )
    str_final = Project.project_name + random_str
    file_id = hashlib.md5(str_final.encode("utf-8")).hexdigest()

    # Faz upload da imagem no MinIO
    await upload_minio(
        minio_client, f"images/{file_id}.svg", im_bytes, content_type="image/svg+xml"
    )
    # Faz upload do grafo no MinIO
    json_data = json.dumps(graph_dict)
    json_bytes = json_data.encode("utf-8")
    await upload_minio(
        minio_client,
        f"graph/{file_id}.json",
        json_bytes,
        content_type="application/json",
    )

    # Configuração inicial do projeto
    configs_project = {
        "project_id": file_id,
        "project_name": Project.project_name,
        "image_s3_uri": f"images/{file_id}.svg",
        "graph_s3_uri": f"graph/{file_id}.json",
        "createdTime": datetime.datetime.now().isoformat(),
    }

    # Insere os dados no MongoDB
    collection.insert_one(configs_project)

    return DatasReturn(project_id=file_id)

from fastapi import FastAPI
from app.endpoints import data, inference, list_projects, list_trains, train
from app.db.mongodb import get_mongodb
from app.core.minio_config import get_minio_client
from app.core.grpc.grpc_client import init_grpc_client
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="EvacuaAI", version="0.0.1")

origins = [
    "http://localhost:3000",  # Exemplo: URL do seu frontend React (se houver)
    "http://localhost",  # Caso seu frontend rode na mesma máquina em outra porta
    "*",  # Permite todas as origens (apenas para desenvolvimento!)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas do módulo users
app.include_router(data.router, prefix="/create", tags=["Data"])
app.include_router(inference.router, prefix="/inference", tags=["Inferece"])
app.include_router(list_projects.router, prefix="/projects", tags=["Projects"])
app.include_router(list_trains.router, prefix="/train_ids", tags=["Projects"])
app.include_router(train.router, prefix="/train_project", tags=["Train"])

mongodb_col = None
minio_client = None


@app.on_event("startup")
def startup_db():
    global mongodb_client, mongodb_db, mongodb_col, minio_client
    mongodb_client, mongodb_db, mongodb_col = get_mongodb()  # Conectar ao MongoDB
    minio_client = get_minio_client()  # Conectar ao MinIO
    init_grpc_client(app, "localhost:50051")
    print("✅ Connection to MongoDB, MinIO adn Grpc Server established!")


@app.on_event("shutdown")
def shutdown_db():
    global mongodb_client
    if mongodb_client:
        mongodb_client.close()
    app.state.grpc_channel.close()
    print("🔴 MongoDB and Grpc Server connection closed!")


@app.get("/")
def root():
    return {"message": "EvacuaAI API started."}

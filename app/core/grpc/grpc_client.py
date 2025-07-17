import grpc
from fastapi import Request

import app.core.grpc.evacuai_rl_pb2_grpc as evacuai_rl_pb2_grpc


def init_grpc_client(app, target: str):
    """
    Inicializa o cliente gRPC e salva na instância do app FastAPI.
    """
    channel = grpc.insecure_channel(target)
    stub = evacuai_rl_pb2_grpc.ReinforcementLearningStub(channel)
    app.state.grpc_channel = channel
    app.state.grpc_stub = stub


def close_grpc_client(app):
    """
    Fecha o canal gRPC se estiver presente.
    """
    if hasattr(app.state, "grpc_channel"):
        app.state.grpc_channel.close()


def get_grpc_stub(request: Request):
    """
    Função usada no Depends para obter o stub gRPC.
    """
    return request.app.state.grpc_stub

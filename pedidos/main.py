from fastapi import FastAPI
from pydantic import BaseModel
import uuid

app = FastAPI(title="Pedidos Service")

class Pedido(BaseModel):
    item_id: int
    quantidade: int

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/pedidos/")
def criar_pedido(pedido: Pedido):
    # Lógica simplificada de banco de dados
    pedido_id = str(uuid.uuid4())
    return {"id": pedido_id, "item_id": pedido.item_id, "quantidade": pedido.quantidade, "status": "criado"}

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Pagamentos Service")

class Pagamento(BaseModel):
    pedido_id: str
    valor: float

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/pagamentos/")
def processar_pagamento(pagamento: Pagamento):
    # Simula integração externa
    return {"pedido_id": pagamento.pedido_id, "status": "aprovado", "transacao_id": "tx-12345"}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Estoque Service")

# Mock banco de dados
estoque_db = {
    1: {"quantidade": 100},
    2: {"quantidade": 50}
}

class BaixaEstoque(BaseModel):
    item_id: int
    quantidade: int

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/estoque/{item_id}")
def consultar_estoque(item_id: int):
    item = estoque_db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return {"item_id": item_id, "quantidade": item["quantidade"]}

@app.post("/estoque/baixa")
def baixar_estoque(baixa: BaixaEstoque):
    item = estoque_db.get(baixa.item_id)
    if not item or item["quantidade"] < baixa.quantidade:
        raise HTTPException(status_code=400, detail="Estoque insuficiente")
    
    estoque_db[baixa.item_id]["quantidade"] -= baixa.quantidade
    return {"item_id": baixa.item_id, "nova_quantidade": estoque_db[baixa.item_id]["quantidade"]}

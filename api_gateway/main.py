from fastapi import FastAPI, HTTPException
import httpx
import os

app = FastAPI(title="API Gateway - Loja Veloz")

PEDIDOS_URL = os.getenv("PEDIDOS_URL", "http://localhost:8001")
PAGAMENTOS_URL = os.getenv("PAGAMENTOS_URL", "http://localhost:8002")
ESTOQUE_URL = os.getenv("ESTOQUE_URL", "http://localhost:8003")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/pedidos/")
async def criar_pedido(item_id: int, quantidade: int):
    async with httpx.AsyncClient() as client:
        # 1. Verifica estoque
        estoque_resp = await client.get(f"{ESTOQUE_URL}/estoque/{item_id}")
        if estoque_resp.status_code != 200 or estoque_resp.json().get("quantidade", 0) < quantidade:
            raise HTTPException(status_code=400, detail="Estoque insuficiente")
        
        # 2. Cria pedido
        pedido_resp = await client.post(f"{PEDIDOS_URL}/pedidos/", json={"item_id": item_id, "quantidade": quantidade})
        pedido = pedido_resp.json()
        
        # 3. Processa Pagamento
        pagamento_resp = await client.post(f"{PAGAMENTOS_URL}/pagamentos/", json={"pedido_id": pedido["id"], "valor": 100.0})
        
        # 4. Baixa no estoque
        await client.post(f"{ESTOQUE_URL}/estoque/baixa", json={"item_id": item_id, "quantidade": quantidade})
        
        return {"status": "Pedido processado com sucesso", "pedido": pedido, "pagamento": pagamento_resp.json()}

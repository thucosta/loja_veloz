# Loja Veloz - Plataforma de Pedidos em Microsserviços

Este repositório contém a solução completa para o desafio da Loja Veloz, contemplando microsserviços em Python (FastAPI), conteinerização, orquestração Kubernetes, CI/CD e Infraestrutura como Código (Terraform).

## Estrutura do Projeto

- `/api_gateway`: Serviço Gateway que centraliza e roteia as requisições.
- `/pedidos`: Serviço de Pedidos.
- `/pagamentos`: Serviço de Pagamentos.
- `/estoque`: Serviço de Estoque.
- `/k8s`: Manifests do Kubernetes (Deployments, Services, ConfigMaps, Secrets, HPA).
- `/terraform`: Esqueleto de Infraestrutura como Código para AWS EKS.
- `docker-compose.yml`: Arquivo para subir o ambiente localmente.
- `.github/workflows/ci.yml`: Pipeline de CI/CD para o GitHub Actions.

## Como rodar localmente (Docker Compose)

1. Certifique-se de ter o Docker e Docker Compose instalados.
2. Execute o comando:
   ```bash
   docker-compose up --build -d
   ```
3. A API Gateway estará disponível em `http://localhost:8000`. Você pode testar os endpoints através da documentação do Swagger em `http://localhost:8000/docs`.

## Relatórios

- [Relatório Teórico (Parte 1)](RELATORIO_TEORICO.md)
- [Relatório Prático (Parte 2)](RELATORIO_PRATICO.md)

## Segurança e Otimização

Foi utilizado FastAPI para garantir performance e documentação nativa. Além disso, as imagens Docker utilizam `multi-stage builds` e usuário `non-root` para maior segurança. Recomendamos o uso de ferramentas como **OWASP ZAP** para análise de vulnerabilidades.

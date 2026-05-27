# Relatório Prático - Loja Veloz

## 1. Ambiente Local (Docker Compose)
Foi desenvolvida uma arquitetura com 4 microsserviços (`api_gateway`, `pedidos`, `pagamentos`, `estoque`). 
Através do arquivo `docker-compose.yml`, todos os serviços são inicializados em uma rede isolada do tipo `bridge` (`loja_rede`), garantindo a comunicação interna através de DNS interno (ex: o gateway chama o serviço de pedidos pela URL `http://pedidos:8000`).
Para subir o projeto localmente, basta rodar:
```bash
docker-compose up --build -d
```

## 2. Conteinerização e Versionamento
Os `Dockerfiles` de cada serviço seguem as melhores práticas:
- **Multi-stage builds:** O primeiro estágio (builder) instala as dependências e gera os pacotes *wheel*. O segundo estágio (run) apenas copia esses arquivos e a aplicação, resultando em imagens leves (baseadas no `python:3.11-slim`).
- **Segurança (Non-Root):** Um usuário `appuser` é criado, e o comando `USER appuser` é utilizado antes do `CMD`, mitigando riscos de segurança críticos (como fuga de privilégios do contêiner).

## 3. Kubernetes (Ambiente de Produção Mínimo)
No diretório `/k8s`, encontram-se os manifests essenciais para o cluster da Loja Veloz:
- **Deployments e Services:** Cada microsserviço tem seu Deployment com 2 réplicas (garantindo redundância) e um Service correspondente.
- **ConfigMaps e Secrets:** As URLs dos serviços são injetadas através de variáveis de ambiente gerenciadas por um `ConfigMap`. Credenciais sensíveis, como a senha do banco de dados, estão base64-encoded no `Secret`.
- **Probes:** Foram configurados `livenessProbe` e `readinessProbe` baseados no endpoint `/health` de cada serviço. Se a aplicação travar, o K8s fará o restart automático.
- **HPA:** O arquivo `hpa.yaml` define o *Horizontal Pod Autoscaler* para o API Gateway, monitorando o limite de CPU (70%) para escalar as réplicas de 2 até 10 instâncias.

## 4. Pipeline de CI/CD
A automação está garantida via GitHub Actions (`.github/workflows/ci.yml`). O pipeline executa 3 jobs principais:
1. **Build e Testes (`build-and-test`):** Baixa o código, instala o Python, dependências e simula a execução do Pytest para cada serviço usando matrizes (`matrix`).
2. **Build e Push de Imagem (`docker-build-push`):** Se os testes passarem e o código estiver na branch `main`, imagens Docker são construídas e enviadas para o DockerHub (`lojaveloz/api_gateway:latest`, etc.).
3. **Deploy Contínuo (`deploy-k8s`):** Configura o `kubectl` usando o Kubeconfig injetado pelas *Secrets* do GitHub, e aplica todos os manifests da pasta `k8s` diretamente no cluster.

## 5. Observabilidade, Deploy e Escala
- **Estratégia de Deploy:** Utiliza-se a estratégia de **Rolling Update** nativa do K8s (atualiza os pods gradualmente, mantendo o serviço sempre disponível).
- **Observabilidade:** Foi desenhada a injeção do cabeçalho de tracing via API Gateway usando bibliotecas *OpenTelemetry*. Recomenda-se exportar as métricas padrão da aplicação (latência, taxas de erro 4xx/5xx e volume de requisições HTTP) para um servidor *Prometheus* e visualizar no *Grafana*.
- **Infraestrutura:** O provisionamento da nuvem (cluster EKS na AWS) foi codificado em Terraform (`/terraform/main.tf`), provisionando módulos seguros e modulares de VPC (Redes Privadas) e os Node Groups do Kubernetes.

## 6. Referência Pública (Fonte de Pesquisa)
Para arquitetar essa solução, utilizamos como caso de sucesso e referência primária a documentação oficial da AWS e do Google Cloud Architecture Center. Especificamente:
- A abordagem de orquestração de e-commerce é fortemente inspirada no projeto **Google Cloud Microservices Demo (Online Boutique)** (https://github.com/GoogleCloudPlatform/microservices-demo), que aplica um micro-ecossistema similar contendo Cart, Payment, e Checkout services em gRPC/HTTP e os gerencia via GKE e Kubernetes nativo com foco total em confiabilidade e *zero-downtime deploys*.

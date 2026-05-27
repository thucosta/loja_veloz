# Relatório Teórico - Loja Veloz

## 1. Arquitetura de Microsserviços e o Papel do DevOps

A arquitetura de microsserviços divide uma aplicação em pequenos serviços independentes que se comunicam via rede (geralmente APIs REST ou mensageria). Diferente do modelo monolítico, onde qualquer falha ou pico de acesso afeta todo o sistema, os microsserviços permitem escalar partes específicas da aplicação (ex: apenas o módulo de Estoque durante a Black Friday). 

O DevOps atua como o catalisador dessa arquitetura em ambientes *cloud-native*. Sem automação, gerenciar dezenas de microsserviços seria impossível. Práticas DevOps garantem CI/CD (integração e entrega contínuas), infraestrutura como código (IaC) e observabilidade profunda, garantindo resiliência e estabilidade nos deploys.

## 2. Conteinerização: Docker vs Kubernetes

**Conteinerização** é o empacotamento do código da aplicação com todas as suas dependências, garantindo que o software rode exatamente igual no ambiente do desenvolvedor e em produção. 

- **Docker:** É o motor de criação e execução de contêineres. Utilizamos o Docker e o `docker-compose` em ambientes de desenvolvimento para subir todos os serviços com um único comando.
- **Kubernetes (K8s):** É um orquestrador de contêineres. Enquanto o Docker roda os contêineres, o Kubernetes gerencia contêineres em escala: ele reinicia contêineres que falharam, distribui o tráfego de rede (Load Balancing), e escala instâncias automaticamente.
  
**Quando usar cada um?** Docker/Compose é excelente para ambientes de desenvolvimento e aplicações simples de um único nó. Kubernetes deve ser utilizado em produção quando a aplicação é complexa, distribuída e requer alta disponibilidade, resiliência e auto-escalabilidade.

## 3. Fundamentação Teórica

### Orquestração de Containers
No K8s, usamos **Deployments** para garantir que uma quantidade X de instâncias (Pods) da nossa aplicação estejam sempre rodando. Utilizamos **Services** para criar pontos de entrada de rede estáveis, mesmo quando os Pods são destruídos e recriados com IPs diferentes. **Probes (Liveness e Readiness)** garantem que o K8s saiba quando a aplicação está pronta para receber tráfego e quando ela travou e precisa ser reiniciada.

### CI/CD em Ambientes Distribuídos
A Integração Contínua (CI) garante que cada commit dispare testes automatizados e gere uma nova imagem Docker. A Entrega Contínua (CD) pega essa imagem, injeta as credenciais corretas (Secrets) e faz o deploy automatizado no Kubernetes. Isso diminui drasticamente o erro humano e acelera o tempo entre o desenvolvimento e a disponibilização ao usuário.

### Observabilidade
Com muitos serviços rodando, não podemos olhar logs de máquina em máquina. 
- **Métricas:** Mostram o "estado de saúde" (uso de CPU, RAM, requisições por segundo). Ex: Prometheus.
- **Logs:** Registros de eventos de cada serviço centralizados em uma plataforma (Ex: ELK Stack - Elasticsearch, Logstash, Kibana).
- **Traces Distribuídos:** Ferramentas como OpenTelemetry ou Jaeger, que injetam um `Trace ID` na requisição do Gateway e o propagam para o Pedido, Pagamento e Estoque, permitindo visualizar exatamente onde ocorreu lentidão ou falha.

## 4. Justificativa das Decisões Arquiteturais

1. **Python com FastAPI:** Escolhido por ser um framework moderno, assíncrono e de alta performance, ideal para lidar com I/O de rede intensivo típico de microsserviços.
2. **Multi-stage Dockerfiles:** Imagens finais extremamente enxutas e sem compiladores desnecessários, reduzindo a superfície de ataque e o tempo de pull/push.
3. **Imagens Non-Root:** Medida fundamental de segurança. Se o contêiner for comprometido, o invasor não terá privilégios de administrador no host do Kubernetes.
4. **Horizontal Pod Autoscaler (HPA):** Configurado para escalar o Gateway baseando-se no uso de CPU. Se a loja tiver um pico de acessos repentino, o HPA criará novos Pods automaticamente, desativando-os quando o tráfego baixar, economizando recursos (e dinheiro).
5. **Estratégia Rolling Update:** É a estratégia padrão do K8s e foi escolhida por realizar deploys graduais (sem *downtime*). Para a Loja Veloz, garante que o e-commerce nunca fique fora do ar durante atualizações de versão.

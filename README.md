# Sentiment MLOps Pipeline

End-to-end production-grade MLOps pipeline for real-time sentiment analysis. Built with modern MLOps practices including feature stores, model registries, automated retraining, and comprehensive monitoring.

## Architecture
─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│   Kafka     │────▶│   Stream     │────▶│   Feature   │────▶│   Model     │
│  Producer   │     │  Processor   │     │   Store     │     │  Registry   │
└─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
│
┌─────────────┐     ┌──────────────┐     ┌─────────────┐           │
│  Prometheus │◀────│    FastAPI   │◀────│  Predictor  │◀──────────┘
│   + Grafana │     │    Service   │     │             │
└─────────────┘     └──────────────┘     └─────────────┘
│
┌─────────────┐
│  Drift      │
│  Detector   │
└─────────────┘


## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Streaming** | Apache Kafka |
| **Feature Store** | Feast |
| **Model Registry** | MLflow |
| **API** | FastAPI + Uvicorn |
| **Monitoring** | Prometheus, Grafana, Evidently |
| **Orchestration** | Apache Airflow |
| **Infrastructure** | Terraform, Kubernetes |
| **CI/CD** | GitHub Actions |

## Quick Start

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- Kafka (or use provided docker-compose)

### 1. Clone & Setup

```bash
git clone <repo-url>
cd sentiment-mlops-pipeline
cp .env.example .env
# Edit .env with your credentials
```
2. Install Dependencies
```bash
make install
# or
pip install -r requirements.txt
```
3. Start Infrastructure
```bash
make infra-up
# Starts: Kafka, MLflow, PostgreSQL, Prometheus, Grafana
```
4. Run Training Pipeline
```bash
make train
# or
python -m src.pipelines.training_pipeline
```
5. Start API Service
```bash
make serve
# or
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```
6. Test Inference
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is absolutely amazing!"}'
```

Project Structure
```sentiment-mlops-pipeline/
├── src/
│   ├── data_ingestion/      # Kafka producers & stream processors
│   ├── feature_engineering/ # Text preprocessing & feature store client
│   ├── models/              # Model definition, training & registry
│   ├── inference/           # Batch & real-time prediction logic
│   ├── api/                 # FastAPI application with routers
│   ├── monitoring/          # Drift detection & metrics export
│   ├── pipelines/           # Orchestrated training & inference pipelines
│   └── utils/               # Config, logging, S3 utilities
├── configs/                 # YAML configurations for all components
├── tests/                   # Unit, integration & benchmark tests
├── notebooks/               # EDA & experimentation notebooks
├── deployment/              # Docker, Terraform, K8s, GitHub Actions
├── docs/                    # Architecture & setup documentation
└── scripts/                 # Infrastructure & pipeline shell scripts
```
Makefile Commands
| Command               | Description                                 |
| --------------------- | ------------------------------------------- |
| `make install`        | Install all dependencies                    |
| `make infra-up`       | Start local infrastructure (Docker Compose) |
| `make infra-down`     | Stop local infrastructure                   |
| `make train`          | Run full training pipeline                  |
| `make evaluate`       | Run model evaluation                        |
| `make serve`          | Start API server locally                    |
| `make test`           | Run all tests                               |
| `make lint`           | Run code linting & formatting               |
| `make build`          | Build Docker image                          |
| `make deploy-staging` | Deploy to staging environment               |
| `make deploy-prod`    | Deploy to production (K8s)                  |

API Endpoints
| Method | Endpoint         | Description                               |
| ------ | ---------------- | ----------------------------------------- |
| `POST` | `/predict`       | Single text sentiment prediction          |
| `POST` | `/predict/batch` | Batch sentiment predictions               |
| `GET`  | `/health`        | Service health check                      |
| `GET`  | `/metrics`       | Prometheus metrics                        |
| `GET`  | `/model/info`    | Current model metadata                    |
| `POST` | `/feedback`      | Submit prediction feedback for retraining |

Monitoring & Observability

Metrics Exported
* Inference latency (p50, p95, p99)
* Throughput (requests/sec)
* Prediction distribution (positive / negative / neutral)
* Model confidence scores
* Data drift scores (KL divergence, PSI)

Alerts Configured
* Model accuracy drops below threshold
* Data drift detected (PSI > 0.2)
* Inference latency p99 > 500ms
* Error rate > 1%
* Feature null rate spike

Dashboards
* Grafana: Model Performance
* Grafana: Data Drift
* Grafana: System Health

Model Details
| Property               | Value                               |
| ---------------------- | ----------------------------------- |
| **Architecture**       | DistilBERT fine-tuned for sentiment |
| **Classes**            | Negative, Neutral, Positive         |
| **Input**              | Raw text (max 512 tokens)           |
| **Output**             | Class probabilities + confidence    |
| **Latency**            | ~15ms (GPU) / ~120ms (CPU)          |
| **Retraining Trigger** | Drift detected OR weekly schedule   |

CI/CD Pipelines

.github/workflows/ci.yml
* Lint & format checks (black, isort, flake8)
* Unit & integration tests
* Docker image build & scan

.github/workflows/ml-pipeline.yml
* Triggered on data drift or schedule
* Runs full training pipeline
* Evaluates against production model
* Auto-promotes if accuracy improvement > 2%

.github/workflows/cd.yml
* Deploys to staging on PR merge
* Deploys to production on manual approval
* Blue-green deployment with K8s

Environment Variables
Copy .env.example to .env and configure:
| Variable                  | Description            | Required |
| ------------------------- | ---------------------- | -------- |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka broker addresses | Yes      |
| `MLFLOW_TRACKING_URI`     | MLflow server URL      | Yes      |
| `AWS_ACCESS_KEY_ID`       | S3 access key          | Yes      |
| `AWS_SECRET_ACCESS_KEY`   | S3 secret key          | Yes      |
| `S3_BUCKET`               | Model artifact bucket  | Yes      |
| `FEATURE_STORE_URL`       | Feast online store URL | Yes      |
| `PROMETHEUS_PUSHGATEWAY`  | Metrics push gateway   | No       |
| `SLACK_WEBHOOK_URL`       | Alert notifications    | No       |

Running Tests
```bash
# All tests
make test

# Specific test suites
pytest tests/test_api.py -v
pytest tests/test_model.py -v
pytest tests/test_pipeline.py -v

# Benchmarks
pytest tests/benchmark.py --benchmark-only
```
Deployment
Local (Docker Compose)
```bash
docker-compose -f docker-compose.yml up --build
```
Staging (Kubernetes)
```bash
kubectl apply -f deployment/k8s/ --namespace=staging
```
Production (Terraform + K8s)
```bash
cd deployment/terraform
terraform init && terraform apply
kubectl apply -f ../k8s/ --namespace=production
```
Contributing
1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit changes (git commit -m 'Add amazing feature')
4. Push to branch (git push origin feature/amazing-feature)
5. Open a Pull Request
All PRs must pass CI checks and require one approval before merging.

License
MIT License — see LICENSE for details.

Contact
* Issues: GitHub Issues
* Discussions: GitHub Discussions
* Email: mlops-team@yourcompany.com

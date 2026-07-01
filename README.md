# Platform work on a pricing service

DevOps work on a Spring Boot 4 pricing and messaging service that runs on Postgres,
Kafka, Prometheus and Loki. This repository holds my deliverables. The application
itself is the base service that was provided, so it is not copied in here.

## Why there is a repo and a PDF

The PDF is the writeup. It carries the reasoning, the decisions I made and the
screenshots, and it reads on its own. This repository holds the code the writeup points to.
A Helm chart, a dashboard, a pipeline and a script are easier to read as real files than
as long blocks pasted into a document, so they live here and the PDF links to them.

## Where each task lives

| Task | What it is | Where |
|------|------------|-------|
| 1. Identify the issues | triage writeup and the evidence I captured | `docs/report.html`, `docs/evidence/` |
| 2. Design a deployment | Helm chart, managed dependencies, ArgoCD application | `deploy/chart/`, `deploy/infra/`, `deploy/argocd/` |
| 3. Design a dashboard | Grafana dashboard model | `observability/` |
| 4. Automate a manual task | scheduled reporting job | `automation/` |
| 5. Improve the CI/CD pipeline | rebuilt pipeline | `ci/` |
| 6. Code review | in the report | `docs/report.html` |
| 7. AI in DevOps | in the report | `docs/report.html` |

## Run it

The base app runs with the provided Docker Compose stack. To deploy the service the way
this repo describes it:

```bash
# managed dependencies, standing in for a managed Postgres and Kafka
kubectl apply -f deploy/infra/

# the app, with Helm
helm install pricing-app ./deploy/chart -n pricing

# or with ArgoCD for GitOps
kubectl apply -f deploy/argocd/application.yaml
```

The chart runs a `pricing-service` image built from the base app.

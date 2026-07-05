# Platform work on a pricing service

DevOps work on a Spring Boot 4 pricing and messaging service that runs on Postgres,
Kafka, Prometheus and Loki. This repository holds my deliverables and is the config
half of a two-repo GitOps split. The application lives in its own repository,
[springboot-4-demo](https://github.com/sejoonkimmm/springboot-4-demo) (the provided
base app plus a CI workflow that builds and pushes its image to GHCR).

## Why there is a repo and a PDF

The PDF is the writeup. It carries the reasoning, the decisions I made and the
screenshots, and it reads on its own. This repository holds the code the writeup points to.
A Helm chart, a dashboard, a pipeline and a script are easier to read as real files than
as long blocks pasted into a document, so they live here and the PDF links to them.
The prose answers (the code review and the essay) live in the writeup only.
The writeup itself is the submission to DKV and is not tracked in this repository.

## Where each task lives

| Task | What it is | Where |
|------|------------|-------|
| 1. Identify the issues | triage writeup and the evidence I captured | `task-1-issue-analysis/` |
| 2. Design a deployment | Helm chart, managed dependencies, ArgoCD | `task-2-deployment/` |
| 3. Design a dashboard | Grafana dashboard model | `task-3-dashboard/` |
| 4. Automate a manual task | scheduled reporting job | `task-4-automation/` |
| 5. Improve the CI/CD pipeline | rebuilt pipeline | `task-5-cicd/` |
| 6. Code review | PR review comment | in the writeup |
| 7. AI in DevOps | short essay | in the writeup |

## Run it

The base app runs with the provided Docker Compose stack. To deploy the service the way
this repo describes it:

```bash
# managed dependencies, standing in for a managed Postgres and Kafka
kubectl apply -f task-2-deployment/infra/

# the app, with Helm
helm install pricing ./task-2-deployment/helm-chart -n pricing

# or with ArgoCD app-of-apps for GitOps
kubectl apply -f task-2-deployment/argocd/root.yaml
```

The chart runs `ghcr.io/sejoonkimmm/springboot-4-demo`, built and pushed by the app
repository's workflow on every push (short-sha tags, semver on release tags).

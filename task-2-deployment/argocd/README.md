# ArgoCD deployment

GitOps for the pricing service. ArgoCD syncs from this git repo, so the cluster
always matches what is in `main`. Nothing is applied to prod by hand.

## Topology

```
platform-root  (app-of-apps)   root.yaml
  ├─ infra      wave 0          apps/infra.yaml    -> ../infra        (Postgres, Kafka)
  └─ pricing    wave 1          apps/pricing.yaml  -> ../helm-chart   (the app)
```

`infra` syncs first (wave 0), then `pricing` (wave 1). Both land in the `pricing`
namespace, because the app reaches Postgres and Kafka by short service name.

## Run it

```bash
kubectl apply -f task-2-deployment/argocd/root.yaml
kubectl -n argocd get applications
kubectl -n pricing get pods,svc,hpa
```

Rollback: revert the git commit (ArgoCD re-syncs to it) or `argocd app rollback pricing <revision>`.

## Files

- `root.yaml` — the only object you apply by hand; owns the whole platform.
- `apps/` — the children the root manages: `infra` and `pricing`.
- `application.yaml` — a single plain Application. The simplest alternative, kept
  for reference against the app-of-apps choice.
- `applicationset/envs.yaml` — one template renders the chart into dev and prod
  from a per-env values file, so environments do not drift by hand-editing. Not
  synced by the root (it would collide with the live `pricing` app); apply on its
  own for the per-env layout.
- `applicationset/preview.yaml` — one ephemeral stack per open pull request. Smoke
  and contract tests run against the preview copy before merge, which is how a
  silent bad version is caught before prod. The pullRequest generator needs a
  GitHub token, so it ships as a manifest, not run on kind:

  ```bash
  kubectl -n argocd create secret generic github-scm \
    --from-literal=token=<github_pat_with_repo_read>
  ```

## Image versioning

The image tag lives in git. Dev follows the app repo's short SHA (`values-dev.yaml`),
prod is pinned to a version (`values-prod.yaml` holds `1.0.0`). No environment uses `latest`.

The image comes from GHCR. The app repository
([springboot-4-demo](https://github.com/sejoonkimmm/springboot-4-demo)) builds and
pushes `ghcr.io/sejoonkimmm/springboot-4-demo` on every push, tagged `sha-<short>`,
plus a semver tag on release tags. Promoting to prod is a reviewed commit here that
bumps the pinned version. The remaining automation step would be ArgoCD Image Updater
(or a Renovate rule) to bump the dev tag automatically.

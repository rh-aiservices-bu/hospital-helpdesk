---
name: rhoai-tutorial-admin-setup
description: "Install and configure RHOAI 3.5 on OpenShift so a regular user can complete a GenAI tutorial without admin blockers — channel pins, DSC flags, genAiStudio, model registry, S3 storage, minimal RBAC, verified gotchas"
---

# Install & Configure RHOAI 3.5 for a GenAI Tutorial (cluster-admin role)

Goal: a regular user (no admin rights) can, without any `oc` admin commands:
1. Log into the RHOAI dashboard.
2. Create an A.I. project from the dashboard.
3. Deploy a model from the model catalog (or via S3/URI per the tutorial) and serve it.
4. Use the Gen AI Studio Playground with that model.
5. Run the tutorial's workbench, notebook, RAG, and MCP-ticketing flows.

## 1. Subscribe to the RHOAI operator (stable-3.5 channel)
```bash
oc create -f - <<'EOF'
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: rhods-operator
  namespace: openshift-operators
spec:
  channel: stable-3.5
  name: rhods-operator
  source: redhat-operators
  sourceNamespace: openshift-marketplace
  startingCSV: rhods-operator.3.5.0
EOF
# Wait for CSV Succeeded (takes ~3-5 min):
oc get csv -n openshift-operators -w
```
**Warning:** do NOT use the `stable` channel — it installs 2.25.x, a different product generation (no gen-ai-ui, different flags). If 2.x is installed, uninstall first (below); in-place channel switch 2.25 → 3.5 does NOT trigger an upgrade (the installplan keeps referencing the old CSV).

## 2. Create DSCI + DSC (component selection matters)
```bash
# DSCI
oc create -f - <<'EOF'
apiVersion: dscinitialization.opendatahub.io/v1
kind: DSCInitialization
metadata:
  name: default
spec:
  applicationsNamespace: redhat-ods-applications
  monitoring:
    managementState: Managed
EOF

# DSC — enable what the tutorial needs, remove what it doesn't
oc create -f - <<'EOF'
apiVersion: datasciencecluster.opendatahub.io/v1
kind: DataScienceCluster
metadata:
  name: default-dsc
spec:
  components:
    dashboard:
      managementState: Managed
    datasciencepipelines:
      managementState: Managed
    kserve:
      managementState: Managed
    workbenches:
      managementState: Managed
    trustyai:
      managementState: Managed
    modelregistry:
      managementState: Managed
    ogx:                     # ships gen-ai-ui + llama-stack operator (tutorial playground)
      managementState: Managed
    llamastackoperator:      # DEPRECATED in 3.5 — must be Removed before ogx (operator guardrail)
      managementState: Removed
    mlflowoperator:
      managementState: Removed
EOF
```
**Guardrails (verified):**
- `llamastackoperator` MUST be `Removed` (deprecated in 3.5; the operator refuses to provision `ogx` otherwise, error: "LlamaStackOperator is set to Managed; it has been deprecated, set it to Removed before enabling OGX").
- A single `DSCInitialization` named `default` is auto-created by the operator in 3.5 — creating another is denied ("Only one instance allowed").

## 3. Wait for the DSC to go Ready
```bash
oc wait --for=jsonpath='{.status.phase}'=Ready dsc/default-dsc --timeout=1200s
```
Verify dashboard pods + gen-ai-ui pod are Running in `redhat-ods-applications`:
```bash
oc get pods -n redhat-ods-applications | grep -E "rhods-dashboard|gen-ai-ui|model-catalog"
```

## 4. Enable Gen AI Studio (Technology Preview) in the dashboard
The model catalog UI (search bar + model tiles on AI hub → Models) is hidden by default. Two-part flag: patch the CR **and restart the dashboard** — the operator does not propagate this flag to the running backend without a restart (verified).
```bash
oc patch odhdashboardconfig odh-dashboard-config -n redhat-ods-applications \
  --type=merge -p '{"spec":{"dashboardConfig":{"genAiStudio":true,"genAiTracing":true}}}'

# REQUIRED — restart to pick up the flag:
oc rollout restart deploy/rhods-dashboard -n redhat-ods-applications
oc rollout status deploy/rhods-dashboard -n redhat-ods-applications
```
Verify via the CR (NOT the HTTP route — `/api/config` sits behind oauth-proxy and just redirects to the SSO login page):
```bash
oc get odhdashboardconfig odh-dashboard-config -n redhat-ods-applications \
  -o jsonpath='{.spec.dashboardConfig.genAiStudio}'
```

## 5. Model registry (model catalog + AI-asset-endpoint integration)
```bash
oc create -f - <<'EOF'
apiVersion: components.platform.opendatahub.io/v1alpha1
kind: ModelRegistry
metadata:
  name: default-modelregistry        # name MUST be exactly this (webhook enforced)
  namespace: redhat-ods-applications
spec:
  managementState: Managed
  gateway:
    domain: <your-dashboard-domain>  # e.g. rh-ai.apps.cluster-6d7fk.dyn.redhatworkshops.io
EOF
```
**Gotcha (verified):** the controller does NOT auto-sync `spec.gateway.domain` from GatewayConfig — omitted, the registry goes `NotReady` with "gateway domain is missing for ModelRegistry". Read the domain from `oc get gatewayconfig default-gateway -o jsonpath='{.status.domain}'` and patch if needed.

## 6. Model storage (for the tutorial's model deploy)
vLLM on CPU needs the model directory to contain BOTH `model.gguf` AND `config.json` (from the HF repo's `/raw/main/config.json`). A bare `.gguf` alone fails with "Invalid repository ID or local directory specified: '/mnt/models'. For HF models: ensure the presence of a 'config.json'".
Options:
- **S3 (recommended):** create a bucket (e.g. NooBaa `s3` route if ODF is installed), upload `model.gguf` + `config.json` under `models/<dir>/`, then give the user a connection secret:
  ```yaml
  apiVersion: v1
  kind: Secret
  metadata:
    name: my-storage-connection
    namespace: <user-project>
    labels:
      opendatahub.io/dashboard: "true"
      opendatahub.io/managed: "true"
    annotations:
      opendatahub.io/connection-type: s3
      opendatahub.io/connection-type-ref: s3
  type: Opaque
  stringData:
    AWS_ACCESS_KEY_ID: ...
    AWS_SECRET_ACCESS_KEY: ...
    AWS_DEFAULT_REGION: us-east-1
    AWS_S3_BUCKET: ...
    AWS_S3_ENDPOINT: https://<s3-route>   # https, not http — storage-initializer needs TLS CA bundle path
  ```
- **URI (direct file):** a URL responding `application/octet-stream` (e.g. HF `/resolve/main/...gguf`). A bare HF repo *page* fails the octet-stream check.

## 7. User RBAC (so the user can use the Playground)
The Playground backend checks K8s access for the user's own namespace; with default project-scoped RBAC a regular user can list services only in their own project.
- **Recommended: minimal project-scoped RBAC** (preserves the regular-user premise any reviewer depends on):
  ```bash
  oc create rolebinding edit -n <user-project> --clusterrole=edit --user=user1
  ```
  Verify with `oc auth can-i --as=user1 -n <user-project> get services`, and grant only what the tutorial needs (notebooks/isvc/secrets/services get+create).
- **Do NOT grant the `admin` ClusterRole** "for convenience" — a privileged reviewer invalidates every permission-related finding in the companion review, and the grant silently lands wrong: run from a project dir, `oc adm policy add-cluster-role-to-user admin user1` creates a **namespaced RoleBinding**, not a cluster-wide one.
- If you grant anything beyond project-scoped `edit`, record the exact privilege level in the handoff checklist — the reviewer must know and must label permission findings untested.

## 8. ConfigMap the Playground needs (verified 404 without it)
```bash
oc create -f - <<'EOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: gen-ai-aa-mcp-servers
  namespace: redhat-ods-applications
data:
  mcp_servers.json: "[]"
EOF
```
Without it, the Playground page hangs on "Loading" (the `/gen-ai/api/v1/aaa/mcps` call 404s and the UI never recovers).

## 9. Keycloak dashboard access (if the cluster uses Keycloak SSO)
Confirm the user exists in the Keycloak realm backing the RHOAI dashboard (workshop cluster: `sso` realm via `idp-4-ocp`). A user who can log into the OCP console can log into the dashboard, but confirm before handoff.

## Gotchas (all verified, all bite a fresh admin)

| # | Gotcha | Symptom | Fix |
|---|--------|---------|-----|
| 1 | `stable` channel = 2.25.x | gen-ai-ui missing, no model catalog | use `stable-3.5` + `startingCSV` |
| 2 | 2.25 → 3.5 channel switch does nothing | installplan still references old CSV | uninstall 2.25 first |
| 3 | `llamastackoperator` deprecated | ogx provisioning fails | set `Removed` before `ogx: Managed` |
| 4 | DSCI already exists | "Only one instance allowed" | operator auto-creates `default`; don't create another |
| 5 | `genAiStudio` flag not picked up | catalog UI still hidden | restart the dashboard deployment |
| 6 | ModelRegistry gateway domain | NotReady, "gateway domain is missing" | patch `spec.gateway.domain` manually |
| 7 | Bare GGUF without config.json | vLLM crash on predictor start | upload `config.json` beside the `.gguf` |
| 8 | Project created from OCP console | invisible to AI hub (no `opendatahub.io/dashboard=true` label) | create from the RHOAI dashboard, or add the label |
| 9 | Missing `gen-ai-aa-mcp-servers` ConfigMap | Playground hangs on Loading | create the ConfigMap (step 8) |
| 10 | 2.x-era genAi module-federation debugging | irrelevant in 3.5 | 3.5 ships `gen-ai-ui` natively; skip 2.x docs |
| 11 | `curl /api/config` to verify flags | redirects to SSO login page (oauth-proxy) | verify via `oc get odhdashboardconfig -o jsonpath=...` |
| 12 | `add-cluster-role-to-user admin` from a project dir | creates a namespaced RoleBinding, not cluster-wide | run from a non-project dir or use explicit RoleBinding; prefer minimal RBAC |

## Uninstall procedure (for a clean re-install)
```bash
# Delete CRs first
oc delete datasciencecluster --all
oc delete dscinitialization --all
# Remove finalizer if stuck
oc get dsci default -o jsonpath='{.metadata.finalizers}'
oc patch dsci default --type=merge -p '{"metadata":{"finalizers":null}}'
# Delete subscription + CSV
oc delete sub rhods-operator -n openshift-operators --ignore-not-found
oc delete csv -n openshift-operators --all
# Purge leftover CRDs and namespaces
oc get crd -o name | grep -iE "opendatahub|nim\.|kserve|modelmesh|llamastack" | xargs -r oc delete
oc delete ns redhat-ods-applications redhat-ods-monitoring rhods-notebooks --ignore-not-found
```

## Handoff checklist (before telling the user to start)
- [ ] `oc get dsc` → Ready
- [ ] Dashboard URL loads; user can log in
- [ ] `genAiStudio` flag true in `oc get odhdashboardconfig odh-dashboard-config -n redhat-ods-applications -o jsonpath='{.spec.dashboardConfig.genAiStudio}'`
- [ ] Model catalog search bar visible on AI hub → Models
- [ ] `default-modelregistry` Ready with gateway domain set
- [ ] S3/URI model location ready with `model.gguf` + `config.json`
- [ ] `gen-ai-aa-mcp-servers` ConfigMap exists
- [ ] User has access to their own project + Playground
- [ ] User's exact privilege level recorded (role/RoleBinding granted, namespace scope)
- [ ] MCP ticketing server reachable (module 6 of the tutorial)

Hand the user only the expected-state checklist — see the companion skill `platform-tutorial-user-review` for the regular-user side.

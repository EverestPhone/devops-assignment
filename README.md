##  Setup Local and Test
wsl --update   We will test:

Docker (local containers)

Kubernetes deployment

Ingress

HPA scaling

Worker behavior

Prometheus metrics

Failure scenarios

CI/CD validation mindset

All using PowerShell on Windows.

🧰 PHASE 0 — Prerequisites (Production Mindset)

Open PowerShell as Administrator

✅ 1. Verify Docker
docker --version
docker info


Expected:

Server version visible

No errors

If Docker Desktop:

Ensure Kubernetes is ENABLED

Docker Desktop → Settings → Kubernetes → Enable

✅ 2. Verify kubectl
kubectl version --client
kubectl get nodes


Expected:

NAME             STATUS   ROLES           AGE
docker-desktop   Ready    control-plane   ...


If using Minikube:

minikube start
kubectl get nodes

📦 PHASE 1 — Extract the ZIP File

Move to Downloads:

cd $HOME\Downloads


Extract:

Expand-Archive .\agnos-devops-assignment-production.zip


Enter folder:

cd .\agnos-devops-assignment-prod


Check structure:

tree /F


You should see:

api\
worker\
k8s\
monitoring\
.github\
README.md


This confirms project structure integrity.

🐳 PHASE 2 — Build Docker Images (Local Validation)

This validates Dockerfiles and app correctness before Kubernetes.

🔹 Build API
docker build -t agnos-api:local .\api

🔹 Build Worker
docker build -t agnos-worker:local .\worker


Verify:

docker images


You should see:

agnos-api
agnos-worker

🧪 PHASE 3 — Test API Container Standalone

Run API:

docker run -e APP_ENV=dev -p 8000:8000 agnos-api:local


Open new PowerShell window.

🔹 Test Health Endpoint
curl http://localhost:8000/health


Expected:

{"status":"ok","environment":"dev"}


This validates:

FastAPI working

Environment variable working

Logging working

🔹 Test Metrics Endpoint
curl http://localhost:8000/metrics


You should see Prometheus metrics:

api_requests_total
api_request_latency_seconds


This validates observability layer.

Stop container:

docker ps
docker stop <container_id>

☸️ PHASE 4 — Kubernetes Deployment

Now we test production orchestration.

🔹 Deploy All Manifests
kubectl apply -f .\k8s\base\

🔹 Verify Resources
kubectl get all


Check:

Deployment/api

Deployment/worker

Service/api-service

Ingress

Pods Running

🔹 Check Pod Status
kubectl get pods -o wide


Ensure:

STATUS = Running

READY = 1/1

🌐 PHASE 5 — Access API from Localhost

Since service is ClusterIP, we port-forward.

🔹 Port Forward
kubectl port-forward svc/api-service 8080:80


Open new PowerShell window.

🔹 Test API via Kubernetes
curl http://localhost:8080/health


This confirms:

Service routing works

Deployment works

Pod networking works

🔍 PHASE 6 — Test Worker Logs

Find worker pod:

kubectl get pods


Then:

kubectl logs <worker-pod-name>


You should see structured JSON logs:

{"updated_timestamp":"...","environment":"dev"}


This validates:

Worker running

Logging structured

Restart policy active

📊 PHASE 7 — Validate HPA (Scaling Test)

Check HPA:

kubectl get hpa
If "kubectl : No resources found in default namespace." found, check
kubectl get pods -n kube-system

🔹 Generate Load

Open new PowerShell:

for ($i=0; $i -lt 300; $i++) {
    curl http://localhost:8080/health | Out-Null
}


Wait 1–2 minutes.

Check pods:

kubectl get pods


If CPU threshold triggered → replicas increase.

This validates auto-scaling capability.

🔥 PHASE 8 — Failure Testing (Important for Interview)
🧨 Test API Crash

Delete pod:

kubectl delete pod <api-pod-name>


Immediately check:

kubectl get pods -w


New pod should recreate automatically.

This proves:

Self-healing

Deployment controller working

🧨 Test Worker Crash
kubectl delete pod <worker-pod-name>


It should restart automatically.

🧨 Test Rolling Restart
kubectl rollout restart deployment api


Check:

kubectl rollout status deployment api

📈 PHASE 9 — Test Prometheus Metrics

Port-forward again:

kubectl port-forward svc/api-service 9090:80


Test:

curl http://localhost:9090/metrics


This validates metrics endpoint for monitoring.

🔐 PHASE 10 — CI/CD Mindset Validation

Push to GitHub:

git init
git add .
git commit -m "Production DevOps assignment"
git branch -M main
git remote add origin https://github.com/EverestPhone/devops-assignment.git
git push -u origin main


Then:

GitHub → Actions tab
Confirm:

Docker build runs

Trivy scan runs

No failed jobs
# Agnos DevOps Production-Grade Assignment

## 🚀 Architecture Overview

- FastAPI API Service
- Background Worker
- Docker multi-stage builds
- Kubernetes (HA, probes, resource limits)
- Ingress controller
- Prometheus monitoring
- Trivy security scanning
- GitHub Actions CI/CD
- Environment overlays (DEV/UAT/PROD)

---

## 🏗 System Design

API → Service → Ingress  
Worker runs separately  
Prometheus scrapes /metrics endpoint  
HPA scales API pods based on CPU  

---

## 🌍 Environment Strategy

- DEV: minimal replicas, debug enabled  
- UAT: production-like testing  
- PROD: high availability, scaling enabled  

Environment variable:
```
APP_ENV=dev|uat|prod
```

---

## 🔐 Security

- Trivy container scanning in CI  
- Resource limits  
- Non-root slim images  
- Readiness & liveness probes  

---

## 📊 Observability

- Structured JSON logs  
- Prometheus metrics  
- HPA scaling based on CPU  

---

## ⚠ Failure Handling

| Scenario | Mitigation |
|----------|------------|
| API crash | Kubernetes auto-restart |
| Worker infinite retry | Add backoff strategy |
| Bad deployment | kubectl rollout undo |
| Node failure | Pods rescheduled |


---

## 🎯 Why This Design?

This solution demonstrates:
- Reliability
- Observability
- Security best practices
- Kubernetes fundamentals
- CI/CD automation

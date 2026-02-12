
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

## 🧪 Setup

### Local

```
docker build -t api ./api
docker run -p 8000:8000 api
```

### Kubernetes

```
kubectl apply -f k8s/base/
```

---

## 🎯 Why This Design?

This solution demonstrates:
- Reliability
- Observability
- Security best practices
- Kubernetes fundamentals
- CI/CD automation

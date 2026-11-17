## Incident Monitor: CI/CD and Monitoring Pipeline for a ServiceNow-style Service

A small Python service that reports incident counts by priority and exposes them as Prometheus metrics. The service is the vehicle. The real subject of this project is the delivery pipeline around it: every change merged to main is tested, packaged, published and deployed to Kubernetes automatically, and the running service is monitored on a Grafana dashboard.


## Goal

Build and understand a complete DevOps workflow end to end:

- Write code in VS Code and manage it with Git and GitHub (branches and pull requests).
- Package the app with Docker.
- Create the Kubernetes cluster and the monitoring stack with Terraform (Infrastructure as Code).
- Run an automated Jenkins pipeline that tests, builds, publishes and deploys the app.
- Observe the running app with Prometheus and Grafana, and test how it behaves when things break.


## How the pipeline works

- A change is pushed on a feature branch and merged to main through a pull request.
- Jenkins checks out main and reads the Jenkinsfile.
- Test runs the unit tests. Build image creates a Docker image tagged with the Jenkins build number. Push image publishes it to Docker Hub. Deploy updates the Kubernetes Deployment and waits for the rollout to finish.
- Kubernetes replaces the old pods with new ones, using health checks to avoid sending traffic to pods that are not ready.
- Prometheus scrapes the app's /metrics endpoint and Grafana draws the numbers.


## Tech stack

|          Area          |                            Tools                            |
|:----------------------:|:-----------------------------------------------------------:|
| Application            | Python 3.13, Flask, gunicorn, prometheus-client, pytest     |
| Version control        | Git, GitHub (feature branches, pull requests)               |
| Containers             | Docker, Docker Hub                                          |
| Infrastructure as code | Terraform (kind provider and Helm provider)                 |
| Orchestration          | Kubernetes (kind), Helm                                     |
| CI/CD                  | Jenkins (declarative pipeline, running in Docker)           |
| Monitoring             | Prometheus, Grafana (kube-prometheus-stack), ServiceMonitor |
| Editor and OS          | VS Code, Windows with Docker Desktop                        |


## The application

|       Endpoint      |                                      Purpose                                    |
|:-------------------:|:-------------------------------------------------------------------------------:|
|     `/health`       | Returns `{"status":"ok"}`. Used by the Kubernetes readiness and liveness probes |
| `/incidents/summary`| Returns total incidents and counts by priority                                  |
|    `/metrics`       | Prometheus metrics                                                              |

## Repository structure

```
.
├── app/                    Flask application (main.py, servicenow.py)
├── tests/                  pytest unit tests
├── k8s/                    deployment.yaml, service.yaml, servicemonitor.yaml
├── terraform/              main.tf: kind cluster and monitoring stack
├── jenkins/Dockerfile      Jenkins image with Docker CLI, Python and kubectl
├── monitoring/             exported Grafana dashboard (JSON)
├── docs/screenshots/       screenshots used in this README
├── Dockerfile              application image
├── Jenkinsfile             CI/CD pipeline
├── requirements.txt        Python dependencies
└── .gitignore              keeps secrets, state files and kubeconfigs out of Git 
```


## Failure tests

I broke the system on purpose to see how it behaves.

| Test              | What I did                                              | What I saw                                                                                            | How it recovered                                                  |
|-------------------|---------------------------------------------------------|-------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------|
| Kill a pod        | `kubectl delete pod <name>`                             | The Pod got deleted and Kubernetes automatically recreated the deleted pod                            | Kubernetes started a replacement while the other pod kept serving |
| Bad release       | Pushed code that raises an exception on startup         | The Test stage failed and the later stages were skipped, so the bad version never reached the cluster | Fixed the code on a branch, merged, and the next build was green  |
| Scale up and down | `kubectl scale deployment incident-monitor --replicas=4`|  pod count panel changed from 2 to 4                                                                  | Scaled back to 2                                                  |
| Fetch errors      | Set MOCK_MODE to FALSE with no credentials              |  the fetch errors panel rose                                                                          | Set it back to TRUE and re-applied                                |



## Author
Yashvini R, [GitHub](https://github.com/Yashvini2010)
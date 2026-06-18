Kafka KRaft Cluster Deployment on Kubernetes (Minikube)

Overview

This project automates the deployment of a complete Apache Kafka KRaft cluster on Kubernetes using Minikube and Docker. The script provisions the local environment, builds application images, deploys Kafka brokers, creates topics, and validates end-to-end producer-consumer communication.

The deployment uses:

- Apache Kafka in KRaft mode (ZooKeeper-less architecture)
- Kubernetes (Minikube)
- Docker
- StatefulSets
- Producer and Consumer microservices
- Automated topic creation and verification

---

Architecture
```
+---------------------+
|     Producer Job    |
+----------+----------+
           |
           v
+---------------------+
|   Kafka Topic       |
|      posts          |
+----------+----------+
           |
           v
+---------------------+
| Consumer Deployment |
+---------------------+

Kafka Cluster:
-------------------------
Kafka Broker 0 (KRaft)
Kafka Broker 1 (KRaft)
-------------------------
```
---

Prerequisites

Before running the deployment, ensure the following tools are installed:

Tool| Purpose
Colima| Local container runtime
Docker| Container image management
Minikube| Local Kubernetes cluster
Kubectl| Kubernetes CLI
Kafka CLI| Cluster validation

Recommended system resources:
```
- CPU: 4 Cores
- Memory: 10 GB
- Disk: 60 GB
```
---

Deployment Workflow

1. Environment Initialization

The script performs the following:

- Starts Colima
- Waits for Docker daemon readiness
- Starts Minikube using Docker driver
- Connects Docker to Minikube environment
```
colima start --cpu 4 --memory 10 --disk 60

minikube start \
  --driver=docker \
  --memory=7000 \
  --cpus=4
```
---

2. Kubernetes Validation

The cluster is verified before deployment begins.

kubectl get nodes
kubectl cluster-info

---

3. Environment Cleanup

Any previous deployment is removed to ensure a clean installation.

kubectl delete namespace kafka-demo --ignore-not-found=true

A fresh namespace is then created:

kubectl create namespace kafka-demo

---

4. Docker Image Build

Application images are rebuilt for every deployment.

```
Producer

docker build -t producer:v1 ./producer

Consumer

docker build -t consumer:v1 ./consumer
```
---

5. Kafka KRaft Cluster Deployment

The Kafka cluster is deployed using a Kubernetes StatefulSet.

kubectl apply -f k8s/apps/kafka-statefulset.yaml

Deployment includes:

- Kafka Broker 0
- Kafka Broker 1
- KRaft Controller Quorum
- Persistent Storage
- Internal Cluster Networking

---

6. Broker Readiness Validation

The script waits until both brokers become available.
```
kubectl wait \
  --for=condition=ready pod/kafka-0 \
  -n kafka-demo

kubectl wait \
  --for=condition=ready pod/kafka-1 \
  -n kafka-demo
```
---

7. KRaft Quorum Verification

Kafka metadata quorum status is validated.
```
kafka-metadata-quorum \
  --bootstrap-server localhost:9092 \
  describe --status
```
This confirms:

- Active Controller
- Leader Election
- Cluster Health

---

8. Topic Creation

A Kubernetes Job creates the application topic.

kubectl apply -f k8s/apps/topic-job.yaml

Topic created:

posts

---

9. Topic Verification

The script verifies the topic configuration.
```
kafka-topics \
  --describe \
  --topic posts \
  --bootstrap-server localhost:9092
```
---

10. Consumer Deployment

Consumer is deployed as a Kubernetes Deployment.

kubectl apply -f k8s/apps/consumer.yaml

The rollout is monitored until completion.

kubectl rollout status deployment/consumer

---

11. Producer Execution

Producer runs as a Kubernetes Job.
```
kubectl apply -f k8s/apps/producer-job.yaml
```
The producer publishes messages into the "posts" topic.

---

12. End-to-End Validation

Logs are collected from:
```
Producer

kubectl logs job/producer -n kafka-demo

Consumer

kubectl logs deployment/consumer -n kafka-demo
```
Expected outcome:

Producer -> Kafka Topic -> Consumer

Messages produced by the producer should be successfully consumed by the consumer.

---

Monitoring Commands

View Pods
```
kubectl get pods -n kafka-demo

View Services

kubectl get svc -n kafka-demo

View StatefulSets

kubectl get statefulsets -n kafka-demo

Resource Usage

kubectl top pods -n kafka-demo

Kafka Logs

kubectl logs kafka-0 -n kafka-demo
kubectl logs kafka-1 -n kafka-demo
```
---

Deployment Validation Checklist

Verify the following after deployment:

- Colima running
- Docker healthy
- Minikube healthy
- Namespace created
- Producer image built
- Consumer image built
- Kafka Broker 0 running
- Kafka Broker 1 running
- KRaft quorum healthy
- Topic "posts" created
- Consumer deployed
- Producer completed successfully
- Consumer receiving messages

---

Project Structure
```
DevOps-Challenge-main/
│
├── producer/
│   ├── Dockerfile
│   └── Application Code
│
├── consumer/
│   ├── Dockerfile
│   └── Application Code
│
├── k8s/
│   └── apps/
│       ├── kafka-statefulset.yaml
│       ├── topic-job.yaml
│       ├── consumer.yaml
│       └── producer-job.yaml
│
└── deploy.sh
```
---

Final Outcome

After successful execution:

- Kubernetes cluster is running locally.
- Kafka KRaft cluster is operational.
- Topic "posts" is available.
- Producer publishes messages successfully.
- Consumer receives and processes messages.
- End-to-end event streaming is validated without ZooKeeper.

Kafka KRaft Environment ReadyThis version is suitable for GitHub and clearly explains the purpose, architecture, deployment flow, validation steps, and operational commands.
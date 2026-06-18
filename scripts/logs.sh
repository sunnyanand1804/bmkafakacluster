#!/bin/bash

echo "================ PODS ================"
kubectl get pods -n kafka-demo

echo ""
echo "================ CONSUMER LOGS ================"
kubectl logs deployment/consumer -n kafka-demo --tail=50

echo ""
echo "================ PRODUCER LOGS ================"
kubectl logs job/producer -n kafka-demo --tail=50 || true
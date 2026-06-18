#!/bin/bash

kubectl rollout restart statefulset kafka -n kafka-demo

kubectl get pods -n kafka-demo -w
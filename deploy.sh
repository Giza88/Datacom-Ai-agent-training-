#!/usr/bin/env bash

# Azure Container App deploy script (Slide 47)

RESOURCE_GROUP="rg-slide-gen"
CONTAINERAPP_NAME="slidegen-app"
LOCATION="australiaeast"
ACR_NAME="slidegen<yourname>"
BACKEND_IMAGE="slide-gen-backend:latest"
FRONTEND_IMAGE="slide-gen-frontend:latest"

az containerapp up \
  --name $CONTAINERAPP_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --environment slidegen-env \
  --image $ACR_NAME.azurecr.io/$BACKEND_IMAGE \
  --target-port 8000 \
  --ingress external \
  --registry-server $ACR_NAME.azurecr.io \
  --registry-username $ACR_NAME \
  --registry-password "<ACR_PASSWORD>" \
  --yaml azure/aca.yaml

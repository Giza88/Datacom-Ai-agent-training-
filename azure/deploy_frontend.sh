#!/usr/bin/env bash

RESOURCE_GROUP="rg-slide-gen"
BACKEND_NAME="slide-gen-backend"
FRONTEND_NAME="slide-gen-frontend"
ENV_NAME="slide-gen-env"
ACR_NAME="slidegen<yourname>"

echo "Fetching backend internal URL..."
BACKEND_URL=$(az containerapp show \
  --name $BACKEND_NAME \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn -o tsv)

echo "Backend URL: $BACKEND_URL"

echo "Deploying frontend..."
az containerapp create \
  --name $FRONTEND_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $ENV_NAME \
  --image $ACR_NAME.azurecr.io/slide-gen-frontend:latest \
  --registry-server $ACR_NAME.azurecr.io \
  --target-port 80 \
  --ingress external \
  --env-vars VITE_API_URL=https://$BACKEND_URL

echo "Fetching public frontend URL..."
az containerapp show \
  --name $FRONTEND_NAME \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn -o tsv

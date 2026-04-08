# Slide 37B — Azure Deploy Part 3 (ACI)

$RESOURCE_GROUP = "rg-slide-gen"
$BACKEND_NAME   = "slide-gen-backend"
$FRONTEND_NAME  = "slide-gen-frontend"
$ACR_NAME       = "slidegen<yourname>"
$ACR_USERNAME   = "<ACR_USERNAME>"
$ACR_PASSWORD   = "<ACR_PASSWORD>"

Write-Host "Fetching backend FQDN and IP..."
$BACKEND_FQDN = az container show `
  --resource-group $RESOURCE_GROUP `
  --name $BACKEND_NAME `
  --query ipAddress.fqdn -o tsv

$BACKEND_IP = az container show `
  --resource-group $RESOURCE_GROUP `
  --name $BACKEND_NAME `
  --query ipAddress.ip -o tsv

Write-Host "Backend FQDN: $BACKEND_FQDN"
Write-Host "Backend IP:   $BACKEND_IP"

Write-Host "Deploying frontend container to ACI..."
az container create `
  --resource-group $RESOURCE_GROUP `
  --name $FRONTEND_NAME `
  --image "$ACR_NAME.azurecr.io/slide-gen-frontend:latest" `
  --registry-login-server "$ACR_NAME.azurecr.io" `
  --registry-username $ACR_USERNAME `
  --registry-password $ACR_PASSWORD `
  --os-type Linux `
  --cpu 1 `
  --memory 1 `
  --ip-address Public `
  --ports 80 `
  --environment-variables BACKEND_ORIGIN="http://$BACKEND_IP:8000"

Write-Host "Fetching public frontend IP..."
$FRONTEND_IP = az container show `
  --resource-group $RESOURCE_GROUP `
  --name $FRONTEND_NAME `
  --query ipAddress.ip -o tsv

Write-Host "Frontend IP: $FRONTEND_IP"

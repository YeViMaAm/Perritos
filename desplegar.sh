#!/bin/bash

# 1. Variables
NOMBRE_APP="candy-perritos"
RESOURCE_GROUP="yvmalaver90_rg_2805"

echo "📦 Iniciando empaquetado para Azure..."

# 2. Borrar zip viejo si existe
rm -f deploy.zip

# 3. Empaquetar todo (Excluimos lo innecesario para que sea ligero)
zip -r deploy.zip . -x "*.git*" "*__pycache__*" "*.venv*" "*.db" "static/uploads/*" ".pytest_cache/*"

echo "🚀 Subiendo a Azure App Service: $NOMBRE_APP..."

# 4. Subir a Azure
az webapp deployment source config-zip \
  --name $NOMBRE_APP \
  --resource-group $RESOURCE_GROUP \
  --src deploy.zip

# 5. Limpiar archivo local
rm deploy.zip

echo "✅ Despliegue completado con éxito."
echo "🔗 URL: https://$NOMBRE_APP.azurewebsites.net"
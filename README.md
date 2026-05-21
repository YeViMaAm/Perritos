# Validar logs en tiempo real (comando)
az webapp log tail --name candy-perritos --resource-group yvmalaver90_rg_2805


# Abrir la pagina en github (comando)
fastapi dev src/main.py

# Por si no se abre la pagina en github
fuser -k 8000/tcp

# Para correr el scrip para subir a azure
./desplegar.sh

# URL de la API
https://candy-perritos.azurewebsites.net

# URL de documentación
https://candy-perritos.azurewebsites.net/docs


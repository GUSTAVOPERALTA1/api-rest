# api-rest

# run test
´´´
python3 -m pytest -v   
´´´
# run app
´´´
uvicorn main:app --reload
´´´
# docker container
´´´
docker run -it -v /workspace/api-rest/apitest/:/home/apitest --name test -h gustav --net=host tarea-api:0.1
´´´
# actualizar git local 
´´´
git fetch
git pull
´´´
# cambiar configuracion de git
´´´
git pull --rebase origin main
git push -u origin main
´´´

# Comando para correr uvicorn en VISUAL STUDIO CODE
´´´
python3 -m uvicorn main:app --reload
´´´

# Forzar commit a GITHUB
´´´
git push -u origin main --force
´´´
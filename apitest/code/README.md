# run app
´´´
uvicorn main:app --reload
´´´
# docker container
´´´
docker run -it -v /workspace/api-rest/apitest/:/home/apitest --name test -h gustav --net=host tarea-api:0.1
´´´
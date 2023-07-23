DOCKER_USERNAME ?= dimabaril
APPLICATION_NAME ?= flask_app

# build image
build:
	docker build --tag ${DOCKER_USERNAME}/${APPLICATION_NAME} .

# push image to docker hub
push:
	docker push ${DOCKER_USERNAME}/${APPLICATION_NAME}

# run container
run:
	docker run --name ${APPLICATION_NAME} -it -p 5000:5000 ${DOCKER_USERNAME}/${APPLICATION_NAME}

# stop container
stop:
	docker stop ${APPLICATION_NAME}

# remove container
rm:
	docker rm ${APPLICATION_NAME}

# remove image
rmi:
	docker rmi ${DOCKER_USERNAME}/${APPLICATION_NAME}

# remove all
kill:
	docker stop ${APPLICATION_NAME}
	docker rm ${APPLICATION_NAME}
	docker rmi ${DOCKER_USERNAME}/${APPLICATION_NAME}

# без докеров
fr:
	flask run

# наполняем базу
dbp:
	python populate_database.py
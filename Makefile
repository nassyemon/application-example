# variables
DIR := ./
ENV_FILE := ./.env
BUILD_ARG_FILE :=./build_args.env

CSWEB_APP_IMAGE_NAME := csweb-app
CSWEB_NGINX_IMAGE_NAME := csweb-nginx
ADMWEB_APP_IMAGE_NAME := admweb-app
ADMWEB_NGINX_IMAGE_NAME := admweb-nginx
MIGRATE_APP_IMAGE_NAME := migrate-app

ENVS := $(shell cat ${ENV_FILE} | grep -v '\#' | xargs )
BUILD_ARGS := $(shell cat ${BUILD_ARG_FILE} | grep -v '\#' | xargs -I{} echo --build-arg {})
MIGRATIONS_DIR := $(shell ${ENVS}; echo $$MIGRATIONS_DIR)

ECR_ENV_FILE := ./ecr.env
ECR_ENVS := $(shell cat ${ECR_ENV_FILE} | grep -v '\#' | xargs )
GIT_BRANCH := $(shell git branch --show-current)
LAST_COMMIT_ID := $(shell git log --format="%H" -n 1 | grep . || echo default)


CSWEB_APP_REPOSITORY := $(shell ${ECR_ENVS}; echo $$CSWEB_APP_REPOSITORY)
MIGRATE_APP_REPOSITORY := $(shell ${ECR_ENVS}; echo $$MIGRATE_APP_REPOSITORY)
CSWEB_NGINX_REPOSITORY := $(shell ${ECR_ENVS}; echo $$CSWEB_NGINX_REPOSITORY)
ADMWEB_APP_REPOSITORY := $(shell ${ECR_ENVS}; echo $$ADMWEB_APP_REPOSITORY)
ADMWEB_NGINX_REPOSITORY := $(shell ${ECR_ENVS}; echo $$ADMWEB_NGINX_REPOSITORY)

BRANCH_BASED_TAG = latest_${GIT_BRANCH}
LATEST_CSWEB_APP = $(shell docker image ls | grep -E '^${CSWEB_APP_IMAGE_NAME}\s+latest' | awk '{print $$3}')
LATEST_CSWEB_NGINX = $(shell docker image ls | grep -E '^${CSWEB_NGINX_IMAGE_NAME}\s+latest' | awk '{print $$3}')
LATEST_ADMWEB_APP = $(shell docker image ls | grep -E '^${ADMWEB_APP_IMAGE_NAME}\s+latest' | awk '{print $$3}')
LATEST_ADMWEB_NGINX = $(shell docker image ls | grep -E '^${ADMWEB_NGINX_IMAGE_NAME}\s+latest' | awk '{print $$3}')
LATEST_MIGRATE_APP = $(shell docker image ls | grep -E '^${MIGRATE_APP_IMAGE_NAME}\s+latest' | awk '{print $$3}')

define PUSH_APP
	@#$1=lastest-image, $2=repository-name
	@echo aws: profile=${AWS_DEPLOY_PROFILE} region=${region} repository=$2
	@echo branch=${GIT_BRANCH} commit_id=${LAST_COMMIT_ID} image=$1
	@echo tagging to ${LAST_COMMIT_ID} ${BRANCH_BASED_TAG}
	docker tag $1 ${ECR_REGISTRY}/$2:${BRANCH_BASED_TAG}
	docker tag $1 ${ECR_REGISTRY}/$2:${LAST_COMMIT_ID}
	aws ecr get-login-password --profile ${AWS_DEPLOY_PROFILE} --region ${AWS_REGION} | \
		docker login --username AWS --password-stdin https://${ECR_REGISTRY} \
	  && docker push ${ECR_REGISTRY}/$2:${LAST_COMMIT_ID} \
	  && docker push ${ECR_REGISTRY}/$2:${BRANCH_BASED_TAG}
endef

.PHONY: prepare
prepare:
	@mkdir -p ./.volumes/mysql
	@mkdir -p ./.logs/mysql
	@mkdir -p ${MIGRATIONS_DIR}

.PHONY: build
build: prepare
	@docker-compose build

.PHONY: up
up: prepare
	@docker-compose up --build -d

.PHONY: up-watch
up-watch: prepare
	@docker-compose up --build

.PHONY: down
down:
	@docker-compose down

.PHONY: db-init
 db-init: build
	docker-compose run  --entrypoint flask admweb-app db init

.PHONY: db-migrate
db-migrate: build
	docker-compose run --entrypoint flask admweb-app db migrate

.PHONY: db-upgrade
db-upgrade: build
	docker-compose run  --entrypoint flask admweb-app db upgrade

.PHONY: connect-mysql
connect-mysql:
	${ENVS}; mysql --protocol tcp -h localhost -P 3306 -u $${DB_USER} -D $${DB_NAME} -p$${DB_PASSWORD}

# csweb
.PHONY: push-csweb
push-csweb: push-csweb-app push-csweb-nginx

## csweb-app
.PHONY: build-csweb-app
build-csweb-app:
	${ENVS}; docker build ${BUILD_ARGS} ./ -f ./Dockerfile-csweb-app -o out -t ${CSWEB_APP_IMAGE_NAME}:latest

.PHONY: inspect-csweb-app
inspect-csweb-app:
	docker inspect ${LATEST_CSWEB_APP}

.PHONY: login-csweb-app
login-csweb-app: build-csweb-app
	docker run -i -t --env-file ${ENV_FILE} --entrypoint "/bin/bash" ${LATEST_CSWEB_APP}

.PHONY: push-csweb-app
push-csweb-app: build-csweb-app inspect-csweb-app
	$(call PUSH_APP,${LATEST_CSWEB_APP},${CSWEB_APP_REPOSITORY})

## csweb-nginx
.PHONY: build-csweb-nginx
build-csweb-nginx:
	${ENVS}; docker build ${BUILD_ARGS} ./ -f ./Dockerfile-csweb-nginx -o out -t ${CSWEB_NGINX_IMAGE_NAME}:latest

.PHONY: inspect-csweb-nginx
inspect-csweb-nginx:
	docker inspect ${LATEST_CSWEB_NGINX}

.PHONY: login-csweb-nginx
login-csweb-nginx: build-csweb-nginx
	docker run -i -t --env-file ${ENV_FILE} --entrypoint "/bin/sh" ${LATEST_CSWEB_NGINX}

.PHONY: push-migrate
push-csweb-nginx: build-csweb-nginx inspect-csweb-nginx
	$(call PUSH_APP,${LATEST_CSWEB_NGINX},${CSWEB_NGINX_REPOSITORY})


# admweb
.PHONY: push-csadmwebweb
push-admweb: push-admweb-app push-admweb-nginx

## admweb-app
.PHONY: build-admweb-app
build-admweb-app:
	${ENVS}; docker build ${BUILD_ARGS}  ./ -f Dockerfile-admweb-app -o out -t ${ADMWEB_APP_IMAGE_NAME}:latest

.PHONY: inspect-admweb-app
inspect-admweb-app:
	docker inspect ${LATEST_ADMWEB_APP}

.PHONY: login-admweb-app
login-admweb-app: build-admweb-app
	docker run -i -t --env-file ${ENV_FILE} --entrypoint "/bin/bash" ${LATEST_ADMWEB_APP}

.PHONY: push-admweb-app
push-admweb-app: build-admweb-app inspect-admweb-app
	$(call PUSH_APP,${LATEST_ADMWEB_APP},${ADMWEB_APP_REPOSITORY})

## admweb-nginx
.PHONY: build-admweb-nginx
build-admweb-nginx:
	${ENVS}; docker build ${BUILD_ARGS} ./ -f Dockerfile-admweb-nginx -o out -t ${ADMWEB_NGINX_IMAGE_NAME}:latest

.PHONY: inspect-admweb-nginx
inspect-admweb-nginx:
	docker inspect ${LATEST_ADMWEB_NGINX}

.PHONY: login-admweb-nginx
login-admweb-nginx: build-admweb-nginx
	docker run -i -t --env-file ${ENV_FILE} --entrypoint "/bin/sh" ${LATEST_ADMWEB_NGINX}

.PHONY: push-admweb-nginx
push-admweb-nginx: build-admweb-nginx inspect-admweb-nginx
	$(call PUSH_APP,${LATEST_ADMWEB_NGINX},${ADMWEB_NGINX_REPOSITORY})

# migrate-app
.PHONY: build-migrate
build-migrate: db-migrate
	${ENVS}; docker build ${BUILD_ARGS} ./ -f Dockerfile-admweb-app -o out -t ${MIGRATE_APP_IMAGE_NAME}:latest

.PHONY: inspect-migrate
inspect-migrate:
	docker inspect ${LATEST_MIGRATE_APP}

.PHONY: login-migrate
login-migrate: build-migrate
	docker run -i -t --env-file ${ENV_FILE} --entrypoint "/bin/bash" ${LATEST_MIGRATE_APP}

.PHONY: push-migrate
push-migrate: build-migrate inspect-migrate
	$(call PUSH_APP,${LATEST_MIGRATE_APP},${MIGRATE_APP_REPOSITORY})

# other
.PHONY: clean
clean:
	@echo "nothing to do (not implemented)."

.PHONY: sandbox
sandbox:
	@echo ${AWS_DEPLOY_PROFILE} $(AWS_REGION) $(ECR_REGISTRY)
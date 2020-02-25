#!/bin/bash
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker build -t kryptedgaming/krypted:experimental --build-arg VERSION=$TRAVIS_BRANCH ./docker/app/ --no-cache
if [ $? -ne 0 ]; then 
    exit 1
fi 
docker build -t kryptedgaming/krypted_celery:experimental --build-arg VERSION=$TRAVIS_BRANCH ./docker/celery/ --no-cache
if [ $? -ne 0 ]; then 
    exit 1
fi 
docker push kryptedgaming/krypted:experimental
if [ $? -ne 0 ]; then 
    exit 1
fi 
docker push kryptedgaming/krypted_celery:experimental
if [ $? -ne 0 ]; then 
    exit 1
fi 

exit 0 
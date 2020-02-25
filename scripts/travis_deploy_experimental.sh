#!/bin/bash
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker build -t kryptedgaming/krypted:experimental --build-arg VERSION=$TRAVIS_BRANCH ./docker/app/ --no-cache
docker build -t kryptedgaming/krypted_celery:experimental --build-arg VERSION=$TRAVIS_BRANCH ./docker/celery/ --no-cache
docker push kryptedgaming/krypted:experimental
docker push kryptedgaming/krypted_celery:experimental

exit 0 
#!/bin/bash
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
echo "docker build -t kryptedgaming/krypted:experimental --build-arg VERSION=$(git rev-parse --abbrev-ref HEAD) ./docker/app/ --no-cache"
echo "docker build -t kryptedgaming/krypted_celery:experimental --build-arg VERSION=$(git rev-parse --abbrev-ref HEAD) ./docker/celery/ --no-cache"
echo "docker push kryptedgaming/krypted:experimental"
echo "docker push kryptedgaming/krypted_celery:experimental"

exit 0 
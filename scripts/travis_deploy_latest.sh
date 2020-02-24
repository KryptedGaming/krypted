#!/bin/bash
echo "docker build -t kryptedgaming/krypted:latest --build-arg VERSION=$(git rev-parse --abbrev-ref HEAD) ./docker/app/ --no-cache"
echo "docker build -t kryptedgaming/krypted_celery:latest --build-arg VERSION=$(git rev-parse --abbrev-ref HEAD) ./docker/celery/ --no-cache"
echo "docker push kryptedgaming/krypted:latest"
echo "docker push kryptedgaming/krypted_celery:latest"

exit 0 
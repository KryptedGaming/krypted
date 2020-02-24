#!/bin/bash
echo "docker build -t kryptedgaming/krypted:latest --build-arg VERSION=$(git rev-parse --abbrev-ref HEAD) ./docker/app/ --no-cache"
echo "docker build -t kryptedgaming/krypted_celery:latest --build-arg VERSION=$(git rev-parse --abbrev-ref HEAD) ./docker/celery/ --no-cache"
echo "docker push kryptedgaming/krypted:experimental"
echo "docker push kryptedgaming/krypted_celery:experimental"

exit 0 
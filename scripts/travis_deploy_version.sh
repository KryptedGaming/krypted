#!/bin/bash
CHANGED_FILES=($(git diff --name-only $TRAVIS_COMMIT_RANGE))
if echo $CHANGED_FILES | grep -q "app/app/__init__.py"; then 
    VERSION=`grep "__version__ = " app/app/__init__.py | awk '{ print $3}'| tr -d \'`
    echo "Updated to version: $s"
    echo "docker build -t kryptedgaming/krypted:$VERSION --build-arg VERSION=$(git rev-parse --abbrev-ref HEAD) ./docker/app/ --no-cache"
    echo "docker build -t kryptedgaming/krypted_celery:$VERSION --build-arg VERSION=$(git rev-parse --abbrev-ref HEAD) ./docker/celery/ --no-cache"
    echo "docker push kryptedgaming/krypted:$VERSION"
    echo "docker push kryptedgaming/krypted_celery:$VERSION"
fi

exit 0 
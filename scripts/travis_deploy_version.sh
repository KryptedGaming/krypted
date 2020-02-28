#!/bin/bash
if [ "$TRAVIS_PULL_REQUEST" != "false" ]; then 
 exit 0
fi 
 
VERSION=$(grep "__version__ = " app/app/__init__.py | awk '{ print $3}'| tr -d \')
docker build -t kryptedgaming/krypted:"$VERSION" --build-arg VERSION="$TRAVIS_BRANCH" ./docker/app/ --no-cache
if [ $? -ne 0 ]; then 
    exit 1
fi 
docker build -t kryptedgaming/krypted_celery:"$VERSION" --build-arg VERSION="$TRAVIS_BRANCH" ./docker/celery/ --no-cache
if [ $? -ne 0 ]; then 
    exit 1
fi 
docker push kryptedgaming/krypted:"$VERSION"
if [ $? -ne 0 ]; then 
    exit 1
fi 
docker push kryptedgaming/krypted_celery:"$VERSION"
if [ $? -ne 0 ]; then 
    exit 1
fi 

exit 0 
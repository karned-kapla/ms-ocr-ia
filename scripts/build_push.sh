#!/bin/zsh
echo 'version ?'
read version

docker build -t killiankopp/ms-ocr-ia:$version .
docker push killiankopp/ms-ocr-ia:$version

docker tag killiankopp/ms-ocr-ia:$version killiankopp/ms-ocr-ia:latest
docker push killiankopp/ms-ocr-ia:latest

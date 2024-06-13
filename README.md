# ms-ocr-ia

**Création de l'image Docker de l'API**
```shell
docker build -t ms-ocr-ia .
```

**Lancement de l'API**
```shell
docker run -d --name ms-ocr-ia -p 8900:8000 ms-ocr-ia
```
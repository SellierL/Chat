# TP Chat - Django REST Framework avec PostgreSQL et Docker

Projet Django REST Framework avec deux bases PostgreSQL :

- une base principale pour les propriétaires et les chats ;
- une base refuge pour les chats adoptés/transférés.

Le projet est entièrement lancé avec Docker Compose.

## Prérequis

- Docker Desktop
- VS Code ou un terminal
- Un fichier `.env` à la racine du projet

## Fichier `.env`

Créer un fichier `.env` à la racine du projet avec

## Lancer le projet

Depuis la racine du projet :

```bash
docker compose up --build
```

Au démarrage, le conteneur Django :

1. attend les deux bases PostgreSQL ;
2. applique les migrations ;
3. crée l’utilisateur autorisé ;
4. insère les données de test ;
5. lance le serveur Django.

## Accès aux pages

Dashboard principal :

```text
http://localhost:8000/
```

API REST :

```text
http://localhost:8000/api/
```

API des propriétaires :

```text
http://localhost:8000/api/owners/
```

API des chats :

```text
http://localhost:8000/api/cats/
```

API des chats du refuge :

```text
http://localhost:8000/api/shelter-cats/
```

Dashboard refuge :

```text
http://localhost:8000/shelter/
```

Page de connexion :

```text
http://localhost:8000/accounts/login/
```

Identifiants de test :

```text
username : admin_refuge
password : admin1234
```

## Réinitialiser les bases

Pour supprimer les données et repartir de zéro :

```bash
docker compose down -v
docker compose up --build
```

## Vérifier les bases PostgreSQL

Base principale :

```bash
docker compose exec db psql -U cat_user -d cat_db -c "\dt"
```

Base refuge :

```bash
docker compose exec shelter_db psql -U shelter_user -d shelter_db -c "\dt"
```

## Arrêter le projet

```bash
docker compose down
```

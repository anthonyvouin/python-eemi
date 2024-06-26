# GradeTrack

### Présentation du projet

Ce projet implémente un système de gestion des notes des élèves en utilisant FastAPI. L'API permet d'ajouter, récupérer et supprimer des informations sur les élèves et leurs notes.

#### Cloner le projet

```bash
git clone https://github.com/anthonyvouin/python-eemi.git
cd python-eemi
```

#### Installer les dépendances
```bash
poetry install
```
#### Lancer le projet
```bash
poetry run uvicorn main:app --reload
```
L'API sera accessible à l'adresse suivante : http://127.0.0.1:8000.

---

## Accès aux routes

Pour accéder aux différentes routes de notre API, un swagger a été mis en place grâce à l'utilisation de FastAPI.

Pour y accéder [cliquer ici](http://127.0.0.1:8000)


---
## Get token JWT

Pour le début du projet : 
1. Créez un compte : /user/

2. Se Connecter : /user/login

3. Récuperer le token lors de la connection

4. Sur PostMan (ou autre app...) Renseigner le token avec bearer token lors de l'utilisation de la route pour créer un étudiant. 

Exemple : bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJsYWxhYWEiLCJleHAiOjE3MTk0MTg5MTh9.Mj3pVPhuStLyB67enEytsruwRBI98fr4S_eMNddoWl4

---

## Lancement des tests

Nous avons réaliser des tests avec pytest pour lancer vos tests, effectuer la commande suivante :
```bash
poetry run pytest
```

---
## Choix de la DB 

Pour ce projet nous avons utilisé SQL Lite pour pouvoirs faire des jointure, pour sa légéreté et sa simplicité
---

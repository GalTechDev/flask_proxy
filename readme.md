
---
# flask reverse proxy

Ce projet est une application Flask utilisée comme reverse proxy pour gérer des redirections en fonction des sous-domaines spécifiés dans un fichier de configuration.

## Fonctionnalités

- Redirection des sous-domaines vers des destinations spécifiées.
- Prise en charge des connexions WebSocket pour certains sous-domaines.

## Configuration

Le fichier de configuration `config.json` est utilisé pour définir les paramètres de l'application. Voici un exemple de structure de fichier de configuration :

```json
{
    "domain": "votredomaine.com",
    "subdomain": "www",
    "ip": "votre_ip",
    "port": 80,
    "redirection": {
        "nom_sousdomaine": {
            "protocole": "http://",
            "domain": "votre_destination",
            "websocket": true
        }
    }
}
```

- `domain`: le domaine principal de votre application.
- `subdomain`: le sous-domaine par défaut.
- `ip`: l'adresse IP sur laquelle l'application sera hébergée.
- `port`: le port sur lequel l'application écoutera les requêtes.
- `redirection`: un dictionnaire contenant les informations de redirection pour chaque sous-domaine. Vous pouvez ajouter autant de sous-domaines que nécessaire.

## Utilisation

1. Assurez-vous d'avoir Python installé sur votre système.
2. Installez les dépendances en exécutant `pip install -r requirements.txt`.
3. Configurez votre fichier `config.json` selon vos besoins.
4. Lancez l'application.
5. Accédez à l'application à l'adresse spécifiée dans votre fichier de configuration.

## Remarques

- Assurez-vous que les ports spécifiés dans votre fichier de configuration sont accessibles et autorisés sur votre système.

---
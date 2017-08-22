# Krypted Auth
Advanced authentication system for Krypted Gaming.

#### Current Status
- Waiting for ESI routes to stabilize (EVE Swagger Interface), have been having issues with important API routes

- Customizing current AllianceAuth fork (what we're currently using for auth)

- Learning a bit of sysadmin to help in the deployment of this application (Apache, server deployment)

# Description
Over the years of playing video games, Krypted Gaming has used many tools to integrate with our main games. Linking characters to accounts, assigning groups across a multitude of services, and broadcasting tailored events to each game has been a constant struggle for us. This web application is the all-in-one solution for everything Krypted.

# Design Goals
- Modular (add support for any new games we have)

- Beautiful (looking good on the web is important to us)

- Intuitive (no complicated UIs with poor help text)

# Technologies
- Python

- Django

- ESI (EVE Swagger Interface), Pyswagger, EsiPy

- websocket-client (for sending messages to discord bot)

# Screenshots
![Login](https://github.com/porowns/krypted-auth/blob/master/screenshots/login.png)

![Dashboard](https://github.com/porowns/krypted-auth/blob/master/screenshots/dashboard.png)

![EVE Online Integration](https://github.com/porowns/krypted-auth/blob/master/screenshots/game_integration.png)

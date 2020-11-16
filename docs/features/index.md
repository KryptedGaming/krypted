# Features

Krypted Platform is built as a barebone Django application, with tools and infrastructure to heavily extend it with advanced Django applications. 

Your base installation won't have much- meaning you'll want to enable features from multiple sources.

## Core Features

|   Application Name   |   Description  | Additional Information |
|  ---  |  ---  | ---  |
|   `accounts`   |   Simple login system with accounts, user profiles, and login system.  | User Guide | 
|   `applications`   |   Application system for members applying to your community.  | User Guide | 
|   `group_requests`   |   Adds group requests for your community members.  | User Guide | 

To install core features, simply add the `Application Name` to `INSTALLED_APPS`. 

## Official Packages
|   Package Name    |   Latest Version    |   Link    |
|  ---  |  ---  |  ---  |
|    `django-eveonline-connector`   |   [![PyPI version](https://badge.fury.io/py/django-eveonline-connector.svg)](https://badge.fury.io/py/django-eveonline-connector)    |  [GitHub](https://github.com/KryptedGaming/django-eveonline-connector)   |
|    `django-eveonline-timerboard`   |  [![PyPI version](https://badge.fury.io/py/django-eveonline-timerboard.svg)](https://badge.fury.io/py/django-eveonline-timerboard)   |  [GitHub](https://github.com/KryptedGaming/django-eveonline-timerboard)   |
|    `django-discord-connector`   |   [![PyPI version](https://badge.fury.io/py/django-discord-connector.svg)](https://badge.fury.io/py/django-discord-connector)    |  [GitHub](https://github.com/KryptedGaming/django-discord-connector)   |
|    `django-eveonline-doctrine-manager`  |   [![PyPI version](https://badge.fury.io/py/django-eveonline-doctrine-manager.svg)](https://badge.fury.io/py/django-eveonline-doctrine-manager)    |  [GitHub](https://github.com/KryptedGaming/django-eveonline-doctrine-manager)   |
|    `django-eveonline-group-states`  |   [![PyPI version](https://badge.fury.io/py/django-eveonline-group-states.svg)](https://badge.fury.io/py/django-eveonline-group-states)   |  [GitHub](https://github.com/KryptedGaming/django-eveonline-group-states)   |

Installing official packages is as simple as using `pip` (or specifying them under `PIP_INSTALLS`), and including them in `INSTALLED_APPS`. 

## Community Packages
|   Package Name    |   Latest Version    |   Link    |
|  ---  |  ---  |  ---  |
|    `django-eveonline-buyback`   |   [![PyPI version](https://badge.fury.io/py/django-eveonline-buyback.svg)](https://badge.fury.io/py/django-eveonline-buyback)    |  [GitHub](https://github.com/b5n/django-eveonline-buyback)   |
|    `django-pathfinder-statcrunch`   |  [![PyPI version](https://badge.fury.io/py/django-pathfinder-statcrunch.svg)](https://badge.fury.io/py/django-pathfinder-statcrunch)  |  [GitHub](https://github.com/porowns/django-pathfinder-statcrunch)   |

Installing community packages is **usually** the same as installating official packages, but we recommend reading their instructions individually.  

## Adding Packages
If your package is not listed here, submit a pull request following the same format. Badges are generated [here](https://badge.fury.io).
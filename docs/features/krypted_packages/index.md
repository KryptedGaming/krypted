# Krypted Packages
These are packages contributed and maintained by Krypted Gaming.

|   Package Name    |   Description    |   Link    |
|  ---  |  ---  |  ---  |
|    django-eveonline-connector   |   Provides EVE Online SSO & entity models    |  [GitHub](https://github.com/KryptedGaming/django-eveonline-connector)   |
|    django-eveonline-entity-extensions   |   Adds entity (characters, etc) data models, views, and tasks    |  [GitHub](https://github.com/KryptedGaming/django-eveonline-entity-extensions)   |
|    django-eveonline-timerboard   |   Provides timerboard for EVE Online    |  [GitHub](https://github.com/KryptedGaming/django-eveonline-timerboard)   |
|    django-discord-connector   |   Adds Discord syncing and SSO    |  [GitHub](https://github.com/KryptedGaming/django-discord-connector)   |
|    django-discourse-connector  |   Adds Discourse syncing and SSO    |  [GitHub](https://github.com/KryptedGaming/django-discourse-connector)   |

# Installing Packages
## PyPi
Typically, our packages are pushed to PyPi whenever we release. 

1. Install the package `pip3 install <package_name>`
2. Follow the instructions in the package README.md
3. Add the package to your `settings.py` file (under `KRYPTED_APPS`, replace `-` with `_`)

## Manually
If you want the latest version of our packages, you should install clone them and install them.

1. Clone the package `git clone <package_url>`
2. Install with pip `pip3 install -e <package_name>`
3. Follow instructions {2} and {3} from PyPi installation
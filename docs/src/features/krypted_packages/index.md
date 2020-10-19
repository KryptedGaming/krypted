## Krypted Packages
These are packages contributed and maintained by Krypted Gaming.

|   Package Name    |   Description    |   Link    |
|  ---  |  ---  |  ---  |
|    django-eveonline-connector   |   Provides EVE Online SSO & entity models    |  [GitHub](https://github.com/KryptedGaming/django-eveonline-connector)   |
|    django-eveonline-entity-extensions   |   Adds entity (characters, etc) data models, views, and tasks    |  [GitHub](https://github.com/KryptedGaming/django-eveonline-entity-extensions)   |
|    django-eveonline-timerboard   |   Provides timerboard for EVE Online    |  [GitHub](https://github.com/KryptedGaming/django-eveonline-timerboard)   |
|    django-discord-connector   |   Adds Discord syncing and SSO    |  [GitHub](https://github.com/KryptedGaming/django-discord-connector)   |
|    django-discourse-connector  |   Adds Discourse syncing and SSO    |  [GitHub](https://github.com/KryptedGaming/django-discourse-connector)   |
|    django-eveonline-doctrine-manager  |   Adds Doctrines and Fittings    |  [GitHub](https://github.com/KryptedGaming/django-eveonline-doctrine-manager)   |
|    django-eveonline-group-states  |   State management (corporations, alliances) for EVE Online    |  [GitHub](https://github.com/KryptedGaming/django-eveonline-group-states)   |

### Installing Packages
#### Docker 
If you're using Docker, you'll simply specify packages in the `.env` file. 

1. Under the `REQUIREMENTS`, add KryptedGaming/<package_name> (e.g django-discord-connector).
2. Under the `EXTENSIONS`, add the extension name. This is what the package says to add into `INSTALLED_APPS`, e.g django_discord_connector). 

#### PyPi
Typically, our packages are pushed to PyPi whenever we release. 

1. Install the package `pip3 install <package_name>`
2. Follow the instructions in the package README.md
3. Add the package to your `settings.py` file (under `EXTENSIONS`, replace `-` with `_`)

#### Manually
If you want the latest version of our packages, you should install clone them and install them.

1. Clone the package `git clone <package_url>`
2. Install with pip `pip3 install -e <package_name>`
3. Follow instructions {2} and {3} from PyPi installation
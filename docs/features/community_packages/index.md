# Community Packages
These are packages contributed by the community.

|   Package Name    |   Description    |   Link    |
|  ---  |  ---  |  ---  |
|       |       |       |

## Installing Packages
### Docker 
If you're using Docker, you'll simply specify packages in the `.env` file. 

1. Under the `REQUIREMENTS`, add KryptedGaming/<package_name> (e.g django-discord-connector).
2. Under the `EXTENSIONS`, add the extension name. This is what the package says to add into `INSTALLED_APPS`, e.g django_discord_connector). 

### PyPi
Typically, our packages are pushed to PyPi when they are released. 

1. Install the package `pip3 install <package_name>`
2. Follow the instructions in the package README.md
3. Add the package to your `settings.py` file (under `EXTENSIONS`, replace `-` with `_`)

### Manually
If you want the latest version of a package, you should install clone them and install them.

1. Clone the package `git clone <package_url>`
2. Install with pip `pip3 install -e <package_name>`
3. Follow instructions {2} and {3} from PyPi installation
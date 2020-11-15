# Contributing
Krypted Platform was built as an easily extendable platform, making contributions as easy as building your own standalone Django package. Without contributors like you, our platform wouldn't be special!
## Installation
Follow `Local Installation` instructions [here](../installation/index.md#local-installation).

## Development Environment
* [VSCode](https://code.visualstudio.com/) is our recommended IDE. We recommend the `Python` extension and `py-coverage-view`.
* Juniper Notebooks is highly recommended. Follow instructions from the `./launcher install` and use `python3 manage.py shell_plus --notebook`.
* Windows users are highly recommended to use [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

## Special Sauce
There's a ton of *special sauce* baked into the platform to make your life easier. 
### Package Template
We recommend forking from our [package template](https://github.com/KryptedGaming/django-package-template) to follow our practices. 

### Launcher
#### What is the launcher?
The launcher is our developer tool that handles a lot of the common commands that you'll be running. It's made to run in the root project directory, and helps you handle things like running Django, celery, and coverage. Understanding the launcher will save you a *ton* of time, and we highly recommend you use it when developing extensions.

#### Launcher Commands

| Command | Description |
| --- | --- |
| launcher env      | Creates a virtual environment, enable it with `source ./myvenv/bin/active` |
| launcher install  | Installs the development enviroment |
| launcher test     | Runs the application tests *with* code coverage | 
| launcher run      | Runs the web application on `127.0.0.1:8000` | 
| launcher celery   | Starts the Celery worker and Celery beat |
| launcher flower   | Launches Celery flower on `127.0.0.1:5555` | 

#### Extending the Launcher
The launcher is written in Shell, so simply add a function and case statement for it, and you're good to go!

### Sidebar Extensions
Including your extension in the sidebar is fairly easy, we automatically check for `sidebar.html` in every `EXTENSION` template folder. 

[Check out this example.](https://github.com/KryptedGaming/django-eveonline-connector/tree/master/django_eveonline_connector/templates/django_eveonline_connector)

### Package Binder
The package binder is a way to check for versions, requirements, and celery tasks for your application. 

[See this example.](https://github.com/KryptedGaming/django-eveonline-connector/blob/master/django_eveonline_connector/apps.py). Check out the code under `if apps.is_installed('packagebinder')`.
## Contribution Guildelines
Krypted accepts contributions in the form of **packages**, which are simply [reusable Django Applications](https://docs.djangoproject.com/en/2.2/intro/reusable-apps/). All of our community packages can be found [here](../features/community_packages/index).

Alternatively, you can contribute to our [Krypted Packages](../features/krypted_packages/index) in the form of pull requests. 

There are a few requirements to become a community package,

1. The application must separate, with the preferred installation being `pip3 install <package>`
2. The application must have test cases, with decent coverage. 
3. The application must be open source.


## Mentorship
For mentorship on contributing, reach out to us on [Discord](https://discord.gg/YAmSMPx). 

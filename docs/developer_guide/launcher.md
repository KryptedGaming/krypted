## Launcher
### What is the launcher?
The launcher is our developer tool that handles a lot of the common commands that you'll be running. It's made to run in the root project directory, and helps you handle things like running Django, celery, and coverage. Understanding the launcher will save you a *ton* of time, and we highly recommend you use it when developing extensions.

### Launcher Commands

| Command | Description |
| --- | --- |
| launcher env      | Creates a virtual environment, enable it with `source ./myvenv/bin/active` |
| launcher install  | Installs the development enviroment |
| launcher test     | Runs the application tests *with* code coverage | 
| launcher run      | Runs the web application on `127.0.0.1:8000` | 
| launcher celery   | Starts the Celery worker and Celery beat |
| launcher flower   | Launches Celery flower on `127.0.0.1:5555` | 

### Extending the Launcher
The launcher is written in Shell, so simply add a function and case statement for it, and you're good to go!
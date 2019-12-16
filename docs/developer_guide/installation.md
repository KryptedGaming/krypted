# Installation
Installing the Krypted platform developers is fairly simple, since we have scripts that will do most of the work.

## Clone the Repository
Clone the GitHub repository to your local file system.
`git clone https://github.com/KryptedGaming/krypted.git`

## Run the installation script
1. Navigate to the directory `cd krypted`
2. Ensure permissions are correct `chmod +x ./install/install.sh launcher`
3. Create a virtual environment `./launcher env`
4. Enter your virtual environment `source ./myenv/bin/activate`
4. Run the installation script `./launcher install`
5. Verify your installation `./launcher test`

## Recommended: VSCode
We recommend you use VSCode when developing, because it's awesome.

1. Install VSCode from [this link](https://code.visualstudio.com/)
2. Get the `Python` extension for VSCode
3. Get the `py-coverage-view` extension for VSCode (for code coverage when running `./launcher test`)

## Recommended: Juniper Notebooks
By default, the developer requirements installs shell plus and notebook. 

1. Enable `django-extensions` in your `INSTALLED_APPS`
2. Start notebook with `python3 manage.py shell_plus --notebook`
3. Create a notebook, start developing

By utilizing this tool, you'll be able to refresh your code changes and re-run previous code. It's a lifesaver for Python development, especially when debugging.
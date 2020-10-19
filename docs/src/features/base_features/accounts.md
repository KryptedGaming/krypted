### Accounts
Accounts enables our login system, user profiles, and other crucial account features. 

#### Enabling Accounts
1. Docker: Add `accounts` to the list of `EXTENSIONS` in the `.env` file
2. Other: Add `accounts` to the `EXTENSIONS` in the `settings.py` file

#### Notes
1. If there are no email settings (e.g `EMAIL_HOST`, etc), there will be no email verification.

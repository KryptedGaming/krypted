# EVE Online Connector Guide
## Quick Steps
To set up the `django_eveonline_connector` package:
1. Install it (varies, Docker vs Development)
2. (Recommended) Load the default schedule (`python3 manage.py loaddata eveonline_default_schedule`)
3. Create a CCP Application (https://developers.eveonline.com/applications)
4. Add all scopes, enter your callback url (e.g `http://<your_site>/eveonline/sso/callback`)
4. Create an EVE Online client in the Admin Panel (`http://<your_site>/admin`)
5. Input the `CLIENT ID` from your application 
6. Input the `CLIENT_SECRET` from your application

## Periodic Tasks
There are a ton of EVE Online tasks, below are the ones you need to worry about. 

| Command | Description |
| --- | --- |
| `update_all_characters`     | Update character details |
| `update_all_corporations`     | Update corporation details |
| `update_all_alliances`     | Update alliance details |

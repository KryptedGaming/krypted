## EVE Connector
### Overview
The EVE Online Connector is our base module for ESI. This adds characters, corporations, and alliance objects and the tasks to update them. *It's required by nearly other EVE Online package.*

### Quick Steps
To set up the `django_eveonline_connector` package:
1. Install it (varies, Docker vs Development)
2. (Recommended) Load the default schedule (`python3 manage.py loaddata eveonline_default_schedule`)
3. Create a CCP Application (https://developers.eveonline.com/applications)
4. Add all scopes, enter your callback url (e.g `http://<your_site>/eveonline/sso/callback`)
4. Create an EVE Online client in the Admin Panel (`http://<your_site>/admin`)
5. Input the `CLIENT ID` from your application 
6. Input the `CLIENT_SECRET` from your application

### Detailed Steps 
#### 1. Create an EVE Online application
1. Navigate to https://developers.eveonline.com/applications
2. Log in, create a new application
3. Fill out a name. Recommended: [TICKER] - Krypted Platform
4. Fill out a description. 
5. Under connection type, select Authentication & API Access.
6. Add all scopes. 
7. Under callback URL, add `http://<your_site>/eveonline/sso/callback` (`your_site` is your site domain). Save this for later. 
8. Save the application.
9. Copy the CLIENT ID. Save this for later.
10. Copy the CLIENT SECRET. Save this for later. 

#### 2. Create an EVE Online client 
1. Navigate to your Admin Panel on the Krypted platform
2. Click EVE Clients
3. Create an EVE Client 
4. Fill out the CALLBACK URL from Step #1 
5. Fill out the CLIENT ID from Step #1 
6. Fill out the CLIENT SECRET from Step #1 

#### (Optional) Modifying Scopes
At any time, if you need to modify scopes, you can navigate to EVE SCOPES in the Admin Panel and create (or delete) scopes. 

### Tasks
* `django_eveonline_connector.tasks.update_all_characters` This will update all character tokens and their affiliations.
* `django_eveonline_connector.tasks.update_all_corporations` This will update all corporations and their affiliations.
* `django_eveonline_connector.tasks.update_all_alliances` This will update all alliances and their affiliations. 

### Permissions

|    Permission   |   Action    |
|  ---  |  ---  |
| Can view eve charcter  |   Ability to view eve character list  |
| Can view eve corporation   |  Ability to view eve corporation list   |

### Recommened Task Schedule

| Command | Action | Interval |
| --- | --- | --- | 
| `django_eveonline_connector.tasks.update_all_characters`     | Update character details | Every 4 hours |
| `django_eveonline_connector.tasks.update_all_corporations`     | Update corporation details | Every day |
| `django_eveonline_connector.tasks.update_all_alliances`     | Update alliance details | Every day | 
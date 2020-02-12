## EVE Entity Extensions
### Overview
The `django_eveonline_entity_extensions` module extends the EVE Connector, adding objects for journal entries, skills, transactions, contacts, contracts, and many other ESI entities. 

It's great for light auditing and skill checks, and is required by more advanced auditing packages. 

### Quick Steps 
1. Install `django_eveonline_entity_extensions`
2. See permissions and tasks

### Permissions
All of the `view` permissions for EVE Online entity extensions are used. For example, if you want to allow someone to view assets, they need to have the view permission. 

### Tasks 
Tasks for the entity extensions are fairly expensive, and make a ton of ESI calls. We recommend that you use them sparingly, and only update information that is needed. 

Tasks are in the format `update_all_eve_<entity>_<action>`, For example, `update_all_eve_character_skills`. 


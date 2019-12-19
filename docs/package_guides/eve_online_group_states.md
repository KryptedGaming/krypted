## EVE Group States
### Overview
The `django_eveonline_group_states` package allows you to create group states that enable groups based on other Krypted groups, corporations, and alliances. For example, you may create a state called `Blue` which enables your alliance. Then, you would enable it so that members are that state are automatically added to a `Blue` group that syncs with Discord. 

States are extremely powerful, and can be used in numerous ways to set up your community. 

### Quick Steps 
1. Install `django_eveonline_group_states`
2. Navigate to EVE Group States in the Admin Panel
3. Create your group states

|   Variable    |    Meaning   |
|  ---  |  ---  |
|   `Name`    |    The name for your group state   |
|   `Qualifying Groups`    |   Groups that qualify a user to be in this state    |
|   `Qualifying Corporations`    |   Corporations that qualify a user to be in this state    |
|   `Qualifying Alliances`   |    Alliances that qualify a user to be in this state   |
|   `Default Groups`   |   Groups that are automatically assigned to users in this state    |
|   `Enabling Groups`    |  Groups that users in this state can be in     |
|   `Priority`   |   Users are assigned the highest priority state they can be in    |


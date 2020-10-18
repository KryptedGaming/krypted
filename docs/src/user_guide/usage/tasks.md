## Understanding Tasks
Most actions in the Krypted platform are Celery tasks, which allows us to perform backend actions without interrupting the end-user. There are two forms of tasks that we utilize: **Periodic Tasks** and **Signal Tasks**. 

### Signal Tasks
Signal tasks are tasks triggered by events in the web application. For example, if someone adds a new EVE Online character, we might want to re-verify their groups to make sure they are still eligible. 

These are implemented by developers. 

### Periodic Tasks
These are tasks set by **YOU** to run in the background. For example, you might want to check every 5 minutes that everyones' Discord roles are up to date. 

To create a Periodic Task:
1. Navigate to the Admin Panel
2. Click Periodic Tasks
3. Create a new task
4. Add a name for your task (e.g Update All Discord User Groups)
5. Select the registered task (e.g `sync_discord_user_groups`)
6. Add an Interval Schedule (e.g every 5 minutes)

Tasks will be your largest performance hit, so be smart about them. 
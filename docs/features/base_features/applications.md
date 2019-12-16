# Applications
Applications enables our application system, allowing users to submit applications for approval.

## Enabling Applications
1. Docker: Add `applications` to the list of `EXTENSIONS` in the `.env` file
2. Other: Add `applications` to the `EXTENSIONS` in the `settings.py` file

## Creating Templates
Templates are what users will fill out for submission, and will be created in your administration panel.

1. Navigate to your administration panel (https://DOMAIN/admin/)
2. Look for `Application templates`, this is where you will manage templates
3. Name and description are what you'd expect, this is what the user will see when deciding what to submit. 
4. Questions are what questions you'd like people to answer on submission. Click the `+` icon to add questions, or select from existing. 
5. "Groups to add" are groups that are added on application approval.
6. "Groups to remove" are groups that are removed on applcation approval or rejection. 
7. "Required group" is a required group for a user to view this application template. 

## Applications
Under the sidebar menu, you'll see a new `Applications` tab. This is where you'll create and manage applications. 

* The permission `View Application` is required to manage applications. 
* The permission `Change Application` is required to approve or deny applications. 
* If the `django_eveonline_connector` package is installed, applications will display the characters of the applicant. 
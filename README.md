
#About
This is very basic task tracking system. It is o so basic.

You can create a task and delete it, you can even change it's status to "Done".

For this project Django was used. All the views were written as class based 
views, which I got to know trough working on this. Before I did not use them.

What is special about this project is, that it is Django but is playing 
nicely with Google App Engine datastore. Basically it's working with NoSQL 
database.

This was possible with the use of [djangae](http://djangae.readthedocs
.org/en/latest/)(jan-gee), developed by people from [Potato London]
(https://p.ota.to/).

### Eventual consistency

Pages needed a refresh after updating an object in the application

This is due to the fact that the Google App Engine datastore is an 'eventually consistant' database. Once an entity is saved some data retrieval operations may not immediately reflect this change. To read more about this see the Google App Engine [Datastore](https://cloud.google.com/appengine/docs/python/datastore/) documentation.

I solved this with using the Djangae built contrib app.
It caches recently created and/or modified objects so that it knows about them even if they're not yet being returned by the Datastore. You can read more about what it is doing and how
 [here](http://djangae.readthedocs.org/en/latest/consistency/)
 
####Other possible solutions:
* We could just plainly wait for specific amount of time and then call the 
view. This of course is not very efficient and has all sorts of problems, 
however based on the complexity and the scale of the project it could be a 
solution in some cases.
* We could send a request to DB but and trust it to actually execute 
everything while we would change UI without conformation from DB. Seems very
 error prone.
* We can store object in cache and make inmemory changes.


----------
## Setup

- Run `./install_deps` (this will pip install requirements, and download the App Engine SDK)
- `python manage.py loaddata site`
- `python manage.py runserver`


## Tasks - bugs

- Update a ticket - an internal server error occurs
- It is possible to move a ticket from one project to another by altering the URL on the edit ticket page. This should not be allowed
- Tickets will long descriptions break the layout

## Tasks - new features

- On the ticket list page if there are no tickets show "No tickets have been created for this project"
- On the ticket list page if there are no users assigned to a ticket show "No assigned users" in the "assigned" field
- On the project list page, add a new column showing the count of how many tickets there are in each project
- On the project list page, projects that the user has assigned tickets on should be shown above the other projects
- In the edit ticket page show only the email address of each user in the "Assignees" input
- Add the ability to delete tickets
- Improve the multiselect for assignees on the edit ticket page. Consider using a library such as [Chosen](http://harvesthq.github.io/chosen/) to help with this
- Add a watch task to the default gulp task so that changes to any of the SCSS files result in the CSS files being updated


## Bonus tasks

If you feel like carrying on improving this application, please do!

The following consistency task is one that you might like to have a look at.



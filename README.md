HexOcean task for Backend Python+django Engineer position.

Start date: 30.05.2022.
Finish date: 06.05.2022.

Time spent: 55-60 hours

**Note**

I recommend to use this version and use swagger API.

Make sure you have docker and docker-compose installed, 
and install all requirements in file requirements.txt.


Clone git repository, get into valid directory and type in terminal:
docker-compose up

This version of project is made for default API Rest framework user UI.

In this project user authorization is made by token in Swagger UI.

To get admin panel, you need to createsuperuser.
Command:
docker-compose run --rm app sh -c "python manage.py createsuperuser"

Admin site link: http://0.0.0.0:8000/admin/

In admin panel to define which tier using user you need to type in field account_plan:
"bp" - for Basic tier
"pp" - for Premium tier
"ep" - for Enterprise tier
"**" - 2 letters for custom tier created by admin.


Next in application tiers you must create a tier for user and CustomImages also.

Swagger API UI:
http://0.0.0.0:8000/api/docs/

To log in user go to the bottom of site and use POST method /api/user/token/
When credentials are validated, copy token and in top of site you have authorize panel.
type Token and paste your token in "tokenAuth (apiKey)".
Example:
Token 30e2e5c2efe693f5e84eb9ded047e74c5c45cadb

Now you are logged in.

Not admin users can't change anything in tiers, only list method.

To upload image check id of instance /api/tier/custom_images/

Next go to the /api/tier/custom_images/{id}/upload-image/
and change format of request from application/json to multipart/form-data
paste id your image, and it's uploaded!

You can check list of your images in /api/tier/custom_images/
Don't change the value of field "0", and execute code.


To flush database:
In terminal:
1) docker-compose down
2) delete migrations in core directory and tiers.
3) docker-compose up -d --build --remove-orphans
4) docker-compose run --rm app sh -c "python manage.py makemigrations"
5) docker-compose up

Project with Django rest framework default API UI:
https://github.com/Catalyze97/HexOcean-task

**IMPORTANT NOTE** - 
I've changed my schema model of project in last three days, and application tiers was created 
to check how many users are using Basic tier, Premium tier etc. I had no time to refactor this code to work properly,
so this application doesn't fulfill all of its intended functions.
I had no time to create expiring links, but I had an idea how to make this thing.
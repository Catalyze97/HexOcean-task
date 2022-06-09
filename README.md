Start date: 30.05.2022.
Finish date: 06.05.2022.

Time spent: 55-60 hours

Make sure you have docker and docker-compose installed, 
and install all requirements in file requirements.txt.


Clone git repository, get into valid directory and type in terminal:
docker-compose up

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

To log in user go to the link: http://0.0.0.0:8000/api/user/login/
To log in you need in the content box paste json code and post, example:

{
    "email": "user@example.com",
    "password": "password12345745"
}

To log out user go to the link: http://0.0.0.0:8000/api/user/logout/

Check user is logged in:
http://0.0.0.0:8000/api/user/me/

Tier app url:
http://0.0.0.0:8000/api/tier/

App with images:
Check id which you want upload an image.
Here you can also create new custom image instance.
http://0.0.0.0:8000/api/tier/custom_images/

App with uploading images:
After **/custom_images/{PASTE THERE AN ID}/upload-image/

example:
http://0.0.0.0:8000/api/tier/custom_images/1/upload-image/

After you uploaded images you can again check links to your image,
there are only links to user account tier.
http://0.0.0.0:8000/api/tier/custom_images/

To flush database:
In terminal:
1) docker-compose down
2) delete migrations in core directory and tiers.
3) docker-compose up -d --build --remove-orphans
4) docker-compose run --rm app sh -c "python manage.py makemigrations"
5) docker-compose up

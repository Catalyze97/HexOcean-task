How to install:
1. Make sure you have docker and docker-compose installed
2. Clone git repository, get into valid directory and type in terminal:
docker-compose up
3. Create admin user:
docker-compose run --rm app sh -c "python manage.py createsuperuser"
4. Enjoy

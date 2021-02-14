# My-Venue
## To run the Site:
1. Clone this repo to your local machine run `git clone https://github.com/TimilsinaBimal/My-Venue.git`
2. If you don't have `pipenv` install it by running `pip install pipenv`
3. Go to the repo folder and run  `pipenv install --ignore-pipfile`
4. Now go to `myvenue` folder and run  `python manage.py runserver`
5. You need to create MYSQL database named `myvenuedb` in order to run and store data.
6. After you successfully create database run `python manage.py makemigrations` and then `python manage.py migrate`
7. To create admin run `python manage.py createsuperuser` in the project folder.
8. You can change database details in  `settings.py` file inside `myvenue` folder.

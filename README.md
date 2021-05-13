# online-computer-store-project
# Django Notes

Install These:
  - pip install Django==2.5.2
  - pycharm


Register your completed model in admin.py

	- python manage.py makemigrations
	- python manage.py migrate
	
	
If you're finished, run

	- python manage.py runserver
  
	or 
  
	- Click on run button in pycharm
If there is no superuser, run the command 

	- python manage.py createsuperuser

Also,


Creating a “models” (this creates database tables) Go to models.py Django’s official website is a great and easy resource https://docs.djangoproject.com/en/2.1/ref/models/


# Checklist

Main features of the system:
- [x] 1. The online store has a homepage showing 3 suggested systems chosen by a store manager and 3 most popular computers per number of sales.
- [x] 2.The system provides choices of OS (e.g., win, mac, linux), main purpose (business, scientific computing, or gaming), and architecture (e.g., intel, arm) for the customer to choose from, a new page associated with the choices for different parts, such as cpu, gpu, ram, hard disk, battery, screen, software with possible constraints (a more powerful gpu needs better battery, gaming purpose needs better gpu/screen resolution etc.), and the prices, voting, discussions about each item (if available)

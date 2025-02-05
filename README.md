# Book and User Management System

## Overview:

- The Book and User Management System is a Django-based application designed to manage the inventory and reservations of books in an online library. It allows creating, deleting, and updating book entries, as well as creating, deleting, and updating user profiles.

## Permissions:

- Administrators: Can create books and change the status of a book.
- Users: Can reserve and list books.

## Deployment:

- Create a Virtual Environment: Set up a virtual environment to install dependencies.
- Install Dependencies: Run the command pip install -r requirements.txt to install Django and other necessary packages.
- Configure Database Settings: Update the database configurations in settings.py.
- Run Migrations: Execute python manage.py migrate to apply database migrations.
- Create a Superuser: Create an administrative superuser with python manage.py createsuperuser.
- Start the Development Server: Launch the development server with python manage.py runserver.

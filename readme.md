## Devcommunity -- Django
Web application, allow developers connent, share projects and skills. And also they are allowed to rate projects.
This web application is built with Python Django 4, Ninja template engine and for design bootstrap latest version is used in some parts. It also provide api for other application inorder to use its data.
This is build for learning purpose.


1. For the **Admin Panel** the default django admin panel is used.
2. For the **API** the django **rest_framwork** is used.
3. And **JWT** is used **API Authentication**.
4. Reset password funtionality.

**Type of users:**
1. **Super Admin:** This group of user can perform any activity in the system.
    - Perform CRUD on other users.
    - Perform CRUD on Skills.
    - Perform CRUD on projects.
    - Perform CRUD on Tags.
    - Perform CRUD on Reviews.
    - Reset Password.
    - Send message to other users.
2. **Developers:** This group of user can perform certain activities.
    - Perform CRUD of projects only related to theirselves.
    - Edit their profile only.
    - Add new tags to their projects.
    - Perform CRUD on skills related to their selves only.
    - Reset Password.
    - Send message to other users.
    - Review and rate other developers work.
3. **Public Users:** This group of users can only view and send message to developers.

## Prerequisites Modules To Install
1. Python3: Install on [(linux)](https://docs.python-guide.org/starting/install3/linux/)  [(windows)](https://docs.python-guide.org/starting/install3/win/).
2. PostgreSQL (In my case I use postgreSQL): For database [(linux)](https://tecadmin.net/install-postgresql-server-on-ubuntu/) [(Windows)](https://www.guru99.com/download-install-postgresql.html).
3. Setup python virtual environment: [(linux)](https://www.liquidweb.com/kb/how-to-setup-a-python-virtual-environment-on-windows-10/) [(Windows)](https://www.liquidweb.com/kb/how-to-setup-a-python-virtual-environment-on-windows-10/)

**Note: Install the bellow packages inside virtual environment.**
1. Install Django.
    ```
    pip(3) install django
    ```
2. Install Django rest framework.
    ```
    pip(3) install djangorestframework
    ```
3. Install Django JWT package.
    ```
    pip(3) install djangorestframework-simplejwt
    ```
4. Install Django django environment package.
    ```
    pip(3) install django-environ
    ```
5. Install Django python postgreSQL package if you are using postgreSQL as database.
    ```
    pip(3) install psycopg2-binary
    ```
6. Install Django python pillow package for image processing.
    ```
    pip(3) install Pillow
    ```

## Project Structure
1. **devcommunity**: This is the main application of the project. it conatains settings, main urls and server configuration files.
2. **project**: This is project application folder and contains all files and static files related to project application.
2. **user**: This is user profile application folder and contains all files and static files related to user profile application.
4. **templates:** Main templates of the project, and it contains navigation, footer, messages and main template.
5. **static:** Contain static files for overall project and user uploaded assets will also be stored inside this folder.
6. **api:** Rest framework api related code.

## How To Run Project
1. After installing all the packges clone or download this project.
2. Open the project and create new .env file inside devcommunity folder (which is the project folder for the application). and add the following attributes. And add the database and email host details. I used SMTP mailtrap as email host and postgreSQl as Database.
    ```
    EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST='smtp.mailtrap.io'
    EMAIL_HOST_USER=''
    EMAIL_HOST_PASSWORD=''

    DATABASE_NAME=''
    DATABASE_USER=''
    DATABASE_PASSWORD=''
    DATABASE_HOST='127.0.0.1'
    DATABASE_PORT='5432'
    ```
3. Activate your virtual environment. And navigate to project directory where the manage.py file exists using CMD or Terminal.
4. Create migrations.
    ```
    python(3) manage.py makemigrations
    python(3) manage.py migrate
    ```
4. Create Super user.
    ```
    python(3) manage.py createsuperuser
    ```
5. Now run the server.
    ```
    Python(3) manage.py runserver
    ```
6. Now the server is running in localhost:8000

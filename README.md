# Social-Media
#### A Django Chat-Rooms with templates , using Django channels and Websockets.

## Tools :
- Django
- Channels
- HTML
- Css
- Java Script
  
## Featues :
- Register , Login, Logout
- Create New Chat Room , Delete
- Change password of room by admin
- Real-Time Chats
- Multible asynchronous connections in chat


## Installation :
  ### Requirements
  - Python (3.x.x)
  ### SetUp
  - Create virtual environment in Unix , Windows
    ```
    python -m venv venv
    ```
  - Copy project folder to /venv/
    
  - Activate Virtual Environment
    
    Windows
    ```
    /venv/Scripts/activate
    ```
    Unix
    ```
    source /venv/Scripts/activate
    ```
  - Install Requirements
    ```
    cd Chat-Room
    pip install -r requirements.txt
    ```
  - Create database
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
  - Create Admin User (username,password) required
    ```
    python manage.py createsuperuser
    ```
  - Runserver
    ```
    python manage.py runserver
    ```
## Running Tests
run the following command :
```
python manage.py test
```


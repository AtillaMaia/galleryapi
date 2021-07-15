# Getting Started
These steps will get this Python application running on your local machine as a Back-end task <br/> 
using Django framework.

1. Download Python (3.9.5): <br/>
https://www.python.org/downloads/release/python-395/
   

2. In the current folder project (***./gallery/back/***), create a virtual environment and activate it. Follow the <br/> 
   instructions on https://docs.python.org/3/library/venv.html 
   

3. Install application requirements:
```
pip install -r requirements.txt
```

4. In the current folder project (***./gallery/back/***), create a ***.env*** file and set the config <br/>
   variables as the example in .env.example <br/>
   **Note: To run remotely, set these variables on your personal server.  
   

5. Django requirements:
```
python manage.py migrate
python manage.py createsuperuser    # host to approve new photos
python manage.py collectstatic      # in order to show swagger in production (in this case)
```

6. Run:
```
python manage.py runserver
```

# Usage

In order to display the endpoints documentation, Swagger is provided at: 
```
http://127.0.0.1:8000/docs/    # localhost
{URL}/docs/                    # remote  
```

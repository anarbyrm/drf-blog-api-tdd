# Blog Api (TDD)
Blog app api built with Django. This project created following the Test Driven Developement (TDD). It has authentication system, permissions, CRUD functionality for posts and their comments.


# Try the APIs
This project is dockerized, so it is really easy to set this project up on your local computer.

1. Create a virtual environment and activate:
      <div><code>python3 -m venv .venv</code></div>

2. Download packages inside the requirements.txt:
      <div><code>source .venv/bin/activate</code></div>
      
3. Build your containers (Make sure you installed docker on your computer):
      <div><code>docker-compose build</code></div>
      
4. "Up" your containers:
      <div><code>docker-compose up</code></div>
      
5. (Additional) check for tests:
      <div><code>docker-compose run --rm django-app sh -c "python3 manage.py test"</code></div>


6. (Additional) after making changes to models:
      <div><code>docker-compose run --rm django-app sh -c "python3 manage.py makemigrations"</code></div>
      

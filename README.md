# MPB
Python REST API

This project is a backend server and DB for blog.

In this solution I used:
* Python as language
* Flask for web serive with RESTful API
* SQLAlchemy as ORM to access DB
* PyJWT for JWT Authentication

I used Sqlite as database 
after a little research I figured that SQL DB is more suitable for SQLAlchemy ORM that works realy good with flask.
In addition, I looked for easy to implement DB as a begginer in Python and Sqlite works very well for me the task definition

## DB Design:

#### User table:
  - id : primeryKey
  - username: str
  - email: str
  - password: str (Hash)
  - created_date : date
 
#### Post table:
  - id: primeryKey
  - titel: str
  - description: str
  - created_date: date
  - updated_date: date
  - created_user: ForeignKey to User.id
  - likes: int
  
#### Like table:
  - id: primeryKey
  - post_id : ForeignKey to Post.id
  - user_id : ForeignKey to User.id
 
  
## Arbitrary input rule:
  ### Post title need to be unique
  
## API documentation:

### Authentication API : http://127.0.0.1:5000/api/auth/
Routs: (with SWAGGER)
  http://127.0.0.1:5000/api/auth/login
  * register (POST) - add new User
    - body:
        - username
        - email
        - password
    - response:
        - 201 - create new user
        - 400 - not valid data request
        - 409 - data already exists
      
    
  http://127.0.0.1:5000/api/auth/register
  * login (POST) - retrive JSON Token info
    - body:
        - username
        - email
        - password
    - response:
        - 200 - login user
        - 401 - wrong credentials
      
### Blog API : http://127.0.0.1:5000/api/posts/
Routs: (with no SWAGGER)
  http://127.0.0.1:5000/api/posts/
  * get_posts (GET) - get all posts
    - header:
        - JWT
    - response:
        - 200 - get posts
      
  http://127.0.0.1:5000/api/posts/1
  * get_post (GET) - get post by id
    - header:
        - JWT
    - response:
        - 200 - get post
        - 404 - post not found
      
  http://127.0.0.1:5000/api/posts/ 
  * create_post (POST) - new post with logged on user info
    - header:
        - JWT
    - body:
        - titel ( > 1 , < 100 , unique)
        - description ( > 1 , < 1000 )
    - response:
      -  201 - create new post
      -  400 - not valid data request
      -  409 - post already exists
      
   http://127.0.0.1:5000/api/posts/1
   * edit_post (PUT, PATCH) - edit exists post by id with logged on user info
    Authoraized only for created user
    - header:
        - JWT
    - body:
        - titel ( > 1 , < 100 , unique)
        - description ( > 1 , < 1000 )
    - response:
        - 200 - post edited
        - 400 - not valid data request
        - 401 - not authoraized
        - 404 - post not found
      
   http://127.0.0.1:5000/api/posts/1
   * delete_post (DELETE) - delete post by id with logged on user info
    Authoraized only for created user
    - header:
        - JWT
    - response:
        - 204 - post deleted
        - 401 - not authoraized
        - 404 - post not found
      
   http://127.0.0.1:5000/api/posts/like/1
   * add_like (POST) - add loke to post by id with logged on user info
    - header:
        - JWT
    - response:
        - 201 - new like created
        - 404 - post not found
        - 409 - like already exists
      
   http://127.0.0.1:5000/api/posts/like/1
   * remove_like (DELETE) - add loke to post by id with logged on user info
    Authoraized only for created user
    - header:
        - JWT  
    - response:
        - 204 - like deleted
        - 401 - not authoraized
        - 404 - like not found
     
## RUN Project:
  You should have pip version 21.2.4 installed and Python 3.10.2
  
  pip install: https://pip.pypa.io/en/stable/cli/pip_install/
  
  Python setup: https://www.python.org/downloads/
  
  To start app, run the following commands:
  - pip install -r requirements.txt (only for the first time)
  - python -m flask run 

## TEST Project:
  Postman link: https://www.getpostman.com/collections/defe8d6cde59aa0e942f
  
  Also will shared by Email
  
### Develop localy and publish on GitHub
  

      
   
      
  



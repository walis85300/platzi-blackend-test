
# Platzi backend test

  

Hi! I'm Eduardo Álvarez and I made this site, working with Docker, Django and MySQL.

  

### Requirements

- [Docker](https://www.docker.com/)

  

### Especifications

- Inside the project is Dockerfile, this file constains all the scripts and requirements necessary for the execution of the project

- The app is composed of 3 applications, each of them responsible for a specific functionality
		- *Profiles*: contains the logic to handle login, logout, sign up and see the profile detail 
		- *Plans*: constains the logic to handle subscriptions (create and cancel)
		- *Webhooks*: contains the view to handle the stripe webhooks, in this case it is necessary to define three methods to control the events that stripe generates (customer.subscription.created, customer.subscription.deleted and invoice.payment.succeeded)

### How to run

- Clone this repository
```

$ git clone https://github.com/walis85300/platzi-blackend-test.git

$ cd platzi-blackend-test
```
- You need to create a ```.env``` file inside the project folder, the ```STRIPE_SECRET_KEY``` must be defined in this file.

- Run docker with ```docker-compose```
```
docker-compose up 
```
- From any mysql handler you access the database, this in order to create the database that the application will use, the credentials for database are 
		- *user*: root
		- *password*: laclave
- Access to django server shell using  ```docker exec -it django_server_platzi bash```, then execute ```python manage.py makemigrations``` and then ```python manage.py migrate```
- Within the project there are two files that will allow the connection mediating SSL and HTTPS

- You can access to the site at https://localhost 

### Unit tests

I write some unit test, of course you can run it

- You need to write the following command in order to access to the docker machine ```docker exec -it django_server_platzi bash```
- Once there execute the following command ```python manage.py test ```
# Enjoy :)

You can contact me: eduardo.alvarez@protonmail.com, my user in GitHub is walis85300 (in twitter too, and facebook too)
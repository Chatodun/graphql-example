# GraphQL Example

## Getting Started

### Prerequisites

- python3.12
- Docker
- docker-compose
- poetry
- Postgres


### Running with Docker
Start services  
```
docker-compose up -d --build
```

Server is up and running on port 8000

### Getting Started
- **open [url](http://127.0.0.1:8000/signup/) and create account**

- **Important by default, all users who contain the prefix *admin* in username will get the permission to view users:
for example *admin123***

- **users without admin prefix: for example *lalala* will not have access to user browsing**
- **after creating an account, enter the created username and password on the [login](http://127.0.0.1:8000/login/) page and check the functionality of the requests**
- **To change the user, go to this [url](http://127.0.0.1:8000/logout/) and create/log in as an already created user without administrator permissions**
# **CodeCollab: Real-Time Collaborative Code Editor**

CodeCollab is a web-based platform built with Django where multiple users can join a workspace and edit code files simultaneously in real-time. This project is designed to explore advanced concepts in web development, including concurrency with Django Channels, background tasks with Celery, and a robust, scalable architecture using Docker and PostgreSQL.

## **🚀 Development Setup (with Docker)**

This project is fully containerized using Docker and Docker Compose, which is the recommended way to run it for development.

### **Prerequisites**

* [Docker](https://www.docker.com/products/docker-desktop/)  
* [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)  
* Git

### **Step-by-Step Instructions**

1. **Clone the Repository**  
   git clone https://github.com/n-saakib/codecollab.git  
   cd codecollab

2. Create the Environment File  
   The project uses a .env file to manage secrets and environment-specific settings. Copy the example file to create your own local version.  
   cp .env.example .env

   Now, open the .env file and fill in the required values. You will need to generate a Django SECRET\_KEY. You can do this with the following command (once Django is installed in the container):  
   \# You'll run this command later, after the container is built.  
   docker-compose run \--rm api python \-c 'from django.core.management.utils import get\_random\_secret\_key; print(get\_random\_secret\_key())'

3. Build and Run the Containers  
   This command will build the Django application image and start the api and db services in the background.  
   docker-compose up \--build \-d

4. Run Initial Database Migrations  
   The containers are running, but the PostgreSQL database is empty. We need to create the database schema from our Django models.  
   docker-compose exec api python manage.py migrate

5. Create a Superuser  
   To access the Django admin panel, you need to create an administrator account.  
   docker-compose exec api python manage.py createsuperuser

   Follow the prompts to create your user.  
6. You're Ready\!  
   The application is now running.  
   * **Web Application:** [http://localhost:8000](https://www.google.com/search?q=http://localhost:8000)  
   * **Admin Panel:** [http://localhost:8000/admin/](https://www.google.com/search?q=http://localhost:8000/admin/)

## **🏛️ Project Architecture & Concepts**

### **Models (/projects/models.py & /users/models.py)**

The data structure is designed to be scalable and organized.

* **User**: A custom user model that inherits from Django's AbstractUser. This allows us to add custom fields like avatar and last\_seen in the future.  
* **Project**: The main container for a workspace. It has an owner and can have many members.  
* **ProjectMembership**: A "through" model that defines the relationship between a User and a Project. This is crucial because it allows us to store extra information about the relationship, specifically the user's role (e.g., 'Editor' or 'Viewer').  
* **FileSystemItem**: An abstract base model that provides common fields (name, project, parent) for both files and folders, keeping our code DRY.  
* **Folder**: A concrete model inheriting from FileSystemItem that represents a directory. It can have a parent folder, creating a nested structure.  
* **File**: A concrete model inheriting from FileSystemItem that represents a file. It includes a content field to store the text/code and a language field for syntax highlighting.

### **Settings (/config/settings.py)**

The project configuration emphasizes security and portability.

* **Secret Management**: We use django-environ to load all sensitive data (like SECRET\_KEY and database credentials) from a .env file. This file is **not** committed to Git, which prevents secrets from being exposed.  
* **Database**: The application is configured to connect to a PostgreSQL database, the connection details for which are supplied by Docker Compose from the .env file.  
* **Custom User Model**: The AUTH\_USER\_MODEL \= 'users.User' setting tells Django to use our custom user model throughout the entire project, including for authentication and permissions.

### **Useful Docker Commands**

* **Start containers in the background:** docker-compose up \-d  
* **Stop and remove containers:** docker-compose down  
* **View live logs:** docker-compose logs \-f  
* **Run a command inside the api container:** docker-compose exec api \<your-command\> (e.g., bash, python manage.py shell)
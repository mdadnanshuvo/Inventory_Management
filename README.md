# Inventory Management System

## Project Scope

The **Inventory Management System** is a Django-based application for managing property data with geospatial capabilities. The project uses PostgreSQL with the PostGIS extension to handle geospatial data, enabling features like hierarchical location nesting and property geolocation.

---

## Features

- **Geospatial Data Handling**: Uses PostGIS for managing and querying geospatial data.
- **Django Admin Interface**: Provides intuitive data management.
- **Multilingual Support**: Stores property descriptions and policies in multiple languages.
- **Custom Commands**: Generate sitemaps or import data via command-line utilities.
- **User Groups**: Supports role-based permissions for property owners.
- **Dockerized**: Easily deployable with Docker.
- **Testing**: Unit tests ensure over 70% code coverage.

---

## Project Directory Structure

```markdown
Inventory_Management/
├── InventoryManagement/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py
│   ├── db_init.py
│   ├── languages.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── locale/
├── property/
│   ├── __pycache__/
│   ├── migrations/
│   ├── templates/
│   │   └── property/
│   │       ├── home.html
│   │       ├── property_owner_signup.html
│   ├── management/
│   │   └── commands/
│   │       ├── generate_sitemap.py
│   │       ├── import_accommodation.py
│   │       ├── import_location.py
│   ├── tests/
│   ├── uploads/
│   ├── utils/
│   │   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
├── .coverage
├── .dockerignore
├── .gitignore
├── backup_database.sh
├── config.py
├── coverage.xml
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── manage.py
├── mydatabase_backup.sql
├── pytest.ini
├── README.md
├── requirements.txt
├── restore_database.sh
├── sitemap.json
```

## Installation

To get started with the project, clone the repository and follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/mdadnanshuvo/Inventory_Management.git
    ```

2. Navigate to the project directory:
    ```bash
    cd Inventory_Management
    ```

3. Install dependencies and run the application using Docker:

    - Make sure you have [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed on your machine.

    - Build and start the Docker containers:
      ```bash
      docker-compose up --build
      ```

    - This will start the following services:
      - **Django (Backend)**: Running on `http://localhost:8000`
      - **PostgreSQL with PostGIS**
      - **pgAdmin**: Access at `http://localhost:5050`

      
    - For the **Django app**, you can access the application by visiting:
      ```bash
      http://localhost:8000
      ```
      

    - **Visiting pgAdmin**:
        1. Open your browser and go to [http://localhost:5050](http://localhost:5050).
        2. Log in to pgAdmin with the following credentials:
           - **email**: [admin@admin.com]
           - **Password**: [admin] (or whatever password you’ve set in your `docker-compose.yml` or `.env` file)
        
        3. Once logged in, you can add a new PostgreSQL server to manage your database:
            - **Host**: `postgres_postgis1` (this is the service name of the PostgreSQL container)
            - **Port**: `5432`
            - **Username**: [myuser]
            - **Password**: [mypassword]

        

4. Stopping the containers:

    - To stop the containers, use the following command:
      ```bash
      docker-compose down
      ```

5. Docker Entry Point and Data Restoration

   To ensure that the necessary data is restored and the environment is properly set up each time the container starts, a custom entry point has been configured in the `Dockerfile`. The entry point is specified as follows:

```Dockerfile
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
```
This entry point is responsible for restoring data, which eliminates the need to manually recreate superuser accounts or groups every time the repository is cloned and containers are run on a new machine.

  **Login credentials for signing up as admin or superuser:**
     -username : adnanshuvo
     -password : pass4docker
     

 **Handling Entry Point Failures**
 In some cases, due to permission issues or other errors, the entry point might fail to run, preventing the restoration of data. If you encounter any problems with the entry point or data restoration, you can manually restart the 
 application and set it up from scratch by following these steps:
 
 **Steps to Start from Scratch**

   - Remove Existing Containers:
    If there were issues with the entry point or data restoration, first remove ``` ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]``` line from the Dockerfile.

  - Stop all the containers:
    
      ```
    docker-compose down
      ```
    
  - Rebuild the containers:
    
     ```
    docker-compose build
     ```
    
  - Start the containers:
    
     ```
    docker-compose up
     ```

  - Create the Superuser (If Necessary):
     After the containers are up, you may need to manually create a Django superuser if the data restoration did not complete successfully. To do this, run:
    
     ```
    docker-compose exec django_app1 python manage.py createsuperuser
     ```

  - Apply Database Migrations:

    If necessary, apply the database migrations to ensure the database schema is up-to-date:
      
       ```
       docker-compose exec django_app1 python manage.py makemigrations
       docker-compose exec django_app1 python manage.py migrate
       ```
    

## User Registration and Admin Approval Process

### 1. User Registration

Users can register by submitting the registration form at the following URL:
- **Registration Form**: [http://localhost:8000/signup/](http://localhost:8000/signup/)

Once the registration form is submitted, the user’s account will be created, but they will need to be approved by an **admin** to access the system with specific permissions.

### 2. Admin Approval Process

The admin will need to approve the newly registered user and assign them the necessary permissions. Here’s how the admin can approve users:

1. **Login to the Django Admin Panel**:
   - Visit [http://localhost:8000/admin](http://localhost:8000/admin).
   - Use the admin credentials to log in:
     - **Username**: `adnanshuvo`
     - **Password**: `pass4docker`

2. **Approve the User**:
   - In the Django Admin panel, navigate to the **Users** section.
   - Find the newly registered user (who will be in a "pending approval" state).
   - Click on the user’s name to edit their profile.
   - **Make the user a Staff member**:
     - Under the **Permissions** section, check the **Staff status** checkbox. This will grant the user access to the Django Admin interface.
   
3. **Assign User to the Property Owner Group**:
   - In the same user edit page, under **Groups**, select the **Property Owner** group.
   - Save the changes.

By approving the user as a staff member and adding them to the **Property Owner** group, they will be able to manage their own accommodations.

### 3. User Permissions

After being approved, the user will have access to the following:

1. **Login to the Application**:
   - The user can now log in using their username and password at [http://localhost:8000/login/](http://localhost:8000/admin).

2. **Access Accommodations**:
   - The user can add, view, and edit only their own accommodations. They will not be able to access accommodations added by other users.

3. **Add New Accommodation**:
   - After logging in, the user can navigate to the **Accommodations** section and click on **Add Accommodation**.
   - The user can fill in the accommodation details and submit the form. The newly added accommodation will be associated with the user who submitted it.

4. **View and Edit Own Accommodations**:
   - Users will only see their own accommodations listed in the application.
   - They can edit the details of their accommodations, but will not be able to edit or view accommodations created by other users.

---

## Important Notes:

- **Admin Role**: The admin has full control over the users and accommodations. They are responsible for approving users and assigning them to the appropriate groups.
- **Permissions**: Users approved as **staff** and members of the **Property Owner** group will have access to manage only their own accommodations. Admins can override these permissions if necessary.
- **Security**: Make sure to assign roles and permissions carefully to maintain the integrity and security of the application. Only trusted users should be granted staff permissions.

---

By following this process, the application ensures that users can only manage their own accommodations after being approved by the admin.


## Importing Data via CLI

In addition to the web interface, you can import data using the Django CLI (Command Line Interface) within your Docker container. The following commands can be used by both **admin** and **property owners**, provided they are authenticated and have the necessary permissions.

### 1. Importing Locations

Both **admins** and **property owners** can import location data using a CSV file. To import locations, follow these steps:

1. Prepare a CSV file containing the location data. Please follow the csv data format that already existed in the uploads folder. Besides, as the csv files are AI generated, there could be some unstructured data. The app will only accept the data that meet the requirements of the model. For example, the file could be named `locations.csv` and located in the `uploads/` directory of your project.

2. Run the following Docker command to import the locations:

   ```bash
   docker exec -it django_app1 python manage.py import_location uploads/locations.csv
   ```
    
### 2. Importing Accommodations

Authenticated property owners can also import bulk accommodations using a CSV file. To import accommodations, follow these steps:

1. Prepare a CSV file with accommodation data. A sample CSV file (accommodations.csv) is already provided in the uploads/ folder.

Run the following Docker command to import the accommodations:

```bash
   docker exec -it django_app1 python manage.py import_accommodation hridoy robu12345 uploads/accommodations.csv
   ```
In this command:

- `hridoy` is the **property owner's username**.
- `robu12345` is the **property owner's password**.
- `uploads/accommodations.csv` is the **path to the CSV file** containing accommodation data.


### 3. Generating Sitemap

To generate a sitemap for your site, follow these steps:

1. Run the following Docker command to generate the sitemap:

   ```bash
   docker exec -it django_app1 python manage.py generate_sitemap
   ```


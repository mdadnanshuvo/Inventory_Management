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

    - Clone the repository:
      ```bash
      git clone https://github.com/mdadnanshuvo/Inventory_Management.git
      cd Inventory_Management
      ```

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

    - This will stop and remove the containers, but the volumes and data will persist.

## Notes:
- Ensure your environment variables are set correctly for connecting to the PostgreSQL database (such as `DATABASE_URL`, `DB_USER`, `DB_PASSWORD`).
- If you want to connect the Django app to the PostgreSQL container, use the service name (`postgres_postgis1`) as the hostname in your database settings.

      

4. Set up the database (if applicable):
    - [Insert database setup instructions, e.g., create the database schema, run migrations]

5. Run the application:
    - For the backend:
        ```bash
        [Insert backend run command, e.g., dotnet run]
        ```
    - For the frontend:
        ```bash
        [Insert frontend run command, e.g., npm start]
        ```

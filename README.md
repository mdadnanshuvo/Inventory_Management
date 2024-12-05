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

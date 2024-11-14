# Simple Shop

A simple e-commerce backend API for managing products, categories, and a cart system. 

## Table of Contents

- [Simple Shop](#simple-shop)
  - [Table of Contents](#table-of-contents)
  - [Version](#version)
  - [Author](#author)
  - [Features](#features)
  - [Technologies](#technologies)
  - [Installation and Setup](#installation-and-setup)
  - [Loading Fixtures](#loading-fixtures)
  - [Accessing Swagger and Admin Panel](#accessing-swagger-and-admin-panel)

## Version

0.1.0

## Author

Denis Snegirev

## Features

This project offers a structured API with the following features:

- User Authentication using Djoser and AuthToken.
- Product and Category management using Django Admin Panel.
- API for user shopping cart management.
- Pre-configured Swagger documentation.

## Technologies

The primary technologies and libraries used in this project include:

- **Django 5.1.3** - Backend framework.
- **Django REST framework (DRF) 3.15.2** - REST API development.
- **Djoser 2.3.1** - Authentication.
- **DRF Spectacular 0.27.2** - Swagger/OpenAPI documentation.
- **Django Cors Headers 4.6.0** - CORS support for the API.

## Installation and Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/snegirevdv/simple-shop.git
   cd simple-shop
   ```

2. **Set Up Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # `venv\Scripts\activate` for Windows
   ```

3. **Install Dependencies:** Install required packages from `requirements.txt`.

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:** Copy the provided `.env.example` file to create a `.env` file and set necessary environment variables.

   ```bash
   cp .env.example .env
   ```

5. **Database Setup:** Apply migrations to set up the database.

   ```bash
   cd src
   python manage.py migrate
   ```

6. **Run the Developement Server:**

   ```bash
   python manage.py runserver
   ```

## Loading Fixtures

To load initial data for categories, subcategories, and products, run the following commands:

```bash
python manage.py loaddata src/categories/fixtures/categories.json
python manage.py loaddata src/categories/fixtures/subcategories.json
python manage.py loaddata src/products/fixtures/products.json
```

## Accessing Swagger and Admin Panel

- **Swagger Documentation:** Access the API documentation at:

  ```
  http://127.0.0.1:8000/api/docs/
  ```

- **Admin Panel:** The Django Admin interface is available at:

  ```
  http://127.0.0.1:8000/admin/
  ```

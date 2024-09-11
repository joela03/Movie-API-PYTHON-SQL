Movie API Python & SQL

A Python-based API that interacts with a SQL database to retrieve and manage movie data. This project provides a RESTful API for managing a movie collection, allowing users to perform CRUD (Create, Read, Update, Delete) operations.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Project Overview
The **Movie API** is designed to showcase strong SQL and data management skills through the use of PostgreSQL as the primary database. This project provides a RESTful API that allows users to perform various operations on movie data, with a heavy emphasis on database interactions.

The main purpose of this project is to demonstrate efficient database querying, schema design, and data manipulation using SQL. It involves complex SQL operations such as joins, filtering, and aggregations, which are essential for data analytics and business intelligence.

This project highlights:
- **SQL Optimization**: Efficiently designed queries for retrieving movie data, including sorting, filtering, and aggregations.
- **Data Management**: Using SQL to handle CRUD (Create, Read, Update, Delete) operations on the movie dataset.
- **Schema Design**: An optimized relational database schema for storing movie details and user ratings, ensuring normalization and integrity.
- **PostgreSQL Functions and Indexing**: Use of SQL functions and indexing to improve performance, especially for large datasets.

Whether you're interested in data analysis, data science, or backend development, this project showcases practical SQL skills that are critical for managing and analyzing data.

## Features
- Add new movies with details (title, genre, release date, etc.).
- Update existing movie information.
- Delete movies from the database.
- Retrieve a list of all movies or a specific movie by ID.
- Search and filter movies by various attributes (e.g., genre, rating).

## Technologies Used
- **Python 3.x**: Backend language for API logic.
- **Flask**: Web framework for creating RESTful API.
- **PostgreSQL**: Relational database to store and manage movie data.
- **SQLAlchemy**: ORM (Object-Relational Mapping) to interact with PostgreSQL.
- **Postman**: For testing API endpoints (optional, for development use).
  
## Installation

To run this project locally, follow these steps:

### Prerequisites
- Python 3.x installed
- PostgreSQL installed and running
- `pip` for managing Python packages
- `virtualenv` (optional but recommended for environment management)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/joela03/Movie-API-PYTHON-SQL.git
   cd Movie-API-PYTHON-SQL
2. Create and activate a virtual environment:
    *python3 -m venv .venv*
    *source env/bin/activate  # On Windows use `env\Scripts\activate`*
3. Install dependencies:
    *pip install -r requirements.txt*
4. Set up PostgreSQL:
    Ensure PostgreSQL is installed and running.
    Create a database:
    *CREATE DATABASE movie_db;*
    Update the database connection string in the project config file (config.py or .env file depending on your setup).
5. Run the python file
    *python3 api.py*

## API Endpoints
Here is a summary of the main API endpoints:

Method	Endpoint	  Description
GET	    /movies	      Retrieve all movies
GET	    /movies/<id>  Retrieve a specific movie
POST	/movies	      Add a new movie
PUT	    /movies/<id>  Update an existing movie
DELETE	/movies/<id>  Delete a movie

Testing
To run the tests, use the following command:
pytest test_api.py
You can also use Postman to manually test the API endpoints.
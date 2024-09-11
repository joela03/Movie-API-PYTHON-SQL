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
The **Movie API** is a simple RESTful API built with Python and PostgreSQL that allows users to manage a movie database. Users can add, update, delete, and retrieve movies and related information such as movie title, genre, and ratings. This project is an excellent example of how Python can be used to build a backend API while leveraging a relational database to store and query data.

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

API Endpoints
Here is a summary of the main API endpoints:

Method	Endpoint	  Description
GET	    /movies	      Retrieve all movies
GET	    /movies/<id>  Retrieve a specific movie
POST	/movies	      Add a new movie
PUT	    /movies/<id>  Update an existing movie
DELETE	/movies/<id>  Delete a movie .
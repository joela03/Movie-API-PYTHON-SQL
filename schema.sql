-- This file contains all of the SQL commands to create the database, tables and relationships for the Movies Database

DROP TABLE movie_genres;
DROP TABLE genre;
DROP TABLE languages;
DROP TABLE country;
DROP TABLE movie;

CREATE TABLE movie_genres (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    movie_id BIGINT NOT NULL,
    genre_id BIGINT NOT NULL
    );

CREATE TABLE genre(
    genre_id BIGINT,
    genre_name VARCHAR(30) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE languages(
    language_id BIGINT,
    language_name VARCHAR(30) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE country(
    country_id BIGINT,
    country_name VARCHAR(56) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE movie(
    movie_id INT GENERATED ALWAYS AS IDENTITY,
    title TEXT NOT NULL,
    release_date DATE NOT NULL,
    score FLOAT NOT NULL,
    overview TEXT NOT NULL,
    orig_title VARCHAR(191) NOT NULL,
    orig_lang INT NOT NULL,
    budget FLOAT NOT NULL,
    revenue FLOAT NOT NULL,
    country_id INT NOT NULL,
    PRIMARY KEY(movie_id)
);
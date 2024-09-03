"""The purpose of this script is to create function's that load the csv into our psql movies database"""

import csv
import psycopg2
import psycopg2.extras


connection = psycopg2.connect(host='localhost', user='joel',
                              dbname='movies', port=5432)

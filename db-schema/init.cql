-- Exécuter les commandes suivante dans le terminale depuis le repertoire parent pour copier les fichiers csv dans notre conteneur :
-- docker cp db-schema/restaurants.csv cassandra-c01:/restaurants.csv
-- docker cp db-schema/restaurants_inspections.csv cassandra-c01:/restaurants_inspections.csv

CREATE KEYSPACE IF NOT EXISTS resto WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor': 2};

USE resto;

CREATE TABLE restaurant (id int, name varchar, borough varchar, buildingnum varchar, street varchar, zipcode int, phone text, cuisinetype varchar, primary key (id));

CREATE TABLE inspection (idrestaurant int, inspectiondate timestamp, violationcode varchar, violationdescription varchar, criticalflag varchar, score int, grade varchar, primary key (idrestaurant, inspectiondate));

CREATE INDEX index_cuisinetype ON resto.restaurant(cuisinetype);

CREATE INDEX index_grade ON resto.inspection(grade);

COPY Restaurant (id, name, borough, buildingnum, street, zipcode, phone, cuisinetype) FROM 'restaurants.csv' WITH DELIMITER=',';

COPY Inspection (idrestaurant, inspectiondate, violationcode, violationdescription, criticalflag, score, grade) FROM 'restaurants_inspections.csv' WITH DELIMITER=',';
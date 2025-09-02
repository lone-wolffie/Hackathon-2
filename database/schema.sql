CREATE DATABASE recipe_recommender_db;

USE recipe_recommender_db;

CREATE TABLE recipes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255),
  description TEXT,
  nutrition VARCHAR(255)
);

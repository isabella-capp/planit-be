USE test_db;

DROP TABLE IF EXISTS animals;
CREATE TABLE animals (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  habitat VARCHAR(255),
  diet VARCHAR(255)
);

INSERT INTO animals (name, habitat, diet) VALUES
  ('dog', 'land', 'omnivore'),
  ('cat', 'land', 'carnivore'),
  ('fish', 'water', 'omnivore'),
  ('bird', 'air', 'omnivore'),
  ('snake', 'land', 'carnivore'),
  ('whale', 'water', 'omnivore'),
  ('eagle', 'air', 'carnivore'),
  ('shark', 'water', 'carnivore'),
  ('elephant', 'land', 'herbivore');
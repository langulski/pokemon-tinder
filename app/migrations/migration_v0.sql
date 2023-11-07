CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    active BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS pokemons (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30),
    description TEXT,
    hp SMALLINT ,
    attack SMALLINT,
    defense SMALLINT ,
    special_attack SMALLINT ,
    special_defense SMALLINT,
    speed SMALLINT ,
    type_1 VARCHAR(15),
    type_2 VARCHAR(15),
    ability_1 VARCHAR(30),
    ability_2 VARCHAR(30),
    img_url TEXT,
    weight FLOAT
);


CREATE TABLE IF NOT EXISTS selected_pokemons(
    id SERIAL PRIMARY KEY,
    user_id INT,
    pokemon_id INT,
    love BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (pokemon_id) REFERENCES pokemons(id)
);
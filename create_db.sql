CREATE TABLE pokemons (
    id int NOT NULL,
    name varchar(64) UNIQUE NOT NULL,
    base_experience int,
    height int,
    order_number int,
    weight int,
    PRIMARY KEY (id)
);

CREATE TABLE types (
    id int NOT NULL,
    name varchar(32) NOT NULL,
    PRIMARY KEY (name)
);

CREATE TABLE pokemons_types (
    pokemon varchar(64) NOT NULL,
    type varchar(32) NOT NULL,
    PRIMARY KEY (pokemon, type),
    FOREIGN KEY (pokemon) REFERENCES pokemons(name),
    FOREIGN KEY (type) REFERENCES types(name)
);

CREATE TABLE damages (
    attacker varchar(32) NOT NULL,
    defender varchar(32) NOT NULL,
    multiplier float NOT NULL,
    PRIMARY KEY (attacker, defender),
    FOREIGN KEY (attacker) REFERENCES types(name),
    FOREIGN KEY (defender) REFERENCES types(name)
);

CREATE TABLE users (
    id int NOT NULL,
    first_name varchar(64) NOT NULL,
    last_name varchar(64),
    username varchar(64),
    PRIMARY KEY (id)
);

CREATE TABLE chats (
    id bigint NOT NULL,
    type varchar(64) NOT NULL,
    title varchar(256),
    username varchar(64),
    first_name varchar(64),
    last_name varchar(64),
    PRIMARY KEY (id)
);


--DROP TABLE damages;
--DROP TABLE pokemons_types;
--DROP TABLE types;
--DROP TABLE pokemons;
--DROP TABLE users;
--DROP TABLE chats;
--
--DELETE FROM damages;
--DELETE FROM pokemons_types;
--DELETE FROM types;
--DELETE FROM pokemons;
--DELETE FROM users;
--DELETE FROM chats;

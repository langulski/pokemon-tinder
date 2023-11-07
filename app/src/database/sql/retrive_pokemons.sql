SELECT
   pokemons.id,
   pokemons.name,
   REPLACE(REPLACE(pokemons.description, '\n', ' '), '\x0c', '') AS description,
   pokemons.hp,
   pokemons.attack,
   pokemons.defense,
   pokemons.speed,
   pokemons.type_1,
   pokemons.type_2,
   pokemons.img_url
FROM
   pokemons
ORDER BY pokemons.id
LIMIT {limit}
OFFSET (SELECT MAX(pokemon_id) FROM selected_pokemons WHERE user_id={user_id}) + {offset}

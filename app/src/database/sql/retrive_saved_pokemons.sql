SELECT
   pokemons.id,
   pokemons.name,
   pokemons.description,
   pokemons.hp,
   pokemons.attack,
   pokemons.defense,
   pokemons.speed,
   pokemons.type_1,
   pokemons.type_2,
   pokemons.img_url
FROM
   pokemons

INNER JOIN selected_pokemons
ON selected_pokemons.pokemon_id = pokemon_id
WHERE 
1=1
AND selected_pokemons.user_id = {user_id}
AND selected_pokemons.love = true
GROUP BY pokemons.id, selected_pokemons.user_id
ORDER BY pokemons.id
LIMIT {limit}


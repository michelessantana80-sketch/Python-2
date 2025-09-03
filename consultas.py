

#consultas

#selecionar bebidas

consulta01 = '''

            SELECT country, total_litres_of_pure_alcohol
            FROM bebidas
            ORDER BY total_litres_of_pure_alcohol DESC
            LIMIT 10
        '''
consulta02 = '''
            SELECT AVG(beer_servings) AS cerveja, AVG (spirit_servings) AS destilados, AVG (wine_servings) AS vinho
            FROM bebidas
'''
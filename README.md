# Bola de Cristal do Futebol

## Rotas
- /teams [GET]
   - retorna todos os times disponivel em forma de array
    ```
    {
      "count": 20,
      "teams": [
        {
          "id": 1765,
          "name": "Fluminense FC",
          "shortname": "Fluminense"
        },
        {
          "id": 1766,
          "name": "CA Mineiro",
          "shortname": "Mineiro"
        },
        ...
      ]
    }
    ```
- /calculate [POST]
  - recebe um body com um array que deve conter 2 objetos onde dentro deve haver id de times
    ```
    [
    	{
    		"id": "1769"
    	},
    	{
    		"id": "1783"
    	}
    ]
    ```
  - retorna os seguintes valores
    ```
    {
        "odds": {
            "oddEmpate": "3.00",
            "oddTeamA": "2.00",
            "oddTeamB": "2.00",
            "probabilidadeEmpate": "33.33%",
            "probabilidadeTimeA": "50.00%",
            "probabilidadeTimeB": "50.00%"
        },
        "teamStats": {
            "teamA": {
                "draw": 9,
                "goalDifference": 26,
                "goalFor": 58,
                "id": 1769,
                "lost": 8,
                "name": "SE Palmeiras",
                "shortName": "Palmeiras",
                "won": 18
            },
            "teamB": {
                "draw": 9,
                "goalDifference": 17,
                "goalFor": 54,
                "id": 1783,
                "lost": 8,
                "name": "CR Flamengo",
                "shortName": "Flamengo",
                "won": 18
            }
        }
    }
```

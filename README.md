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
    	"Odd de Empate": "3.00",
    	"Odd do Flamengo": "2.00",
    	"Odd do Palmeiras": "2.00",
    	"Probabilidade de empate": "33.33%",
    	"Probabilidade de time Flamengo ganhar": "50.00%",
    	"Probabilidade de time Palmeiras ganhar": "50.00%"
    }
    ```

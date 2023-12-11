from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS # Importação da extensão CORS

load_dotenv()

app = Flask(__name__)

CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}}) # Inicialização do CORS com a aplicação Flask

API_TOKEN = os.getenv("API_TOKEN")
BASE_URL = "https://api.football-data.org/v4"


@app.route("/")
def hello_world():
    return jsonify({"message": "Hello, World!"})


@app.route("/teams")
def getAllTeams():
    api_url = f"{BASE_URL}/competitions/BSA/teams?sesson=2023"

    headers = {"X-Auth-Token": API_TOKEN, "Content-Type": "application/json"}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        all_data_teams = response.json()["teams"]
        filtered_data_teams = []

        for team in all_data_teams:
            filtered_data_teams.append(
                {"id": team["id"], "name": team["name"], "shortname": team["shortName"]}
            )

        return jsonify(
            {"count": len(filtered_data_teams), "teams": filtered_data_teams}
        )
    else:
        return jsonify({"error": "Failed to fetch data from external API"}), 500


def calculate_probabilities_and_odds(teams_info):
    # Desestrutura os dados dos times
    team_info_A, team_info_B = teams_info

    # Probabilidades e odds
    P_A = (team_info_A["won"] + team_info_B["draw"]) / (
        team_info_A["won"]
        + team_info_A["draw"]
        + team_info_B["won"]
        + team_info_B["draw"]
    )
    P_Draw = (team_info_A["draw"] + team_info_B["draw"]) / (
        team_info_A["won"]
        + team_info_A["draw"]
        + team_info_B["won"]
        + team_info_B["draw"]
    )
    P_B = (team_info_B["won"] + team_info_A["draw"]) / (
        team_info_A["won"]
        + team_info_A["draw"]
        + team_info_B["won"]
        + team_info_B["draw"]
    )

    odd_A = 1 / P_A
    odd_Draw = 1 / P_Draw
    odd_B = 1 / P_B

    json_result = {
        "probabilidadeEmpate": f"{P_Draw * 100:.2f}%",
        "probabilidadeTeamA": f"{P_A * 100:.2f}%",
        "probabilidadeTeamB": f"{P_B * 100:.2f}%",
        "oddTeamA": f"{odd_A:.2f}",
        "oddEmpate": f"{odd_Draw:.2f}",
        "oddTeamB": f"{odd_B:.2f}",
    }

    return json_result


@app.route("/calculate", methods=["POST"])
def calculateOdds():
    try:
        data = request.json

        if not data:
            return jsonify({"error": "Nenhum dado fornecido"}), 400

        if len(data) != 2:
            return jsonify({"error": "Precisa conter 2 times"}), 400

        if "id" not in data[0] or "id" not in data[1]:
            return (
                jsonify(
                    {
                        "error": "A propriedade 'minha_propriedade' é obrigatória para os dois itens"
                    }
                ),
                400,
            )

        team_a, team_b = data

        api_url = f"{BASE_URL}/competitions/BSA/standings"

        headers = {"X-Auth-Token": API_TOKEN, "Content-Type": "application/json"}

        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            all_teams = response.json()["standings"][0]["table"]
            teams_to_check = []

            for team_data in all_teams:
                if (
                    str(team_data["team"]["id"]) == team_a["id"]
                    or str(team_data["team"]["id"]) == team_b["id"]
                ):
                    teams_to_check.append(
                        {
                            "id": team_data["team"]["id"],
                            "name": team_data["team"]["name"],
                            "shortName": team_data["team"]["shortName"],
                            "goalFor": team_data["goalsFor"],
                            "goalDifference": team_data["goalDifference"],
                            "won": team_data["won"],
                            "draw": team_data["draw"],
                            "lost": team_data["lost"],
                        }
                    )

            odds_info = calculate_probabilities_and_odds(teams_to_check)
            teams_stats = {
                "teamA": teams_to_check[0],
                "teamB": teams_to_check[1],
            }

            return jsonify({"odds": odds_info, "teamStats": teams_stats})
        else:
            return jsonify({"error": "Failed to fetch data from external API"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

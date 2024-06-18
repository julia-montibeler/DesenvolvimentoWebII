from flask import Flask, render_template, request, jsonify
import requests

from models.pokemon import Pokemon

app = Flask(__name__, static_url_path='')

def fetch_pokemon_data(id):
    url = f"https://pokeapi.co/api/v2/pokemon/{id}"
    response = requests.get(url)
    data = response.json()
    return {
        'id': data['id'],
        'name': data['name'].capitalize(),
        'sprites': data['sprites']['front_default'],
        'types': [t['type']['name'].capitalize() for t in data['types']],
    }

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/buscar', methods=["GET", "POST"])
def buscar():
    pokemon_name = request.form["nome"].lower()
    pokemon_data = fetch_pokemon_data(pokemon_name)
    if pokemon_data:
        return render_template('home.html', nome=pokemon_data['name'], foto=pokemon_data['sprites'])
    return "Not found"

@app.route('/pokedex')
def pokedex():
    pokemon_list = [" ".join(i["name"].split("-")).title() for i in requests.get(f'https://pokeapi.co/api/v2/pokemon/?limit=-1').json()["results"]]
    return render_template("pokedex.html", pokemon=pokemon_list)

@app.route('/api/pokemon/<int:id>')
def pokemon_detail(id):
    pokemon_data = fetch_pokemon_data(id)
    if pokemon_data:
        return jsonify(pokemon_data)
    return jsonify({'error': 'Pokémon não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)

import json
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
    silhouette = "https://i.pinimg.com/originals/3d/f6/ef/3df6eff48175fa05ec90a00415fcfe25.png"
    return render_template('home.html', nome = "??", foto = silhouette, peso = 0, altura = 0, tipos = "??", id = 0, foto_costas = silhouette, foto_shiny = silhouette, foto_costas_shiny = silhouette)

@app.route('/buscar', methods = ["GET", "POST"])
def buscar():
    pokemon = request.form["nome"].lower()
    try:
        res = json.loads(requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}").text)

        print(res["forms"][0]["name"].title())

        foto = res["sprites"]["front_default"]
        foto_costas = res["sprites"]["back_default"]
        foto_shiny = res["sprites"]["front_shiny"]
        foto_costas_shiny = res["sprites"]["back_shiny"]
        nome = res["forms"][0]["name"].title()
        id = res["id"]
        peso = res["weight"]
        altura = res["height"]
        tipos = [res["types"][0]["type"]["name"].title()]
        if len(res["types"])> 1:
            tipos.append(" e " + res["types"][1]["type"]["name"].title())
          
    except:
        silhouette = "https://i.pinimg.com/originals/3d/f6/ef/3df6eff48175fa05ec90a00415fcfe25.png"
        return render_template('home.html', nome = "??", foto = silhouette, peso = 0, altura = 0, tipos = "??", id = 0, foto_costas = silhouette, foto_shiny = silhouette, foto_costas_shiny = silhouette)
    
    return render_template('home.html', nome = nome, foto = foto, peso = peso, altura = altura, tipos = tipos, id = id, foto_costas = foto_costas, foto_shiny = foto_shiny, foto_costas_shiny = foto_costas_shiny)

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

from flask import Flask, render_template, request
import requests
import json

from models.pokemon import Pokemon

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/buscar', methods = ["GET", "POST"])
def buscar():
    pokemon = Pokemon(request.form["nome"].lower(), "")
    try:
          res = json.loads(requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon.nome}").text)
          result = res["sprites"]
          result = result["front_default"]
          pokemon.foto = result
    except:
          return "not found"
    return render_template('home.html', nome = pokemon.nome, foto = pokemon.foto)
    
@app.route('/adivinhar')

def adivinhar():
    return render_template("adivinhar.html")

@app.route('/pokedex', methods = ["GET", "POST"])

def pokedex():
    pokemon = [" ".join(i["name"].split("-")).title() for i in requests.get(f'https://pokeapi.co/api/v2/pokemon/?limit=-1').json()["results"]]
    return render_template("pokedex.html", pokemon=pokemon)


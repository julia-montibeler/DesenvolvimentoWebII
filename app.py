from flask import Flask, json, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    return render_template('home.html', nome="??", foto=silhouette, peso=0, altura=0, tipos="??", id=0, foto_costas=silhouette, foto_shiny=silhouette, foto_costas_shiny=silhouette)

@app.route('/buscar', methods=["GET", "POST"])
@login_required
def buscar():
    pokemon = request.form["nome"].lower()
    try:
        res = json.loads(requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}").text)
        foto = res["sprites"]["front_default"]
        foto_costas = res["sprites"]["back_default"]
        foto_shiny = res["sprites"]["front_shiny"]
        foto_costas_shiny = res["sprites"]["back_shiny"]
        nome = res["forms"][0]["name"].title()
        id = res["id"]
        peso = res["weight"]
        altura = res["height"]
        tipos = [res["types"][0]["type"]["name"].title()]
        if len(res["types"]) > 1:
            tipos.append(" e " + res["types"][1]["type"]["name"].title())
    except:
        silhouette = "https://i.pinimg.com/originals/3d/f6/ef/3df6eff48175fa05ec90a00415fcfe25.png"
        return render_template('home.html', nome="??", foto=silhouette, peso=0, altura=0, tipos="??", id=0, foto_costas=silhouette, foto_shiny=silhouette, foto_costas_shiny=silhouette)
    return render_template('home.html', nome=nome, foto=foto, peso=peso, altura=altura, tipos=tipos, id=id, foto_costas=foto_costas, foto_shiny=foto_shiny, foto_costas_shiny=foto_costas_shiny)

@app.route('/pokedex')
@login_required
def pokedex():
    pokemon_list = [" ".join(i["name"].split("-")).title() for i in requests.get(f'https://pokeapi.co/api/v2/pokemon/?limit=-1').json()["results"]]
    return render_template("pokedex.html", pokemon=pokemon_list)

@app.route('/api/pokemon/<int:id>')
def pokemon_detail(id):
    pokemon_data = fetch_pokemon_data(id)
    if pokemon_data:
        return jsonify(pokemon_data)
    return jsonify({'error': 'Pokémon não encontrado'}), 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
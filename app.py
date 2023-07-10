from flask import Flask, redirect, render_template, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
from sqlalchemy.sql import text

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Sunniva2023'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = False
debug = DebugToolbarExtension(app)


connect_db(app)

@app.route('/')
def show_homepage():
    """Renders index.html template"""
    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes)


@app.route('/api/cupcakes')
def get_cupcakes():
    """Get Data about all cupcake"""

    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]

    return jsonify(cupcakes=all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def get_one_cupcake(id):
    """Grabs a single cupcake with id"""

    cupcake = Cupcake.query.get_or_404(id)

    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Creates a new cupcake"""

    data = request.json

    new_cupcake = Cupcake(
        flavor=data["flavor"],
        size=data["size"],
        rating=data["rating"],
        image=data['image'] or None)
    
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)
   
@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """Update Cupcake's"""

    data = request.json
    cupcake = Cupcake.query.get_or_404(id)
    
    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.size = data.get('size', cupcake.size)
    cupcake.rating = data.get('rating', cupcake.rating)
    cupcake.image = data.get('image', cupcake.image)

    db.session.commit()
    response_json = jsonify(cupcake=cupcake.serialize())
    return response_json

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """Delete a cupcake from API"""

    delete_cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(delete_cupcake)
    db.session.commit()

    response_json = jsonify(message="DELETED")
    return response_json
    


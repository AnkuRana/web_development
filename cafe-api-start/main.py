from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
API_KEY = "get-your-own-key"

##Connect to Database
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)
    
    def to_dict(self):
        return {column.name:getattr(self,column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record
@app.route("/random")
def get_random():
    cafes = db.session.query(Cafe).all()
    random_choice = random.choice(cafes)
    random_choice = random_choice.to_dict()
    return jsonify(cafe=random_choice)

@app.route("/all")
def get_all_cafes():
    cafes = db.session.query(Cafe).all()
    cafes_dict = { cafe.name: cafe.to_dict() for cafe in cafes }
    return jsonify(cafes=cafes_dict)

@app.route("/search")
def serachby_location():
    location = request.args.get("loc")
    cafes = db.session.query(Cafe).all()
    cafes_dict = {}
    for cafe in cafes:
        if cafe.location == location:
             cafes_dict[cafe.name]=cafe.to_dict()
    if cafes_dict == {}:
        cafes_dict["error"] = {"not found": "Sorry, we could not find cafe at that location."}
    return jsonify(cafes=cafes_dict)
## HTTP POST - Create Record

@app.route("/add", methods=["POST","GET"])
def add_cafe():
    data = request.form
    response_dict = {"response": {'Error': 'Failed to add new cafe.'} }

    # they are local variables
    has_wifi = False
    has_sockets = False
    has_toilet = False
    can_take_calls = False

    if request.method == "POST":
    #     here key value pairs are being sent by a post request like data['has_wifi']
    # rewuest send through post request comes as string even if they are boolean
        # if data["has_wifi"] == "true":
        #     has_wifi = True
        # if data["has_sockets"] == "true":
        #     has_sockets = True
        # if data["has_toilet"] == "true":
        #     has_toilet = True
        # if data["can_take_calls"] == "true":
        #     can_take_calls = True
        cafe = Cafe(
            name=data["name"],
            map_url=data["map_url"],
            img_url=data["img_url"],
            location=data["location"],
            seats=data["seats"],
            has_toilet=bool(data["has_toilet"]),
            has_wifi=bool(data["has_wifi"]),
            has_sockets=bool(data["has_sockets"]),
            can_take_calls=bool(data["can_take_calls"]),
            coffee_price=data["coffee_price"]
            )
        db.session.add(cafe)
        db.session.commit()
        response_dict["response"] = {"success": "Successfully added the new cafe."}
    return jsonify(new_cafe=response_dict)
## HTTP PUT/PATCH - Update Record

@app.route("/update-price/<int:id>", methods=["PATCH"])
def update_price(id):
    response_dict = {}
    response_dict["response"]= {"error": "Failed to update the price."}
    new_price = request.args.get("new_price")
    cafe = db.get_or_404(Cafe, id)
    if cafe:
        # cafe = db.session.execute(db.select(Cafe).filter_by(id=id)).scalar() #scalar is requred refer doc
        #if this method is used
        cafe.coffee_price = new_price
        db.session.commit()
        response_dict["response"] = {"success": "Successfully  updated the new price."}
        return jsonify(reponse=response_dict), 200
    else:
        return jsonify(reponse=response_dict), 404
        

## HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    response_dict = {}
    cafe = db.get_or_404(Cafe, cafe_id , description=f"searched cafe with id={cafe_id} does not exist.")
    if cafe:
        if request.args.get("api_key") == API_KEY:
            db.session.delete(cafe)
            db.session.commit()
            response_dict["response"] = {"success": "Successfully deleted the cafe from list of cafes."}
            return jsonify(reponse=response_dict), 200
        else:
            response_dict["response"] = {"Forbidden": "You are not authorised to carry out this action."}
            return jsonify(reponse=response_dict), 403
    else:
        response_dict["response"] = {"error": "Cafe with provided id does not exist."}
        return jsonify(reponse=response_dict), 404


if __name__ == '__main__':
    app.run(debug=True)

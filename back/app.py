import json
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///garage.sqlite3'
app.config['SECRET_KEY'] = "random string"
CORS(app)

db = SQLAlchemy(app)

# Model
class Car(db.Model):
    id = db.Column('car_id', db.Integer, primary_key=True)
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    color = db.Column(db.String(50))
    owner = db.Column(db.String(100))

    def __init__(self, brand, model, color, owner):
        self.brand = brand
        self.model = model
        self.color = color
        self.owner = owner

    def to_dict(self):
        return {
            'id': self.id,
            'brand': self.brand,
            'model': self.model,
            'color': self.color,
            'owner': self.owner
        }


@app.route("/")
def show_all_cars():
    cars_list = [car.to_dict() for car in Car.query.all()]
    json_data = json.dumps(cars_list)
    return json_data

@app.route('/new', methods=['POST'])
def add_car():
    data = request.get_json()
    brand = data['brand']
    model = data['model']
    color = data['color']
    owner = data['owner']

    new_car = Car(brand, model, color, owner)
    db.session.add(new_car)
    db.session.commit()
    return "A new car was added."

@app.route("/delete/<int:car_id>", methods=["DELETE"])
def delete_car(car_id):
    car = Car.query.get(car_id)
    if car:
        db.session.delete(car)
        db.session.commit()
        return "Car deleted successfully"
    else:
        return "Car not found"

@app.route("/update/<int:car_id>", methods=["PUT"])
def update_car(car_id):
    car = Car.query.get(car_id)
    if car:
        data = request.get_json()
        car.brand = data['brand']
        car.model = data['model']
        car.color = data['color']
        car.owner = data['owner']
        db.session.commit()
        return "Car updated successfully"
    else:
        return "Car not found"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

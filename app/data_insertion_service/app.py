from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import time
import psycopg2
from sqlalchemy.exc import OperationalError

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@db:5432/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    value = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Data {self.name}>'
    
def wait_for_db():
    retries = 5
    while retries > 0:
        try:
            # Try to create a connection to the database
            db.session.execute('SELECT 1')
            return
        except OperationalError:
            retries -= 1
            print("Database is not ready, retrying in 5 seconds...")
            time.sleep(5)
    raise Exception("Database is not ready after multiple attempts")

@app.route('/insert_data', methods=['POST'])
def insert_data():
    data = request.json
    new_entry = Data(name=data['name'], value=data['value'])
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Data inserted successfully"}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created within the application context
    app.run(host='0.0.0.0', port=5001)

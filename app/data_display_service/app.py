from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@db:5432/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    value = db.Column(db.String(120), nullable=False)

@app.route('/get_data', methods=['GET'])
def get_data():
    data = Data.query.all()
    data_list = [{"id": row.id, "name": row.name, "value": row.value} for row in data]
    return jsonify(data_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

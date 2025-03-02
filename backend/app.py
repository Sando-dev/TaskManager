from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#configura la base de datos SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

@app.route("/")
def hello_world():
    return "Hola, mundo"

if __name__ == "__main__":
    app.run(debug=True)
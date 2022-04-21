from flask_app import app
from flask_app.controllers import users, apis

if __name__ == "__main__":
    app.run(debug=True)
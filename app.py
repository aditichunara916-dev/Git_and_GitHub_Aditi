from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
import json
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv
import os
from forms import DataForm

app = Flask(__name__)

load_dotenv()

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

csrf = CSRFProtect(app)

client = MongoClient(os.getenv("MONGO_URI"))
db = client["flask_assignment_3"]
collection = db["users"]


@app.route('/api')
def api():
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
        return jsonify(data)
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({"error": "Unable to read data"}), 500

@app.route('/', methods=['GET', 'POST'])
def form():
    form = DataForm()

    if form.validate_on_submit():
        name = form.name.data.strip()
        email = form.email.data.strip()

        try:
            collection.insert_one({
                'name': name,
                'email': email
            })
            return redirect(url_for('success'))

        except PyMongoError:
            return render_template('form.html', form=form, error="Database error")

    return render_template('form.html', form=form)

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    item_name = request.form.get('itemName')
    item_description = request.form.get('itemDescription')

    collection.insert_one({
        'itemName': item_name,
        'itemDescription': item_description
    })

    return "To-Do item submitted successfully"

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run()
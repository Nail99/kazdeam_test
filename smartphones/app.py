import json
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    with open('smartphones.json') as json_file:
        data = json.load(json_file)
    return data


@app.route('/smartphones/<int:price>')
def smartphones_by_price(price):
    with open('smartphones.json') as json_file:
        data = json.load(json_file)
    filtered_data = [item for item in data if item['price'] == str(price)]
    return filtered_data


if __name__ == '__main__':
    app.run(debug=True)

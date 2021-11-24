import json
from flask_caching import Cache

from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

with open('raw_data.json') as f:
    data = json.load(f)


def calculate(value_one, value_two, amount):
    return (value_two / value_one) * float(amount)


@app.route("/", methods=['POST', 'GET'])
def home():
    """Simple html converter. Render result of conversion"""

    if request.method == "POST":
        currency = request.form.get("currency")
        convert_currency = request.form.get("convert_currency")
        try:
            amount = request.form.get("amount")
        except ValueError as e:
            return e

        currency = currency.upper()
        convert_currency = convert_currency.upper()
        currency_value = data["rates"][currency]
        convert_currency_value = data["rates"][convert_currency]

        new_amount = calculate(currency_value, convert_currency_value, amount)
        new_amount = f"{new_amount:.2f}"

        return render_template(['home.html'], value=new_amount)
    return render_template(['home.html'])


@app.route("/api")
def get_all():
    return jsonify(data['rates'])


@app.route('/api/<string:currency_one><string:currency_two><int:amount>')
def get_currency(currency_one, currency_two, amount):
    # i - case insensitive
    icurrency_one = currency_one.upper()
    icurrency_two = currency_two.upper()
    value_one = data['rates'][icurrency_one]
    value_two = data['rates'][icurrency_two]

    new_amount = calculate(value_one, value_two, amount)
    context = {"currency_one": currency_one, "currency_two": currency_two, "amount": amount, "new_amount": new_amount}

    return jsonify(context=context)


@app.route('/api/convert')
@Cache.cached(timeout=100000, key_prefix='all_components')
def convert():
    """Api endpoint returns the result as json"""

    currency_one = request.args.get("currency_one")
    currency_two = request.args.get("currency_two")
    amount = request.args.get("amount")
    try:
        amount = int(amount)
        assert amount > 0
    except TypeError as e:
        return e
    except Exception as e:
        return e
    #
    # currency_one = currency_one.upper()
    # currency_two = currency_two.upper()

    value_one = data["rates"][currency_one]
    value_two = data["rates"][currency_two]

    new_value = calculate(value_one, value_two, amount)

    context = {
        "currency_one": currency_one,
        "currency_two": currency_two,
        "amount": new_value
    }

    return jsonify(context)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True)

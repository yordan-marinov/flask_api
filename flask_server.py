import json
from flask import Flask, request, render_template

app = Flask(__name__)

with open('raw_data.json') as f:
    exchange_rates_data = json.load(f)


def exchange(value_one, value_two, amount):
    """Calculate the amount by current rate. Return float"""

    return (value_two / value_one) * float(amount)


def get_requested_data(request_method=None):
    """Collecting the requested data. Return JSON"""

    base_currency = request_method.get("base_currency").upper()
    to_currency = request_method.get("to_currency").upper()

    amount = request_method.get("amount")
    try:
        amount = int(amount)
        assert amount > 0
    except TypeError as e:
        return e
    except Exception as e:
        return e

    base_currency_value = exchange_rates_data["rates"][base_currency]
    to_currency_value = exchange_rates_data["rates"][to_currency]

    return {
        "base_currency": base_currency,
        "to_currency": to_currency,
        "base_currency_value": base_currency_value,
        "to_currency_value": to_currency_value,
        "amount": amount
    }


@app.route("/", methods=['POST', 'GET'])
def home():
    """Simple html form. Return JSON"""

    if request.method == "POST":
        (
            base_currency,
            to_currency,
            base_currency_value,
            to_currency_value,
            amount_value
        ) = get_requested_data(request_method=request.form).values()

        converted_amount_value = f"{exchange(base_currency_value, to_currency_value, amount_value):.2f}"

        return {
            "base_currency": base_currency,
            "to_currency": to_currency,
            "amount_to_convert": f"{amount_value:.2f}",
            "converted_amount": converted_amount_value
        }

    return render_template(['home.html'])


@app.route('/api/convert')
def convert():
    """API endpoint converts two given currencies to current rates. Return JSON"""

    (
        base_currency,
        to_currency,
        base_currency_value,
        to_currency_value,
        amount_value
    ) = get_requested_data(request_method=request.args).values()

    converted_amount_value = f"{exchange(base_currency_value, to_currency_value, amount_value):.2f}"

    return {
        "base_currency": base_currency,
        "to_currency": to_currency,
        "amount_to_convert": f"{amount_value:.2f}",
        "converted_amount": converted_amount_value
    }


@app.route("/api/all")
def get_all_currencies_rates():
    """API end point for all current currencies - rates. Return JSON"""

    return exchange_rates_data['rates']


@app.route('/convert/<string:base_currency><string:to_currency><int:amount>')
def url_query_string_convert(base_currency, to_currency, amount):
    """URL query string converter. Return JSON"""

    base_currency_value = exchange_rates_data['rates'][base_currency.upper()]
    to_currency_value = exchange_rates_data['rates'][to_currency.upper()]

    converted_amount = exchange(base_currency_value, to_currency_value, amount)
    return {
        "base_currency": base_currency,
        "to_currency": to_currency,
        "amount": amount,
        "converted_amount": converted_amount
    }


if __name__ == '__main__':
    app.run(debug=True)

import os
from flask import Flask, redirect, request, render_template
import stripe
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

app = Flask(__name__)

products = [
    {'id': 'prod_1', 'name': 'Producto 1', 'price': 10},
    {'id': 'prod_2', 'name': 'Producto 2', 'price': 15},
    {'id': 'prod_3', 'name': 'Producto 3', 'price': 20}
]

YOUR_DOMAIN = os.environ.get('APP_DOMAIN')

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        selected_products = request.form.getlist('product')
        line_items = []

        for product_id in selected_products:
            product = next((p for p in products if p['id'] == product_id), None)
            if product:
                line_items.append({
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': product['name'],
                        },
                        'unit_amount': product['price'] * 100,
                    },
                    'quantity': 1
                })

        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

if __name__ == '__main__':
    app.run(port=4242)

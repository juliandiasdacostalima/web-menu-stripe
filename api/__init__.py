import logging
import os
import stripe
import json

import azure.functions as func

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

products = [
    {'id': 'prod_1', 'name': 'Producto 1', 'price': 10},
    {'id': 'prod_2', 'name': 'Producto 2', 'price': 15},
    {'id': 'prod_3', 'name': 'Producto 3', 'price': 20}
]

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        selected_products = body.get('products', [])
        line_items = []

        for product_id in selected_products:
            product = next((p for p in products if p['id'] == product_id), None)
            if product:
                line_items.append({
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {'name': product['name']},
                        'unit_amount': product['price'] * 100,
                    },
                    'quantity': 1
                })

        YOUR_DOMAIN = os.environ.get('APP_DOMAIN')

        session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )

        return func.HttpResponse(
            json.dumps({'url': session.url}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(str(e), status_code=500)

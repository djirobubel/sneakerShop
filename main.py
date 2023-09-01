from flask import Flask
from blueprints.product.product import product_bp
from blueprints.user.user import user_bp
from blueprints.order.order import order_bp

app = Flask(__name__)
app.register_blueprint(product_bp)
app.register_blueprint(user_bp)
app.register_blueprint(order_bp)

if __name__ == "__main__":
    app.run()

from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

app.secret_key = "devops-login-secret-key"


# ============================================================
# LOGIN / HOME
# ============================================================

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        email = request.form["email"]

        session["email"] = email
        session["cart"] = []

        return redirect(url_for("menu"))

    return render_template("login.html")


# ============================================================
# MENU
# ============================================================

@app.route("/menu")
def menu():

    email = session.get("email")
    cart = session.get("cart", [])

    # Count how many of each food item is in the cart
    quantities = {}

    for item in cart:
        quantities[item] = quantities.get(item, 0) + 1

    return render_template(
        "menu.html",
        email=email,
        cart_count=len(cart),
        quantities=quantities
    )


# ============================================================
# ADD ITEM FROM MENU
# ============================================================

@app.route("/add/<item>")
def add_to_cart(item):

    cart = session.get("cart", [])

    cart.append(item)

    session["cart"] = cart

    return redirect(url_for("menu"))


# ============================================================
# CART
# ============================================================

@app.route("/cart")
def cart():

    cart = session.get("cart", [])

    return render_template(
        "cart.html",
        cart=cart
    )


# ============================================================
# REMOVE ONE ITEM
# Used by the "-" button
# ============================================================

@app.route("/cart/remove/<item>")
def remove_from_cart(item):

    cart = session.get("cart", [])

    if item in cart:
        cart.remove(item)

    session["cart"] = cart

    return redirect(url_for("cart"))


# ============================================================
# REMOVE ONE ITEM FROM MENU
# Used by the "-" button on the Menu
# ============================================================

@app.route("/menu/remove/<item>")
def remove_from_menu(item):

    cart = session.get("cart", [])

    if item in cart:
        cart.remove(item)

    session["cart"] = cart

    return redirect(url_for("menu"))


# ============================================================
# ADD ONE ITEM FROM CART
# Used by the "+" button in the Cart
# ============================================================

@app.route("/cart/add/<item>")
def add_from_cart(item):

    cart = session.get("cart", [])

    cart.append(item)

    session["cart"] = cart

    return redirect(url_for("cart"))


# ============================================================
# REMOVE ENTIRE ITEM FROM CART
# Used by the "Remove" button
# ============================================================

@app.route("/cart/remove-all/<item>")
def remove_all_from_cart(item):

    cart = session.get("cart", [])

    # Remove every occurrence of this item
    cart = [
        cart_item
        for cart_item in cart
        if cart_item != item
    ]

    session["cart"] = cart

    return redirect(url_for("cart"))


# ============================================================
# PLACE ORDER
# ============================================================

@app.route("/place-order", methods=["POST"])
def place_order():

    cart = session.get("cart", [])

    if not cart:
        return redirect(url_for("menu"))

    # Clear the cart after placing the order
    session["cart"] = []

    return render_template("order_success.html")


# ============================================================
# START FLASK
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
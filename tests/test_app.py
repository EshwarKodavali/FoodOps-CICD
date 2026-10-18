from app import app


def test_home_page():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_login_redirects_to_menu():
    client = app.test_client()

    response = client.post(
        "/",
        data={"email": "test@example.com"},
        follow_redirects=False
    )

    assert response.status_code == 302
    assert response.headers["Location"] == "/menu"


def test_add_item_to_cart():
    client = app.test_client()

    with client.session_transaction() as session:
        session["cart"] = []

    response = client.get("/add/Biryani")

    assert response.status_code == 302

    with client.session_transaction() as session:
        assert "Biryani" in session["cart"]


def test_place_order():
    client = app.test_client()

    with client.session_transaction() as session:
        session["cart"] = ["Biryani"]

    response = client.post("/place-order")

    assert response.status_code == 200

    with client.session_transaction() as session:
        assert session["cart"] == []
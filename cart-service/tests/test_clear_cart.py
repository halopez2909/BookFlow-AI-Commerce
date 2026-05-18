def test_clear_cart(client):
    response_1 = client.post(
        "/cart/items",
        json={
            "customer_id": "customer-test",
            "book_id": "book-1",
            "quantity": 2,
        },
    )

    response_2 = client.post(
        "/cart/items",
        json={
            "customer_id": "customer-test",
            "book_id": "book-2",
            "quantity": 1,
        },
    )

    assert response_1.status_code == 201
    assert response_2.status_code == 201

    clear_response = client.delete("/cart/customer-test")

    assert clear_response.status_code == 200

    data = clear_response.json()

    assert data["customer_id"] == "customer-test"
    assert data["items"] == []
    assert data["total"] == "0.00"


def test_get_cart_returns_active_cart(client):
    response = client.get("/cart/customer-test")

    assert response.status_code == 200

    data = response.json()

    assert data["customer_id"] == "customer-test"
    assert data["status"] == "active"
    assert data["items"] == []
    assert data["total"] == "0.00"

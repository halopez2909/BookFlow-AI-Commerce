def test_update_cart_item_quantity(client):
    create_response = client.post(
        "/cart/items",
        json={
            "customer_id": "customer-test",
            "book_id": "book-1",
            "quantity": 2,
        },
    )

    assert create_response.status_code == 201

    item_id = create_response.json()["items"][0]["id"]

    update_response = client.put(
        f"/cart/items/{item_id}",
        json={
            "quantity": 5,
        },
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["items"][0]["id"] == item_id
    assert data["items"][0]["quantity"] == 5
    assert data["items"][0]["subtotal"] == "250000.00"
    assert data["total"] == "250000.00"


def test_delete_cart_item(client):
    create_response = client.post(
        "/cart/items",
        json={
            "customer_id": "customer-test",
            "book_id": "book-1",
            "quantity": 2,
        },
    )

    assert create_response.status_code == 201

    item_id = create_response.json()["items"][0]["id"]

    delete_response = client.delete(f"/cart/items/{item_id}")

    assert delete_response.status_code == 200

    data = delete_response.json()

    assert data["items"] == []
    assert data["total"] == "0.00"

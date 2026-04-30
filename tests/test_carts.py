import pytest
from utils.data import cart_payload, product_array, junk_data, new_user
from utils.API_client import get_all_carts,get_cart_by_id, create_cart, update_cart, delete_cart
from utils.helpers import assert_response, assert_cart_structure, assert_cart_content_is_not_empty, assert_product_from_cart_structure,assert_product_from_cart_is_valid

def test_get_all_carts(session,base_url): #Note: body contains two extra fields (date and __v) that were not documented
    response = get_all_carts(session,base_url)
    assert_response(response)
    assert response.status_code == 200
    carts = response.json()
    for cart in carts:
        assert_cart_structure(cart)
        assert_cart_content_is_not_empty(cart)

def test_structure_of_products_in_carts(session,base_url):
    response = get_all_carts(session,base_url) #Note: Products inside carts have only two fields (productId,quantity) instead of the documented full array of fields from products
    assert_response(response)
    assert response.status_code == 200
    carts = response.json()
    for cart in carts:
        products = cart['products']
        for product in products:
            assert_product_from_cart_structure(product)
            assert_product_from_cart_is_valid(product)

def test_get_cart_by_id(session,base_url):
    all_carts = get_all_carts(session,base_url).json()
    first_cart = all_carts[0]
    response = get_cart_by_id(session,base_url,1)
    assert_response(response)
    assert response.status_code == 200
    get_first_cart = response.json()
    assert first_cart == get_first_cart

@pytest.mark.parametrize('id,expected_result',[
    (1,200),
    (2,200),
    pytest.param(19, 200, marks=pytest.mark.xfail(reason="BUG, body appears to be null, when 20 carts where described in docs")),
    pytest.param(20, 200, marks=pytest.mark.xfail(reason="BUG, body appears to be null, when 20 carts where described in docs")),
])
def test_get_cart_by_id_edge_cases(session,base_url,id,expected_result):
    response = get_cart_by_id(session,base_url,id)
    assert_response(response)
    assert response.status_code == expected_result
    cart = response.json()
    assert_cart_structure(cart)
    assert_cart_content_is_not_empty(cart)

@pytest.mark.parametrize('id',
    list(range(1, 8)) +
    [pytest.param(i, marks=pytest.mark.xfail(reason='BUG, carts 8-20 return null, API should have 20 carts'))
     for i in range(8, 21)])
def test_check_individual_carts_by_id(session,base_url,id):
    response = get_cart_by_id(session,base_url,id)
    assert response.status_code == 200
    cart = response.json()
    assert_cart_structure(cart)
    assert_cart_content_is_not_empty(cart)

@pytest.mark.parametrize('id,expected_result',[
    (-1,400),
    (0,400),
    (21, 404)
])
@pytest.mark.xfail(reason = "BUG, all responses are 200 with a null body")
def test_get_cart_by_id_negative_cases(session,base_url,id,expected_result):
    response = get_cart_by_id(session,base_url,id)
    assert_response(response)
    assert response.status_code == expected_result

@pytest.mark.parametrize('id,expected_result',[
    ('a',400),
    pytest.param(25.5, 400,marks=pytest.mark.xfail(reason="BUG, cart get retrieved with a null body and a 200 code")),
    (None, 400),
    (True, 400),
    pytest.param("",400, marks=pytest.mark.xfail(reason="BUG, cart get retrieved with a full list of carts body and a 200 code")),
])
def test_get_cart_by_id_invalid_data(session,base_url,id,expected_result):
    response = get_cart_by_id(session,base_url,id)             #Note: although not documented, the 400 in this instance error comes with a message {"status": "error","message": "cart id should be provided"}
    assert_response(response)
    assert response.status_code == expected_result

@pytest.mark.xfail(reason="BUG, the ID of the cart created is 11, which should not be correct because there are already 20 carts")
def test_create_cart(session,base_url):
    response = create_cart(session,base_url,cart_payload)
    assert response.status_code == 201
    new_cart = response.json()
    assert_cart_structure(new_cart)
    assert_cart_content_is_not_empty(new_cart)
    for item in new_cart['products']:
        assert_product_from_cart_structure(item)
        assert_product_from_cart_is_valid(item)
    assert new_cart['userId'] == new_cart['userId']
    assert new_cart['id'] > 20

@pytest.mark.xfail(reason='BUG, API should return 400 when userId is missing but returns 201 instead with an incomplete body')
def test_create_cart_with_missing_userId(session, base_url):
    missing_field = cart_payload.copy()
    missing_field.pop('userId')
    response = create_cart(session, base_url, missing_field)
    assert_response(response)
    assert response.status_code == 400

@pytest.mark.xfail(reason='BUG, API should return 400 when userId is missing but returns 201 instead with an incomplete body')
def test_create_cart_with_missing_products(session, base_url):
    missing_field = cart_payload.copy()
    missing_field.pop('products')
    response = create_cart(session, base_url, missing_field)
    assert_response(response)
    assert response.status_code == 400

@pytest.mark.xfail(reason='BUG, API should return 400 when userId is missing but returns 201 instead with an incomplete body')
def test_create_cart_with_empty_payload(session, base_url):
    response = create_cart(session, base_url, {})
    assert_response(response)
    assert response.status_code == 400

@pytest.mark.xfail(reason='BUG, API should return 400 when userId is missing but returns 201 instead with only a id:11 body')
def test_create_cart_with_wrong_payload(session, base_url):
    response = create_cart(session, base_url,new_user)
    assert_response(response)
    assert response.status_code == 400

def test_create_cart_with_wrong_data(session, base_url):
    response = create_cart(session, base_url,junk_data)  #Note:the status code is correct, however the format that the body is in a broken HTML, not strictly wrong
    assert_response(response)                            #but not right, the API should implicitly return JSON.
    assert response.status_code == 400

def test_update_cart(session, base_url):
    response = update_cart(session, base_url, 1, cart_payload)
    assert_response(response)
    assert response.status_code == 200
    updated_cart = response.json()
    assert_cart_structure(updated_cart)
    assert_cart_content_is_not_empty(updated_cart)

@pytest.mark.parametrize('id,expected_result',[
    (1,200),
    (2,200),
    (19,200),
    (20,200),
])
def test_update_cart_edge_cases(session, base_url, id, expected_result):
    response = update_cart(session, base_url, id, cart_payload)
    assert response.status_code == expected_result
    if response.content:
        cart = response.json()
        assert_cart_structure(cart)
        assert_cart_content_is_not_empty(cart)
        assert cart['id'] == id

@pytest.mark.parametrize('id,expected_result',[
    (-1,400),
    (0,400),
    (21,404)
])
@pytest.mark.xfail(reason='BUG, API returns 200 instead of 400/404 for invalid/non-existent carts')
def test_update_cart_negative_cases(session, base_url, id, expected_result):
    response = update_cart(session, base_url, id, cart_payload)
    assert_response(response)
    assert response.status_code == expected_result

@pytest.mark.parametrize('id,expected_result',[
    ('a',400), #Although not documented, cases a, true and none returns a message error in JSON with a 400 status code: {"status":"error","message":"something went wrong! check your sent data"}
    pytest.param(25.5,400,marks=pytest.mark.xfail(reason='BUG, API treats float as valid ID')),
    (True,400),
    (None,400),
    pytest.param('',400,marks=pytest.mark.xfail(reason='Not necesarily a bug, API returns error message in HTML')),
])
def test_update_cart_invalid_id(session, base_url, id, expected_result):
    response = update_cart(session, base_url, id, cart_payload)
    assert_response(response)
    assert response.status_code == expected_result

@pytest.mark.xfail(reason='BUG, API should return 400 for empty payload but returns 200 with an id:1')
def test_update_cart_empty_payload(session, base_url):
    response = update_cart(session, base_url, 1, {})
    assert_response(response)
    assert response.status_code == 400

@pytest.mark.xfail(reason='BUG, API should return 400 for wrong schema but returns 200 with an id:1')
def test_update_cart_wrong_schema(session, base_url):
    response = update_cart(session, base_url, 1, new_user)
    assert_response(response)
    assert response.status_code == 400

@pytest.mark.xfail(reason="Not a bug, but the API returns an error in HTML, not JSON")
def test_update_cart_junk_data(session, base_url):
    response = update_cart(session, base_url, 1, junk_data)
    assert_response(response)
    assert response.status_code == 400
    assert 'application/json' in response.headers.get('Content-Type', '')


@pytest.mark.parametrize('id,expected_result',[
    (1,200),
    (2,200),
    (19,200),
    (20,200)
])
@pytest.mark.xfail(reason='BUG, DELETE should return 200 with no body but returns full cart body for 1 and 2, 19, and 20 have a null body')
def test_delete_cart_edge_cases(session, base_url, id, expected_result):
    response = delete_cart(session, base_url, id)
    assert response.status_code == expected_result
    assert not response.content

@pytest.mark.parametrize('id,expected_result',[
    (-1,400),
    (0,400),
    (21,404)
])
@pytest.mark.xfail(reason='BUG, API returns 200 null instead of 400/404')
def test_delete_cart_negative_cases(session, base_url, id, expected_result):
    response = delete_cart(session, base_url, id)
    assert response.status_code == expected_result

@pytest.mark.parametrize('id,expected_result',[
    ('a',400),
    pytest.param(25.5,400,marks=pytest.mark.xfail(reason='BUG, API treats float as valid ID with null body')),
    (True,400),(None,400),
    pytest.param('',400,marks=pytest.mark.xfail(reason='Not necessarily a bug, API returns broken error message in HTML')),
])
def test_delete_cart_invalid_id(session, base_url, id, expected_result):
    response = delete_cart(session, base_url, id) #Again, there is a " {"status":"error","message":"cart id should be provided"} message for a,True and None that is not documented
    assert response.status_code == expected_result

def test_delete_cart_wrong_schema(session, base_url): #Not a bug, but the API returns a body with the response.
    response = delete_cart(session, base_url, new_user)
    assert response.status_code == 400
    assert 'application/json' in response.headers.get('Content-Type', '')





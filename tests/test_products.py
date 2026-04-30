import pytest
from utils.API_client import get_all_products, get_product_by_id, create_product,update_product, delete_product
from utils.helpers import assert_product_structure, assert_field_content_is_not_empty, assert_response
from utils.data import new_product, new_user, junk_data

def test_get_all_products(session,base_url):  #In this case the API accepts both integer and float for price, despite being stated that the price field only contains int, it´s an inconsistency
    response = get_all_products(session,base_url)
    assert_response(response)
    assert response.status_code == 200
    products = response.json()
    for product in products:
        assert_product_structure(product)

def test_get_product_by_id(session,base_url):
    get_product = get_all_products(session,base_url).json()
    product1 = get_product[0]
    response = get_product_by_id(session,base_url,product1['id'])
    assert_response(response)
    assert response.status_code == 200
    products = response.json()
    assert_product_structure(products)
    assert_field_content_is_not_empty(products)
    assert product1 == products

@pytest.mark.parametrize('id,expected_result',[
    (1,200),
    (2,200),
    (19,200),
    (20,200),
])
def test_edge_cases_for_get_product_by_id(session,base_url,id,expected_result):
    response = get_product_by_id(session,base_url,id)
    assert_response(response)
    assert response.status_code == expected_result

@pytest.mark.parametrize('id,expected_result',[
    pytest.param(-1, 400, marks=pytest.mark.xfail(reason="API should return a 400 status for invalid ID but returns a 200 code instead")),
    pytest.param(0, 400, marks=pytest.mark.xfail(reason="API should return a 400 status for invalid ID but returns a 200 code instead")),
    pytest.param(21,404,marks=pytest.mark.xfail(reason="API should return a 404 status for non-existent element but returns a 200 code instead")),
])
def test_negative_cases_for_get_product_id(session,base_url,id,expected_result):
    response = get_product_by_id(session,base_url,id)
    assert_response(response)
    assert response.status_code == expected_result

@pytest.mark.parametrize('id,expected_result',[
    (25.5,400),
    ('a',400),
    (True,400),
    (None,400),
    ('',400), #This negative input returns the whole products list, same as get_all_products
])
@pytest.mark.xfail(reason = 'BUG, The API id field is accepting any type of data when it was stated that it only should be integer')
def test_invalid_inputs_for_get_product_id(session,base_url,id,expected_result):
    response = get_product_by_id(session,base_url,id)
    assert_response(response)
    assert response.status_code == expected_result

def test_create_a_new_product(session,base_url):
    response = create_product(session,base_url,new_product)
    assert_response(response)                                       #The API doesn't simulate creation of new data, but I validate that the data I'm inputting
    assert response.status_code == 201                               #matches the data I'm receiving, enforcing the API contract, also the API creates the id, so I have
    products = response.json()                                       #to check that id exists, not that it will be the same value I will input in the body.
    assert_product_structure(products)
    assert_field_content_is_not_empty(products)
    assert products['id'] > 20

@pytest.mark.xfail(reason= "BUG, the API should not accept the payload without a required field, however, the API processes the data and returns a 201 Created status WITH a body missing a field")
def test_create_a_new_product_with_missing_field(session,base_url):
    missing_field = new_product.copy()
    missing_field.pop('description')
    response = create_product(session,base_url,missing_field)
    assert_response(response)
    assert response.status_code == 400
    products = response.json()
    for key in products:
        assert key not in missing_field

@pytest.mark.xfail(reason='BUG, the API is accepting an incorrect payload and returning an ID with a 201 Created code, output should be 400 Bad Request')
def test_missing_body_for_a_new_product(session,base_url):
    data = {}
    response = create_product(session, base_url, data)
    assert_response(response)
    assert response.status_code == 400

def test_creating_product_with_junk_data(session, base_url):
    response = create_product(session, base_url, junk_data) #API doesn't process the request, which is good, but returns a broken HTML body response
    assert response.status_code == 400
    assert_response(response)
    assert 'text/html' in response.headers.get('Content-Type', '')

@pytest.mark.xfail(reason='BUG, The API is taking a completely different body as required and passing it as a response, enforcing no data validation, returning a 201 created status with a body containing only a ID:21 rather than 400 bad request')
def test_creating_product_with_wrong_payload(session,base_url):
    response = create_product(session,base_url,new_user)
    assert_response(response)
    assert response.status_code == 400

@pytest.mark.parametrize('id,title,price,description,category,image,expected_result',[
    ('21','Hibiscus',9.99,'This is Silver Memories','plant','https://www.davesgarden.com/pics/2009/03/11/amorecuore/b0bee1.jpg',400),
    (21,25,9.99,'This is Silver Memories','plant','https://www.davesgarden.com/pics/2009/03/11/amorecuore/b0bee1.jpg',400),
    (21,'Hibiscus',25,'This is Silver Memories','plant','https://www.davesgarden.com/pics/2009/03/11/amorecuore/b0bee1.jpg',400),
    (21,'Hibiscus',9.99,25,'plant','https://www.davesgarden.com/pics/2009/03/11/amorecuore/b0bee1.jpg',400),
    (21,'Hibiscus',9.99,'This is Silver Memories',25,'https://www.davesgarden.com/pics/2009/03/11/amorecuore/b0bee1.jpg',400),
    (21,'Hibiscus',9.99,'This is Silver Memories','plant',25,400),
])
@pytest.mark.xfail(reason='The API is not enforcing format restrictions to the fields, which leds to a successful creation of product with invalid formated data')
def test_wrong_input_format_for_all_create_product_fields(session,base_url,id,title,price,description,category,image,expected_result):
    data = {'id': id, 'title': title, 'price': price, 'description': description, 'category': category, 'image': image}
    response = create_product(session, base_url, data)   #since the API is not enforcing any field restrictions, the response will always be 201 created.
    assert_response(response)
    assert response.status_code == expected_result


def test_update_product(session,base_url):
    product_id = 1
    response = update_product(session,base_url,product_id,new_product)   #In this instance, for the PUT method, the API holds to the ID value passed as path parameter (product/x)
    assert_response(response)
    assert response.status_code == 200                                   #and completely ignores the ID in the body of the request. That is why I compared the id from thr path parameter
    updated_product = response.json()                                    #to the ID of the response body.
    assert_product_structure(updated_product)
    assert_field_content_is_not_empty(updated_product)
    assert updated_product['id'] == product_id
    for key in new_product:
        if key != 'id':
            assert updated_product[key] == new_product[key]

@pytest.mark.parametrize("id,expected_result",[
    (1,200),
    (2,200),
    (19,200),
    (20,200),
])
def test_edge_cases_for_update_products_id(session,base_url,id,expected_result):
    response = update_product(session,base_url,id,new_product)
    assert_response(response)
    assert response.status_code == expected_result
    updated_product = response.json()
    assert_product_structure(updated_product)
    assert_field_content_is_not_empty(updated_product)
    assert updated_product['id'] == id
    for key in new_product:
        if key != 'id':
            assert updated_product[key] == new_product[key]

@pytest.mark.parametrize("id,expected_result",[
    (-1,400),
    (0,400),
    (21,404),
])
@pytest.mark.xfail(reason='BUG, API should return 400 for invalid IDs and 404 for non-existent products, but returns 200 with the sent body instead')
def test_negative_cases_for_update_products_id(session,base_url,id,expected_result):
    response = update_product(session,base_url,id,new_product)
    assert_response(response)
    assert response.status_code == expected_result

@pytest.mark.parametrize("id,expected_result",[
    pytest.param('1', 400, marks=pytest.mark.xfail(reason="BUG, API treats string '1' as valid integer, returns 200 with sent body")),
    pytest.param(25.5, 400,marks=pytest.mark.xfail(reason="BUG, API treats float as valid integer, returns 200 with sent body")),
    (True, 400),
    (None, 400), #For True and None an error message appears "{"status":"error","message":"something went wrong! check your sent data"}" which isn't documented
    pytest.param("", 400,marks=pytest.mark.xfail(reason="BUG, API should respond 400 code but returns a 404 with a broken HTML response")),
])
def test_invalid_cases_for_update_products_id(session,base_url,id,expected_result):
    response = update_product(session,base_url,id,new_product)
    assert_response(response)
    assert response.status_code == expected_result

@pytest.mark.parametrize('product_id,id,title,price,description,category,image,expected_result',[
    (1,'21','Hibiscus',9.99,'This is Silver Memories','plant','https://www.davesgarden.com/pics/2009/03/11/amorecuore/b0bee1.jpg',400),
    (1,21,25,9.99,'This is Silver Memories','plant','https://www.davesgarden.com/pics/2009/03/11/amorecuore/b0bee1.jpg',400),
    (1,21,'Hibiscus',25,'This is Silver Memories','plant','https://www.davesgarden.com/pics/2009/03/11/amorecuore/b0bee1.jpg',400),
    (1,21,'Hibiscus',9.99,25,'plant','https://www.davesgarden.com/pics/2009/03/11/amorecuore/b0bee1.jpg',400),
    (1,21,'Hibiscus',9.99,'This is Silver Memories',25,'https://www.davesgarden.com/pics/2009/03/11/amorecuore/b0bee1.jpg',400),
    (1,21,'Hibiscus',9.99,'This is Silver Memories','plant',25,400),
])
@pytest.mark.xfail(reason='The API is not enforcing format restrictions to the fields, which leds to a successful creation of product with invalid formated data')
def test_wrong_input_format_for_all_update_product_fields(session,base_url,product_id,id,title,price,description,category,image,expected_result):
    data = {'id': id, 'title': title, 'price': price, 'description': description, 'category': category, 'image': image}
    response = update_product(session, base_url,product_id,data)
    assert_response(response)
    assert response.status_code == expected_result

@pytest.mark.xfail(reason= "BUG, the API should not accept the payload without a required field, however, the API processes the data and returns a 201 Created status WITH a body")
def test_update_a_new_product_with_missing_field(session,base_url):
    missing_field = new_product.copy()
    missing_field.pop('description')
    response = update_product(session,base_url,1,missing_field)
    assert_response(response)
    assert response.status_code == 400
    products = response.json()
    for key in products:
        assert key not in missing_field

@pytest.mark.xfail(reason='BUG, the API is accepting a non existent body, returning a id:1 body content with a 200 status code instead of 400')
def test_missing_body_for_update_a_product(session,base_url):
    data = {}
    response = update_product(session, base_url,1,data)
    assert_response(response)
    assert response.status_code == 400

def test_update_product_with_junk_data(session, base_url):
    response = update_product(session, base_url, 1, junk_data)
    assert response.status_code == 400
    assert_response(response)
    assert 'text/html' in response.headers.get('Content-Type', '') #Response is a broken HTML

@pytest.mark.xfail(reason='BUG, The API is taking a completely different body  returning a id:1 body content with a 200 status code instead of 400')
def test_updating_product_with_wrong_payload(session,base_url):
    response = update_product(session,base_url,1,new_user)
    assert_response(response)
    assert response.status_code == 400

@pytest.mark.xfail(reason = "BUG, Response has a body, and it's a dict with the info of the product" )
def test_delete_product(session,base_url):
    response = delete_product(session,base_url,1)
    assert response.status_code == 200
    assert not response.content, "Response should be empty"

@pytest.mark.parametrize('id,expected_result', [
    (1,200),
    (2,200),
    (19,200),
    (20,200)
])
@pytest.mark.xfail(reason = "BUG, Response has a body, and it's a dict with the info of the product" )
def test_edge_cases_for_delete_product(session,base_url,id,expected_result):
    response = delete_product(session,base_url,id)
    assert response.status_code == expected_result
    assert not response.content, "Response should be empty"

@pytest.mark.parametrize('id,expected_result', [
    (-1,400),
    (0,400),
    (21,404), #This case doubles as deleting a non-existent or deleted user.
])
@pytest.mark.xfail(reason = "BUG, Response code is 200 with a number '1' in the body of the response")
def test_negative_cases_for_delete_product(session,base_url,id,expected_result):
    response = delete_product(session,base_url,id)
    assert response.status_code == expected_result
    assert not response.content, "Response should be empty"

@pytest.mark.parametrize('id,expected_result', [
    ("a",400),
    pytest.param(25.5,404,marks=pytest.mark.xfail(reason="API returns 200 null instead of error")),
    (True,400),
    (None,400),
    pytest.param("", 400,marks=pytest.mark.xfail(reason="BUG, API should respond 400 code but returns a 404 with a broken HTML response")),
    (new_user, 400) #a, True, None and payload new_user return a not documented error message {"status":"error","message":"product id should be provided"}
])
def test_invalid_id_for_delete_product(session,base_url,id,expected_result): #Although there is no documentation if the 400 Bad request should have a body
    response = delete_product(session,base_url,id)
    assert_response(response)                                                #a valid error message shows with a valid response code, not necessarily a bug
    assert response.status_code == expected_result                           #but an undocumented behaviour













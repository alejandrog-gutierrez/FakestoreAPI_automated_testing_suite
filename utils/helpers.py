def assert_user_structure(user):
    assert isinstance(user, dict), "Error, the user should be dict"
    assert isinstance(user['id'], int), "Error, the id should be int"
    assert isinstance(user['username'], str), "Error, the username should be str"
    assert isinstance(user['email'], str), "Error, the email should be str"
    assert isinstance(user['password'], str), "Error, the password should be str"
                                    #This helper ensures that the data that is being received from the API enforces
                                     #the format that is described in the documentation, only ID should be an integer,
                                     #every other field must be a string.
def assert_user_structure_is_not_empty(user):
    assert user['id'] > 0, "Error, the id shouldn't empty"
    assert user['username'] != '',"Error, the username shouldn't be empty"
    assert user['email'] != '', "Error, the email shouldn't be empty"      #This helper ensures user data is not unusable or empty.
    assert "@" in user['email'], "Email is not valid"
    assert len(user['password']) > 0, "Password should not be empty"

def assert_product_structure(product):
    assert isinstance(product, dict), "Error, wrong format product"
    assert isinstance(product['id'], int), "Error, id should be int"
    assert isinstance(product['title'], str), "Error, title should be str"
    assert isinstance(product['price'], (int,float)), "Error, price should be float"
    assert isinstance(product['description'], str), "Error, description should be str"
    assert isinstance(product['category'], str), "Error, category should be str"
    assert isinstance(product['image'], str), "Error, image should be string (link)" # Note:
                                             # According to the API documentation, 'price' should be a float.
                                             # However, the API sometimes returns integer values.
                                             # To avoid false negatives, both int and float are accepted.
def assert_field_content_is_not_empty(product):
    assert product['id'] > 0, "Error, id should be greater than 0"
    assert product['title'] != '', "Error, title should not be empty"
    assert product['price'] >= 0, "Error, price should be >= 0"
    assert product['description'] != '', "Error, description should not be empty"
    assert product['category'] != '', "Error, category should not be empty"
    assert product['image'] != '', "Error, image should not be empty"           #This helper ensures that the data that is being tested is not empty.

def assert_valid_error_message(body):
    assert body is not None, "Error response body should not be None"
    assert isinstance(body, dict), "Error body should be a dict"
    assert body != {}, "Error body should not be empty"
    if "message" in body:
        assert isinstance(body["message"], str), "Error message should be a string"
        assert body["message"].strip() != "", "Error message should not be empty"
    if "status" in body:
        assert isinstance(body["status"], str), "Error status should be a string"  #This helper takes the error message and responses and enforces that the response
        assert body["status"].strip() != "", "Error status should not be empty"     #at least has a basic format

def assert_valid_success_response(body):
    assert body is not None, "Success response body should not be None"
    assert isinstance(body, (dict, list)), "Success body should be dict or list"  #Here we also accept lists because the endpoint get_all_users/products returns a list
    if isinstance(body, dict):                                                      #I also enforce the response has at least a very basic format.
        assert body != {}, "Success response body should not be empty"
    if isinstance(body, list):
        assert len(body) > 0, "Success response list should not be empty"


def assert_response(response):
    content_type = response.headers.get("Content-Type", "") #This gets the response object and gets the format of the response (JSON, HTML, TEXT...)
    body = None                                             #Body is empty before we sort out which format it has

    if response.content:                                    #This part of the executes only if the body has content
            if "application/json" in content_type:
                try:
                    body = response.json()
                    print(f"\n Response is in JSON, you may proceed :) - Status:{response.status_code}")                                               #If the body is JSON, we convert it to list/dict
                except ValueError:
                    assert False, f"Response body is not valid JSON, got: {response.text[:100]}" #This validates the JSON is functional
            else:
                body = response.text
                print(f"\n Non-JSON response detected - Content-Type:{content_type} | Preview: {response.text[:80]}")          #If body is not JSON, I store it as text and print a warning

    if response.status_code in range(400,500):              #This sorts out the body into response codes and validates the format (dict)
            if isinstance(body, dict):                          #however it doesn't validate 200 code strings, that would be an error from the API and each test should have at least one assert regarding content of the object
             assert_valid_error_message(body)                #If the body is correct and the status is 400/404, we send the body object to valid error helper

    elif response.status_code in range (200,300):                #This does the same buy with succesful status codes 200/201
            if isinstance(body, (dict, list)):
                assert_valid_success_response(body)

    else:
        assert response.status_code < 500, "Unexpected server error" #This sorts out 5xx errors and allows 3xx

def print_info(response):
    print(f"\nStatus: {response.status_code}")
    print(f"\nContent-Type: {response.headers.get('Content-Type', '')}")
    print(f"\nBody:{response.text[:100]}")

def assert_cart_structure(cart):
    #Note; the response contains two extra fields (date,__v) which are not documented in the response
    #this helper was adapted real behaviour, validating only documented fields
    assert isinstance(cart, dict)
    assert isinstance(cart['id'], int), "Error, id should be int"
    assert isinstance(cart['userId'], int), "Error, title should be int"
    assert isinstance(cart['products'],list), "Error, products should be a list or dict"

def assert_cart_content_is_not_empty(cart):
    assert cart['id'] > 0, "Error, the id should be >0"
    assert cart['userId'] > 0, "Error, the userId should be > 0"
    assert cart['products'] != [], "Error, the product should exist"

def assert_product_from_cart_structure(product):
    #Note; the documentation says that the array of fields the product should be the same as in the products endpoint
    #However, the response itself only contains "productId" and "quantity", I adapted the helper to the real behaviour
    assert isinstance(product, dict)
    assert isinstance(product['productId'], int), "Error, id should be int"
    assert isinstance(product['quantity'], int), "Error, quantity should be int"

def assert_product_from_cart_is_valid(product):
    assert product['productId'] > 0, "Error, the productId should be > 0"
    assert product['quantity'] > 0, "Error, the quantity should be > 0"
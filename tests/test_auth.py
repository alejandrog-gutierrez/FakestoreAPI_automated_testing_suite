import pytest
from utils.API_client import user_login
from utils.data import user_data, invalid_user_data,new_product
from utils.helpers import assert_response


def test_successful_login(session,base_url):
    response = user_login(session,base_url,user_data['username'],user_data['password'])
    assert_response(response)
    assert response.status_code == 201 #DOC says 200 but since the method is POST, it should be 201
    assert "token" in response.json()
    token = response.json()["token"]
    assert isinstance(token,str)
    assert len(token)>0

def test_unsuccessful_login(session,base_url):
    response = user_login(session,base_url,invalid_user_data['username'],invalid_user_data['password'])
    assert_response(response)
    assert response.status_code == 401                           #Response code should be 400 Bad Request according to documentation,
    assert response.text == "username or password is incorrect"  #however the API returns a 401 unauthorized with the
                                                                 #"username or password is incorrect" statement in an HTML body
                                                                 # Exact match intentional, message was discovered empirically
                                                                 # and is not documented. Fragile by nature but stable for this static mock API.
@pytest.mark.parametrize("username,password,expected_status",[
    (25,'m38rmF$', 401),                                            #This test suite validates the response behaviour through negative case input
    (1.5,'m38rmF$', 401),                                           #For the "username" input field, since it is stated that it only accepts strings.
    (True,'m38rmF$', 401),                                          #The username field correctly reacts with different input, returning a 400 code for invalid data
    (None,'m38rmF$', 400),                                          #and 401 for incorrect data.
    ('','m38rmF$', 400),
])
def test_invalid_login_for_username(session,base_url,username,password,expected_status):
    response = user_login(session,base_url,username,password)
    assert response.status_code == expected_status
    assert_response(response)                                       #Not precisely a Bug, but all instances return an HTML body response, the status is ok though
    if expected_status == 400:
        assert response.text == "username and password are not provided in JSON format"
    elif expected_status == 401:
        assert response.text == "username or password is incorrect"

@pytest.mark.parametrize("username,password,expected_status",[
    ('johnd',25, 401),        #This test suite validates the response behaviour through negative case input
    ('johnd',1.5, 401),       #For the "password" input field, since it is stated that it only accepts strings.
    ('johnd',True, 401),      #The password field correctly reacts with different input, returning a 400 code for invalid data
    ('johnd',None, 400),      #and 401 for incorrect data.
    ('johnd','', 400),
])
def test_invalid_login_for_password(session,base_url,username,password,expected_status):
    response = user_login(session,base_url,username,password)
    assert_response(response)                                       #Again, not precisely a Bug, but all instances return an HTML body response, the status is ok though
    assert response.status_code == expected_status
    if expected_status == 400:
        assert response.text == "username and password are not provided in JSON format"
    elif expected_status == 401:
        assert response.text == "username or password is incorrect"

def test_missing_username_field(session,base_url):
    response = user_login(session,base_url,None,user_data['password'])
    assert_response(response)                                          #Not a JSON response
    assert response.status_code == 400
    assert response.text == "username and password are not provided in JSON format"

def test_missing_password_field(session,base_url):
    response = user_login(session,base_url,user_data['username'],None)   #Not a JSON response
    assert_response(response)                                           #Exact match intentional, message was discovered empirically
    assert response.status_code == 400                                 #and is not documented. Fragile by nature but stable for this static mock API.
    assert response.text == "username and password are not provided in JSON format"

def test_empty_request(session,base_url):
    response = user_login(session,base_url,None,None)
    assert_response(response)
    assert response.status_code == 400
    assert response.text == "username and password are not provided in JSON format"

@pytest.mark.xfail(reason="BUG: API hangs and returns 524 on invalid payload instead of proper 400 response")
def test_wrong_payload(session,base_url):
    response = user_login(session,base_url,new_product,new_product)
    assert_response(response)
    assert response.status_code == 400


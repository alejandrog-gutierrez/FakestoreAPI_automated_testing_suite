import pytest
from utils.API_client import get_all_users, get_user,post_user,update_user, delete_user
from utils.helpers import assert_user_structure, assert_user_structure_is_not_empty, assert_response
from utils.data import new_user,junk_data,new_product

def test_get_all_users(session,base_url):           #This is the minimal validation for API contract in the dictionary for
    response = get_all_users(session,base_url)     #all users, the list return more fields, but the necessary for user creation
    assert response.status_code == 200             #are these 4 fields
    assert_response(response)
    users = response.json()
    for user in users:
        assert_user_structure(user)
        assert_user_structure_is_not_empty(user)

def test_get_user_by_id(session,base_url):
    all_users = get_all_users(session,base_url).json()             #In this test we took the whole list of users, and we used the very first user from the index (all_users[0])
    first_user = all_users[0]                                      #Then we used the id (1) of the first user and BOOM! Hey John, glad to have you around :)
    response = get_user(session,base_url,first_user['id'])
    assert response.status_code == 200
    assert_response(response)
    user1 = response.json()
    for key in first_user:
        assert first_user[key] == user1[key]

@pytest.mark.parametrize('id,expected_status',[ #These are wrong type input cases for ID, float and empty seem to work just fine.
    ('a',400),
    pytest.param(25.5,400,marks=pytest.mark.xfail(reason = 'API should return a 400 status for invalid input but returns a 200 with a null body code instead')),
    (True,400), #a, True and None return a {"status":"error","message":"user id should be provided"} message not documented in the API
    (None,400),
    pytest.param("",404,marks=pytest.mark.xfail(reason = 'API should return a 404 status but returns a 400 status with a broken HTML body')),
])
def test_invalid_inputs_for_users(session,base_url,id,expected_status):
    response = get_user(session,base_url,id)
    assert response.status_code == expected_status
    assert_response(response)

@pytest.mark.parametrize("id,expected_status",[
    (1,200),
    (2,200),
    (9,200),
    (10,200)
])
def test_edge_cases_for_valid_users(session,base_url,id,expected_status):
    response = get_user(session,base_url,id)
    assert response.status_code == expected_status
    user = response.json()
    assert_user_structure(user)
    assert_user_structure_is_not_empty(user)
    assert_response(response)

@pytest.mark.parametrize("id,expected_status",[
    (-1,400),
    (0,400),
    (11,404),
])
@pytest.mark.xfail(reason= "Bug, -1,0 returns a 200 code with a null body instead of 400, 11 returns a 200 code with a null body instead of 404")
def test_negative_cases_for_user(session,base_url,id,expected_status):
    response = get_user(session,base_url,id)
    assert response.status_code == expected_status
    assert_response(response)

@pytest.mark.parametrize("id,username,email,password,expected_result",[
    ('A','Alejandro','hibiscus@hibiscus.com','silvermemories05',400),
    (11,25,'hibiscus@hibiscus.com','silvermemories05',400),
    (11,'Alejandro',25,'silvermemories05',400),
    (11,'Alejandro','hibiscus@hibiscus.com',25,400),
])
@pytest.mark.xfail(reason='BUG, API is accepting invalid data and returns with a 201 code returning the body sent')
def test_wrong_input_for_post_new_user_field(session,base_url,id,username,email,password,expected_result): #Thiscollection tests at least one instance of wrong input for each field, however, looks like the API
    response = post_user(session,base_url,{'id':id,'username':username,'email':email,'password':password}) #always validates data no matter what we give to them, despite that it has documented valid data requirements
    assert response.status_code == expected_result
    assert_response(response)

@pytest.mark.xfail(reason="BUG, API processes missing input fields and returns a 201 OK status and id:1 for body")
def test_create_user_with_missing_field(session,base_url):
    missing_field_data = new_user.copy()
    missing_field_data.pop('username')
    response = post_user(session,base_url,missing_field_data)       #Even with a missing field which is stated to be required in the literature, the response is 201 created...
    assert response.status_code == 400
    assert_response(response)
    user = response.json()
    for key in missing_field_data:
        assert key not in user

@pytest.mark.xfail(reason="BUG, API creates user with empty payload, returns a 201 code with a body containing only id:1")
def test_create_user_with_empty_payload(session,base_url):
    payload = {}
    response = post_user(session,base_url,payload)
    assert response.status_code == 400
    assert_response(response)

def test_creating_user_with_junk_data(session, base_url):
    response = post_user(session, base_url, junk_data)
    assert response.status_code == 400 #This might be a stretch, the API returns a 400 error with a broken HTML body
    assert_response(response)
    assert 'text/html' in response.headers.get('Content-Type', '')

@pytest.mark.xfail(reason='BUG, API accepts payload with incorrect data, returns a 201 code with a body containing id:1')
def test_creating_user_with_wrong_payload(session,base_url):
    response = post_user(session,base_url,new_product)
    assert response.status_code == 400
    assert_response(response)

@pytest.mark.xfail(reason="BUG, API returns only 'id' instead of the whole object")
def test_create_new_user(session,base_url):
    response = post_user(session,base_url,new_user)
    assert response.status_code == 201
    assert_response(response)
    user = response.json()
    assert_user_structure(user)
    assert_user_structure_is_not_empty(user)
    for key in new_user:
        assert user[key] == new_user[key]

@pytest.mark.parametrize("id,expected_result",[
    (1,200),
    (2,200),
    (9,200),
    (10,200),
])
def test_update_existing_user_edge_cases(session,base_url,id,expected_result): #In this instance, the id that gets sent through the body, is the one that gets
    response = update_user(session,base_url,id,new_user)                        #returned by the API.
    assert response.status_code == expected_result
    assert_response(response)
    updated_user = response.json()
    assert_user_structure(updated_user)
    for key in new_user:
        assert new_user[key] == updated_user[key]
    assert id != updated_user['id']

@pytest.mark.parametrize("id,expected_result",[
    (0, 400),
    (-1, 400),
    (11, 404),
])
@pytest.mark.xfail(reason="BUG, API returns 200 with a full payload instead of 400/404")
def test_update_non_existent_user(session, base_url, id, expected_result):
    response = update_user(session, base_url, id, new_user)
    assert response.status_code == expected_result
    assert_response(response)


@pytest.mark.xfail(reason="API accepts an empty payload and returns a 201 code with body {}")
def test_update_user_with_empty_payload(session, base_url):
    response = update_user(session, base_url, 1, {})
    assert response.status_code == 400
    assert_response(response)

@pytest.mark.parametrize("id,username,email,password,expected_result",[
    ('A','Alejandro','hibiscus@hibiscus.com','silvermemories05',400),
    (11,25,'hibiscus@hibiscus.com','silvermemories05',400),
    (11,'Alejandro',25,'silvermemories05',400),
    (11,'Alejandro','hibiscus@hibiscus.com',25,400),
])
@pytest.mark.xfail(reason='BUG, API accepts invalid data and responds 200 with a full body for each entry')
def test_wrong_input_for_update_new_user_field(session,base_url,id,username,email,password,expected_result):
    user_id = 1
    response = update_user(session,base_url,user_id,{'id':id,'username':username,'email':email,'password':password})
    assert response.status_code == expected_result
    assert_response(response)                                                #Same situation with the POST method, the API is not really validating the type of input we are giving to each field

@pytest.mark.xfail(reason='BUG, API accepts incomplete payload, returns 200 code with an incomplete payload')
def test_update_user_with_a_missing_fields(session,base_url):
    user_id = 1
    missing_field_data = new_user.copy()
    missing_field_data.pop('username')
    response = update_user(session,base_url,user_id,missing_field_data)
    assert response.status_code == 400
    assert_response(response)

@pytest.mark.xfail(reason = "Bug, the response of the completed request is the body of the user")
def test_delete_a_user(session,base_url):
    id = 1
    response = delete_user(session,base_url,id)
    deleted_user1 = response.json()
    user1 = get_user(session,base_url,id).json()
    assert response.status_code == 200
    assert user1 != deleted_user1

@pytest.mark.parametrize("id,expected_results",[
    (1,200),
    (2,200),
    (9,200),
    (10,200),
])
@pytest.mark.xfail(reason='BUG, API returns user body when it should be empty')
def test_edge_cases_for_user_delete(session,base_url,id,expected_results):
    response = delete_user(session,base_url,id)
    assert response.status_code == expected_results
    assert not response.content

@pytest.mark.parametrize("id,expected_result",[
    (-1,400),
    (0,400),
    (11,404),
])
@pytest.mark.xfail(reason='BUG, API returns 200 with a null body instead of 400/404')
def test_negative_cases_for_user_delete(session,base_url,id,expected_result):
    response = delete_user(session,base_url,id)     #This test also covers for deleting a non-existing user
    assert response.status_code == expected_result
    assert_response(response)
    assert not response.content

@pytest.mark.parametrize("id,expected_result",[
    ('a',400),
    pytest.param(25.5,404,marks=pytest.mark.xfail(reason="API returns 200 null instead of error")),
    (True,400),
    (None,400), #"a",True and None all return a not documented {"status":"error","message":"user id should be provided"} message error
    pytest.param("", 400,marks=pytest.mark.xfail(reason="BUG, API should respond 400 code but returns a 404 with a broken HTML response")),
    (new_user,400)
])
def test_invalid_values_for_user_delete(session,base_url,id,expected_result):
    response = delete_user(session,base_url,id)
    assert_response(response)
    assert response.status_code == expected_result












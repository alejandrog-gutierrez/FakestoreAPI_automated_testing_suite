#Authorization endpoint
def user_login(session,base_url,username,password):
    response = session.post(f'{base_url}/auth/login',json={"username":username,"password":password})
    return response

#All user endpoint methods (CRUD)
def get_all_users(session,base_url):
    response = session.get(f'{base_url}/users')
    return response

def get_user(session,base_url,id):
    response = session.get(f'{base_url}/users/{id}')
    return response

def post_user(session,base_url,data):
    response = session.post(f'{base_url}/users',json=data)
    return response

def update_user(session,base_url,id,data):
    response = session.put(f'{base_url}/users/{id}',json=data)
    return response

def delete_user(session,base_url,id):
    response = session.delete(f'{base_url}/users/{id}')
    return response

#All products endpoint methods (CRUD)
def get_all_products(session,base_url):
    response = session.get(f'{base_url}/products')
    return response

def get_product_by_id(session,base_url,id):
    response = session.get(f'{base_url}/products/{id}')
    return response

def create_product(session,base_url,data):
    response = session.post(f'{base_url}/products',json=data)
    return response

def update_product(session,base_url,id,data):
    response = session.put(f'{base_url}/products/{id}',json=data)
    return response

def delete_product(session,base_url,id):
    response = session.delete(f'{base_url}/products/{id}')
    return response

#All carts endpoint methods (CRUD)
def get_all_carts(session,base_url):
    response = session.get(f'{base_url}/carts')
    return response

def get_cart_by_id(session,base_url,id):
    response = session.get(f'{base_url}/carts/{id}')
    return response

def create_cart(session,base_url,data):
    response = session.post(f'{base_url}/carts',json=data)
    return response

def update_cart(session,base_url,id,data):
    response = session.put(f'{base_url}/carts/{id}',json=data)
    return response

def delete_cart(session,base_url,id):
    response = session.delete(f'{base_url}/carts/{id}')
    return response
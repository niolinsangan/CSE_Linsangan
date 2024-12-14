import pytest
import json
from app import app
import pymysql
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='session')
def test_db():
    # Create test database connection
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='antonio123',
        database='customermetadatarepository',
        cursorclass=pymysql.cursors.DictCursor
    )
    yield connection
    connection.close()

@pytest.fixture(autouse=True)
def setup_test_db(test_db):
    # Clear test data before each test
    with test_db.cursor() as cursor:
        cursor.execute("DELETE FROM attribute")
        cursor.execute("DELETE FROM business_term_owner")
        cursor.execute("DELETE FROM entity")
        cursor.execute("DELETE FROM glossary_of_business_terms")
        cursor.execute("DELETE FROM source_systems")
        cursor.execute("DELETE FROM business_term_type")
    test_db.commit()

def get_auth_token(client):
    """Helper function to get authentication token"""
    response = client.post('/login', 
                         json={'username': 'admin', 'password': 'admin123'})
    return json.loads(response.data)['token']

# ---------------------------- Authentication Tests ----------------------------
def test_login_success(client):
    response = client.post('/login',
                          json={'username': 'admin', 'password': 'admin123'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data
    assert 'user' in data
    assert data['user']['username'] == 'admin'
    assert data['user']['role'] == 'admin'

def test_login_failure(client):
    response = client.post('/login',
                          json={'username': 'wrong', 'password': 'wrong'})
    assert response.status_code == 401

# ---------------------------- Attribute Tests ----------------------------
def test_get_attributes(client, test_db):
    # First insert test data
    with test_db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO attribute 
            (attribute_id, attribute_name, attribute_datatype) 
            VALUES (1, 'Test Attribute', 'VARCHAR')
        """)
        test_db.commit()

    token = get_auth_token(client)
    response = client.get('/Attribute',
                         headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert b'Test Attribute' in response.data

def test_add_attribute(client):
    token = get_auth_token(client)
    test_attribute = {
        'attribute_id': 1,
        'attribute_name': 'Test Attribute',
        'attribute_datatype': 'VARCHAR',
        'attribute_description': 'Test Description',
        'typical_values': 'Test Values',
        'validation_criteria': 'Test Criteria'
    }
    response = client.post('/Attribute',
                          headers={'Authorization': f'Bearer {token}'},
                          json=test_attribute)
    assert response.status_code == 201

# ---------------------------- Business Term Owner Tests ----------------------------
def test_get_business_term_owners(client, test_db):
    # Insert test data
    with test_db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO business_term_owner 
            (term_owner_code, term_owner_description) 
            VALUES ('TEST01', 'Test Owner')
        """)
        test_db.commit()

    token = get_auth_token(client)
    response = client.get('/Business-Term-Owner',
                         headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert b'Test Owner' in response.data

# ---------------------------- Entity Tests ----------------------------
def test_get_entities(client, test_db):
    # Insert test data
    with test_db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO entity 
            (entity_id, entity_name, entity_description) 
            VALUES (1, 'Test Entity', 'Test Description')
        """)
        test_db.commit()

    token = get_auth_token(client)
    response = client.get('/Entity',
                         headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert b'Test Entity' in response.data

# ---------------------------- Glossary Tests ----------------------------
def test_get_glossary(client, test_db):
    # Insert test data
    current_date = datetime.now().date()
    with test_db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO glossary_of_business_terms 
            (business_term_short_name, date_term_defined) 
            VALUES ('TEST_TERM', %s)
        """, (current_date,))
        test_db.commit()

    token = get_auth_token(client)
    response = client.get('/Glossary-of-Business-Terms',
                         headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert b'TEST_TERM' in response.data

# ---------------------------- Source Systems Tests ----------------------------
def test_get_source_systems(client, test_db):
    # Insert test data
    with test_db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO source_systems 
            (src_system_id, src_system_name) 
            VALUES (1, 'Test System')
        """)
        test_db.commit()

    token = get_auth_token(client)
    response = client.get('/Source-Systems',
                         headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert b'Test System' in response.data

# ---------------------------- Error Handling Tests ----------------------------
def test_missing_token(client):
    response = client.get('/Attribute')
    assert b'Login Required' in response.data

def test_invalid_token(client):
    response = client.get('/Attribute',
                         headers={'Authorization': 'Bearer invalid_token'})
    assert b'Login Required' in response.data

def test_missing_required_fields(client):
    token = get_auth_token(client)
    response = client.post('/Attribute',
                          headers={'Authorization': f'Bearer {token}'},
                          json={})
    assert response.status_code == 400

def test_manage_page_access(client):
    """Test accessing the management page"""
    token = get_auth_token(client)
    response = client.get('/manage',
                         headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert b'Data Management' in response.data

def test_manage_page_unauthorized(client):
    """Test accessing management page without authentication"""
    response = client.get('/manage')
    assert b'Login Required' in response.data

if __name__ == '__main__':
    pytest.main(['-v'])

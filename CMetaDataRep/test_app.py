import pytest
import json
from app import app
import pymysql
from datetime import datetime, timedelta, timezone

# ===================================
# TEST FIXTURES
# ===================================
@pytest.fixture
def client():
    """Create a test client for the app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

#fix later 

@pytest.fixture(scope='session')
def test_db():
    """Create a database connection for testing"""
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
    """Clear test data before each test"""
    with test_db.cursor() as cursor:
        # Clear all tables
        tables = [
            'attribute',
            'business_term_owner',
            'entity',
            'glossary_of_business_terms',
            'source_systems',
            'business_term_type'
        ]
        for table in tables:
            cursor.execute(f"DELETE FROM {table}")
    test_db.commit()

@pytest.fixture(autouse=True)
def setup_users():
    """Ensure test users exist"""
    from app import users
    users.clear()  # Clear existing users first
    users['admin'] = {
        'password': 'admin123',
        'role': 'admin',
        'user_id': 1,
        'email': 'admin@example.com',
        'created_at': datetime.now(timezone.utc)
    }

# ===================================
# HELPER FUNCTIONS
# ===================================
def get_auth_token(client):
    """Get authentication token for testing"""
    response = client.post('/login', 
                          json={'username': 'admin', 'password': 'admin123'})
    assert response.status_code == 200, f"Login failed with status {response.status_code}: {response.data}"
    data = json.loads(response.data)
    assert 'token' in data, f"No token in response: {data}"
    return data['token']

# ===================================
# AUTHENTICATION TESTS
# ===================================
def test_login_success(client):
    """Test successful login"""
    response = client.post('/login',
                          json={'username': 'admin', 'password': 'admin123'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data
    assert 'user' in data
    assert data['user']['username'] == 'admin'
    assert data['user']['role'] == 'admin'

def test_login_failure(client):
    """Test login with invalid credentials"""
    response = client.post('/login',
                          json={'username': 'wrong', 'password': 'wrong'})
    assert response.status_code == 401

def test_register_new_user(client):
    """Test user registration"""
    response = client.post('/register',
                          json={
                              'username': 'testuser',
                              'password': 'test123',
                              'email': 'test@example.com'
                          })
    assert response.status_code == 201

# ===================================
# ATTRIBUTE TESTS
# ===================================
def test_get_attributes(client, test_db):
    """Test retrieving attributes"""
    # Insert test data
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
    """Test adding a new attribute"""
    token = get_auth_token(client)
    assert token is not None, "Failed to get authentication token"
    
    test_attribute = {
        'attribute_id': 1,
        'attribute_name': 'Test Attribute',
        'attribute_datatype': 'VARCHAR',
        'attribute_description': 'Test Description',
        'typical_values': 'Test Values',
        'validation_criteria': 'Test Criteria'
    }
    response = client.post('/Attribute',
                          headers={
                              'Authorization': f'Bearer {token}',
                              'Content-Type': 'application/json'
                          },
                          json=test_attribute)
    assert response.status_code == 201

def test_update_attribute(client, test_db):
    """Test updating an attribute"""
    # First create an attribute
    with test_db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO attribute 
            (attribute_id, attribute_name, attribute_datatype) 
            VALUES (1, 'Original Name', 'VARCHAR')
        """)
        test_db.commit()

    token = get_auth_token(client)
    update_data = {
        'attribute_name': 'Updated Name',
        'attribute_datatype': 'INT',
        'attribute_description': 'Updated Description'
    }
    response = client.put('/Attribute/1',
                         headers={'Authorization': f'Bearer {token}'},
                         json=update_data)
    assert response.status_code == 200

def test_delete_attribute(client, test_db):
    """Test deleting an attribute"""
    # First create an attribute
    with test_db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO attribute 
            (attribute_id, attribute_name, attribute_datatype) 
            VALUES (1, 'To Delete', 'VARCHAR')
        """)
        test_db.commit()

    token = get_auth_token(client)
    response = client.delete('/Attribute/1',
                           headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

# ===================================
# BUSINESS TERM OWNER TESTS
# ===================================
def test_get_business_term_owners(client, test_db):
    """Test retrieving business term owners"""
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

def test_update_business_term_owner(client, test_db):
    """Test updating a business term owner"""
    # First create a business term owner
    with test_db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO business_term_owner 
            (term_owner_code, term_owner_description) 
            VALUES ('TEST01', 'Original Description')
        """)
        test_db.commit()

    token = get_auth_token(client)
    update_data = {
        'term_owner_description': 'Updated Description'
    }
    response = client.put('/Business-Term-Owner/TEST01',
                         headers={'Authorization': f'Bearer {token}'},
                         json=update_data)
    assert response.status_code == 200

def test_delete_business_term_owner(client, test_db):
    """Test deleting a business term owner"""
    # First create a business term owner
    with test_db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO business_term_owner 
            (term_owner_code, term_owner_description) 
            VALUES ('TEST01', 'To Delete')
        """)
        test_db.commit()

    token = get_auth_token(client)
    response = client.delete('/Business-Term-Owner/TEST01',
                           headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

# ===================================
# ENTITY TESTS
# ===================================
def test_get_entities(client, test_db):
    """Test retrieving entities"""
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

def test_update_entity(client, test_db):
    """Test updating an entity"""
    # First create an entity
    with test_db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO entity 
            (entity_id, entity_name, entity_description) 
            VALUES (1, 'Original Name', 'Original Description')
        """)
        test_db.commit()

    token = get_auth_token(client)
    update_data = {
        'entity_name': 'Updated Name',
        'entity_description': 'Updated Description'
    }
    response = client.put('/Entity/1',
                         headers={'Authorization': f'Bearer {token}'},
                         json=update_data)
    assert response.status_code == 200

def test_delete_entity(client, test_db):
    """Test deleting an entity"""
    # First create an entity
    with test_db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO entity 
            (entity_id, entity_name, entity_description) 
            VALUES (1, 'To Delete', 'Description')
        """)
        test_db.commit()

    token = get_auth_token(client)
    response = client.delete('/Entity/1',
                           headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

# ===================================
# GLOSSARY TESTS
# ===================================
def test_get_glossary(client, test_db):
    """Test retrieving glossary terms"""
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

def test_update_glossary_term(client, test_db):
    """Test updating a glossary term"""
    # First create a glossary term
    current_date = datetime.now().date()
    with test_db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO glossary_of_business_terms 
            (business_term_short_name, date_term_defined) 
            VALUES ('TEST_TERM', %s)
        """, (current_date,))
        test_db.commit()

    token = get_auth_token(client)
    update_data = {
        'date_term_defined': (current_date + timedelta(days=1)).strftime('%Y-%m-%d')
    }
    response = client.put('/Glossary-of-Business-Terms/TEST_TERM',
                         headers={'Authorization': f'Bearer {token}'},
                         json=update_data)
    assert response.status_code == 200

def test_delete_glossary_term(client, test_db):
    """Test deleting a glossary term"""
    # First create a glossary term
    with test_db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO glossary_of_business_terms 
            (business_term_short_name, date_term_defined) 
            VALUES ('TEST_TERM', CURRENT_DATE)
        """)
        test_db.commit()

    token = get_auth_token(client)
    response = client.delete('/Glossary-of-Business-Terms/TEST_TERM',
                           headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

# ===================================
# SOURCE SYSTEMS TESTS
# ===================================
def test_get_source_systems(client, test_db):
    """Test retrieving source systems"""
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

# ===================================
# ERROR HANDLING TESTS
# ===================================
def test_missing_required_fields(client):
    """Test handling of missing required fields"""
    token = get_auth_token(client)
    response = client.post('/Attribute',
                          headers={'Authorization': f'Bearer {token}'},
                          json={})
    assert response.status_code == 400

def test_invalid_token(client):
    """Test handling of invalid authentication token"""
    response = client.get('/Attribute',
                         headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 401

if __name__ == '__main__':
    pytest.main(['-v'])

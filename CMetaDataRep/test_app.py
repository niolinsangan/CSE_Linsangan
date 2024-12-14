import pytest
import json
from app import app
import pymysql
from datetime import datetime

# ===================================
# TEST FIXTURES
# ===================================
@pytest.fixture
def client():
    """Create a test client for the app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

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

# ===================================
# HELPER FUNCTIONS
# ===================================
def get_auth_token(client):
    """Get authentication token for testing"""
    response = client.post('/login', 
                         json={'username': 'admin', 'password': 'admin123'})
    return json.loads(response.data)['token']

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

    response = client.get('/Attribute')
    assert response.status_code == 200
    assert b'Test Attribute' in response.data

def test_add_attribute(client):
    """Test adding a new attribute"""
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

    response = client.get('/Business-Term-Owner')
    assert response.status_code == 200
    assert b'Test Owner' in response.data

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

    response = client.get('/Entity')
    assert response.status_code == 200
    assert b'Test Entity' in response.data

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

    response = client.get('/Glossary-of-Business-Terms')
    assert response.status_code == 200
    assert b'TEST_TERM' in response.data

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

    response = client.get('/Source-Systems')
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
    assert b'Login Required' in response.data

if __name__ == '__main__':
    pytest.main(['-v'])

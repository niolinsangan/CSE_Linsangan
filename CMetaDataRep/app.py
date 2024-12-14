from flask import Flask, jsonify, request
import pymysql
from datetime import datetime, timedelta
import jwt
from functools import wraps
import json

# ===================================
# SECURITY AND AUTHENTICATION FUNCTIONS
# ===================================
# Secret key used to sign and verify JWT tokens
SECRET_KEY = 'nioshiii'  # Replace with a strong, unique secret key in production

# Function to create a JWT token
def create_jwt(user_id, role):
    """
    Creates a JWT token for user authentication
    Args:
        user_id: User's unique identifier
        role: User's role (admin, user, etc.)
    Returns:
        str: JWT token
    """
    try:
        payload = {
            'user_id': user_id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        )
        print(f"Generated token: {token}")  # Debug print
        return token
    except Exception as e:
        print(f"Error creating JWT: {e}")  # Debug print
        raise

# Function to decode and verify a JWT token
def decode_jwt(token):
    """
    Decodes and verifies a JWT token
    Args:
        token: JWT token string
    Returns:
        dict: Decoded token payload or error message
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    
    except jwt.ExpiredSignatureError:
        return {'error': 'Token expired'}
    
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}

# Decorator to protect routes with optional role-based access control
def jwt_required(f):
    """
    Decorator to protect routes with JWT authentication
    Args:
        f: Function to be decorated
    Returns:
        Function: Decorated function with JWT verification
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return create_login_form()
        
        try:
            token = token.split(" ")[1]
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user = decoded_token
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return create_login_form()
        except jwt.InvalidTokenError:
            return create_login_form()
            
    return decorated_function


app = Flask(__name__)

# ===================================
# DATABASE CONNECTION
# ===================================
# Dictionary to store user credentials
users = {
    'admin': {
        'password': 'admin123',
        'role': 'admin',
        'user_id': 1,
        'email': 'admin@example.com',
        'created_at': datetime.utcnow()
    },
    'user': {
        'password': 'user123',
        'role': 'user',
        'user_id': 2,
        'email': 'user@example.com',
        'created_at': datetime.utcnow()
    },
    'manager': {
        'password': 'manager123',
        'role': 'manager',
        'user_id': 3,
        'email': 'manager@example.com',
        'created_at': datetime.utcnow()
    },
    'analyst': {
        'password': 'analyst123',
        'role': 'analyst',
        'user_id': 4,
        'email': 'analyst@example.com',
        'created_at': datetime.utcnow()
    },
    'viewer': {
        'password': 'viewer123',
        'role': 'viewer',
        'user_id': 5,
        'email': 'viewer@example.com',
        'created_at': datetime.utcnow()
    }
}

# Function to establish a connection to the MySQL database
def get_db_connection():
    """
    Establishes connection to MySQL database
    Returns:
        Connection: MySQL database connection object
    """
    return pymysql.connect(
        host='localhost',  # MySQL host (localhost for local development)
        user='root',  # Database username
        password='antonio123',  # Database password
        database='customermetadatarepository',  # Database name
        cursorclass=pymysql.cursors.DictCursor  # Ensures that results are returned as dictionaries
    )

# ===================================
# VIEW TEMPLATE GENERATORS
# ===================================
# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login requests
    Methods:
        GET: Returns login form
        POST: Processes login credentials
    Returns:
        GET: HTML login form
        POST: JSON with token and user info or error message
    """
    if request.method == 'GET':
        return create_login_form()
        
    if request.method == 'POST':
        try:
            data = request.json
            username = data.get('username')
            password = data.get('password')

            print(f"Login attempt - Username: {username}, Password: {password}")  # Debug print
            print(f"Available users: {list(users.keys())}")  # Debug print
            
            if username in users:
                print(f"User found, stored password: {users[username]['password']}")  # Debug print
                if users[username]['password'] == password:
                    print("Password matches!")  # Debug print
                    token = create_jwt(
                        user_id=users[username]['user_id'],
                        role=users[username]['role']
                    )
                    print(f"Generated token: {token}")  # Debug print
                    return jsonify({
                        'token': token,
                        'user': {
                            'username': username,
                            'role': users[username]['role']
                        }
                    }), 200
                else:
                    print("Password doesn't match")  # Debug print
            else:
                print(f"User {username} not found")  # Debug print
            
            return jsonify({'error': 'Invalid credentials'}), 401
            
        except Exception as e:
            print(f"Login error: {str(e)}")  # Debug print
            return jsonify({'error': str(e)}), 500

# Define a route for the home page
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Customer Meta Data Repository</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                color: #343a40;
            }
            .header {
                background-color: #007bff;
                color: white;
                padding: 1rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .header-content {
                max-width: 1200px;
                margin: 0 auto;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .nav-links {
                display: flex;
                gap: 20px;
            }
            .nav-links a {
                color: white;
                text-decoration: none;
                padding: 5px 10px;
                border-radius: 4px;
                transition: background-color 0.3s;
            }
            .nav-links a:hover {
                background-color: rgba(255,255,255,0.1);
            }
            .main-content {
                text-align: center;
                padding: 50px 20px;
                max-width: 800px;
                margin: 0 auto;
            }
            h1 {
                margin: 0;
                font-size: 1.5rem;
            }
            .welcome-text {
                margin-top: 40px;
                font-size: 1.2rem;
                line-height: 1.6;
                color: #666;
            }
            .highlight {
                color: #007bff;
                font-weight: 600;
            }
            .features-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-top: 40px;
                text-align: left;
            }
            .feature-card {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
        </style>
    </head>
    <body>
        <header class="header">
            <div class="header-content">
                <h1>Customer Meta Data Repository</h1>
                <nav class="nav-links">
                    <a href="/Attribute">Attribute</a>
                    <a href="/Business-Term-Owner">Business Term Owner</a>
                    <a href="/Entity">Entity</a>
                    <a href="/Glossary-of-Business-Terms">Glossary of Business Terms</a>
                    <a href="/Source-Systems">Source Systems</a>
                    <a href="/manage">Manage Data</a>
                    <a href="/login">Login</a>
                </nav>
            </div>
        </header>
        <main class="main-content">
            <div class="welcome-text">
                <h2>Welcome to the <span class="highlight">Customer Meta Data</span></h2>
                <p>Your centralized solution for managing and organizing customer information 
                   across multiple departments and locations.</p>
                
                <div class="features-grid">
                    <div class="feature-card">
                        <h3>📊 Attribute Management</h3>
                        <p>Define and manage data attributes with detailed metadata, 
                           including data types, formats, and validation rules.</p>
                    </div>
                    <div class="feature-card">
                        <h3>👤 Business Term Ownership</h3>
                        <p>Track business term owners and their responsibilities for 
                           maintaining data definitions and standards.</p>
                    </div>
                    <div class="feature-card">
                        <h3>🔄 Entity Management</h3>
                        <p>Document and organize data entities with their relationships, 
                           dependencies, and business context.</p>
                    </div>
                    <div class="feature-card">
                        <h3>📚 Business Glossary</h3>
                        <p>Maintain a comprehensive glossary of business terms with 
                           standardized definitions and classifications.</p>
                    </div>
                    <div class="feature-card">
                        <h3>🔄 Source Systems</h3>
                        <p>Track and manage data lineage by documenting source systems 
                           and their integration points.</p>
                    </div>
                </div>
                
                <p style="margin-top: 40px;">Use the navigation links above to access different modules of the system.</p>
            </div>
        </main>
    </body>
    </html>
    """

# Custom error handler for 400 Bad Request
@app.errorhandler(400)
def bad_request(error):
    """
    Handles bad request errors (400)
    Args:
        error: Error details
    Returns:
        JSON: Error message with 400 status code
    """
    # Return a JSON response with an error message and 400 status code
    return jsonify({"error": "Invalid JSON"}), 400


# ===================================
# ATTRIBUTE CRUD OPERATIONS
# ===================================
# Add this HTML template for table display
def create_table_view(data, title):
    """
    Generates HTML table view for displaying data
    Args:
        data: List of dictionaries containing table data
        title: Title of the table/page
    Returns:
        str: HTML template string
    """
    if not data:
        return f"""
        <h2>{title}</h2>
        <p>No data available.</p>
        """
    
    headers = data[0].keys()
    primary_key = list(headers)[0]  # First column is usually the primary key
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            h2 {{
                color: #007bff;
                margin-bottom: 20px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #007bff;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f8f9fa;
            }}
            tr:hover {{
                background-color: #f2f2f2;
            }}
            .back-link {{
                display: inline-block;
                margin-top: 20px;
                color: #007bff;
                text-decoration: none;
            }}
            .back-link:hover {{
                text-decoration: underline;
            }}
            .error-message {{
                color: #dc3545;
                margin-top: 20px;
                display: none;
            }}
            
            .crud-buttons {{
                margin: 20px 0;
            }}
            
            .btn {{
                padding: 8px 16px;
                margin-right: 10px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
            }}
            
            .btn-add {{
                background-color: #28a745;
                color: white;
            }}
            
            .btn-edit {{
                background-color: #ffc107;
                color: #000;
            }}
            
            .btn-delete {{
                background-color: #dc3545;
                color: white;
            }}
            
            .modal {{
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.5);
            }}
            
            .modal-content {{
                background-color: white;
                margin: 15% auto;
                padding: 20px;
                width: 400px;
                border-radius: 8px;
                text-align: center;
            }}
            
            .modal-buttons {{
                margin-top: 20px;
                color: #007bff;
                text-decoration: none;
            }}
            
            .btn-confirm {{
                background-color: #dc3545;
                color: white;
            }}
            
            .btn-cancel {{
                background-color: #6c757d;
                color: white;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>{title}</h2>
            
            <div class="crud-buttons">
                <button class="btn btn-add" onclick="location.href='{get_add_url(title)}'">Add New</button>
            </div>

            <div id="tableContent">
                <table>
                    <thead>
                        <tr>
                            {''.join(f'<th>{header}</th>' for header in headers)}
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(
                            f"<tr>"
                            f"{''.join(f'<td>{str(value)}</td>' for value in row.values())}"
                            f"<td>"
                            f"<button class='btn btn-edit' onclick='editRecord({json.dumps(row)})'>Edit</button>"
                            f"<button class='btn btn-delete' onclick='showDeleteModal({json.dumps(row[primary_key])})'>Delete</button>"
                            f"</td>"
                            f"</tr>"
                            for row in data
                        )}
                    </tbody>
                </table>
            </div>
            <a href="/" class="back-link">← Back to Home</a>
        </div>

        <!-- Delete Confirmation Modal -->
        <div id="deleteModal" class="modal">
            <div class="modal-content">
                <h3>Confirm Delete</h3>
                <p>Are you sure you want to delete this record?</p>
                <div class="modal-buttons">
                    <button class="btn btn-confirm" onclick="confirmDelete()">Delete</button>
                    <button class="btn btn-cancel" onclick="hideDeleteModal()">Cancel</button>
                </div>
            </div>
        </div>

        <script>
            let recordToDelete = null;

            function showDeleteModal(id) {{
                recordToDelete = id;
                document.getElementById('deleteModal').style.display = 'block';
            }}

            function hideDeleteModal() {{
                document.getElementById('deleteModal').style.display = 'none';
                recordToDelete = null;
            }}

            function confirmDelete() {{
                if (recordToDelete === null) return;

                fetch(`${{window.location.pathname}}/${{recordToDelete}}`, {{
                    method: 'DELETE'
                }})
                .then(response => {{
                    if (response.ok) {{
                        window.location.reload();
                    }} else {{
                        response.json().then(data => {{
                            alert(data.error || 'Failed to delete record');
                        }});
                    }}
                }})
                .catch(error => {{
                    alert('Error: ' + error);
                }})
                .finally(() => {{
                    hideDeleteModal();
                }});
            }}

            function editRecord(record) {{
                const url = window.location.pathname + '/edit/' + record['{primary_key}'];
                window.location.href = url;
            }}

            // Close modal when clicking outside
            window.onclick = function(event) {{
                const modal = document.getElementById('deleteModal');
                if (event.target === modal) {{
                    hideDeleteModal();
                }}
            }}
        </script>
    </body>
    </html>
    """

def get_add_url(title):
    """
    Maps table titles to their corresponding add URLs
    Args:
        title: Table/page title
    Returns:
        str: URL for adding new records to the table
    """
    url_mapping = {
        "Attributes": "/Attribute/add",
        "Business Term Owners": "/Business-Term-Owner/add",
        "Entities": "/Entity/add",
        "Glossary of Business Terms": "/Glossary-of-Business-Terms/add",
        "Source Systems": "/Source-Systems/add"
    }
    return url_mapping.get(title, "/")

# Update the routes to remove @jwt_required and show data directly
@app.route('/Attribute', methods=['GET'])
def get_attributes():
    """
    Retrieves all attributes from database
    Returns:
        HTML: Table view of attributes
    """
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT attribute_id, attribute_name, attribute_datatype, 
                       attribute_description, typical_values, validation_criteria 
                FROM attribute
            """)
            attributes = cursor.fetchall()
        return create_table_view(attributes, "Attributes")
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>", 500
    finally:
        if connection:
            connection.close()

# POST route to add a new attribute
@app.route('/Attribute', methods=['POST'])
@jwt_required
def add_attribute():
    """
    Adds a new attribute to database
    Returns:
        JSON: Success/error message
    """
    data = request.json
    required_fields = ['attribute_id', 'attribute_name', 'attribute_datatype']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO attribute (attribute_id, attribute_name, attribute_datatype, 
                                     attribute_description, typical_values, validation_criteria)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (data['attribute_id'], data['attribute_name'], data['attribute_datatype'],
                 data.get('attribute_description'), data.get('typical_values'),
                 data.get('validation_criteria')))
            connection.commit()
            print("Attribute added successfully")  # Debug print
        return jsonify({'message': 'Attribute added successfully'}), 201
    except Exception as e:
        print(f"Error adding attribute: {e}")  # Debug print
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

# PUT route to update an attribute
@app.route('/Attribute/<int:id>', methods=['PUT'])
@jwt_required
def update_attribute(id):
    """
    Updates an existing attribute
    Args:
        id: Attribute ID to update
    Returns:
        JSON: Success/error message
    """
    data = request.json
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM attribute WHERE attribute_id = %s", (id,))
            if not cursor.fetchone():
                return jsonify({'error': 'Attribute not found'}), 404
            
            cursor.execute("""
                UPDATE attribute 
                SET attribute_name = %s, attribute_datatype = %s,
                    attribute_description = %s, typical_values = %s,
                    validation_criteria = %s
                WHERE attribute_id = %s
            """, (data['attribute_name'], data['attribute_datatype'],
                 data.get('attribute_description'), data.get('typical_values'),
                 data.get('validation_criteria'), id))
            connection.commit()
        return jsonify({'message': 'Attribute updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

# DELETE route to remove an attribute
@app.route('/Attribute/<int:id>', methods=['DELETE'])
@jwt_required
def delete_attribute(id):
    """
    Deletes an attribute from database
    Args:
        id: Attribute ID to delete
    Returns:
        JSON: Success/error message
    """
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM attribute WHERE attribute_id = %s", (id,))
            if not cursor.fetchone():
                return jsonify({'error': 'Attribute not found'}), 404
            
            cursor.execute("DELETE FROM attribute WHERE attribute_id = %s", (id,))
            connection.commit()
        return jsonify({'message': 'Attribute deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

# ===================================
# BUSINESS TERM OWNER CRUD OPERATIONS
# ===================================
@app.route('/Business-Term-Owner', methods=['GET'])
def get_business_term_owners():
    """
    Retrieves all business term owners
    Returns:
        HTML: Table view of business term owners
    """
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT term_owner_code, term_owner_description 
                FROM business_term_owner
            """)
            owners = cursor.fetchall()
        return create_table_view(owners, "Business Term Owners")
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>", 500
    finally:
        if connection:
            connection.close()

@app.route('/Business-Term-Owner', methods=['POST'])
@jwt_required
def add_business_term_owner():
    """
    Adds a new business term owner to database
    Returns:
        JSON: Success/error message
    """
    data = request.json
    required_fields = ['term_owner_code', 'term_owner_description']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO business_term_owner (term_owner_code, term_owner_description)
                VALUES (%s, %s)
            """, (data['term_owner_code'], data['term_owner_description']))
            connection.commit()
        return jsonify({'message': 'Business Term Owner added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/Business-Term-Owner/<string:code>', methods=['PUT'])
@jwt_required
def update_business_term_owner(code):
    """
    Updates an existing business term owner
    Args:
        code: Owner code to update
    Returns:
        JSON: Success/error message
    """
    data = request.json
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM business_term_owner WHERE term_owner_code = %s", (code,))
            if not cursor.fetchone():
                return jsonify({'error': 'Business Term Owner not found'}), 404
            
            cursor.execute("""
                UPDATE business_term_owner 
                SET term_owner_description = %s
                WHERE term_owner_code = %s
            """, (data['term_owner_description'], code))
            connection.commit()
        return jsonify({'message': 'Business Term Owner updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/Business-Term-Owner/<string:code>', methods=['DELETE'])
@jwt_required
def delete_business_term_owner(code):
    """
    Deletes a business term owner from database
    Args:
        code: Owner code to delete
    Returns:
        JSON: Success/error message
    """
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM business_term_owner WHERE term_owner_code = %s", (code,))
            if not cursor.fetchone():
                return jsonify({'error': 'Business Term Owner not found'}), 404
            
            cursor.execute("DELETE FROM business_term_owner WHERE term_owner_code = %s", (code,))
            connection.commit()
        return jsonify({'message': 'Business Term Owner deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

# ===================================
# ENTITY CRUD OPERATIONS
# ===================================
@app.route('/Entity', methods=['GET'])
def get_entities():
    """
    Retrieves all entities from database
    Returns:
        HTML: Table view of entities
    """
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT entity_id, entity_name, entity_description 
                FROM entity
            """)
            entities = cursor.fetchall()
        return create_table_view(entities, "Entities")
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>", 500
    finally:
        if connection:
            connection.close()

@app.route('/Entity', methods=['POST'])
@jwt_required
def add_entity():
    """
    Adds a new entity to database
    Returns:
        JSON: Success/error message
    """
    data = request.json
    required_fields = ['entity_id', 'entity_name']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO entity (entity_id, entity_name, entity_description)
                VALUES (%s, %s, %s)
            """, (data['entity_id'], data['entity_name'], data.get('entity_description')))
            connection.commit()
        return jsonify({'message': 'Entity added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/Entity/<int:id>', methods=['PUT'])
@jwt_required
def update_entity(id):
    """
    Updates an existing entity
    Args:
        id: Entity ID to update
    Returns:
        JSON: Success/error message
    """
    data = request.json
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM entity WHERE entity_id = %s", (id,))
            if not cursor.fetchone():
                return jsonify({'error': 'Entity not found'}), 404
            
            cursor.execute("""
                UPDATE entity 
                SET entity_name = %s, entity_description = %s
                WHERE entity_id = %s
            """, (data['entity_name'], data.get('entity_description'), id))
            connection.commit()
        return jsonify({'message': 'Entity updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/Entity/<int:id>', methods=['DELETE'])
@jwt_required
def delete_entity(id):
    """
    Deletes an entity from database
    Args:
        id: Entity ID to delete
    Returns:
        JSON: Success/error message
    """
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM entity WHERE entity_id = %s", (id,))
            if not cursor.fetchone():
                return jsonify({'error': 'Entity not found'}), 404
            
            cursor.execute("DELETE FROM entity WHERE entity_id = %s", (id,))
            connection.commit()
        return jsonify({'message': 'Entity deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

# ===================================
# GLOSSARY CRUD OPERATIONS
# ===================================
@app.route('/Glossary-of-Business-Terms', methods=['GET'])
def get_glossary():
    """
    Retrieves all glossary terms
    Returns:
        HTML: Table view of glossary terms
    """
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT business_term_short_name, 
                       DATE_FORMAT(date_term_defined, '%Y-%m-%d') as date_term_defined 
                FROM glossary_of_business_terms
            """)
            terms = cursor.fetchall()
        return create_table_view(terms, "Glossary of Business Terms")
    except Exception as e:
        print(f"Error fetching glossary terms: {e}")  # Debug print
        return f"<h1>Error</h1><p>{str(e)}</p>", 500
    finally:
        if connection:
            connection.close()

@app.route('/Glossary-of-Business-Terms', methods=['POST'])
@jwt_required
def add_glossary_term():
    """
    Adds a new glossary term to database
    Returns:
        JSON: Success/error message
    """
    data = request.json
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO glossary_of_business_terms 
                (business_term_short_name, date_term_defined)
                VALUES (%s, STR_TO_DATE(%s, '%Y-%m-%d'))
            """, (data['business_term_short_name'], data['date_term_defined']))
            connection.commit()
        return jsonify({'message': 'Term added successfully'}), 201
    except Exception as e:
        print(f"Error adding glossary term: {e}")  # Debug print
        if connection:
            connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/Glossary-of-Business-Terms/<string:name>', methods=['PUT'])
@jwt_required
def update_glossary_term(name):
    """
    Updates an existing glossary term
    Args:
        name: Term name to update
    Returns:
        JSON: Success/error message
    """
    data = request.json
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE glossary_of_business_terms 
                SET date_term_defined = STR_TO_DATE(%s, '%Y-%m-%d')
                WHERE business_term_short_name = %s
            """, (data['date_term_defined'], name))
            connection.commit()
        return jsonify({'message': 'Term updated successfully'}), 200
    except Exception as e:
        print(f"Error updating glossary term: {e}")  # Debug print
        if connection:
            connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/Glossary-of-Business-Terms/<string:name>', methods=['DELETE'])
@jwt_required
def delete_glossary_term(name):
    """
    Deletes a glossary term from database
    Args:
        name: Term name to delete
    Returns:
        JSON: Success/error message
    """
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM glossary_of_business_terms 
                WHERE business_term_short_name = %s
            """, (name,))
            connection.commit()
        return jsonify({'message': 'Term deleted successfully'}), 200
    except Exception as e:
        print(f"Error deleting glossary term: {e}")  # Debug print
        if connection:
            connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

# ===================================
# SOURCE SYSTEMS CRUD OPERATIONS
# ===================================
@app.route('/Source-Systems', methods=['GET'])
def get_source_systems():
    """
    Retrieves all source systems
    Returns:
        HTML: Table view of source systems
    """
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT src_system_id, src_system_name 
                FROM source_systems
            """)
            systems = cursor.fetchall()
        return create_table_view(systems, "Source Systems")
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>", 500
    finally:
        if connection:
            connection.close()

@app.route('/Source-Systems', methods=['POST'])
@jwt_required
def add_source_system():
    """
    Adds a new source system to database
    Returns:
        JSON: Success/error message
    """
    data = request.json
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO source_systems 
                (src_system_id, src_system_name)
                VALUES (%s, %s)
            """, (data['src_system_id'], data['src_system_name']))
            connection.commit()
        return jsonify({'message': 'Source system added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

# ===================================
# FORM GENERATORS
# ===================================
# Add this login form template
def create_login_form():
    """
    Generates HTML login form
    Returns:
        str: HTML template for login form
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login Required</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .login-container {
                background-color: white;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                width: 300px;
            }
            h2 {
                color: #007bff;
                margin-bottom: 20px;
                text-align: center;
            }
            .form-group {
                margin-bottom: 15px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                color: #666;
            }
            input {
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                box-sizing: border-box;
            }
            button {
                width: 100%;
                padding: 10px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            button:hover {
                background-color: #0056b3;
            }
            .back-link {
                display: block;
                text-align: center;
                margin-top: 15px;
                color: #007bff;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <h2>Login Required</h2>
            <form id="loginForm">
                <div class="form-group">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit">Login</button>
            </form>
            <a href="/register" class="back-link">Need an account? Register</a>
            <a href="/" class="back-link">← Back to Home</a>
        </div>
        <script>
            document.getElementById('loginForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        username: document.getElementById('username').value,
                        password: document.getElementById('password').value
                    })
                });
                const data = await response.json();
                if (data.token) {
                    localStorage.setItem('token', data.token);
                    window.location.reload();
                } else {
                    alert('Login failed');
                }
            });
        </script>
    </body>
    </html>
    """

# Add this registration form template
def create_register_form():
    """
    Generates HTML registration form
    Returns:
        str: HTML template for registration form
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Register</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .register-container {
                background-color: white;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                width: 300px;
            }
            h2 {
                color: #007bff;
                margin-bottom: 20px;
                text-align: center;
            }
            .form-group {
                margin-bottom: 15px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                color: #666;
            }
            input {
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                box-sizing: border-box;
            }
            button {
                width: 100%;
                padding: 10px;
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                margin-bottom: 10px;
            }
            button:hover {
                background-color: #218838;
            }
            .login-link {
                display: block;
                text-align: center;
                margin-top: 15px;
                color: #007bff;
                text-decoration: none;
            }
            .error-message {
                color: #dc3545;
                margin-bottom: 10px;
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="register-container">
            <h2>Register</h2>
            <p id="errorMessage" class="error-message"></p>
            <form id="registerForm">
                <div class="form-group">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <div class="form-group">
                    <label for="confirmPassword">Confirm Password:</label>
                    <input type="password" id="confirmPassword" name="confirmPassword" required>
                </div>
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <button type="submit">Register</button>
            </form>
            <a href="/login" class="login-link">Already have an account? Login</a>
        </div>
        <script>
            document.getElementById('registerForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const errorMessage = document.getElementById('errorMessage');
                
                // Password validation
                const password = document.getElementById('password').value;
                const confirmPassword = document.getElementById('confirmPassword').value;
                
                if (password !== confirmPassword) {
                    errorMessage.textContent = 'Passwords do not match';
                    errorMessage.style.display = 'block';
                    return;
                }
                
                try {
                    const response = await fetch('/register', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            username: document.getElementById('username').value,
                            password: password,
                            email: document.getElementById('email').value
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        window.location.href = '/login';  // Redirect to login page
                    } else {
                        errorMessage.textContent = data.error || 'Registration failed';
                        errorMessage.style.display = 'block';
                    }
                } catch (error) {
                    errorMessage.textContent = 'An error occurred. Please try again.';
                    errorMessage.style.display = 'block';
                }
            });
        </script>
    </body>
    </html>
    """

# Add registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration
    Methods:
        GET: Returns registration form
        POST: Processes new user registration
    Returns:
        GET: HTML registration form
        POST: JSON success/error message
    """
    if request.method == 'GET':
        return create_register_form()
        
    if request.method == 'POST':
        data = request.json
        required_fields = ['username', 'password', 'email']
        
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        try:
            # Check if username already exists
            if data['username'] in users:
                return jsonify({'error': 'Username already exists'}), 409
            
            # Add new user
            users[data['username']] = {
                'password': data['password'],
                'role': 'user',  # Default role for new registrations
                'user_id': len(users) + 1
            }
            
            return jsonify({'message': 'User registered successfully'}), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# Add this new route for data management
@app.route('/manage')
def manage_data():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Data Management</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h2 {
                color: #007bff;
                margin-bottom: 20px;
            }
            .crud-section {
                margin-bottom: 30px;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
            .crud-buttons {
                margin-top: 10px;
            }
            .btn {
                padding: 8px 16px;
                margin-right: 10px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
            }
            .btn-add {
                background-color: #28a745;
                color: white;
            }
            .btn-view {
                background-color: #007bff;
                color: white;
            }
            .btn-edit {
                background-color: #ffc107;
                color: black;
            }
            .btn-delete {
                background-color: #dc3545;
                color: white;
            }
            .back-link {
                display: inline-block;
                margin-top: 20px;
                color: #007bff;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Data Management</h2>
            
            <div class="crud-section">
                <h3>Attributes</h3>
                <div class="crud-buttons">
                    <button class="btn btn-add" onclick="location.href='/Attribute/add'">Add New</button>
                    <button class="btn btn-view" onclick="location.href='/Attribute'">View All</button>
                </div>
            </div>

            <div class="crud-section">
                <h3>Business Term Owners</h3>
                <div class="crud-buttons">
                    <button class="btn btn-add" onclick="location.href='/Business-Term-Owner/add'">Add New</button>
                    <button class="btn btn-view" onclick="location.href='/Business-Term-Owner'">View All</button>
                </div>
            </div>

            <div class="crud-section">
                <h3>Entities</h3>
                <div class="crud-buttons">
                    <button class="btn btn-add" onclick="location.href='/Entity/add'">Add New</button>
                    <button class="btn btn-view" onclick="location.href='/Entity'">View All</button>
                </div>
            </div>

            <div class="crud-section">
                <h3>Glossary of Business Terms</h3>
                <div class="crud-buttons">
                    <button class="btn btn-add" onclick="location.href='/Glossary-of-Business-Terms/add'">Add New</button>
                    <button class="btn btn-view" onclick="location.href='/Glossary-of-Business-Terms'">View All</button>
                </div>
            </div>

            <div class="crud-section">
                <h3>Source Systems</h3>
                <div class="crud-buttons">
                    <button class="btn btn-add" onclick="location.href='/Source-Systems/add'">Add New</button>
                    <button class="btn btn-view" onclick="location.href='/Source-Systems'">View All</button>
                </div>
            </div>

            <a href="/" class="back-link">← Back to Home</a>
        </div>
    </body>
    </html>
    """

# Add these routes for CRUD operations
@app.route('/Attribute/add', methods=['GET'])
def add_attribute_form():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Attribute</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h2 {
                color: #007bff;
                margin-bottom: 20px;
            }
            .form-group {
                margin-bottom: 15px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                color: #666;
            }
            input, select, textarea {
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                box-sizing: border-box;
            }
            .btn {
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
                margin-right: 10px;
            }
            .btn-primary {
                background-color: #007bff;
                color: white;
            }
            .btn-secondary {
                background-color: #6c757d;
                color: white;
            }
            .back-link {
                display: inline-block;
                margin-top: 20px;
                color: #007bff;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Add New Attribute</h2>
            <form id="attributeForm">
                <div class="form-group">
                    <label for="attribute_id">Attribute ID:</label>
                    <input type="number" id="attribute_id" name="attribute_id" required>
                </div>
                <div class="form-group">
                    <label for="attribute_name">Attribute Name:</label>
                    <input type="text" id="attribute_name" name="attribute_name" required>
                </div>
                <div class="form-group">
                    <label for="attribute_datatype">Data Type:</label>
                    <select id="attribute_datatype" name="attribute_datatype" required>
                        <option value="VARCHAR">VARCHAR</option>
                        <option value="INT">INT</option>
                        <option value="DATE">DATE</option>
                        <option value="DECIMAL">DECIMAL</option>
                        <option value="BOOLEAN">BOOLEAN</option>
                        <option value="TEXT">TEXT</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="attribute_description">Description:</label>
                    <textarea id="attribute_description" name="attribute_description" rows="3"></textarea>
                </div>
                <div class="form-group">
                    <label for="typical_values">Typical Values:</label>
                    <input type="text" id="typical_values" name="typical_values">
                </div>
                <div class="form-group">
                    <label for="validation_criteria">Validation Criteria:</label>
                    <input type="text" id="validation_criteria" name="validation_criteria">
                </div>
                <button type="submit" class="btn btn-primary">Save</button>
                <button type="button" class="btn btn-secondary" onclick="history.back()">Cancel</button>
            </form>
            <a href="/manage" class="back-link">← Back to Management</a>
        </div>

        <script>
            document.getElementById('attributeForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const formData = new FormData(e.target);
                const data = Object.fromEntries(formData);
                const token = localStorage.getItem('token');
                
                try {
                    const response = await fetch('/Attribute', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(data)
                    });
                    
                    if (response.ok) {
                        window.location.href = '/Attribute';
                    } else {
                        const error = await response.json();
                        alert(error.error || 'Failed to add attribute');
                    }
                } catch (error) {
                    alert('An error occurred. Please try again.');
                }
            });
        </script>
    </body>
    </html>
    """

@app.route('/Business-Term-Owner/add', methods=['GET'])
def add_business_term_owner_form():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Business Term Owner</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h2 {
                color: #007bff;
                margin-bottom: 20px;
            }
            .form-group {
                margin-bottom: 15px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                color: #666;
            }
            input, select, textarea {
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                box-sizing: border-box;
            }
            .btn {
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
                margin-right: 10px;
            }
            .btn-primary {
                background-color: #007bff;
                color: white;
            }
            .btn-secondary {
                background-color: #6c757d;
                color: white;
            }
            .back-link {
                display: inline-block;
                margin-top: 20px;
                color: #007bff;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Add New Business Term Owner</h2>
            <form id="ownerForm">
                <div class="form-group">
                    <label for="term_owner_code">Owner Code:</label>
                    <input type="text" id="term_owner_code" name="term_owner_code" required>
                </div>
                <div class="form-group">
                    <label for="term_owner_description">Description:</label>
                    <textarea id="term_owner_description" name="term_owner_description" rows="3" required></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Save</button>
                <button type="button" class="btn btn-secondary" onclick="history.back()">Cancel</button>
            </form>
            <a href="/manage" class="back-link">← Back to Management</a>
        </div>

        <script>
            document.getElementById('ownerForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const formData = new FormData(e.target);
                const data = Object.fromEntries(formData);
                const token = localStorage.getItem('token');
                
                try {
                    const response = await fetch('/Business-Term-Owner', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(data)
                    });
                    
                    if (response.ok) {
                        window.location.href = '/Business-Term-Owner';
                    } else {
                        const error = await response.json();
                        alert(error.error || 'Failed to add business term owner');
                    }
                } catch (error) {
                    alert('An error occurred. Please try again.');
                }
            });
        </script>
    </body>
    </html>
    """

# Add these routes for Entity CRUD
@app.route('/Entity/add', methods=['GET'])
def add_entity_form():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Entity</title>
        <style>
            /* Same styles as other forms */
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Add New Entity</h2>
            <form id="entityForm">
                <div class="form-group">
                    <label for="entity_id">Entity ID:</label>
                    <input type="number" id="entity_id" name="entity_id" required>
                </div>
                <div class="form-group">
                    <label for="entity_name">Entity Name:</label>
                    <input type="text" id="entity_name" name="entity_name" required>
                </div>
                <div class="form-group">
                    <label for="entity_description">Description:</label>
                    <textarea id="entity_description" name="entity_description" rows="3"></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Save</button>
                <button type="button" class="btn btn-secondary" onclick="history.back()">Cancel</button>
            </form>
            <a href="/manage" class="back-link">← Back to Management</a>
        </div>
        <script>
            // Add form submission handler
        </script>
    </body>
    </html>
    """

# Add routes for Glossary CRUD
@app.route('/Glossary-of-Business-Terms/add', methods=['GET'])
def add_glossary_form():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Glossary Term</title>
        <style>
            /* Same styles as other forms */
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Add New Glossary Term</h2>
            <form id="glossaryForm">
                <div class="form-group">
                    <label for="business_term_short_name">Term Name:</label>
                    <input type="text" id="business_term_short_name" name="business_term_short_name" required>
                </div>
                <div class="form-group">
                    <label for="date_term_defined">Date Defined:</label>
                    <input type="date" id="date_term_defined" name="date_term_defined" required>
                </div>
                <button type="submit" class="btn btn-primary">Save</button>
                <button type="button" class="btn btn-secondary" onclick="history.back()">Cancel</button>
            </form>
            <a href="/manage" class="back-link">← Back to Management</a>
        </div>
        <script>
            // Add form submission handler
        </script>
    </body>
    </html>
    """

# Add routes for Source Systems CRUD
@app.route('/Source-Systems/add', methods=['GET'])
def add_source_system_form():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Source System</title>
        <style>
            /* Same styles as other forms */
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Add New Source System</h2>
            <form id="sourceSystemForm">
                <div class="form-group">
                    <label for="src_system_id">System ID:</label>
                    <input type="number" id="src_system_id" name="src_system_id" required>
                </div>
                <div class="form-group">
                    <label for="src_system_name">System Name:</label>
                    <input type="text" id="src_system_name" name="src_system_name" required>
                </div>
                <button type="submit" class="btn btn-primary">Save</button>
                <button type="button" class="btn btn-secondary" onclick="history.back()">Cancel</button>
            </form>
            <a href="/manage" class="back-link">← Back to Management</a>
        </div>
        <script>
            // Add form submission handler
        </script>
    </body>
    </html>
    """

# Add this common style for all edit forms
EDIT_FORM_STYLE = """
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin: 20px;
        background-color: #f5f5f5;
    }
    .container {
        max-width: 600px;
        margin: 0 auto;
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h2 {
        color: #007bff;
        margin-bottom: 20px;
    }
    .form-group {
        margin-bottom: 15px;
    }
    label {
        display: block;
        margin-bottom: 5px;
        color: #666;
    }
    input, select, textarea {
        width: 100%;
        padding: 8px;
        border: 1px solid #ddd;
        border-radius: 4px;
        box-sizing: border-box;
    }
    .btn {
        padding: 10px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
        margin-right: 10px;
    }
    .btn-primary {
        background-color: #007bff;
        color: white;
    }
    .btn-primary:hover {
        background-color: #0056b3;
    }
    .btn-secondary {
        background-color: #6c757d;
        color: white;
    }
    .btn-secondary:hover {
        background-color: #545b62;
    }
    .back-link {
        display: inline-block;
        margin-top: 20px;
        color: #007bff;
        text-decoration: none;
    }
    .back-link:hover {
        text-decoration: underline;
    }
    .nav-links {
        margin-bottom: 20px;
    }
    .nav-links a {
        color: #007bff;
        text-decoration: none;
        margin-right: 15px;
    }
    .nav-links a:hover {
        text-decoration: underline;
    }
    .error-message {
        color: #dc3545;
        margin-bottom: 10px;
        display: none;
    }
"""

@app.route('/Attribute/edit/<int:id>', methods=['GET'])
def edit_attribute_form(id):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM attribute WHERE attribute_id = %s
            """, (id,))
            attribute = cursor.fetchone()
            
        if not attribute:
            return "Attribute not found", 404
            
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Edit Attribute</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h2 {{
                    color: #007bff;
                    margin-bottom: 20px;
                }}
                .form-group {{
                    margin-bottom: 15px;
                }}
                label {{
                    display: block;
                    margin-bottom: 5px;
                    color: #666;
                }}
                input, select, textarea {{
                    width: 100%;
                    padding: 8px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    box-sizing: border-box;
                }}
                .btn {{
                    padding: 10px 20px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 14px;
                    margin-right: 10px;
                }}
                .btn-primary {{
                    background-color: #007bff;
                    color: white;
                }}
                .btn-primary:hover {{
                    background-color: #0056b3;
                }}
                .btn-secondary {{
                    background-color: #6c757d;
                    color: white;
                }}
                .btn-secondary:hover {{
                    background-color: #545b62;
                }}
                .back-link {{
                    display: inline-block;
                    margin-top: 20px;
                    color: #007bff;
                    text-decoration: none;
                }}
                .back-link:hover {{
                    text-decoration: underline;
                }}
                .nav-links {{
                    margin-bottom: 20px;
                }}
                .nav-links a {{
                    color: #007bff;
                    text-decoration: none;
                    margin-right: 15px;
                }}
                .nav-links a:hover {{
                    text-decoration: underline;
                }}
                .error-message {{
                    color: #dc3545;
                    margin-bottom: 10px;
                    display: none;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Edit Attribute</h2>
                <form id="editForm">
                    <div class="form-group">
                        <label for="attribute_name">Attribute Name:</label>
                        <input type="text" id="attribute_name" name="attribute_name" 
                               value="{attribute['attribute_name']}" required>
                    </div>
                    <div class="form-group">
                        <label for="attribute_datatype">Data Type:</label>
                        <select id="attribute_datatype" name="attribute_datatype" required>
                            <option value="VARCHAR" {"selected" if attribute['attribute_datatype'] == 'VARCHAR' else ""}>VARCHAR</option>
                            <option value="INT" {"selected" if attribute['attribute_datatype'] == 'INT' else ""}>INT</option>
                            <option value="DATE" {"selected" if attribute['attribute_datatype'] == 'DATE' else ""}>DATE</option>
                            <option value="DECIMAL" {"selected" if attribute['attribute_datatype'] == 'DECIMAL' else ""}>DECIMAL</option>
                            <option value="BOOLEAN" {"selected" if attribute['attribute_datatype'] == 'BOOLEAN' else ""}>BOOLEAN</option>
                            <option value="TEXT" {"selected" if attribute['attribute_datatype'] == 'TEXT' else ""}>TEXT</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="attribute_description">Description:</label>
                        <textarea id="attribute_description" name="attribute_description" 
                                  rows="3">{attribute['attribute_description'] or ''}</textarea>
                    </div>
                    <div class="form-group">
                        <label for="typical_values">Typical Values:</label>
                        <input type="text" id="typical_values" name="typical_values" 
                               value="{attribute['typical_values'] or ''}">
                    </div>
                    <div class="form-group">
                        <label for="validation_criteria">Validation Criteria:</label>
                        <input type="text" id="validation_criteria" name="validation_criteria" 
                               value="{attribute['validation_criteria'] or ''}">
                    </div>
                    <button type="submit" class="btn btn-primary">Save Changes</button>
                    <button type="button" class="btn btn-secondary" onclick="history.back()">Cancel</button>
                </form>
                <a href="/manage" class="back-link">← Back to Management</a>
            </div>

            <script>
                document.getElementById('editForm').addEventListener('submit', async (e) => {{
                    e.preventDefault();
                    const formData = new FormData(e.target);
                    const data = Object.fromEntries(formData);
                    const token = localStorage.getItem('token');
                    
                    try {{
                        const response = await fetch('/Attribute/{id}', {{
                            method: 'PUT',
                            headers: {{
                                'Content-Type': 'application/json',
                                'Authorization': `Bearer ${{token}}`
                            }},
                            body: JSON.stringify(data)
                        }});
                        
                        if (response.ok) {{
                            window.location.href = '/Attribute';
                        }} else {{
                            const error = await response.json();
                            alert(error.error || 'Failed to update attribute');
                        }}
                    }} catch (error) {{
                        alert('An error occurred. Please try again.');
                    }}
                }});
            </script>
        </body>
        </html>
        """
    except Exception as e:
        return f"Error: {str(e)}", 500
    finally:
        if connection:
            connection.close()

# Add edit form for Business Term Owner
@app.route('/Business-Term-Owner/edit/<string:code>', methods=['GET'])
def edit_business_term_owner_form(code):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM business_term_owner WHERE term_owner_code = %s
            """, (code,))
            owner = cursor.fetchone()
            
        if not owner:
            return "Business Term Owner not found", 404
            
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Edit Business Term Owner</title>
            <style>
                {EDIT_FORM_STYLE}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="nav-links">
                    <a href="/">Home</a>
                    <a href="/Business-Term-Owner">Back to Business Term Owners</a>
                    <a href="/manage">Management</a>
                </div>
                <h2>Edit Business Term Owner</h2>
                <p id="errorMessage" class="error-message"></p>
                <form id="editForm">
                    <div class="form-group">
                        <label for="term_owner_description">Description:</label>
                        <textarea id="term_owner_description" name="term_owner_description" 
                                rows="3" required>{owner['term_owner_description']}</textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Save Changes</button>
                    <button type="button" class="btn btn-secondary" onclick="history.back()">Cancel</button>
                </form>
                <a href="/manage" class="back-link">← Back to Management</a>
            </div>

            <script>
                document.getElementById('editForm').addEventListener('submit', async (e) => {{
                    e.preventDefault();
                    const formData = new FormData(e.target);
                    const data = Object.fromEntries(formData);
                    const token = localStorage.getItem('token');
                    
                    try {{
                        const response = await fetch('/Business-Term-Owner/{code}', {{
                            method: 'PUT',
                            headers: {{
                                'Content-Type': 'application/json',
                                'Authorization': `Bearer ${{token}}`
                            }},
                            body: JSON.stringify(data)
                        }});
                        
                        if (response.ok) {{
                            window.location.href = '/Business-Term-Owner';
                        }} else {{
                            const error = await response.json();
                            alert(error.error || 'Failed to update business term owner');
                        }}
                    }} catch (error) {{
                        alert('An error occurred. Please try again.');
                    }}
                }});
            </script>
        </body>
        </html>
        """
    except Exception as e:
        return f"Error: {str(e)}", 500
    finally:
        if connection:
            connection.close()

# Add edit form for Entity
@app.route('/Entity/edit/<int:id>', methods=['GET'])
def edit_entity_form(id):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM entity WHERE entity_id = %s
            """, (id,))
            entity = cursor.fetchone()
            
        if not entity:
            return "Entity not found", 404
            
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Edit Entity</title>
            <style>
                {EDIT_FORM_STYLE}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="nav-links">
                    <a href="/">Home</a>
                    <a href="/Entity">Back to Entities</a>
                    <a href="/manage">Management</a>
                </div>
                <h2>Edit Entity</h2>
                <p id="errorMessage" class="error-message"></p>
                <form id="editForm">
                    <div class="form-group">
                        <label for="entity_name">Entity Name:</label>
                        <input type="text" id="entity_name" name="entity_name" 
                               value="{entity['entity_name']}" required>
                    </div>
                    <div class="form-group">
                        <label for="entity_description">Description:</label>
                        <textarea id="entity_description" name="entity_description" 
                                rows="3">{entity['entity_description'] or ''}</textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Save Changes</button>
                    <button type="button" class="btn btn-secondary" onclick="history.back()">Cancel</button>
                </form>
                <a href="/manage" class="back-link">← Back to Management</a>
            </div>
        </body>
        </html>
        """
    except Exception as e:
        return f"Error: {str(e)}", 500
    finally:
        if connection:
            connection.close()

# Add edit form for Glossary Terms
@app.route('/Glossary-of-Business-Terms/edit/<string:name>', methods=['GET'])
def edit_glossary_term_form(name):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM glossary_of_business_terms WHERE business_term_short_name = %s
            """, (name,))
            term = cursor.fetchone()
            
        if not term:
            return "Glossary Term not found", 404
            
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Edit Glossary Term</title>
            <style>
                {EDIT_FORM_STYLE}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="nav-links">
                    <a href="/">Home</a>
                    <a href="/Glossary-of-Business-Terms">Back to Glossary Terms</a>
                    <a href="/manage">Management</a>
                </div>
                <h2>Edit Glossary Term</h2>
                <p id="errorMessage" class="error-message"></p>
                <form id="editForm">
                    <div class="form-group">
                        <label for="business_term_short_name">Term Name:</label>
                        <input type="text" id="business_term_short_name" name="business_term_short_name" 
                               value="{term['business_term_short_name']}" readonly>
                    </div>
                    <div class="form-group">
                        <label for="date_term_defined">Date Defined:</label>
                        <input type="date" id="date_term_defined" name="date_term_defined" 
                               value="{term['date_term_defined'].strftime('%Y-%m-%d')}" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Save Changes</button>
                    <button type="button" class="btn btn-secondary" onclick="history.back()">Cancel</button>
                </form>
                <a href="/manage" class="back-link">← Back to Management</a>
            </div>

            <script>
                document.getElementById('editForm').addEventListener('submit', async (e) => {{
                    e.preventDefault();
                    const formData = new FormData(e.target);
                    const data = Object.fromEntries(formData);
                    const token = localStorage.getItem('token');
                    
                    try {{
                        const response = await fetch('/Glossary-of-Business-Terms/{name}', {{
                            method: 'PUT',
                            headers: {{
                                'Content-Type': 'application/json',
                                'Authorization': `Bearer ${{token}}`
                            }},
                            body: JSON.stringify(data)
                        }});
                        
                        if (response.ok) {{
                            window.location.href = '/Glossary-of-Business-Terms';
                        }} else {{
                            const error = await response.json();
                            alert(error.error || 'Failed to update glossary term');
                        }}
                    }} catch (error) {{
                        alert('An error occurred. Please try again.');
                    }}
                }});
            </script>
        </body>
        </html>
        """
    except Exception as e:
        return f"Error: {str(e)}", 500
    finally:
        if connection:
            connection.close()

# Add edit form for Source Systems
@app.route('/Source-Systems/edit/<int:id>', methods=['GET'])
def edit_source_system_form(id):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM source_systems WHERE src_system_id = %s
            """, (id,))
            system = cursor.fetchone()
            
        if not system:
            return "Source System not found", 404
            
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Edit Source System</title>
            <style>
                {EDIT_FORM_STYLE}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="nav-links">
                    <a href="/">Home</a>
                    <a href="/Source-Systems">Back to Source Systems</a>
                    <a href="/manage">Management</a>
                </div>
                <h2>Edit Source System</h2>
                <p id="errorMessage" class="error-message"></p>
                <form id="editForm">
                    <div class="form-group">
                        <label for="src_system_id">System ID:</label>
                        <input type="number" id="src_system_id" name="src_system_id" 
                               value="{system['src_system_id']}" readonly>
                    </div>
                    <div class="form-group">
                        <label for="src_system_name">System Name:</label>
                        <input type="text" id="src_system_name" name="src_system_name" 
                               value="{system['src_system_name']}" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Save Changes</button>
                    <button type="button" class="btn btn-secondary" onclick="history.back()">Cancel</button>
                </form>
                <a href="/manage" class="back-link">← Back to Management</a>
            </div>

            <script>
                document.getElementById('editForm').addEventListener('submit', async (e) => {{
                    e.preventDefault();
                    const formData = new FormData(e.target);
                    const data = Object.fromEntries(formData);
                    const token = localStorage.getItem('token');
                    
                    try {{
                        const response = await fetch('/Source-Systems/{id}', {{
                            method: 'PUT',
                            headers: {{
                                'Content-Type': 'application/json',
                                'Authorization': `Bearer ${{token}}`
                            }},
                            body: JSON.stringify(data)
                        }});
                        
                        if (response.ok) {{
                            window.location.href = '/Source-Systems';
                        }} else {{
                            const error = await response.json();
                            alert(error.error || 'Failed to update source system');
                        }}
                    }} catch (error) {{
                        alert('An error occurred. Please try again.');
                    }}
                }});
            </script>
        </body>
        </html>
        """
    except Exception as e:
        return f"Error: {str(e)}", 500
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)




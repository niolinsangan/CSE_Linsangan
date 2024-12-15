from flask import Flask, jsonify, request
import pymysql
from datetime import datetime, timedelta, timezone
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
            'exp': datetime.now(timezone.utc) + timedelta(hours=1)
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
            return jsonify({'error': 'No token provided'}), 401
        
        try:
            token = token.split(" ")[1]  # Remove 'Bearer ' prefix
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user = decoded_token
            return f(*args, **kwargs)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, IndexError):
            return jsonify({'error': 'Invalid token'}), 401
            
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
        'created_at': datetime.now(timezone.utc)
    },
    'user': {
        'password': 'user123',
        'role': 'user',
        'user_id': 2,
        'email': 'user@example.com',
        'created_at': datetime.now(timezone.utc)
    },
    'manager': {
        'password': 'manager123',
        'role': 'manager',
        'user_id': 3,
        'email': 'manager@example.com',
        'created_at': datetime.now(timezone.utc)
    },
    'analyst': {
        'password': 'analyst123',
        'role': 'analyst',
        'user_id': 4,
        'email': 'analyst@example.com',
        'created_at': datetime.now(timezone.utc)
    },
    'viewer': {
        'password': 'viewer123',
        'role': 'viewer',
        'user_id': 5,
        'email': 'viewer@example.com',
        'created_at': datetime.now(timezone.utc)
    }
}

# Ensure default admin credentials are present
if 'admin' not in users:
    users['admin'] = {
        'password': 'admin123',
        'role': 'admin',
        'user_id': 1,
        'email': 'admin@example.com',
        'created_at': datetime.now(timezone.utc)
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

# Add this function to handle database operations
def execute_query(query, params=None, fetch=False):
    """
    Executes a SQL query with optional parameters
    Args:
        query: SQL query string
        params: Tuple of parameters for the query
        fetch: Boolean indicating whether to fetch results
    Returns:
        List of results if fetch is True, otherwise None
    """
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            connection.commit()
    except Exception as e:
        print(f"Database error: {e}")  # Debug print
        if connection:
            connection.rollback()
        raise
    finally:
        if connection:
            connection.close()

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
            
            if not username or not password:
                return jsonify({'error': 'Username and password are required'}), 401
            
            if username not in users:
                print(f"User {username} not found")  # Debug print
                return jsonify({'error': f'User "{username}" does not exist'}), 401
            
            print(f"User found, stored password: {users[username]['password']}")  # Debug print
            if users[username]['password'] != password:
                print("Password doesn't match")  # Debug print
                return jsonify({'error': 'Incorrect password'}), 401
            
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
            
        except Exception as e:
            print(f"Login error: {str(e)}")  # Debug print
            return jsonify({'error': 'An error occurred during login. Please try again.'}), 500

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
            .auth-buttons {
                display: flex;
                gap: 10px;
            }
            .auth-buttons a, .auth-buttons button {
                color: white;
                text-decoration: none;
                padding: 5px 10px;
                border-radius: 4px;
                transition: background-color 0.3s;
                border: none;
                cursor: pointer;
                font-size: 14px;
            }
            .login-btn {
                background-color: rgba(255,255,255,0.1);
            }
            .logout-btn {
                background-color: #dc3545;
                display: none;  /* Hidden by default */
            }
            .auth-buttons a:hover, .auth-buttons button:hover {
                background-color: rgba(255,255,255,0.2);
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
                    <a href="/manage">Data Management</a>
                    <div class="auth-buttons">
                        <a href="/login" id="loginBtn" class="login-btn">Login</a>
                        <button id="logoutBtn" class="logout-btn" onclick="logout()">Logout</button>
                    </div>
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
        <script>
            // Check if user is logged in
            const token = localStorage.getItem('token');
            const loginBtn = document.getElementById('loginBtn');
            const logoutBtn = document.getElementById('logoutBtn');
            
            if (token) {
                loginBtn.style.display = 'none';
                logoutBtn.style.display = 'block';
            } else {
                loginBtn.style.display = 'block';
                logoutBtn.style.display = 'none';
            }

            // Logout function
            function logout() {
                localStorage.removeItem('token');
                alert('You have been logged out.');
                window.location.reload();
            }
        </script>
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
            .table-container {{
                max-height: 600px;
                overflow-y: auto;
                margin-bottom: 20px;
                border: 1px solid #dee2e6;
                border-radius: 4px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 0;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #007bff;
                color: white;
                position: sticky;
                top: 0;
                z-index: 10;
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
                display: none;
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
            .auth-section {{
                text-align: right;
                margin-bottom: 20px;
            }}
            .btn-login {{
                background-color: #007bff;
                color: white;
            }}
            .btn-logout {{
                background-color: #6c757d;
                color: white;
            }}
            .action-column {{
                display: none;
            }}
            .pagination {{
                display: flex;
                justify-content: center;
                align-items: center;
                margin-top: 20px;
                gap: 10px;
            }}
            .pagination button {{
                padding: 8px 12px;
                border: 1px solid #007bff;
                background-color: white;
                color: #007bff;
                border-radius: 4px;
                cursor: pointer;
            }}
            .pagination button:disabled {{
                border-color: #ccc;
                color: #ccc;
                cursor: not-allowed;
            }}
            .pagination button.active {{
                background-color: #007bff;
                color: white;
            }}
            .pagination-info {{
                margin: 0 15px;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="auth-section">
                <span id="userInfo"></span>
                <button id="loginBtn" class="btn btn-login" onclick="location.href='/login'" style="display: none;">Login to Edit</button>
                <button id="logoutBtn" class="btn btn-logout" onclick="logout()" style="display: none;">Logout</button>
            </div>
            <h2>{title}</h2>
            <div id="crud-buttons" class="crud-buttons">
                <button class="btn btn-add" onclick="location.href='{get_add_url(title)}'">Add New</button>
            </div>

            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            {''.join(f'<th>{header}</th>' for header in headers)}
                            <th class="action-column">Actions</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody">
                        {''.join(
                            f"<tr>"
                            f"{''.join(f'<td>{str(value)}</td>' for value in row.values())}"
                            f"<td class='action-column'>"
                            f"<button class='btn btn-edit' onclick='editRecord({json.dumps(row)})'>Edit</button>"
                            f"<button class='btn btn-delete' onclick='showDeleteModal({json.dumps(row[primary_key])})'>Delete</button>"
                            f"</td>"
                            f"</tr>"
                            for row in data
                        )}
                    </tbody>
                </table>
            </div>

            <div class="pagination">
                <button onclick="previousPage()" id="prevButton">Previous</button>
                <span class="pagination-info">
                    Page <span id="currentPage">1</span> of <span id="totalPages">1</span>
                </span>
                <button onclick="nextPage()" id="nextButton">Next</button>
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
            const token = localStorage.getItem('token');
            const loginBtn = document.getElementById('loginBtn');
            const logoutBtn = document.getElementById('logoutBtn');
            const crudButtons = document.getElementById('crud-buttons');
            const actionColumns = document.getElementsByClassName('action-column');
            const deleteModal = document.getElementById('deleteModal');
            
            // Pagination variables
            const rowsPerPage = 5;
            const rows = Array.from(document.getElementById('tableBody').getElementsByTagName('tr'));
            let currentPage = 1;
            const totalPages = Math.ceil(rows.length / rowsPerPage);
            
            document.getElementById('totalPages').textContent = totalPages;

            // Function to show rows for current page
            function showPage(page) {{
                const start = (page - 1) * rowsPerPage;
                const end = start + rowsPerPage;
                
                rows.forEach((row, index) => {{
                    row.style.display = (index >= start && index < end) ? '' : 'none';
                }});
                
                document.getElementById('currentPage').textContent = page;
                document.getElementById('prevButton').disabled = page === 1;
                document.getElementById('nextButton').disabled = page === totalPages;
            }}

            function previousPage() {{
                if (currentPage > 1) {{
                    currentPage--;
                    showPage(currentPage);
                }}
            }}

            function nextPage() {{
                if (currentPage < totalPages) {{
                    currentPage++;
                    showPage(currentPage);
                }}
            }}

            // Initialize first page
            showPage(1);

            // Check authentication status
            if (token) {{
                // Show edit controls for authenticated users
                logoutBtn.style.display = 'inline-block';
                crudButtons.style.display = 'block';
                for (let col of actionColumns) {{
                    col.style.display = 'table-cell';
                }}
            }} else {{
                // Show login button for unauthenticated users
                loginBtn.style.display = 'inline-block';
            }}

            // Function to log out the user
            function logout() {{
                localStorage.removeItem('token'); // Remove the token from local storage
                alert('You have been logged out.');
                window.location.href = '/login';  // Redirect to login page
            }}

            // Attach the logout function to the logout button
            document.getElementById('logoutBtn').addEventListener('click', logout);

            // Function to show the delete modal
            function showDeleteModal(id) {{
                if (!token) return;
                recordToDelete = id;
                deleteModal.style.display = 'block';
            }}

            // Function to hide the delete modal
            function hideDeleteModal() {{
                deleteModal.style.display = 'none';
                recordToDelete = null;
            }}

            // Function to confirm deletion
            function confirmDelete() {{
                if (!token || recordToDelete === null) return;

                fetch(window.location.pathname + '/' + recordToDelete, {{
                    method: 'DELETE',
                    headers: {{
                        'Authorization': 'Bearer ' + token
                    }}
                }})
                .then(response => {{
                    if (response.status === 401) {{
                        // Token is invalid or expired, log out the user
                        localStorage.removeItem('token');
                        alert('Session expired. Please log in again.');
                        location.reload();
                        return;
                    }}
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
                if (!token) return;
                const url = window.location.pathname + '/edit/' + record['{primary_key}'];
                window.location.href = url;
            }}

            // Close the modal when clicking outside of it
            window.onclick = function(event) {{
                if (event.target === deleteModal) {{
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
    if request.headers.get('Accept') == 'application/json':
        try:
            attributes = execute_query("SELECT * FROM attribute", fetch=True)
            return jsonify(attributes), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return create_api_table_view("Attributes")

@app.route('/Business-Term-Owner', methods=['GET'])
def get_business_term_owners():
    if request.headers.get('Accept') == 'application/json':
        try:
            owners = execute_query("SELECT * FROM business_term_owner", fetch=True)
            return jsonify(owners), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return create_api_table_view("Business Term Owners")

@app.route('/Entity', methods=['GET'])
def get_entities():
    if request.headers.get('Accept') == 'application/json':
        try:
            entities = execute_query("SELECT * FROM entity", fetch=True)
            return jsonify(entities), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return create_api_table_view("Entities")

@app.route('/Glossary-of-Business-Terms', methods=['GET'])
def get_glossary():
    if request.headers.get('Accept') == 'application/json':
        try:
            terms = execute_query("""
                SELECT business_term_short_name, 
                       DATE_FORMAT(date_term_defined, '%Y-%m-%d') as date_term_defined 
                FROM glossary_of_business_terms
            """, fetch=True)
            return jsonify(terms), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return create_api_table_view("Glossary of Business Terms")

@app.route('/Source-Systems', methods=['GET'])
def get_source_systems():
    if request.headers.get('Accept') == 'application/json':
        try:
            systems = execute_query("SELECT * FROM source_systems", fetch=True)
            return jsonify(systems), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return create_api_table_view("Source Systems")

# Remove @jwt_required from these routes
@app.route('/Attribute', methods=['POST'])
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
        execute_query("""
            INSERT INTO attribute (attribute_id, attribute_name, attribute_datatype, 
                                   attribute_description, typical_values, validation_criteria)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (data['attribute_id'], data['attribute_name'], data['attribute_datatype'],
              data.get('attribute_description'), data.get('typical_values'),
              data.get('validation_criteria')))
        return jsonify({'message': 'Attribute added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/Attribute/<int:id>', methods=['PUT'])
def update_attribute(id):
    data = request.json
    try:
        result = execute_query("SELECT * FROM attribute WHERE attribute_id = %s", (id,), fetch=True)
        if not result:
            return jsonify({'error': 'Attribute not found'}), 404
        
        execute_query("""
            UPDATE attribute 
            SET attribute_name = %s, attribute_datatype = %s,
                attribute_description = %s, typical_values = %s,
                validation_criteria = %s
            WHERE attribute_id = %s
        """, (data['attribute_name'], data['attribute_datatype'],
              data.get('attribute_description'), data.get('typical_values'),
              data.get('validation_criteria'), id))
        return jsonify({'message': 'Attribute updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/Attribute/<int:id>', methods=['DELETE'])
def delete_attribute(id):
    try:
        result = execute_query("SELECT * FROM attribute WHERE attribute_id = %s", (id,), fetch=True)
        if not result:
            return jsonify({'error': 'Attribute not found'}), 404
        
        execute_query("DELETE FROM attribute WHERE attribute_id = %s", (id,))
        return jsonify({'message': 'Attribute deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===================================
# BUSINESS TERM OWNER CRUD OPERATIONS
# ===================================
@app.route('/Business-Term-Owner', methods=['POST'])
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
        execute_query("""
            INSERT INTO business_term_owner (term_owner_code, term_owner_description)
            VALUES (%s, %s)
        """, (data['term_owner_code'], data['term_owner_description']))
        return jsonify({'message': 'Business Term Owner added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/Business-Term-Owner/<string:code>', methods=['PUT'])
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
        result = execute_query("SELECT * FROM business_term_owner WHERE term_owner_code = %s", (code,), fetch=True)
        if not result:
            return jsonify({'error': 'Business Term Owner not found'}), 404
        
        execute_query("""
            UPDATE business_term_owner 
            SET term_owner_description = %s
            WHERE term_owner_code = %s
        """, (data['term_owner_description'], code))
        return jsonify({'message': 'Business Term Owner updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/Business-Term-Owner/<string:code>', methods=['DELETE'])
def delete_business_term_owner(code):
    try:
        result = execute_query("SELECT * FROM business_term_owner WHERE term_owner_code = %s", (code,), fetch=True)
        if not result:
            return jsonify({'error': 'Business Term Owner not found'}), 404
        
        execute_query("DELETE FROM business_term_owner WHERE term_owner_code = %s", (code,))
        return jsonify({'message': 'Business Term Owner deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===================================
# ENTITY CRUD OPERATIONS
# ===================================
@app.route('/Entity', methods=['POST'])
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
        execute_query("""
            INSERT INTO entity (entity_id, entity_name, entity_description)
            VALUES (%s, %s, %s)
        """, (data['entity_id'], data['entity_name'], data.get('entity_description')))
        return jsonify({'message': 'Entity added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/Entity/<int:id>', methods=['PUT'])
def update_entity(id):
    """
    Updates an existing entity
    """
    data = request.json
    try:
        result = execute_query("SELECT * FROM entity WHERE entity_id = %s", (id,), fetch=True)
        if not result:
            return jsonify({'error': 'Entity not found'}), 404
        
        execute_query("""
            UPDATE entity 
            SET entity_name = %s, entity_description = %s
            WHERE entity_id = %s
        """, (data['entity_name'], data.get('entity_description'), id))
        return jsonify({'message': 'Entity updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/Entity/<int:id>', methods=['DELETE'])
def delete_entity(id):
    try:
        result = execute_query("SELECT * FROM entity WHERE entity_id = %s", (id,), fetch=True)
        if not result:
            return jsonify({'error': 'Entity not found'}), 404
        
        execute_query("DELETE FROM entity WHERE entity_id = %s", (id,))
        return jsonify({'message': 'Entity deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===================================
# GLOSSARY CRUD OPERATIONS
# ===================================
@app.route('/Glossary-of-Business-Terms', methods=['POST'])
def add_glossary_term():
    """
    Adds a new glossary term to database
    """
    data = request.json
    try:
        execute_query("""
            INSERT INTO glossary_of_business_terms 
            (business_term_short_name, date_term_defined)
            VALUES (%s, STR_TO_DATE(%s, '%Y-%m-%d'))
        """, (data['business_term_short_name'], data['date_term_defined']))
        return jsonify({'message': 'Term added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/Glossary-of-Business-Terms/<string:name>', methods=['PUT'])
def update_glossary_term(name):
    """
    Updates an existing glossary term
    """
    data = request.json
    try:
        result = execute_query("SELECT * FROM glossary_of_business_terms WHERE business_term_short_name = %s", (name,), fetch=True)
        if not result:
            return jsonify({'error': 'Glossary Term not found'}), 404
        
        execute_query("""
            UPDATE glossary_of_business_terms 
            SET date_term_defined = STR_TO_DATE(%s, '%Y-%m-%d')
            WHERE business_term_short_name = %s
        """, (data['date_term_defined'], name))
        return jsonify({'message': 'Term updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/Glossary-of-Business-Terms/<string:name>', methods=['DELETE'])
def delete_glossary_term(name):
    try:
        result = execute_query("SELECT * FROM glossary_of_business_terms WHERE business_term_short_name = %s", (name,), fetch=True)
        if not result:
            return jsonify({'error': 'Glossary Term not found'}), 404
        
        execute_query("DELETE FROM glossary_of_business_terms WHERE business_term_short_name = %s", (name,))
        return jsonify({'message': 'Glossary Term deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===================================
# SOURCE SYSTEMS CRUD OPERATIONS
# ===================================
@app.route('/Source-Systems', methods=['POST'])
def add_source_system():
    """
    Adds a new source system to database
    """
    data = request.json
    try:
        execute_query("""
            INSERT INTO source_systems 
            (src_system_id, src_system_name)
            VALUES (%s, %s)
        """, (data['src_system_id'], data['src_system_name']))
        return jsonify({'message': 'Source system added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
            #errorMessage {
                color: #dc3545;
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                padding: 10px;
                margin-bottom: 15px;
                border-radius: 4px;
                display: none;
                text-align: center;
            }
            .shake {
                animation: shake 0.5s;
            }
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
                20%, 40%, 60%, 80% { transform: translateX(5px); }
            }
            .logged-in-message {
                text-align: center;
                margin-top: 20px;
                color: #28a745;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <h2>Login Required</h2>
            <div id="errorMessage"></div>
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
            <div id="loggedInMessage" class="logged-in-message" style="display: none;">
                You are already logged in.
            </div>
        </div>
        <script>
            const token = localStorage.getItem('token');
            const loggedInMessage = document.getElementById('loggedInMessage');
            const loginForm = document.getElementById('loginForm');

            if (token) {
                loggedInMessage.style.display = 'block';
                loginForm.style.display = 'none';
            }

            loginForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const errorMessage = document.getElementById('errorMessage');
                errorMessage.style.display = 'none';
                
                try {
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
                    
                    if (response.ok && data.token) {
                        localStorage.setItem('token', data.token);
                        if (document.referrer && !document.referrer.includes('/login')) {
                            window.location.href = document.referrer;
                        } else {
                            window.location.href = '/';
                        }
                    } else {
                        errorMessage.textContent = data.error || 'Login failed';
                        errorMessage.style.display = 'block';
                        loginForm.classList.add('shake');
                        setTimeout(() => loginForm.classList.remove('shake'), 500);
                        
                        // Clear password field on error
                        document.getElementById('password').value = '';
                        document.getElementById('password').focus();
                    }
                } catch (error) {
                    errorMessage.textContent = 'An error occurred. Please try again.';
                    errorMessage.style.display = 'block';
                    loginForm.classList.add('shake');
                    setTimeout(() => loginForm.classList.remove('shake'), 500);
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

#
# Add these routes for CRUD operations
@app.route('/Attribute/add', methods=['GET'])
def add_attribute_form():
    return create_add_form("Attribute")

@app.route('/Business-Term-Owner/add', methods=['GET'])
def add_business_term_owner_form():
    return create_add_form("Business-Term-Owner")

@app.route('/Entity/add', methods=['GET'])
def add_entity_form():
    return create_add_form("Entity")

@app.route('/Glossary-of-Business-Terms/add', methods=['GET'])
def add_glossary_term_form():
    return create_add_form("Glossary-of-Business-Terms")

@app.route('/Source-Systems/add', methods=['GET'])
def add_source_system_form():
    return create_add_form("Source-Systems")

# Add these common style for all edit forms
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
                        const response = await fetch('/Attribute/' + id, {{
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

def create_api_table_view(title):
    """
    Creates an HTML template that will fetch and display JSON data
    """
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
            .table-container {{
                overflow-x: auto;
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
            .loading {{
                text-align: center;
                padding: 20px;
            }}
            .error {{
                color: #dc3545;
                padding: 20px;
                text-align: center;
            }}
            .header-actions {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }}
            .logout-btn {{
                padding: 8px 16px;
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                display: none;  /* Hidden by default */
            }}
            .logout-btn:hover {{
                background-color: #c82333;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header-actions">
                <h2>{title}</h2>
                <button id="logoutBtn" class="logout-btn" onclick="logout()">Logout</button>
            </div>
            <div class="table-container">
                <div id="loading" class="loading">Loading...</div>
                <div id="error" class="error" style="display: none;"></div>
                <table id="dataTable" style="display: none;">
                    <thead>
                        <tr id="headerRow"></tr>
                    </thead>
                    <tbody id="tableBody"></tbody>
                </table>
            </div>
            <a href="/" class="back-link">← Back to Home</a>
        </div>

        <script>
            // Check if user is logged in
            const token = localStorage.getItem('token');
            const logoutBtn = document.getElementById('logoutBtn');
            
            if (token) {{
                logoutBtn.style.display = 'block';  // Show logout button if token exists
            }}

            // Logout function
            function logout() {{
                localStorage.removeItem('token');
                alert('You have been logged out.');
                window.location.href = '/login';
            }}

            // Fetch data from the API with Accept header
            fetch(window.location.pathname, {{
                headers: {{
                    'Accept': 'application/json'
                }}
            }})
            .then(response => response.json())
            .then(data => {{
                const table = document.getElementById('dataTable');
                const headerRow = document.getElementById('headerRow');
                const tableBody = document.getElementById('tableBody');
                const loading = document.getElementById('loading');
                
                if (data.length > 0) {{
                    // Create headers
                    Object.keys(data[0]).forEach(key => {{
                        const th = document.createElement('th');
                        th.textContent = key.replace(/_/g, ' ').toUpperCase();
                        headerRow.appendChild(th);
                    }});

                    // Create rows
                    data.forEach(item => {{
                        const row = document.createElement('tr');
                        Object.values(item).forEach(value => {{
                            const td = document.createElement('td');
                            td.textContent = value;
                            row.appendChild(td);
                        }});
                        tableBody.appendChild(row);
                    }});

                    loading.style.display = 'none';
                    table.style.display = 'table';
                }} else {{
                    loading.textContent = 'No data available.';
                }}
            }})
            .catch(error => {{
                const errorDiv = document.getElementById('error');
                const loading = document.getElementById('loading');
                loading.style.display = 'none';
                errorDiv.style.display = 'block';
                errorDiv.textContent = 'Error loading data: ' + error.message;
            }});
        </script>
    </body>
    </html>
    """

@app.route('/some_protected_route', methods=['GET'])
def some_protected_route():
    token = request.headers.get('Authorization')
    if not token or not validate_token(token):
        return jsonify({'error': 'Unauthorized'}), 401
    # Proceed with the rest of the logic

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
                margin: 20px;
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
            .controls {
                margin-bottom: 20px;
                display: flex;
                gap: 10px;
                align-items: center;
            }
            select, button {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #ddd;
            }
            button {
                background-color: #007bff;
                color: white;
                border: none;
                cursor: pointer;
            }
            button:hover {
                background-color: #0056b3;
            }
            .table-container {
                overflow-x: auto;
                margin-top: 20px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #007bff;
                color: white;
            }
            tr:nth-child(even) {
                background-color: #f8f9fa;
            }
            .action-buttons {
                display: flex;
                gap: 5px;
            }
            .edit-btn {
                background-color: #ffc107;
                color: black;
            }
            .delete-btn {
                background-color: #dc3545;
                color: white;
            }
            .back-link {
                display: inline-block;
                margin-top: 20px;
                color: #007bff;
                text-decoration: none;
            }
            .action-buttons button {
                padding: 5px 10px;
                margin: 0 2px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            .edit-btn {
                background-color: #ffc107;
                color: black;
            }
            .delete-btn {
                background-color: #dc3545;
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Data Management</h2>
            <div class="controls">
                <select id="tableSelect" onchange="loadTableData()">
                    <option value="">Select a table</option>
                    <option value="Attribute">Attributes</option>
                    <option value="Business-Term-Owner">Business Term Owners</option>
                    <option value="Entity">Entities</option>
                    <option value="Glossary-of-Business-Terms">Glossary Terms</option>
                    <option value="Source-Systems">Source Systems</option>
                </select>
                <button onclick="addNew()">Add New</button>
            </div>
            <div class="table-container">
                <table id="dataTable">
                    <thead>
                        <tr id="headerRow"></tr>
                    </thead>
                    <tbody id="tableBody"></tbody>
                </table>
            </div>
            <a href="/" class="back-link">← Back to Home</a>
        </div>

        <script>
            const tableSelect = document.getElementById('tableSelect');
            const dataTable = document.getElementById('dataTable');
            const headerRow = document.getElementById('headerRow');
            const tableBody = document.getElementById('tableBody');

            function editItem(table, item) {
                // Get the primary key value based on the table
                let id;
                switch(table) {
                    case 'Attribute':
                        id = item.attribute_id;
                        break;
                    case 'Business-Term-Owner':
                        id = item.term_owner_code;
                        break;
                    case 'Entity':
                        id = item.entity_id;
                        break;
                    case 'Glossary-of-Business-Terms':
                        id = item.business_term_short_name;
                        break;
                    case 'Source-Systems':
                        id = item.src_system_id;
                        break;
                    default:
                        console.error('Unknown table:', table);
                        return;
                }

                window.location.href = `/${table}/edit/${id}`;
            }

            function deleteItem(table, item) {
                if (!confirm('Are you sure you want to delete this item?')) return;

                // Get the primary key value based on the table
                let id;
                switch(table) {
                    case 'Attribute':
                        id = item.attribute_id;
                        break;
                    case 'Business-Term-Owner':
                        id = item.term_owner_code;
                        break;
                    case 'Entity':
                        id = item.entity_id;
                        break;
                    case 'Glossary-of-Business-Terms':
                        id = item.business_term_short_name;
                        break;
                    case 'Source-Systems':
                        id = item.src_system_id;
                        break;
                    default:
                        console.error('Unknown table:', table);
                        return;
                }

                fetch(`/${table}/${id}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    }
                })
                .then(response => {
                    if (response.ok) {
                        loadTableData(); // Reload the table after successful deletion
                        alert('Item deleted successfully');
                    } else {
                        return response.json().then(data => {
                            throw new Error(data.error || 'Failed to delete item');
                        });
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert(error.message || 'Error deleting item');
                });
            }

            // Update loadTableData to include action buttons
            function loadTableData() {
                const selectedTable = tableSelect.value;
                if (!selectedTable) {
                    headerRow.innerHTML = '';
                    tableBody.innerHTML = '';
                    return;
                }

                fetch('/' + selectedTable, {
                    headers: {
                        'Accept': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    headerRow.innerHTML = '';
                    tableBody.innerHTML = '';

                    if (data.length > 0) {
                        // Add headers
                        Object.keys(data[0]).forEach(key => {
                            const th = document.createElement('th');
                            th.textContent = key.replace(/_/g, ' ').toUpperCase();
                            headerRow.appendChild(th);
                        });

                        // Add actions header
                        const actionsHeader = document.createElement('th');
                        actionsHeader.textContent = 'ACTIONS';
                        headerRow.appendChild(actionsHeader);

                        // Add rows
                        data.forEach(item => {
                            const row = document.createElement('tr');
                            
                            // Add data cells
                            Object.values(item).forEach(value => {
                                const td = document.createElement('td');
                                td.textContent = value;
                                row.appendChild(td);
                            });
                            
                            // Add action buttons
                            const actionsTd = document.createElement('td');
                            actionsTd.className = 'action-buttons';
                            
                            const editBtn = document.createElement('button');
                            editBtn.className = 'edit-btn';
                            editBtn.textContent = 'Edit';
                            editBtn.onclick = () => editItem(selectedTable, item);
                            
                            const deleteBtn = document.createElement('button');
                            deleteBtn.className = 'delete-btn';
                            deleteBtn.textContent = 'Delete';
                            deleteBtn.onclick = () => deleteItem(selectedTable, item);
                            
                            actionsTd.appendChild(editBtn);
                            actionsTd.appendChild(deleteBtn);
                            row.appendChild(actionsTd);
                            
                            tableBody.appendChild(row);
                        });

                        dataTable.style.display = 'table';
                    } else {
                        tableBody.innerHTML = '<tr><td colspan="100%">No data available</td></tr>';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    tableBody.innerHTML = '<tr><td colspan="100%">Error loading data</td></tr>';
                });
            }

            function addNew() {
                const selectedTable = tableSelect.value;
                if (!selectedTable) {
                    alert('Please select a table first');
                    return;
                }
                window.location.href = '/' + selectedTable + '/add';
            }
        </script>
    </body>
    </html>
    """

def create_add_form(table_type):
    """
    Creates an HTML form for adding new records based on table type
    """
    form_fields = {
        'Attribute': [
            {'name': 'attribute_id', 'type': 'number', 'label': 'Attribute ID'},
            {'name': 'attribute_name', 'type': 'text', 'label': 'Attribute Name'},
            {'name': 'attribute_datatype', 'type': 'text', 'label': 'Data Type'},
            {'name': 'attribute_description', 'type': 'text', 'label': 'Description'},
            {'name': 'typical_values', 'type': 'text', 'label': 'Typical Values'},
            {'name': 'validation_criteria', 'type': 'text', 'label': 'Validation Criteria'}
        ],
        'Business-Term-Owner': [
            {'name': 'term_owner_code', 'type': 'text', 'label': 'Owner Code'},
            {'name': 'term_owner_description', 'type': 'text', 'label': 'Description'}
        ],
        'Entity': [
            {'name': 'entity_id', 'type': 'number', 'label': 'Entity ID'},
            {'name': 'entity_name', 'type': 'text', 'label': 'Entity Name'},
            {'name': 'entity_description', 'type': 'text', 'label': 'Description'}
        ],
        'Glossary-of-Business-Terms': [
            {'name': 'business_term_short_name', 'type': 'text', 'label': 'Term Name'},
            {'name': 'date_term_defined', 'type': 'date', 'label': 'Date Defined'}
        ],
        'Source-Systems': [
            {'name': 'src_system_id', 'type': 'number', 'label': 'System ID'},
            {'name': 'src_system_name', 'type': 'text', 'label': 'System Name'}
        ]
    }

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add {table_type}</title>
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
            input, select {{
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                box-sizing: border-box;
            }}
            button {{
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                margin-right: 10px;
            }}
            .btn-primary {{
                background-color: #007bff;
                color: white;
            }}
            .btn-secondary {{
                background-color: #6c757d;
                color: white;
            }}
            .back-link {{
                display: inline-block;
                margin-top: 20px;
                color: #007bff;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Add New {table_type}</h2>
            <form id="addForm">
                {
                    ''.join(
                        f'''
                        <div class="form-group">
                            <label for="{field['name']}">{field['label']}:</label>
                            <input type="{field['type']}" id="{field['name']}" 
                                   name="{field['name']}" required>
                        </div>
                        '''
                        for field in form_fields[table_type]
                    )
                }
                <button type="submit" class="btn btn-primary">Save</button>
                <button type="button" class="btn btn-secondary" onclick="history.back()">Cancel</button>
            </form>
            <a href="/manage" class="back-link">← Back to Management</a>
        </div>

        <script>
            document.getElementById('addForm').addEventListener('submit', async (e) => {{
                e.preventDefault();
                const formData = new FormData(e.target);
                const data = Object.fromEntries(formData);
                
                try {{
                    const response = await fetch(window.location.pathname.replace('/add', ''), {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json'
                        }},
                        body: JSON.stringify(data)
                    }});
                    
                    if (response.ok) {{
                        window.location.href = '/manage';
                    }} else {{
                        const error = await response.json();
                        alert(error.error || 'Failed to add item');
                    }}
                }} catch (error) {{
                    alert('An error occurred. Please try again.');
                }}
            }});
        </script>
    </body>
    </html>
    """

# Add routes for the add forms
@app.route('/<table>/add', methods=['GET'])
def add_form(table):
    return create_add_form(table)

def create_edit_form(table_type, item):
    """
    Creates an HTML form for editing records based on table type
    """
    form_fields = {
        'Attribute': [
            {'name': 'attribute_id', 'type': 'number', 'label': 'Attribute ID', 'readonly': True},
            {'name': 'attribute_name', 'type': 'text', 'label': 'Attribute Name'},
            {'name': 'attribute_datatype', 'type': 'text', 'label': 'Data Type'},
            {'name': 'attribute_description', 'type': 'text', 'label': 'Description'},
            {'name': 'typical_values', 'type': 'text', 'label': 'Typical Values'},
            {'name': 'validation_criteria', 'type': 'text', 'label': 'Validation Criteria'}
        ],
        'Business-Term-Owner': [
            {'name': 'term_owner_code', 'type': 'text', 'label': 'Owner Code', 'readonly': True},
            {'name': 'term_owner_description', 'type': 'text', 'label': 'Description'}
        ],
        'Entity': [
            {'name': 'entity_id', 'type': 'number', 'label': 'Entity ID', 'readonly': True},
            {'name': 'entity_name', 'type': 'text', 'label': 'Entity Name'},
            {'name': 'entity_description', 'type': 'text', 'label': 'Description'}
        ],
        'Glossary-of-Business-Terms': [
            {'name': 'business_term_short_name', 'type': 'text', 'label': 'Term Name', 'readonly': True},
            {'name': 'date_term_defined', 'type': 'date', 'label': 'Date Defined'}
        ],
        'Source-Systems': [
            {'name': 'src_system_id', 'type': 'number', 'label': 'System ID', 'readonly': True},
            {'name': 'src_system_name', 'type': 'text', 'label': 'System Name'}
        ]
    }

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Edit {table_type}</title>
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
            input, select {{
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                box-sizing: border-box;
            }}
            input[readonly] {{
                background-color: #e9ecef;
            }}
            button {{
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                margin-right: 10px;
            }}
            .btn-primary {{
                background-color: #007bff;
                color: white;
            }}
            .btn-secondary {{
                background-color: #6c757d;
                color: white;
            }}
            .back-link {{
                display: inline-block;
                margin-top: 20px;
                color: #007bff;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Edit {table_type}</h2>
            <form id="editForm">
                {
                    ''.join(
                        f'''
                        <div class="form-group">
                            <label for="{field['name']}">{field['label']}:</label>
                            <input type="{field['type']}" 
                                   id="{field['name']}" 
                                   name="{field['name']}" 
                                   value="{item.get(field['name'], '')}"
                                   {'readonly' if field.get('readonly') else ''}
                                   required>
                        </div>
                        '''
                        for field in form_fields[table_type]
                    )
                }
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
                
                try {{
                    const response = await fetch(window.location.pathname.replace('/edit', ''), {{
                        method: 'PUT',
                        headers: {{
                            'Content-Type': 'application/json'
                        }},
                        body: JSON.stringify(data)
                    }});
                    
                    if (response.ok) {{
                        window.location.href = '/manage';
                    }} else {{
                        const error = await response.json();
                        alert(error.error || 'Failed to update item');
                    }}
                }} catch (error) {{
                    alert('An error occurred. Please try again.');
                }}
            }});
        </script>
    </body>
    </html>
    """

# Add route for edit forms
@app.route('/<table>/edit/<id>', methods=['GET'])
def edit_form(table, id):
    try:
        # Get the item data based on the table type and ID
        query_map = {
            'Attribute': ("SELECT * FROM attribute WHERE attribute_id = %s", int(id)),
            'Business-Term-Owner': ("SELECT * FROM business_term_owner WHERE term_owner_code = %s", id),
            'Entity': ("SELECT * FROM entity WHERE entity_id = %s", int(id)),
            'Glossary-of-Business-Terms': ("SELECT * FROM glossary_of_business_terms WHERE business_term_short_name = %s", id),
            'Source-Systems': ("SELECT * FROM source_systems WHERE src_system_id = %s", int(id))
        }
        
        if table not in query_map:
            return "Invalid table type", 400
            
        query, param = query_map[table]
        result = execute_query(query, (param,), fetch=True)
        
        if not result:
            return "Item not found", 404
            
        return create_edit_form(table, result[0])
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)




import pymysql
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# Database connection configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'antonio123',
    'database': 'customermetadatarepository',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**db_config)

def insert_users(cursor):
    print("Inserting Users...")
    users = [
        (1, 'admin', generate_password_hash('admin123'), 'admin', 'admin@example.com'),
        (2, 'user', generate_password_hash('user123'), 'user', 'user@example.com'),
        (3, 'manager', generate_password_hash('manager123'), 'manager', 'manager@example.com')
    ]
    
    for user in users:
        cursor.execute("""
            INSERT INTO users (user_id, username, password, role, email)
            VALUES (%s, %s, %s, %s, %s)
        """, user)
    print("Users insertion complete!")

def insert_data():
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        insert_users(cursor)
        
        # Insert Attributes (25 records)
        print("Inserting Attributes...")
        attributes = [
            (1, 'CustomerID', 'INT', 'Unique identifier for customer', '1000-9999', 'Must be positive'),
            (2, 'CustomerName', 'VARCHAR', 'Full name of customer', 'John Doe', 'Non-empty string'),
            (3, 'EmailAddress', 'VARCHAR', 'Customer email contact', 'example@email.com', 'Valid email format'),
            (4, 'DateOfBirth', 'DATE', 'Customer birth date', '1990-01-01', 'Valid date format'),
            (5, 'AccountBalance', 'DECIMAL', 'Current account balance', '1000.00', 'Non-negative number'),
            (6, 'PhoneNumber', 'VARCHAR', 'Contact phone number', '+1-123-456-7890', 'Valid phone format'),
            (7, 'Address', 'VARCHAR', 'Physical address', '123 Main St', 'Non-empty string'),
            (8, 'PostalCode', 'VARCHAR', 'Postal/ZIP code', '12345', 'Valid postal format'),
            (9, 'Country', 'VARCHAR', 'Country of residence', 'USA', 'ISO country code'),
            (10, 'Gender', 'CHAR', 'Customer gender', 'M/F', 'Single character'),
            (11, 'AccountType', 'VARCHAR', 'Type of account', 'Savings/Checking', 'Predefined values'),
            (12, 'JoinDate', 'DATE', 'Customer join date', '2023-01-01', 'Valid date'),
            (13, 'LastLoginDate', 'DATETIME', 'Last system login', '2024-03-20 10:00:00', 'Valid timestamp'),
            (14, 'PreferredLanguage', 'VARCHAR', 'Communication language', 'English', 'ISO language code'),
            (15, 'CreditScore', 'INT', 'Customer credit score', '300-850', 'Valid range'),
            (16, 'EmploymentStatus', 'VARCHAR', 'Current employment', 'Employed', 'Predefined status'),
            (17, 'Income', 'DECIMAL', 'Annual income', '50000.00', 'Positive number'),
            (18, 'MaritalStatus', 'VARCHAR', 'Marital status', 'Single/Married', 'Valid status'),
            (19, 'NumberOfDependents', 'INT', 'Number of dependents', '0-10', 'Non-negative'),
            (20, 'TaxID', 'VARCHAR', 'Tax identification', '123-45-6789', 'Valid format'),
            (21, 'Nationality', 'VARCHAR', 'Customer nationality', 'American', 'Valid nationality'),
            (22, 'OccupationType', 'VARCHAR', 'Type of occupation', 'Professional', 'Valid occupation'),
            (23, 'RiskProfile', 'VARCHAR', 'Customer risk level', 'Low/Medium/High', 'Valid risk level'),
            (24, 'LoyaltyPoints', 'INT', 'Customer loyalty points', '0-999999', 'Non-negative'),
            (25, 'PreferredContact', 'VARCHAR', 'Preferred contact method', 'Email/Phone', 'Valid method')
        ]
        
        for attr in attributes:
            cursor.execute("""
                INSERT INTO attribute 
                (attribute_id, attribute_name, attribute_datatype, 
                attribute_description, typical_values, validation_criteria)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, attr)
        
        # Insert Business Term Types (25 records)
        print("Inserting Business Term Types...")
        term_types = [(i, desc) for i, desc in enumerate([
            'Personal Information', 'Account Details', 'Transaction Data', 'Contact Information',
            'Security Data', 'Financial Information', 'Employment Data', 'Identity Verification',
            'Address Information', 'Communication Preferences', 'Risk Assessment', 'Compliance Data',
            'Marketing Preferences', 'Service History', 'Product Preferences', 'Channel Information',
            'Document Management', 'Relationship Data', 'Behavioral Data', 'Authentication Data',
            'Audit Information', 'Regulatory Reporting', 'Analytics Data', 'Reference Data',
            'Master Data'], 1)]
        
        for term_type in term_types:
            cursor.execute("""
                INSERT INTO business_term_type 
                (business_term_type_code, business_term_type_description)
                VALUES (%s, %s)
            """, term_type)
        
        # Insert Business Term Owners (25 records)
        print("Inserting Business Term Owners...")
        term_owners = [
            (f'OWN{i:03d}', f'Data Owner {i}') for i in range(1, 26)
        ]
        
        for owner in term_owners:
            cursor.execute("""
                INSERT INTO business_term_owner 
                (term_owner_code, term_owner_description)
                VALUES (%s, %s)
            """, owner)
        
        # Insert Entities (25 records)
        print("Inserting Entities...")
        entities = [
            (1, 'Customer', 'Core customer information'),
            (2, 'Account', 'Account details'),
            (3, 'Transaction', 'Transaction records'),
            (4, 'Address', 'Address information'),
            (5, 'Contact', 'Contact details'),
            (6, 'Document', 'Document management'),
            (7, 'Product', 'Product information'),
            (8, 'Service', 'Service details'),
            (9, 'Employee', 'Employee information'),
            (10, 'Department', 'Department details'),
            (11, 'Branch', 'Branch information'),
            (12, 'Contract', 'Contract details'),
            (13, 'Payment', 'Payment information'),
            (14, 'Complaint', 'Complaint management'),
            (15, 'Feedback', 'Customer feedback'),
            (16, 'Campaign', 'Marketing campaign'),
            (17, 'Event', 'Event management'),
            (18, 'Report', 'Reporting entity'),
            (19, 'Policy', 'Policy information'),
            (20, 'Audit', 'Audit records'),
            (21, 'Risk', 'Risk assessment'),
            (22, 'Compliance', 'Compliance records'),
            (23, 'Channel', 'Channel information'),
            (24, 'Partner', 'Partner details'),
            (25, 'Vendor', 'Vendor information')
        ]
        
        for entity in entities:
            cursor.execute("""
                INSERT INTO entity 
                (entity_id, entity_name, entity_description)
                VALUES (%s, %s, %s)
            """, entity)
        
        # Insert Glossary Terms (25 records)
        print("Inserting Glossary Terms...")
        base_date = datetime.now().date()
        glossary_terms = [
            (f'TERM_{i:03d}', base_date - timedelta(days=i)) for i in range(25)
        ]
        
        for term in glossary_terms:
            cursor.execute("""
                INSERT INTO glossary_of_business_terms 
                (business_term_short_name, date_term_defined)
                VALUES (%s, %s)
            """, term)
        
        # Insert Source Systems (25 records)
        print("Inserting Source Systems...")
        source_systems = [
            (i, f'System_{i}') for i in range(1, 26)
        ]
        
        for system in source_systems:
            cursor.execute("""
                INSERT INTO source_systems 
                (src_system_id, src_system_name)
                VALUES (%s, %s)
            """, system)

        # Commit all changes
        connection.commit()
        print("All data inserted successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
        if connection:
            connection.rollback()
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    insert_data()
import pymysql
from datetime import datetime

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='antonio123',
        database='customermetadatarepository',
        cursorclass=pymysql.cursors.DictCursor
    )

def init_db():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Clear existing data
            cursor.execute("DELETE FROM attribute")
            cursor.execute("DELETE FROM business_term_owner")
            cursor.execute("DELETE FROM entity")
            cursor.execute("DELETE FROM glossary_of_business_terms")
            cursor.execute("DELETE FROM source_systems")

            # Insert sample data into attribute
            cursor.execute("""
                INSERT INTO attribute (attribute_id, attribute_name, attribute_datatype, attribute_description, typical_values, validation_criteria) VALUES
                (1, 'Customer ID', 'VARCHAR', 'Unique identifier for customers', 'CUS001, CUS002', 'Must start with CUS'),
                (2, 'First Name', 'VARCHAR', 'Customer first name', 'John, Jane', 'Non-empty string'),
                (3, 'Last Name', 'VARCHAR', 'Customer last name', 'Doe, Smith', 'Non-empty string'),
                (4, 'Email', 'VARCHAR', 'Customer email address', 'example@email.com', 'Valid email format'),
                (5, 'Phone Number', 'VARCHAR', 'Customer contact number', '+1-123-456-7890', 'Valid phone format')
            """)

            # Insert sample data into business_term_owner
            cursor.execute("""
                INSERT INTO business_term_owner (term_owner_code, term_owner_description) VALUES
                ('CRM001', 'Customer Relations Manager'),
                ('SAL001', 'Sales Department Head'),
                ('MKT001', 'Marketing Team Lead'),
                ('SUP001', 'Support Team Manager'),
                ('FIN001', 'Finance Department Head')
            """)

            # Insert sample data into entity
            cursor.execute("""
                INSERT INTO entity (entity_id, entity_name, entity_description) VALUES
                (1, 'Customer', 'Core customer information'),
                (2, 'Order', 'Customer order details'),
                (3, 'Product', 'Product catalog information'),
                (4, 'Invoice', 'Billing and payment information'),
                (5, 'Support_Ticket', 'Customer support records')
            """)

            # Insert sample data into glossary_of_business_terms
            current_date = datetime.now().date().isoformat()
            cursor.execute(f"""
                INSERT INTO glossary_of_business_terms (business_term_short_name, date_term_defined) VALUES
                ('CUST', '{current_date}'),
                ('ORD', '{current_date}'),
                ('PROD', '{current_date}'),
                ('INV', '{current_date}'),
                ('SUPP', '{current_date}')
            """)

            # Insert sample data into source_systems
            cursor.execute("""
                INSERT INTO source_systems (src_system_id, src_system_name) VALUES
                (1, 'CRM System'),
                (2, 'Sales Portal'),
                (3, 'Marketing Platform'),
                (4, 'Support Desk'),
                (5, 'Billing System')
            """)

            connection.commit()
            print("Database initialized successfully!")

    except Exception as e:
        print(f"Error initializing database: {e}")
        connection.rollback()
    finally:
        connection.close()

if __name__ == '__main__':
    init_db() 
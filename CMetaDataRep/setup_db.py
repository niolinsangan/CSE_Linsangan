import pymysql

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='antonio123',
        database='customermetadatarepository',
        cursorclass=pymysql.cursors.DictCursor
    )

def setup_database():
    # Read the schema SQL file
    with open('CMetaDataRep/schema.sql', 'r') as file:
        schema_sql = file.read()

    # Split the SQL commands
    commands = schema_sql.split(';')

    # Connect to the database and execute each command
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            for command in commands:
                if command.strip():
                    cursor.execute(command)
            connection.commit()
            print("Database tables created successfully!")

            # Insert sample data
            # Attributes
            cursor.execute("""
                INSERT INTO attribute (attribute_id, attribute_name, attribute_datatype, attribute_description, typical_values, validation_criteria) VALUES
                (1, 'Customer ID', 'VARCHAR', 'Unique identifier for customers', 'CUS001, CUS002', 'Must start with CUS'),
                (2, 'First Name', 'VARCHAR', 'Customer first name', 'John, Jane', 'Non-empty string'),
                (3, 'Last Name', 'VARCHAR', 'Customer last name', 'Doe, Smith', 'Non-empty string'),
                (4, 'Email', 'VARCHAR', 'Customer email address', 'example@email.com', 'Valid email format'),
                (5, 'Phone Number', 'VARCHAR', 'Customer contact number', '+1-123-456-7890', 'Valid phone format')
            """)

            # Business Term Owners
            cursor.execute("""
                INSERT INTO business_term_owner (term_owner_code, term_owner_description) VALUES
                ('CRM001', 'Customer Relations Manager'),
                ('SAL001', 'Sales Department Head'),
                ('MKT001', 'Marketing Team Lead'),
                ('SUP001', 'Support Team Manager'),
                ('FIN001', 'Finance Department Head')
            """)

            # Entities
            cursor.execute("""
                INSERT INTO entity (entity_id, entity_name, entity_description) VALUES
                (1, 'Customer', 'Core customer information'),
                (2, 'Order', 'Customer order details'),
                (3, 'Product', 'Product catalog information'),
                (4, 'Invoice', 'Billing and payment information'),
                (5, 'Support_Ticket', 'Customer support records')
            """)

            # Glossary Terms
            cursor.execute("""
                INSERT INTO glossary_of_business_terms (business_term_short_name, date_term_defined) VALUES
                ('CUST', CURRENT_DATE),
                ('ORD', CURRENT_DATE),
                ('PROD', CURRENT_DATE),
                ('INV', CURRENT_DATE),
                ('SUPP', CURRENT_DATE)
            """)

            # Source Systems
            cursor.execute("""
                INSERT INTO source_systems (src_system_id, src_system_name) VALUES
                (1, 'CRM System'),
                (2, 'Sales Portal'),
                (3, 'Marketing Platform'),
                (4, 'Support Desk'),
                (5, 'Billing System')
            """)

            # Business Term Types
            cursor.execute("""
                INSERT INTO business_term_type (term_type_code, term_type_description) VALUES
                ('BUS', 'Business Term'),
                ('TECH', 'Technical Term'),
                ('PROC', 'Process Term'),
                ('KPI', 'Performance Indicator'),
                ('REG', 'Regulatory Term')
            """)

            connection.commit()
            print("Sample data inserted successfully!")

    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        connection.close()

if __name__ == '__main__':
    setup_database() 
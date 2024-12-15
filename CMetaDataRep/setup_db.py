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
                (5, 'Phone Number', 'VARCHAR', 'Customer contact number', '+1-123-456-7890', 'Valid phone format'),
                (6, 'Address', 'VARCHAR', 'Customer address', '123 Main St, 456 Elm St', 'Non-empty string'),
                (7, 'City', 'VARCHAR', 'City of residence', 'New York, Los Angeles', 'Non-empty string'),
                (8, 'State', 'VARCHAR', 'State of residence', 'NY, CA', 'Valid state code'),
                (9, 'Zip Code', 'VARCHAR', 'Postal code', '10001, 90001', 'Valid zip format'),
                (10, 'Country', 'VARCHAR', 'Country of residence', 'USA, Canada', 'Non-empty string'),
                (11, 'Date of Birth', 'DATE', 'Customer birth date', '1990-01-01, 1985-05-15', 'Valid date format'),
                (12, 'Gender', 'VARCHAR', 'Customer gender', 'Male, Female', 'Non-empty string'),
                (13, 'Account Balance', 'DECIMAL', 'Current account balance', '100.00, 250.50', 'Non-negative number'),
                (14, 'Membership Level', 'VARCHAR', 'Customer membership level', 'Gold, Silver', 'Non-empty string'),
                (15, 'Newsletter Subscription', 'BOOLEAN', 'Subscribed to newsletter', 'True, False', 'Boolean value'),
                (16, 'Preferred Contact Method', 'VARCHAR', 'Preferred method of contact', 'Email, Phone', 'Non-empty string'),
                (17, 'Last Purchase Date', 'DATE', 'Date of last purchase', '2023-01-01, 2023-02-15', 'Valid date format'),
                (18, 'Loyalty Points', 'INT', 'Accumulated loyalty points', '100, 200', 'Non-negative integer'),
                (19, 'Referral Source', 'VARCHAR', 'Source of referral', 'Friend, Online', 'Non-empty string'),
                (20, 'Occupation', 'VARCHAR', 'Customer occupation', 'Engineer, Teacher', 'Non-empty string'),
                (21, 'Marital Status', 'VARCHAR', 'Marital status', 'Single, Married', 'Non-empty string'),
                (22, 'Number of Dependents', 'INT', 'Number of dependents', '0, 2', 'Non-negative integer'),
                (23, 'Annual Income', 'DECIMAL', 'Annual income', '50000.00, 75000.00', 'Non-negative number'),
                (24, 'Credit Score', 'INT', 'Credit score', '700, 750', 'Non-negative integer'),
                (25, 'Employment Status', 'VARCHAR', 'Employment status', 'Employed, Unemployed', 'Non-empty string')
            """)

            # Business Term Owners
            cursor.execute("""
                INSERT INTO business_term_owner (term_owner_code, term_owner_description) VALUES
                ('CRM001', 'Customer Relations Manager'),
                ('SAL001', 'Sales Department Head'),
                ('MKT001', 'Marketing Team Lead'),
                ('SUP001', 'Support Team Manager'),
                ('FIN001', 'Finance Department Head'),
                ('HR001', 'Human Resources Manager'),
                ('IT001', 'IT Department Head'),
                ('OPS001', 'Operations Manager'),
                ('QA001', 'Quality Assurance Lead'),
                ('DEV001', 'Development Team Lead'),
                ('PRD001', 'Product Manager'),
                ('CS001', 'Customer Service Manager'),
                ('LOG001', 'Logistics Coordinator'),
                ('PR001', 'Public Relations Officer'),
                ('RND001', 'Research and Development Head'),
                ('HR002', 'Assistant HR Manager'),
                ('IT002', 'Assistant IT Manager'),
                ('OPS002', 'Assistant Operations Manager'),
                ('QA002', 'Assistant QA Lead'),
                ('DEV002', 'Assistant Development Lead'),
                ('PRD002', 'Assistant Product Manager'),
                ('CS002', 'Assistant Customer Service Manager'),
                ('LOG002', 'Assistant Logistics Coordinator'),
                ('PR002', 'Assistant PR Officer'),
                ('RND002', 'Assistant R&D Head')
            """)

            # Entities
            cursor.execute("""
                INSERT INTO entity (entity_id, entity_name, entity_description) VALUES
                (1, 'Customer', 'Core customer information'),
                (2, 'Order', 'Customer order details'),
                (3, 'Product', 'Product catalog information'),
                (4, 'Invoice', 'Billing and payment information'),
                (5, 'Support_Ticket', 'Customer support records'),
                (6, 'Supplier', 'Supplier information and contracts'),
                (7, 'Warehouse', 'Warehouse inventory and logistics'),
                (8, 'Employee', 'Employee records and payroll'),
                (9, 'Department', 'Departmental structure and hierarchy'),
                (10, 'Project', 'Project management and timelines'),
                (11, 'Campaign', 'Marketing campaign details'),
                (12, 'Event', 'Corporate events and schedules'),
                (13, 'Asset', 'Company assets and valuations'),
                (14, 'Contract', 'Legal contracts and agreements'),
                (15, 'Policy', 'Company policies and procedures'),
                (16, 'Supplier', 'Supplier information and contracts'),
                (17, 'Warehouse', 'Warehouse inventory and logistics'),
                (18, 'Employee', 'Employee records and payroll'),
                (19, 'Department', 'Departmental structure and hierarchy'),
                (20, 'Project', 'Project management and timelines'),
                (21, 'Campaign', 'Marketing campaign details'),
                (22, 'Event', 'Corporate events and schedules'),
                (23, 'Asset', 'Company assets and valuations'),
                (24, 'Contract', 'Legal contracts and agreements'),
                (25, 'Policy', 'Company policies and procedures')
            """)

            # Glossary Terms
            cursor.execute("""
                INSERT INTO glossary_of_business_terms (business_term_short_name, date_term_defined) VALUES
                ('CUST', CURRENT_DATE),
                ('ORD', CURRENT_DATE),
                ('PROD', CURRENT_DATE),
                ('INV', CURRENT_DATE),
                ('SUPP', CURRENT_DATE),
                ('WHSE', CURRENT_DATE),
                ('EMPL', CURRENT_DATE),
                ('DEPT', CURRENT_DATE),
                ('PROJ', CURRENT_DATE),
                ('CMPN', CURRENT_DATE),
                ('EVNT', CURRENT_DATE),
                ('ASST', CURRENT_DATE),
                ('CNTR', CURRENT_DATE),
                ('POLC', CURRENT_DATE),
                ('SUPP2', CURRENT_DATE),
                ('WHSE2', CURRENT_DATE),
                ('EMPL2', CURRENT_DATE),
                ('DEPT2', CURRENT_DATE),
                ('PROJ2', CURRENT_DATE),
                ('CMPN2', CURRENT_DATE),
                ('EVNT2', CURRENT_DATE),
                ('ASST2', CURRENT_DATE),
                ('CNTR2', CURRENT_DATE),
                ('POLC2', CURRENT_DATE)
            """)

            # Source Systems
            cursor.execute("""
                INSERT INTO source_systems (src_system_id, src_system_name) VALUES
                (1, 'CRM System'),
                (2, 'Sales Portal'),
                (3, 'Marketing Platform'),
                (4, 'Support Desk'),
                (5, 'Billing System'),
                (6, 'HR System'),
                (7, 'IT Management Portal'),
                (8, 'Operations Dashboard'),
                (9, 'QA Tracking System'),
                (10, 'Development Environment'),
                (11, 'Product Lifecycle Management'),
                (12, 'Customer Service Platform'),
                (13, 'Logistics Management System'),
                (14, 'Public Relations Tool'),
                (15, 'R&D Database'),
                (16, 'HR System 2'),
                (17, 'IT Management Portal 2'),
                (18, 'Operations Dashboard 2'),
                (19, 'QA Tracking System 2'),
                (20, 'Development Environment 2'),
                (21, 'Product Lifecycle Management 2'),
                (22, 'Customer Service Platform 2'),
                (23, 'Logistics Management System 2'),
                (24, 'Public Relations Tool 2'),
                (25, 'R&D Database 2')
            """)

            # Business Term Types
            cursor.execute("""
                INSERT INTO business_term_type (term_type_code, term_type_description) VALUES
                ('BUS', 'Business Term'),
                ('TECH', 'Technical Term'),
                ('PROC', 'Process Term'),
                ('KPI', 'Performance Indicator'),
                ('REG', 'Regulatory Term')
                ('FIN', 'Financial Term'),
                ('HR', 'Human Resources Term'),
                ('MKT', 'Marketing Term'),
                ('IT', 'Information Technology Term'),
                ('OPS', 'Operations Term'),
                ('SALES', 'Sales Term'),
                ('LEGAL', 'Legal Term'),
                ('RISK', 'Risk Management Term'),
                ('COMPLIANCE', 'Compliance Term'),
                ('SUPPLY', 'Supply Chain Term'),
                ('CUSTOMER', 'Customer Service Term'),
                ('PRODUCT', 'Product Management Term'),
                ('PROJECT', 'Project Management Term'),
                ('STRATEGY', 'Strategic Planning Term'),
                ('INNOVATION', 'Innovation Term'),
                ('BRAND', 'Brand Management Term'),
                ('DATA', 'Data Management Term'),
                ('ANALYTICS', 'Analytics Term'),
                ('RESEARCH', 'Research and Development Term'),
                ('QUALITY', 'Quality Assurance Term')

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
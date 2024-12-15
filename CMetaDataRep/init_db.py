import pymysql

def initialize_database():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='antonio123',
        database='customermetadatarepository',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with connection.cursor() as cursor:
            # Insert initial data
            cursor.execute("""
                INSERT INTO attribute (attribute_id, attribute_name, attribute_datatype)
                VALUES (1, 'Sample Attribute', 'VARCHAR')
                ON DUPLICATE KEY UPDATE attribute_name=attribute_name
            """)
            cursor.execute("""
                INSERT INTO business_term_owner (term_owner_code, term_owner_description)
                VALUES ('OWNER1', 'Sample Owner')
                ON DUPLICATE KEY UPDATE term_owner_description=term_owner_description
            """)
            # Add more initial data as needed
            connection.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
        if connection:
            connection.rollback()
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    initialize_database() 
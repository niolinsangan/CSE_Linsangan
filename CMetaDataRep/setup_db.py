import pymysql
from faker import Faker

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='antonio123',
        database='customermetadatarepository',
        cursorclass=pymysql.cursors.DictCursor
    )

def setup_database():
    connection = get_db_connection()
    fake = Faker()
    
    try:
        with connection.cursor() as cursor:
            # Create tables if they don't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attribute (
                    attribute_id INT PRIMARY KEY,
                    attribute_name VARCHAR(100),
                    attribute_datatype VARCHAR(100),
                    attribute_description TEXT,
                    typical_values TEXT,
                    validation_criteria TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS business_term_owner (
                    term_owner_code VARCHAR(100) PRIMARY KEY,
                    term_owner_description VARCHAR(100)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS business_term_type (
                    term_type_code INT PRIMARY KEY,
                    term_type_description VARCHAR(100)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS entity (
                    entity_id INT PRIMARY KEY,
                    entity_name VARCHAR(100),
                    entity_description VARCHAR(100)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS glossary_of_business_terms (
                    business_term_short_name VARCHAR(100) PRIMARY KEY,
                    date_term_defined DATE
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS source_systems (
                    src_system_id INT PRIMARY KEY,
                    src_system_name VARCHAR(100)
                )
            """)

            # Insert fake data into glossary_of_business_terms table
            cursor.executemany("""
                INSERT INTO glossary_of_business_terms (business_term_short_name, date_term_defined) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE date_term_defined=VALUES(date_term_defined)
            """, [(fake.word().upper(), fake.date_this_decade()) for _ in range(25)])
            
            # Insert fake data into business_term_owner table
            cursor.executemany("""
                INSERT INTO business_term_owner (term_owner_code, term_owner_description) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE term_owner_description=VALUES(term_owner_description)
            """, [(fake.unique.word().upper(), fake.name()) for _ in range(25)])

            # Insert fake data into source_systems table
            cursor.executemany("""
                INSERT INTO source_systems (src_system_id, src_system_name) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE src_system_name=VALUES(src_system_name)
            """, [(i, fake.company()) for i in range(1, 26)])

            # Insert fake data into business_term_type table
            cursor.executemany("""
                INSERT INTO business_term_type (term_type_code, term_type_description) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE term_type_description=VALUES(term_type_description)
            """, [(i, fake.catch_phrase()) for i in range(1, 26)])

            # Insert fake data into attribute table
            cursor.executemany("""
                INSERT INTO attribute (attribute_id, attribute_name, attribute_datatype, attribute_description, typical_values, validation_criteria) 
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE attribute_name=VALUES(attribute_name), attribute_datatype=VALUES(attribute_datatype),
                attribute_description=VALUES(attribute_description), typical_values=VALUES(typical_values), validation_criteria=VALUES(validation_criteria)
            """, [(i, fake.word(), 'VARCHAR', fake.sentence(), fake.word(), fake.sentence()) for i in range(1, 26)])

            # Insert fake data into entity table
            cursor.executemany("""
                INSERT INTO entity (entity_id, entity_name, entity_description) 
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE entity_name=VALUES(entity_name), entity_description=VALUES(entity_description)
            """, [(i, fake.company(), fake.catch_phrase()) for i in range(1, 26)])

            connection.commit()
            print("Sample data inserted successfully!")

    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        connection.close()

if __name__ == '__main__':
    setup_database() 
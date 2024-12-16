
# Customer Metadata Repository

## Overview
The Customer Metadata Repository is a web application designed to manage and store metadata related to customer attributes, business terms, entities, and source systems. This application provides a RESTful API for user authentication, data management, and retrieval.

## Features
- User authentication with JWT tokens
- CRUD operations for attributes, business term owners, entities, glossary terms, and source systems
- Comprehensive test suite using pytest

## Technologies Used
- Python
- Flask
- PyMySQL
- JWT for authentication
- pytest for testing

## Installation

### Prerequisites
- Python 3.x
- MySQL or MariaDB
- pip

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/CustomerMetadataRepository.git
   cd CustomerMetadataRepository
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up the database:
   - Update the database connection details in `CMetaDataRep/init_db.py`.
   - Run the database initialization script:
     ```bash
     python CMetaDataRep/init_db.py
     ```

## Usage
To run the application, execute the following command:
     ```bash
     python CMetaDataRep/app.py run
     ```

If data is missing use this:
     ```bash
     python CMetaDataRep/setup_db.py
     ```
To run tests use:
     ```bash
     python CMetaDataRep/test_app.py
     ```



## API Endpoints
- **POST /login**: Authenticate user and receive a JWT token.
- **POST /register**: Register a new user.
- **GET /Attribute**: Retrieve all attributes.
- **POST /Attribute**: Add a new attribute.
- **PUT /Attribute/{id}**: Update an existing attribute.
- **DELETE /Attribute/{id}**: Delete an attribute.
- **GET /Business-Term-Owner**: Retrieve all business term owners.
- **POST /Business-Term-Owner**: Add a new business term owner.
- **PUT /Business-Term-Owner/{code}**: Update a business term owner.
- **DELETE /Business-Term-Owner/{code}**: Delete a business term owner.
- **GET /Entity**: Retrieve all entities.
- **POST /Entity**: Add a new entity.
- **PUT /Entity/{id}**: Update an existing entity.
- **DELETE /Entity/{id}**: Delete an entity.
- **GET /Glossary-of-Business-Terms**: Retrieve glossary terms.
- **POST /Glossary-of-Business-Terms**: Add a new glossary term.
- **PUT /Glossary-of-Business-Terms/{term}**: Update a glossary term.
- **DELETE /Glossary-of-Business-Terms/{term}**: Delete a glossary term.
- **GET /Source-Systems**: Retrieve source systems.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.





# Allotments Management System API

## Description
This project is an **Allotments Management System** API that allows users to manage allotment sites, departments, residents, and rentals. It implements role-based access control and uses **JWT authentication** for securing endpoints.

## Installation
To install the required dependencies, run the following command:
```bash
pip install -r requirements.txt
```

## Configuration
To configure the database:

1. Create the `allotments` MySQL database to your server or import the `allotments.sql` in the dbSetup folder.
2. Update the database configuration in the Flask app with your database connection details.

### Environment variables needed:
- `MYSQL_HOST`: The hostname for the MySQL database
- `MYSQL_USER`: MySQL username 
- `MYSQL_PASSWORD`: MySQL password
- `MYSQL_DB`: Name of the database
- `SECRET_KEY`: bakanese
---

## API Endpoints

Here’s a list of the main API endpoints:

| Endpoint             | Method   | Description                           |
|----------------------|----------|---------------------------------------|
| `/`                  | `GET`    | Home route that returns the homepage  |
| `/login`             | `POST`   | User login (returns JWT token)        |
| `/departments`       | `GET`    | List all departments                  |
| `/departments/<id>`  | `GET`    | Get a specific department by ID       |
| `/departments`       | `POST`   | Create a new department               |
| `/departments/<id>`  | `PUT`    | Update a department                   |
| `/departments/<id>`  | `DELETE` | Delete a department                   |
| `/sites`             | `GET`    | List all sites                        |
| `/sites/<id>`        | `GET`    | Get a specific site by ID             |
| `/sites`             | `POST`   | Create a new site                     |
| `/sites/<id>`        | `PUT`    | Update a site                         |
| `/sites/<id>`        | `DELETE` | Delete a site                         |
| `/residents`         | `GET`    | List all residents                    |
| `/residents/<id>`    | `GET`    | Get a specific resident by ID         |
| `/residents`         | `POST`   | Create a new resident                 |
| `/residents/<id>`    | `PUT`    | Update a resident                     |
| `/residents/<id>`    | `DELETE` | Delete a resident                     |
| `/rentals`           | `GET`    | List all rentals                      |
| `/rentals/<id>`      | `GET`    | Get a specific rental by ID           |
| `/rentals`           | `POST`   | Create a new rental                   |
| `/rentals/<id>`      | `PUT`    | Update a rental                       |
| `/rentals/<id>`      | `DELETE` | Delete a rental                       |
| `/allotments`        | `GET`    | List all allotments                   |
| `/allotments/<id>`   | `GET`    | Get a specific allotment by ID        |
| `/allotments`        | `POST`   | Create a new allotment                |
| `/allotments/<id>`   | `PUT`    | Update an allotment                   |
| `/allotments/<id>`   | `DELETE` | Delete an allotment                   |

---

## Testing

To run the tests for the application, follow these steps:

1. **Install the dependencies**:
   Ensure you have installed all dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the tests**:
   Run the following command to execute the test suite:
   ```bash
   pytest --maxfail=1 --disable-warnings -v
   ```

   This will run all the tests and show you a detailed result.

---

## Git Commit Guidelines

This project follows **Conventional Commits** for commit messages. Here’s a brief overview:

- **feat**: Add a new feature to the application.
- **fix**: Fix a bug or issue in the code.
- **docs**: Update documentation (e.g., README.md).
- **test**: Add or modify tests.

### Example commit messages:
```bash
feat: add JWT authentication for secure endpoints
fix: resolve issue with role-based access control in departments
docs: update README with new API endpoints
test: add tests for user authentication and authorization
```

---

### Additional Notes:
- Make sure to replace the environment variables `DATABASE_URL` and `SECRET_KEY` with your actual values before running the application.
- The API is secured with **JWT** tokens, and each protected endpoint requires a valid token with the appropriate role.


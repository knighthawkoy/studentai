# v3 changes
Key Changes Made:

Imported bcrypt and caught exceptions where needed.
Used bcrypt.checkpw for password comparison during login.
Decoded hashed password before storing it into the database.
Encapsulated database operations within try-except blocks for error handling.
Updated the HTTP method for /account/logout to 'POST'.
Implemented better token validation and storage practices.
Included checks for existence and correct parsing of swagger.json.
Replaced app.run() with a production-ready WSGI server like waitress.

# V4 changes.

Now supports deleting the user.

# v5 changes

Database Connection Pooling: Instead of creating a new database connection on every request, use a connection pool to manage the connections efficiently.
Password Hashing in Background Task: For better performance with bcrypt, hashing can be done asynchronously if it's allowed in your setup.
Global Database Connection: Initialize the global database connection once rather than on each function call.
Error Handling: Improve error handling with more specific exceptions and ensure sensitive information is not returned in responses.
Token Validation: Create a separate decorator function for validating tokens to reduce redundancy across different routes.
Environment Variables: Use environment variables for configuration settings like the database path or server port.
Swagger UI Configuration: Define the SWAGGER_URL and API_URL inside the app configuration.


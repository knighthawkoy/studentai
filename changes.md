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


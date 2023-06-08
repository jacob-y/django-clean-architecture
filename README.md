# django-clean-architecture

Full rewrite of example in progress.

Django example of calling the PayPal API to make payments, using the clean architecture pattern:

- `Entities`: core domain objects, written in pure python.
- `Domain`: use cases to interact with the domain data, written in pure python.
- `Application`: concrete implementation of external dependencies (database, HTTP calls, etc.).
- `Infrastructure`: the framework & third-party libraries.

The dependencies must follow this order: `Entities` <- `Domain` <- `Application` <- `Infrastructure`.

See the `modules` README.md files for details.

To run: `python manage.py runserver`

You will need to have your own PayPal sandbox account to test the application.

Put your PayPal credentials in the `fileStorage` folder (see the README for details).

# django-clean-architecture

This project is Python/Django example of a Clean Architecture implementation for pedagogical purposes.

Implementing the Clean Architecture patterns with Python / Django is not obvious, as Python and Django have not been natively designed to do it.
That is why I wrote this example as a demo.

I used the Python type hints as much as possible (with the usual limitations).

To implement abstract classes and interfaces, I relied on the `abc` module as Python does not natively provide interfaces.

The private / protected / public statuses of class functions & variables are implemented with the usual Python namespace conventions (starting with a `_` for protected methods and `__` for private methods)

The application is a payment gateway integration REST API, as I designed a very similar system in PHP at iRaiser.

I used the Django REST framework in the `webapps` folder.

Only PayPal is implemented, I will add Stripe later to have several gateway implementations in the example.

### Organization

The projects follow the Clean Architecture patterns, with these layers:

- `Entities`: core domain objects, written in pure python.
- `Domain`: use cases to interact with the domain data, written in pure python.
- `Application`: concrete implementation of external dependencies (database, HTTP calls, etc.).
- `Infrastructure`: the framework & third-party libraries.

The dependencies must follow this order: `Entities` <- `Domain` <- `Application` <- `Infrastructure`.

See the `modules` README.md files for details.

### How to run

Start the server: `python manage.py runserver`

You will need to have your own PayPal sandbox account to test the application
 (you will need to have a developer account and a sandbox business account).

Put your PayPal credentials in the `fileStorage` folder.

```
{
  "client_id": "YOUR_PAYPAL_SANDBOX_CLIENT_ID",
  "client_secret": "YOUR_PAYPALSANDBOX_CLIENT_SECRET"
}
```
You will find them in the PayPal developer back-office.

### Usage Examples

#### Create a payment

POST http://127.0.0.1:8000/payment/create

```json
{
    "email": "YOUR_PAYPAL_CUSTOMER_EMAIL",
    "first_name": "Donald",
    "last_name": "Duck",
    "address1": "199 route de clisson",
    "address2": "2nd Etape",
    "post_code": "44229",
    "city": "Saint Sébastien sur Loire",
    "country_code": "FR",
    "transaction_id": "CHANGE_THIS_FOR_EVERY_REQUEST",
    "lang": "fr-FR",
    "amount": 20.00,
    "currency": "EUR",
    "return_url": "https://YOUR_DOMAIN"
}
```

Response

```json
{
    "gateway_id": "YOUR_ID",
    "gateway_status": "",
    "status": "PENDING",
    "redirect_url": "https://www.sandbox.paypal.com/checkoutnow?token=YOUR_ID"
}
```

If you open the `redirect_url`, you will be able to authenticate on PayPal as a payer, and after be redirected on `https://YOUR_DOMAIN?token=YOUR_ID&PayerID=YOUR_PAYER_ID`.

#### Capture a payment

POST http://127.0.0.1:8000/payment/YOUR_ID/capture

Response

```json
{
    "gateway_id": "YOUR_ID",
    "gateway_status": "COMPLETED",
    "status": "SUCCESSFUL"
}
```
#### Refund a payment

POST http://127.0.0.1:8000/payment/YOUR_ID/refund

Response

```json
{
    "gateway_id": "YOUR_ID",
    "gateway_status": "REFUNDED",
    "status": "REFUNDED"
}
```

#### Get a payment status

GET http://127.0.0.1:8000/payment/YOUR_ID

Response

```json
{
    "gateway_id": "YOUR_ID",
    "gateway_status": "REFUNDED",
    "status": "REFUNDED"
}
```
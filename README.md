# django-clean-architecture

This a payment gateway APIs integration framework, with both a REST API interface and a web UI.

Made with Django, the project follows the Clean Architecture principles.
You will get details inside the folders README.md files.

This is a portfolio of similar (and much more complex) real projects that I have worked on.

PayPal and Stripe (for credit card and IBAN) have been implemented as demo examples in sandbox.

Only sandbox single payments with EUR are possible, with PayPal, Credit Card and SEPA.

You will have to use your own sandbox PayPal & Stripe accounts (for merchant and customer) to use the Web UI, the REST API and run the integration tests.

Else you will only be able to run the unit tests.

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

**You will need to have your own PayPal & Stripe sandbox accounts to test the application.**

Put your PayPal and / or Stripe credentials in the `fileStorage` folder.

```
{
  "paypal": {
    "client_id": "YOUR_PAYPAL_SANDBOX_CLIENT_ID",
    "client_secret": "YOUR_PAYPALSANDBOX_CLIENT_SECRET"
  },
  "stripe": {
    "secret_key": "YOU_STRIPE_SECRET_KEY"
  }
}
```
You will find them in the PayPal & Stripe developer back-offices.

### Usage Examples

#### Create a payment

POST http://127.0.0.1:8000/payment/{method}/create

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

POST http://127.0.0.1:8000/payment/{method}/{ID}/capture

Response

```json
{
    "gateway_id": "YOUR_ID",
    "gateway_status": "COMPLETED",
    "status": "SUCCESSFUL"
}
```

#### Get a payment status

GET http://127.0.0.1:8000/payment/{method}/{ID}

Response

```json
{
    "gateway_id": "YOUR_ID",
    "gateway_status": "REFUNDED",
    "status": "REFUNDED"
}
```

### User Interface

Demos: 
- http://127.0.0.1:8000/paypal
- http://127.0.0.1:8000/card
- http://127.0.0.1:8000/iban

You will be able to make a sandbox payment flow.

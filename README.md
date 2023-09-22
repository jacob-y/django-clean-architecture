# django-clean-architecture

Full rewrite of example in progress.

Django example of calling the PayPal API to make payments.


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
    "status": "SUCCESSFUL"
}
```
#### Refund a payment

POST http://127.0.0.1:8000/payment/YOUR_ID/refund

Response

```json
{
    "gateway_id": "YOUR_ID",
    "status": "REFUNDED"
}
```

#### Get a payment status

GET http://127.0.0.1:8000/payment/YOUR_ID

Response

```json
{
    "gateway_id": "YOUR_ID",
    "status": "REFUNDED"
}
```
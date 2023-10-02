The `Application` layer implements external dependencies using the interfaces in `Domain/Plugin`.

Contains the HTTP requests to the PayPal endpoints and the returned data interpretation.

The HTTP library used in this implementation is abstracted, to be implemented on the `Infrastructure` layer.
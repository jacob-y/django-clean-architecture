The `Services` implements the uses cases offered by the application.

This layer is be called to perform actions on the `Entities` we previously defined.

External dependencies are to be abstracted by the `Plugin` and `Model` abstract classes.

We have a mapping between our representation of the payment flow and the payment gateway representation of the payment flow (that depends on the payment method business rules).

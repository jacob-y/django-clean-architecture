The `Plugin` folder contains interfaces to third-party APIs (libraries, HTTP endpoints, SDKs, etc.), to be implemented in `Application/PluginAdaptor`.

That allow us to easily change the implementation of the payment gateway calls, for instance if we want to replace the raw HTTP calls by an official PayPal SDK or a library coming from an open source project.
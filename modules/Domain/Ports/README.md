`Ports` offers the interfaces to be used by the `Infrastrucure` web controllers.

This layer is used to abstract the input processing (if you want to rewrite the API, and replace an XML interface by JSON for instance).

This layer is often not implemented, in that case the web controllers calls directly the `Domain` and `Entites` objects without going through the `Application` layer.

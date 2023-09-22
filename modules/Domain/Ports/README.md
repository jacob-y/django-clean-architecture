The `Ports` folder offers the interfaces to be used by the `Infrastrucure` web controllers.
 
The input processing is abstracted (if you want to rewrite the API, and replace an XML interface by JSON for instance).
Often not implemented because the abstraction of the input if unecessary.
In that case the web controllers calls directly the `Domain` and `Entites` objects.

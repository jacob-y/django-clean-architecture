This folder contains the two layers of tests:

- `Unit`: no dependency on the framework, database or external APIs. Everything is mocked. Run Instantly. Checked before accepting any commit.
- `Integration`: performs calls on the API sandboxes, but the front-end is not tested. Takes some time to run because of API calls.

Since we have no web interface, there is no end-to-end tests.

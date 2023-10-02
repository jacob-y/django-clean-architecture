This folder contains the three layers of tests:

- `Unit`: no dependency on the framework, database or external APIs. Everything is mocked. Run Instantly. Checked before accepting any commit.
- `Integration`: performs calls on the API sandboxes, but the front-end is not tested. Takes some time to run because of API calls. Integrate it in you CI / CD pipeline.
- `E2E`: end-to-end tests, run with cypress to run a browser, tests everything but takes a very long time to run. Usually manually run by developers.

Only unit tests are implemented, integration tests are to be added layer.

We will need to add a graphical interface in the application to run E2E tests with cypress layer.
# Ebook Delivery Application

This application was built to provide a simple delivery service for ebooks that are purchased or licensed by the libraries but not hosted by a vendor. The application presents a landing page for each ebook, on which all files associated with that item are displayed for download. "Ebook" in this case is a loose term that could refer to any item presented to the user as a file or collection of files. This application is format-agnostic; files are served to the user to the browser, and will be rendered by the browser when possible (e.g., PDF) or downloaded to be opened in another appropriate application.

## Development

`pipenv install --dev` is a great starting point.

If you run into issues with `xmlsec1`, you may need to install an external
dependency. On macOS, `brew install libxmlsec1` is likely all you need.

To run tests locally,

```shell
pipenv run pytest --cov=ebooks tests/
```

Ask on engineering Slack for useful local environment settings. You can include
them in a `.env` file locally and flask will autoload them if you include
`FLASK_ENV=development` in that file.

To run the local app once you have the env noted above:

```shell
pipenv run python runserver.py
```

If you are being prompted for SAML login locally, be sure to check you are
running in development mode with `FLASK_ENV=development` in your `.env`.

## Deployment

- The application is currently deployed on Heroku and auto-deploys to staging from Github master.
- Environment variables needed for fully-functional deployment include:
  - `ALEPH_API_KEY`: API key for the Barton API
  - `ALEPH_API_URL`: Base URL for the Barton API
  - `AWS_ACCESS_KEY_ID`: Access key for AWS S3 bucket access
  - `AWS_BUCKET_NAME`: Name of S3 bucket
  - `AWS_REGION_NAME`
  - `AWS_SECRET_ACCESS_KEY`: Secret key for AWS S3 bucket access
  - `IDP_CERT`: Cert for IDP where SAML SP is registered
  - `IDP_ENTITY_ID`: Entity ID for IDP where SAML SP is registered
  - `IDP_SSO_URL`: Single sign-on URL for IDP where SMAL SP is registered
  - `SECRET_KEY`: Application secret key, required by Flask
  - `SENTRY_DSN`: Optional, used to log exceptions to Sentry
  - `SP_ACS_URL`: ACS URL used by SAML SP (must be registered with IDP)
  - `SP_CERT`: Cert for SAML SP (must be registered with IDP)
  - `SP_ENTITY_ID`: Entity ID for SAML SP (must be registered with IDP)
  - `SP_KEY`: Private key for SAML SP

## Assumptions, of which there are several

- All items presented in the application require users to be MIT authenticated for access. Authentication is done via touchstone on any attempt to access item landing pages. This application is configured as a SAML SP with MIT's Touchstone service.
- All items presented in the application must be catalogued in Barton. Each item's metadata and file(s) are retrieved using its Barton bibliographic record number.
- Discovery is assumed to take place in Barton, and access is provided via a link to each item's URL, included in the Barton record for the item. Item URLs follow the format http://lib-ebooks.mit.edu/item/[Barton-record-number].
- All ebook files delivered by the application are stored in Amazon S3. Instructions for uploading files to our S3 bucket are documented in Cataloging.

## Serials

Serials are a special snowflake and have a separate view in order to present files by volume, in reverse chronological order. This is done via a complicated file naming scheme that is documented in Cataloging.

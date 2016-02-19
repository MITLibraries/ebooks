# Ebook Delivery Application #

This application was built to provide a simple delivery service for ebooks that are purchased or licensed by the libraries but not hosted by a vendor. The application presents a landing page for each ebook, on which all files associated with that item are displayed for download. "Ebook" in this case is a loose term that could refer to any item presented to the user as a file or collection of files. This application is format-agnostic; files are served to the user to the browser, and will be rendered by the browser when possible (e.g., PDF) or downloaded to be opened in another appropriate application.

## Assumptions, of which there are several ##
* The ebooks application was designed to be run on a Libraries apache server configured for Shibboleth, so authentication is assumed to be performed outside the application itself. 
* All items presented in the application must be catalogued in Barton. Each item's metadata and file(s) are retrieved using its Barton bibliographic record number.
* Discovery is assumed to take place in Barton, and access is provided via a link to each item's URL, included in the Barton record for the item. Item URLs follow the format http://[server-name].mit.edu/secure/ebooks/[Barton-record-number].
* Access to the Barton API is IP-based, so in order for the application to retrieve item metadata the machine running it must be on the approved IP list.
* The application was built and tested to run in Python 2.6. 

## Serials ##

Serials are a special snowflake and have a separate view in order to present files by volume, in reverse chronological order. This is done via a complicated file naming scheme that is documented in Cataloging.

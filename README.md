Map Of Life Point Uploader
===

Code for the registration and upload of user-provided datasets into Map Of Life's CartoDB infrastructure.

Author: [Javier Otegui](mailto:javier.otegui@gmail.com) 
Link to the application: [https://beta.mol.org](https://beta.mol.org) 

Changelog
---

**[v0.2 - GCS support]**

* Uploaded files stored in Google Cloud Storage
* Allow correct uploads of files larger than 1Mb
* Removed template option

[v0.1 - Initial release]

* Default values for missing fields
* Default values for empty records
* Support for non-ASCII characters (at least Spanish chars)
* Header alignment
* Extra fields
* Metadata

**BOLD** indicates live version.

What it does
---

This application enables a web site with a form for registered users and/or institutions to upload one or more collections of observations. These observations are uploaded to the Map Of Life CartoDB instance and, later, ingested in the general Map Of Life mapping infrastructure to enable integrated visualizations of the information. Some metadata are also stored for improved discoverability and dataset management.

How does it work?
---

The main data form allows the upload of all the information in a maximum of 4 steps.

### 1. File Upload

First of all, a file with the observations must be provided. This file should have one of the following formats:

* CSV
* TXT
* TSV

Fields should be separated using one of these separators:

* Comma ( , )
* Semicolon ( ; )
* Tab
* Pipe ( | )

If any of these requirements are not met, the file will not be accepted.

### 2. Header alignment

There is a minimum set of information each record must have in order to be usable in Map Of Life. This is translated to a set of fields that must be present in the file, and each record should have some value in these fields. These required fields are:

* Scientific name
* Latitude
* Longitude
* Precision of the coordinates (in meters)
* Date of the observation
* Who recorded the observation

In this section, the user is presented with this minimum set of required fields, and a system to indicate either if any of the fields in his/her file corresponds to these required fields, or a default value to be used for that field in all the records.

The application won't move forward until all fields have either a selected field or a default value. In some cases, it is good to have both filled, as a means to improve completeness of the dataset, since empty fields will be filled with the default value but complete fields will keep their value.

After aligning the headers, the application will parse the content of the file in search for basic quality issues. If something is wrong, it will fall back to the main page with a detailed report of what went wrong.

### 3. Extra headers (optional)

This step will only be shown if there are more fields than the default ones.

Here, all the extra fields in the file will show up, with the possibility of asigning a default DarwinCore term and a brief descripion to each one. Although optional, it is highly recommendable to fill everything in this form, since it will help other users understand the meaning of those fields.

### 4. Dataset metadata

The last step is providing some metadata about the dataset, such as title, scopes and persons behind it. Some of the fields are required, some are optional, but we recommend filling every field in the form to improve discoverability and for better understanding of the dataset.

### Finally

After the last step, the application will upload the information to two tables in the CartoDB instance of Map Of Life, one for the observations and another one for the associated metadata. These records will eventually be ingested in the mapping framework.

Accessibility
---
A working instance should be available via Google App Engine, currently accessible via the following URL:

[https://beta.mol.org](https://beta.mol.org) 

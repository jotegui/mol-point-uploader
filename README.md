Map Of Life Point Uploader
===

Code for the registration and upload of user-provided datasets into Map Of Life's CartoDB infrastructure.

Author: Javier Otegui (javier.otegui@gmail.com)

Changelog
---

* Dev branch: Changes
	* Default values for missing fields
	* Default values for empty records
	* Support for non-ASCII characters (at least Spanish chars)
* *Master branch: Initial release
	* Header alignment
	* Extra fields
	* Metadata

(*) Indicates live version

What it does
---

This application enables a web site with a form for registered users and/or institutions to upload one or more collections of observations. These observations are uploaded to the Map Of Life CartoDB instance and, later, ingested in the general Map Of Life mapping infrastructure to enable integrated visualizations of the information. Some metadata are also stored for improved discoverability and dataset management.

How does it work?
---

The application is available via a Google App Engine instance, ideally accessible via this url:

http://point-uploads.map-of-life.appspot.com/

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

In later steps, the content of the file is parsed for basic completeness and quality. We offer a template with the best format and set of fields, which we highly recommend. In case the template is used, there is an option to indicate so, and some checks might be ignored.

### 2. Header alignment (only without template)

If the "Template used" checkbox is checked, this step will be ommitted. The application will, however, check if the template is actually used. If file headers are different from the template ones, the user will be redirected to this section.

There is a minimum set of information each record must have in order to be usable in Map Of Life. This is translated to a set of fields that must be present in the file, and each record should have some value in these fields. These required fields are:

* Scientific name
* Latitude
* Longitude
* Datum the coordinates are recorded with
* Precision of the coordinates (in meters)
* Date of the observation
* Who recorded the observation

In this section, the user is presented with this minimum set of required fields, and a system to indicate either if any of the fields in his/her file corresponds to these required fields, or a default value to be used for that field in all the records.

The application won't move forward until all fields have either a selected field or a default value. In some cases, it is good to have both filled, as a means to improve completeness of the dataset, since empty fields will be filled with the default value but complete fields will keep their value.

After aligning the headers, the application will parse the content of the file in search for basic quality issues. If something is wrong, it will fall back to the main page with a detailed report of what went wrong.

### 3. Extra headers (optional)

This step will only be shown if there are more fields than the default ones (or the ones in the template).

Here, all the extra fields in the file will show up, with the possibility of asigning a default DarwinCore term and a brief descripion to each one. Although optional, it is highly recommendable to fill everything in this form, since it will help other users understand the meaning of those fields.

### 4. Dataset metadata

The last step is providing some metadata about the dataset, such as title, scopes and persons behind it. Some of the fields are required, some are optional, but we recommend filling every field in the form to improve discoverability and for better understanding of the dataset.

### Finally

After the last step, the application will upload the information to two tables in the CartoDB instance of Map Of Life, one for the observations and another one for the associated metadata. These records will eventually be ingested in the mapping framework.

Requirements
---

In principle, no requirements are needed since this is a Google App Engine instance, accessible online. However, in order to make a local copy work, Python 2.7 must be installed, with the following modules available:

* Flask - To handle the web framework
* Requests - To handle requests to CartoDB

Accessibility
---
A working instance should be available via Google App Engine, ideally accessible through the point-uploads subdomain of the map-of-life appspot:

http://point-uploads.map-of-life.appspot.com/

Development
---

To launch a local version, make sure the Google App Engine SDK for python is installed and the base folder is added to the `$PATH` envvar (so that `dev_appserver.py` and `appcfg.py` are accessible directly). Then simply execute:

    ./launch.sh

And a new instance will be available via `localhost:8080`.

**CAUTION**: Even though it's a local instance, all uploads will try to go directly to CartoDB, and without the proper API key, uploads will probably fail. Make sure to change the CartoDB instance in the code to point uploads to the proper database and tables.

Deployment
---

When changes are made to the code base, deploy those changes with the following script

    ./deploy.sh

Which will commit changes in the App Engine instance to the `point-uploads` version of the `mol-api` application
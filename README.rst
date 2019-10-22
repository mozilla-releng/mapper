Mapper
------

When we convert hg repositories to git, and vice versa, the hg changeset SHA
(the 40 character hexadecimal string that you get when you commit a change) is
different to the git commit id (the equivalent SHA used by git).

In order to keep track of which hg changeset SHAs relate to which git commit
SHAs, we keep a database of the mappings, together with details about the
project the SHAs come from, and what time they were inserted into the database.

The vcs sync tool (checked into mozharness) is the tool which performs the
conversion between hg repos and git repos, and this is documented separately.
It is responsible for performing the conversion - this is outside the scope of
mapper.

Mapper is an HTTP API that allows:

- insertion of new mappings and projects (a "project" is essentially the name
  of the repo - e.g. build-tools) (HTTP POST)
- insertion of git/hg mappings for a given project (HTTP POST)
- retrieval of mappings for a given project (HTTP GET)

Behind the scenes, it is reading/writing from the database (using sqlalchemy).

.. note::
   The vcs sync tool is a client of the mapper: it is vcs sync that inserts
   into mapper (i.e. uses the HTTP POST methods).

The other clients of mapper are:

- people / developers - wanting to query mappings
- ``b2g_build.py`` - the build script for b2g - since this needs to lookup
  SHAs in order to reference frozen commit versions in manifests


Request authentication credentials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`Open a bug on bugzila`_ and request new taskcluster client credentials that
that you will then use in.

Use the following points to guide you opening the bug:

#. **Product** field should be ``Release Engineering``
#. **Component** field should be ``Applications: Mapper``
#. **Summary** field should be ``Requesting taskcluster client credentials to use with mapper``
#. **Description** field should contain:

   - who is the responsible person and which is the responsible team
   - what is the purpose of usage
   - what should be the expiration date of the credentials (suggested is one year)
   - which level of access is required:

     - Create new project
     - Insert mappings

.. _`Open a bug on bugzila`: https://bugzilla.mozilla.org/enter_bug.cgi?product=Release%20Engineering&component=Applications%3A%20Mapper


How to generate taskcluster client credentials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Go to https://tools.taskcluster.net/auth/clients.

#. Make sure you are logged into taskcluster.

#. Fill the ``Create New Client`` form:

   :ClientId: Make sure to include the Bug number by following the template
              ::
                  project/releng/services/mapper/bug<NUMBER>

   :Description: Who is responsible and which team, also where is this token used.
   :Expires: Requested expiration, by default set it to 1 year.
   :Client Scopes: List of scopes requested based on the requested level of access:

      - Create new project
        ::
           project:releng:services/mapper/api/project/insert

      - Insert mappings
        ::
           project:releng:services/mapper/api/mapping/insert

#. Send ``clientId`` and ``accessToken`` in a JSON authentication file via
   https://send.firefox.com. Format of authentication file should be:

   .. code-block:: json
      {
          "clientId": "project/releng/services/mapper/bug<NUMBER>",
          "accessToken": "<TOKEN-WHICH-WAS-PROMPTED-IN-TASKCLUSTER-TOOLS>"
      }
.. _`Rok Garbas`: https://phonebook.mozilla.org/?search/Rok%20Garbas
.. _`Release Engineering`: https://wiki.mozilla.org/ReleaseEngineering#Contacting_Release_Engineering


Local Development
^^^^^^^^^^^^^^^^^

Use `docker-compose up` to run `api` (and postgresql database). The API will be
available at https://localhost:8004/apidocs. When visiting
https://localhost:8004 you will be redirected to the location of the frontend.


Deployment process
^^^^^^^^^^^^^^^^^^

To trigger the deployment you have to push the code to the branch with the same
name as environment you want to deploy to.

This will start Taskcluster graph which will build and push docker
image to docker hub (`mozilla/releng-mapper`_) with the same tag as is the
environment.

Cloudops team Jenkins is listening for the change and will deploy it to `GCP`_
once it confirms that the docker images was build in a trusted environment. It
usually takes around 5min for deployment to be done. For more how things are 
configures you can check `cloudops infrastructure`_.:

You can check that the service was deployed correctly by visiting the
``/__version__`` endpoint which should include

.. _`GCP`: https://cloud.google.com
.. _`mozilla/releng-mapper`: https://hub.docker.com/r/mozilla/releng-mapper
.. _`cloudops infrastructure`: https://github.com/mozilla-services/cloudops-infra/tree/master/projects/relengapi/


Deployed Environments
^^^^^^^^^^^^^^^^^^^^^

We have a number of deployed ToolTool environments.

- Dev

   :URL: https://mapper.testing.mozilla-releng.net/
   :Taskcluster Secret: project/releng/mapper/config:dev
   :Taskcluster Client ID: project/releng/mapper/dev


- Staging

   :URL: https://mapper.staging.mozilla-releng.net/
   :Taskcluster Secret: project/releng/mapper/config:staging
   :Taskcluster Client ID: project/releng/mapper/staging

- Production

   :URL: https://mapper.mozilla-releng.net/
   :Taskcluster Secret: project/releng/mapper/config:production
   :Taskcluster Client ID: project/releng/mapper/production

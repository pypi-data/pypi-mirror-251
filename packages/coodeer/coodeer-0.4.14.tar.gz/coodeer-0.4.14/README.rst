README
======

Library and CLI Tool for creating minimalistic, local debian packages repository.
Debian packages are expected to reside in an S3 bucket.
The ``dpkg-scanpackages`` is required to be locally installed.

CLI Usage
---------

Prerequisites
"""""""""""""

Set up environment variables: AWS Credentials and default bucket name.

.. code:: console

    # copy example files
    # envrc (https://direnv.net/)
    cp .envrc.example .envrc
    # .. add AWS credentials if needed, adjust bucket ..
    direnv allow

Upload debian packages
""""""""""""""""""""""

.. code:: console

    coodeer upload example-dependencies_1.23_all.deb
    coodeer upload example_1.23.0_all.deb
    coodeer upload example_1.23.1_all.deb


Publish (default) specification
"""""""""""""""""""""""""""""""

.. code:: console

    coodeer publish repository-specification.example.yaml

Create repositories
"""""""""""""""""""

.. code:: console

    coodeer create /tmp/my-repositories

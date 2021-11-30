.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/arbiterd.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/arbiterd
    .. image:: https://readthedocs.org/projects/arbiterd/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://arbiterd.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/arbiterd/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/arbiterd
    .. image:: https://img.shields.io/pypi/v/arbiterd.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/arbiterd/
    .. image:: https://img.shields.io/conda/vn/conda-forge/arbiterd.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/arbiterd
    .. image:: https://pepy.tech/badge/arbiterd/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/arbiterd
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/arbiterd

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

.. image:: https://img.shields.io/badge/security-bandit-yellow.svg
    :target: https://github.com/PyCQA/bandit
    :alt: Security Status

.. image:: https://github.com/SeanMooney/arbiterd/actions/workflows/tox.yml/badge.svg
    :target: https://github.com/SeanMooney/arbiterd/actions/workflows/tox.yml/badge.svg
    :alt: Tox CI Status

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

.. image:: https://readthedocs.org/projects/arbiterd/badge/?version=latest
   :alt: ReadTheDocs
   :target: https://arbiterd.readthedocs.io/en/stable/
|

========
Arbiterd
========


    Arbiterd - power and performance arbiter daemon


Arbiterd is a work in progress python daemon for the management
of server power usage and performance with integration with OpenStack-nova.

Arbiterd is currently pre-alpha in the early stages of bootstrapping and should not be used in any production environment.


.. _pyscaffold-notes:

Making Changes & Contributing
=============================

This project uses `pre-commit`_, please make sure to install it before making any
changes::

    pip install pre-commit
    cd arbiterd
    pre-commit install

It is a good idea to update the hooks to the latest version::

    pre-commit autoupdate

Don't forget to tell your contributors to also install and use pre-commit.

.. _pre-commit: https://pre-commit.com/

This project uses tox to execute tests, build docs and automate other development task that are not suitable for automation via pre-commit.

Note
====

This project has been set up using PyScaffold 4.1.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.

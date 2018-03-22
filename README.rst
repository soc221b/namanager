=========
namanager
=========

.. include-documentation-begin-marker

.. image:: https://travis-ci.org/iattempt/namanager.svg?branch=master
        :target: https://travis-ci.org/iattempt/namanager

.. image:: https://ci.appveyor.com/api/projects/status/ovpdobns85n3d86k/branch/master?svg=true
        :target: https://ci.appveyor.com/project/iattempt/namanager/branch/master

.. image:: https://codecov.io/gh/iattempt/namanager/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/iattempt/namanager


A file or/and directory name manager which could determine names are/aren't expectable, and you could also automatically rename it.

.. include-documentation-end-marker


Features
--------

* Match or ignore particular files/directories.
* Supports checking of most common format of letter-cases (upper, lower, camel, and pascal-case).
* Supports checking of convention of word separators (underscore-to-dash/dash-to-underscore).

How to use?
-----------

Installation
~~~~~~~~~~~~

* First of all check you already have **pip** installed, and then just type in :code:`pip install namanager`

Running
~~~~~~~

1) Configure your *settings.json*.

2) Run command :code:`namanager` or :code:`namanager --settings /path/to/your/settings` if the settings file not existed in your current working directory or CWD.

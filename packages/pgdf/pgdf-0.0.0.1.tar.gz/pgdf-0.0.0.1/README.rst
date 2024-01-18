====
pgdf
====

Tool built with **p**ython to summarize **g**it **d**if**f**

**********
Motivation
**********

This tool can put diffs into Excel.

************
Installation
************

This tool is installed with pip:

.. code-block:: bash

    $ pip install pgdf

*****
Usage
*****

Go to the Git repository directory, then:

.. code-block:: bash

    $ pgdf 09c03f56 93496ef3
    $ pgdf 09c03f56 93496ef3 dir/path file/path
    $ pgdf feature/something origin/main

It generates an Excel file that contains summary of the differences.

************
Excel Format
************

The output excel file contains two sheets, :code:`Summary` and :code:`Diff`.

**Summary**

The summary sheet contains the summary of the differences.
It is same as the result of `git diff --stats` for the specified commits.

**Diff**

The diff sheet contains the differences of the markdown files.



************
PyPI package
************

https://pypi.org/project/pgdf/

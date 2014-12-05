|Build Status|

Shortstack
==========

Today
-----

Shortstack is a Python web application that does a very simple thing:
render `Jinja2 <http://jinja.pocoo.org/docs/dev/>`__ templates from an
on-disk project folder that resembles a traditional website (so, the URL
/foo/ will be served by the *template* foo/index.html). You might find
it useful for prototypes and simple websites.

What's next
-----------

We're working on an extension system (`planning
wiki <https://github.com/cfpb/shortstack/wiki/Extensions>`__) that will
make it easy to incorprate data and services from any source into a
Shortstack site.

Extensions will be able to:

-  add information to the template context, either globally on based on
   URL patterns.
-  provide more complex rules for resolving URL's to templates (for
   example, specifying that URL's like /blog/my\_post/ will use the
   template at \_layouts/articles.html)
-  return a list of all URL's that the extension adds. (for generating
   static sites)
-  Register
   `filters <http://jinja.pocoo.org/docs/dev/api/#writing-filters>`__
   and `tests <http://jinja.pocoo.org/docs/dev/api/#writing-tests>`__

Shortstack will shine when used as a rendering engine for content that
may live in your CMS, data files, microservices, search index, or all of
the above.

Other things on the to-do list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Generate a static HTML version of a site
-  Flesh out the documentation with
   `sphinx <https://pythonhosted.org/an_example_pypi_project/sphinx.html>`__

Make it go
----------

We're working on a simpler demo project, but in the meantime, give it a
try with `Owning a Home <https://github.com/cfpb/owning-a-home>`__!

Follow the instructions to build the front-end resources (node, grunt,
bower, etc) while ignoring the stuff about Sheer and Elasticsearch.

Make and activate `a new
virtualenv <https://virtualenv.pypa.io/en/latest/virtualenv.html#usage>`__
using your favorite method (we like
`virtualenvwrapper <https://virtualenvwrapper.readthedocs.org/en/latest/>`__),
and check out this repository to a folder on your computer somewhere.

Install shortstack (and all of it's dependencies) into your virtualenv
with:

::

    pip install -e /path/to/shortstack

Then, start the local server with:

::

    cd /path/to/owning-a-home/dist/

    shorts serve --url /owning-a-home/

You should then be able to open your web browser to
http://localhost:7000/ and view the site!

What just happened?
~~~~~~~~~~~~~~~~~~~

The page you're looking at has been rendered through Jinja2. You may
have noticed that you were redirected to /owning-a-home/. This "site"
was actually built to be deployed at that path on a server, so we passed
that --url argument so that links keep working.

Run the tests
-------------

We use `tox <https://tox.readthedocs.org/en/latest/>`__ to test against
Python versions 2.6,2.7,3.3, and 3.4

::

    cd /path/to/shortstack
    pip install tox
    tox

If you are missing any of those Python versions, tox will complain. You
can limit tox to testing a particualr python, like so:

::

    tox -e py27,py34

If you just want to see the coverage report, or pylint output:

::

    tox -e coverage

or ``tox -e pylint``

Open source licensing info
--------------------------

1. `TERMS <TERMS.md>`__
2. LICENSE
3. `CFPB Source Code
   Policy <https://github.com/cfpb/source-code-policy/>`__

.. |Build Status| image:: https://travis-ci.org/cfpb/shortstack.svg
   :target: https://travis-ci.org/cfpb/shortstack

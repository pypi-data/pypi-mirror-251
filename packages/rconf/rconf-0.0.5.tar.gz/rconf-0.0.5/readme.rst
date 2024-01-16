########################################################################
RConf
########################################################################

************************************************************************
What
************************************************************************

.. from src/__init__.py

Extensible Python package to resolve references and apply patches in
`JSON <https://datatracker.ietf.org/doc/html/rfc8259>`_ and
`TOML <https://toml.io/en/v1.0.0>`_ configurations.

It uses Python's
`json module <https://docs.python.org/3/library/json.html>`_ and
`tomllib module <https://docs.python.org/3/library/tomllib.html>`_ to decode,
handles local and remote reference URLs using
`urllib <https://docs.python.org/3/library/urllib.html>`_,
and resolves document fragments specified through pointers,
optionally applying patches.

- References follow the
  `JSON Reference draft <https://datatracker.ietf.org/doc/html/draft-pbryan-zyp-json-ref-03>`_.
- Reference patches are based on
  `RFC 6902 <https://datatracker.ietf.org/doc/html/rfc6902>`_,
  extended with shorthand notations, an *assign* and a *merge* operation.
- JSON pointers follow
  `RFC 6901 <https://datatracker.ietf.org/doc/html/rfc6901>`_.
- TOML pointers are
  `TOML keys <https://toml.io/en/v1.0.0#keys>`_
  extended with array indices.


It can be used as a drop-in replacement for

- ``json.load`` and ``tomllib.load`` (``rconf.load``),
- ``json.loads`` and ``tomllib.loads`` (``rconf.loads``),

with an additional ``rconf.loadu`` to load URLs and local paths
and ``rconf.loadc`` to load a Python ``dict``.
These functions all resolve references and apply patches.


************************************************************************
Why
************************************************************************

``rconf`` allows a developer to

- not care about configuration location (URLs) and
- not care about configuration format (decoders),

and a user to

- reduce duplication by allowing URLs,
- reduce duplication by allowing references,
- reduce duplication by allowing patches and
- mix and match formats already in use.


************************************************************************
How
************************************************************************

Installation
========================================================================

.. from docs/index.rst

RConf is `pip <https://pip.pypa.io>`_-installable:

.. code-block:: console

    $ pip install rconf


Load a URL (with fragment pointer)
========================================================================

This snippet loads a document from a URL,
and resolves the pointer in its fragment:

.. code-block:: python

  import json
  import rconf

  config = rconf.loadu("https://github.com/manifest.json#/icons/0")
  print(json.dumps(config, indent=4))

.. code-block:: json

  {
      "sizes": "114x114",
      "src": "https://github.githubassets.com/apple-touch-icon-114x114.png"
  }

or, with an explicit pointer,

.. code-block:: python

  import json
  import rconf

  config = rconf.loadu(
      "https://raw.githubusercontent.com/pypa/build/main/pyproject.toml",
      ptr="project.description",
  )
  print(json.dumps(config, indent=4))


.. code-block:: json

  "A simple, correct Python build frontend"


Load and patch a string
========================================================================

The string (``config``) contains a JSON document with a reference (``$ref``)
and a patch assignment for ``/name``.

.. code-block:: python

  import json
  import rconf

  config = rconf.loads("""
  {
      "github-icon": {
          "$ref": "https://github.com/manifest.json#/icons/0",
          "/name": "GitHub icon"
      }
  }
  """)
  print(json.dumps(config, indent=4))

.. code-block:: json

  {
      "github-icon": {
          "sizes": "114x114",
          "src": "https://github.githubassets.com/apple-touch-icon-114x114.png",
          "name": "GitHub icon"
      }
  }


Mix and patch
========================================================================

Formats can be mixed,
like this JSON document referencing a TOML document,
patched with a ``$patch`` array using both the full and shorthand notations.

.. code-block:: python

  import json
  import rconf

  config = rconf.loads("""
  {
      "$ref": "data:application/toml;base64,W3Byb2plY3RdCnRpdGxlID0gIlByb2plY3QgdGl0bGUiCmRlc2NyaXB0aW9uID0gIlByb2plY3QgZGVzY3JpcHRpb24iCnJlYWRtZSA9ICJyZWFkbWUubWQiCg==",
      "$patch": [
          {"op": "move", "path": "/project/name", "from": "/project/title"},
          ["-", "/project/readme"],
          ["+", "/project/dynamic", ["version"]]
      ]
  }
  """)
  print(json.dumps(config, indent=4))

.. code-block:: json

  {
      "project": {
          "description": "Project description",
          "name": "Project title",
          "dynamic": [
              "version"
          ]
      }
  }


Command Line Interface
========================================================================

.. from docs/usage.rst

``rconf`` is added as a CLI tool,
to translate JSON and TOML files with (or without) references and patches,
and works with URLs or file paths.

.. code-block:: console

  $ rconf dump https://github.com/manifest.json#/icons/0
  {
      "sizes": "114x114",
      "src": "https://github.githubassets.com/apple-touch-icon-114x114.png"
  }

``rconf dump`` behavior can be modified with a configuration file.
``rconf config`` can show or create an example.

Those using bash/zsh can activate auto completion,
provided by `argcomplete <https://kislyuk.github.io/argcomplete>`_.

.. code-block:: console

    $ pip install rconf[sh]
    $ activate-global-python-argcomplete --user


************************************************************************
Definitions
************************************************************************

Definitions can be found on the
`definitions <http://fthyssen.github.io/rconf/definitions.html>`_ page.


************************************************************************
Usage
************************************************************************

A more thorough description can be found on the
`usage <http://fthyssen.github.io/rconf/usage.html>`_ page,
with details in the
`reference <http://fthyssen.github.io/rconf/reference.html>`_.

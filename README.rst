This module provides Pygments_ with a lexer for BitBake_ files. To
install, run the usual ::
    
    $ sudo python setup.py install

This will register the BitBake lexer as a Pygments plugin so that
``pygmentize`` et al. can use it. The lexer will be used for files
matching ``*.bb``, ``*.bbclass``, ``*.inc``, and ``*.conf``.

.. _Pygments: http://pygments.org/
.. _BitBake: http://bitbake.berlios.de/manual/

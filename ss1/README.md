Capture The Flag for SonarSource! (v1)
======================================

Build a docker image for an internal security challenge at SonarSource.

Requirements
------------

Software:

* `pwgen` -- for generating random passwords
* `docker` -- obviously

Building the image
------------------

Regenerate the passwords:

    ./configure.sh

Build the image:

    ./build.sh

Run tests:

    # TODO the solutions are not included, must be fetched
    ./run-tests.sh

Disclaimer
----------

The challenges are based on an [online contest organized by Stripe][stripe1].

Solutions
---------

The solutions are intentionally omitted from this project.

Please keep your own solutions private.

Links
-----

* [Online contest by Stripe (v1)][stripe1]
* [How to exploit buffer overflows ("smash the stack")](https://insecure.org/stf/smashstack.html)
* [The CTF ASCII art generator](http://patorjk.com/software/taag/#p=testall&f=Graffiti&t=CTF)

[stripe1]: https://stripe.com/blog/capture-the-flag

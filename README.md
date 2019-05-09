Capture The Flag!
=================

Remaster Linux Live CD images for the purpose of creating ready to
use security wargames with pre-installed vulnerabilities to exploit.


Requirements
------------

You will need the following in order to build the Live CD using
the scripts in this project:

* Linux, with root access using `sudo`
* `git`
* `make`, `gcc` -- for building vulnerable programs
* `pwgen` -- for generating random passwords
* `rsync`
* `genisoimage` -- for `mkisofs`
* `advancecomp` -- for `advdef`
* `squashfs-tools` -- for `unsquashfs`
* `curl` -- for downloading packages and other files


Requirements when building in 64-bit systems
--------------------------------------------

The base Live CD is 32-bit, and therefore the C programs
must be built 32-bit too. In order to do that you need
to install 32-bit development libraries. In Debian for
example the package is called `libc6-dev-i386`.


Building the Live CD
--------------------

You have different options to build the CD:

* Basic build: using a single script to build everything
* 3-step build: 3 steps to give you a chance to customize
* Expert build: if you want to understand everything

Choose whichever method is most suitable for you.


Basic build (for the impatient)
-------------------------------

To fetch all the necessary files including the 8MB TinyCore base
base image, the hacking contest data and all the required TinyCore
packages and remaster the CD:

    ./scripts/rebuild.sh

Note: some of the steps need to run `sudo`, so you will be prompted
for your password one or more times.


3-step build
------------

The idea of this build method is to create the basic CD data but stop
before rebuilding the image so that you can customize it first.

1. Build the basic CD data:

        ./scripts/build.sh

   Note: some of the steps need to run `sudo`, so you will be
   prompted for your password one or more times.

2. Customize the contents in the `extract` directory. This step is
   completely up to you, depending on what you want to customize.
   You might want to install some custom packages, for example
   keymaps for non US keyboards:

        sudo ./scripts/install-tcz.sh kmaps

3. Create the final ISO:

        sudo ./scripts/pack-iso.sh


Disclaimer
----------

The challenges are based on the original online contest
organized by Stripe:
https://stripe.com/blog/capture-the-flag


Using the Live CD
-----------------

See http://janosgyerik.github.com/capture-the-flag/


Screenshots
-----------

![Start](https://github.com/janosgyerik/capture-the-flag/raw/master/images/start.png)
![End](https://github.com/janosgyerik/capture-the-flag/raw/master/images/end.png)


Solutions
---------

The solutions are intentionally omitted from this project.
You can find the solutions to the original Stripe challenges on the internet,
but don't be surprised if they won't work on this Live CD out of the box.
That's intentional too ;-)

Please keep your own solutions private.


Abusing the CD
--------------

If you want to get root access in the live system,
you can either do `su - tc` to become the admin user,
or boot the system with the `mc superuser` boot option.
This is no secret, and you won't learn anything this way.


Links
-----

* [Latest ISO image](https://github.com/janosgyerik/capture-the-flag/releases/download/v1.0/ctf1-r14.iso)
* [Blog announcement of Capture The Flag, by Stripe](https://stripe.com/blog/capture-the-flag)
* [Blog announcement of Capture The Flag 2.0, by Stripe](https://stripe.com/blog/capture-the-flag-20)
* https://insecure.org/stf/smashstack.html
* [Tiny Core Linux](http://distro.ibiblio.org/tinycorelinux/)
* [The CTF ASCII art generator](http://patorjk.com/software/taag/#p=testall&f=Graffiti&t=CTF)

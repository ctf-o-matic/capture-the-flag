ctf-o-matic
===========
Remaster Linux Live CD images for the purpose of creating ready to
use hacking contests with pre-installed vulnerabilities to exploit.


Requirements
------------
You will need the following in order to build the Live CD using
the scripts in this project:

* Linux, with root access using `sudo`
* `git`
* `make`, `gcc` -- for building vulnerable programs
* `pwgen` -- for generating random passwords
* `genisoimage` -- for `mkisofs`
* `advancecomp` -- for `advdef`
* `squashfs-tools` -- for `unsquashfs`
* `curl` -- for downloading packages and other files


Building the Live CD
--------------------
You have different options to build the CD.

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


Todo
----
* Add build number or revision indicator on boot screen

* Re-implement /levels/level02/level02.py without flask (save 3MB)

* Implement the second Capture The Flag contest of Stripe

* maybe: Generalize the scripts to use with other than TinyCore


Disclaimer
----------
The challenges are based on the original online contest
organized by Stripe:
https://stripe.com/blog/capture-the-flag


Links
-----
* https://stripe.com/blog/capture-the-flag
* https://stripe.com/blog/capture-the-flag-20
* http://io.smashthestack.org:84/
* http://patorjk.com/software/taag/#p=testall&f=Graffiti&t=CTF



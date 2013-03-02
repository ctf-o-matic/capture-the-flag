ctf-o-matic
===========
Remaster Linux Live CD images for the purpose of creating ready to
use hacking contests with pre-installed vulnerabilities to exploit.

**IMPORTANT: this is a work in progress**


Requirements
------------
You will need the following in order to build the Live CD using
the scripts in this project:

* Linux, with root access using `sudo`
* `git`
* `make`
* `gcc`
* `pwgen` -- for generating random passwords
* `genisoimage` -- for `mkisofs`
* `advancecomp` -- for `advdef`
* `squashfs-tools` -- for `unsquashfs`
* `curl`


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
Create the basic CD data but stop before rebuilding the image to
give you a chance to customize.

1. Build the basic CD data:

        ./scripts/build.sh

   Note: some of the steps need to run `sudo`, so you will be
   prompted for your password one or more times.

2. Install custom packages, for example keymaps for non US keyboards:

        sudo ./scripts/install-tcz.sh kmaps

3. Create the final ISO:

        sudo ./scripts/pack-iso.sh


Progress
--------
* Verified levels: 1, 3
* *Should* work but not verified levels: 4, 6


Todo
----
* Verify that levels 4, 6 work.

* Setup levels 2 and 5 (require web server, php, python)

* Add software inside the live cd:
    - lighttpd
    - php
    - curl or wget or both
    - gdb
    - objdump
    - perl
    - python

* maybe: Generalize the scripts to use with other than TinyCore

* maybe: Implement the second Capture The Flag contest of Stripe

* Explain how to switch the keymap when booting the livecd (i.e : mc kmap=azerty/fr rom french) 


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



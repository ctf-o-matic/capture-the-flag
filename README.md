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
* `make`, `gcc` -- for building vulnerable programs
* `pwgen` -- for generating random passwords
* `rsync`
* `genisoimage` -- for `mkisofs`
* `advancecomp` -- for `advdef`
* `squashfs-tools` -- for `unsquashfs`
* `curl` -- for downloading packages and other files


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
* Setup level 2 (requires web server, maybe lighttpd?)

* Confirm that level 4 can be hacked

* Setup level 5 and confirm it can be hacked

* Confirm that level 6 can be hacked

* maybe: Generalize the scripts to use with other than TinyCore

* maybe: Implement the second Capture The Flag contest of Stripe


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



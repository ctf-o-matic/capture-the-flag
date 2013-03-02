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
* `pwgen`
* `genisoimage`
* `advancecomp`
* `squashfs-tools`
* `curl`


How to use
----------
1. Download the smallest TinyCore Linux live cd image from: 
   http://distro.ibiblio.org/tinycorelinux/downloads.html

2. Copy or symlink the live cd image file to `livecd.iso`

3. Get the files of the first Capture The Flag contest from GitHub:

        ./scripts/get-ctf1.sh

4. Unpack the live cd image:

        sudo ./scripts/unpack-iso.sh
        # TODO: we should not need root here

5. Unpack the squashfs image inside the live cd

        sudo ./scripts/unpack-squashfs.sh
        # TODO: do we really need root here?

6. Install software:

        sudo ./scripts/install-openssh.sh

7. Setup the capture the flag challenges:

        sudo ./scripts/setup-ctf1.sh

8. Rebuild the iso:

        sudo ./scripts/repack.sh
        # TODO: do we really need root here?


Progress
--------
* Verified levels: 1, 3
* *Should* work but not verified levels: 4, 6


Todo
----
* Use `sudo` *inside* the scripts, only when necessary, and eliminate
  all the `sudo` calls from the above steps if possible

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



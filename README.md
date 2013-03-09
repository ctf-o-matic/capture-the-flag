ctf-o-matic
===========
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


Disclaimer
----------
The challenges are based on the original online contest
organized by Stripe:
https://stripe.com/blog/capture-the-flag


Solutions
---------
The solutions are intentionally omitted from this project.
You may find the solutions to the original Stripe challenges,
but don't be surprised if they don't work on this Live CD.
That is intentional too ;-)

However, the solutions already reveal too much information,
so for maximum enjoyment of this contest-on-a-CD it is best
to not look for the solutions at all.

Please keep your own solutions private.


How to use the CD
-----------------
The easiest way to use is with a software like VirtualBox,
for example by following these steps:

1. Create a new virtual machine: Linux, 2.6 kernel
2. Memory: 256MB
3. Hard disk: no need for a disk
4. CD: configure the virtual machine to use the ISO image
   of the Live CD as a CD drive
5. Start the Virtual Machine

At the boot prompt, you may want to enter `fr`, `jp` or `hu`
to use French, Japanese or Hungarian keymap, respectively.

All the regular boot options of TinyCore should work as well.


Screenshots
-----------
![Start](https://github.com/janosgyerik/ctf-o-matic/raw/master/images/start.png)
![End](https://github.com/janosgyerik/ctf-o-matic/raw/master/images/end.png)


Abusing the CD
--------------
The same way that you cannot really protect a system from an
attacker who has physical access to it, it is impossible to
protect the Live CD, so we did not even try to do that.

If you want to get root access in the live system, you can
either do `su - tc` to become the admin user, or boot the
system with the `mc superuser` standard TinyCore boot option.

Actually there is nothing wrong with this. The CD is more
user-friendly this way, as it gives you the opportunity to
install additional software you may prefer to use to pass
the challenges.


Links
-----
* https://stripe.com/blog/capture-the-flag
* https://stripe.com/blog/capture-the-flag-20
* http://io.smashthestack.org:84/
* http://patorjk.com/software/taag/#p=testall&f=Graffiti&t=CTF


Todo
----
* Re-implement /levels/level02/level02.py without flask (save 3MB)

* Implement the second Capture The Flag contest of Stripe

* maybe: Generalize the scripts to use with other than TinyCore



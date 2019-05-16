Capture The Flag! (v1, by Stripe)
=================================

The content of [Stripe's first Capture The Flag contest][stripe1-blog],
packaged as a Live CD in ISO format, as well as the scripts to build the ISO itself.

For "players"
-------------

If you just want to replay the levels of the contest,
head over to the [homepage of this contest][stripe1-play].

The rest of this document (as well as this entire repository) concerns the technical details of *packaging* the content, not for *consuming* it.
Enjoy!

Challenges when packaging a hacking contest
-------------------------------------------

*Which operating system to use as the base image?*

This was driven by some key elements of the contest:

- Each level is represented by a distinct user account, where the user's password is stored in a `.password` file, with restricted permissions, only accessible by the user itself.

- On each level, the `.password` file of a user could be accessed by exploiting vulnerabilities in a program running with the user's permissions.

  - On some levels the user was running the vulnerable program, and participants could interact with this running program through some HTTP port, and pass to it some malicious input to reveal the contents of the `.password` file. These vulnerable programs were written in PHP and Python.

  - On other levels the vulnerable program had the setuid bit set, so that participants could run it directly, and pass to it some malicious input to reveal the contents of the `.password` file. These vulnerable programs were written in C.

In short, the content of the contest requires:

- multiple user accounts
- an SSH server, to allow login to the user accounts
- multiple ports, handling HTTP requests
- PHP, and a web server to run PHP code
- Python
- setuid feature: the ability to run programs with the privileges of the file owner, instead of the current user
- C programs compiled into binary, on a vulnerable architecture
- basic hacking tools: the tools needed by participants to exploit the vulnerabilities of the programs, and other helpful tools, such as text editors and scripting tools to implement and execute exploit reasonably easily

Lastly, unrelated to the content of the contest,
to maximize the usability of the package,
its size should be as small as possible.

*What is the challenge in including C programs?*

The vulnerable C programs must be compiled on the same architecture as the base image. A simple and easy approach is to include C compilers in the image, with the drawback of increased size, as compilers can be large.

We could have used a separate build machine to compile the vulnerable programs and copy them to the image, without including the compiler. However, having the compiler and related build tools can be helpful for participants. Therefore, we have decided to include gcc despite the added disk size.

*What vulnerable architecture is needed for C programs?*

We are not security experts. To us, some of the vulnerabilities *seem* harder to exploit on modern architectures such as x64, compared to for example i386. We used an architecture where we could confirm that the levels are possible to pass.

*What is the challenge in supporting setuid feature?*

The shell on Tiny Core uses *busybox ash*,
which has a security feature to drop setuid privileges in some cases,
making some of the vulnerabilities difficult to recreate.
We were able to enforce setuid privileges by modifying the vulnerable programs to also include this:

    // circumvent busybox ash dropping privileges
    uid_t uid = geteuid();
    setreuid(uid, uid);

We were concerned that these modifications may confuse the participants,
so we made additional efforts to keep them hidden.

*What is the challenge in including PHP?*

PHP typically runs in a web server.
The level using PHP is not very interesting.
And it doesn't really require PHP, the vulnerability in questions could happen in any web framework.
Python is necessary for a higher, interesting level.
So we reimplemented the level to use Python instead of PHP.

Package as a Live CD
--------------------

To package as an ISO image that can be used as a Live CD in a virtualization software such as VirtualBox, see [livecd/README.md](livecd/README.md).

Package as a Docker image
-------------------------

Coming soon!

stripe1-blog: https://stripe.com/blog/capture-the-flag
stripe1-play: http://janosgyerik.github.com/capture-the-flag/stripe1

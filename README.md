SAUR the Emperor of AUR local repository management!
========================

SAUR (pronounced /zɑːr/) is a wrapper script around the excellent
[aurutils](//github.com/AladW/aurutils) for managing a ArchLinux repository.

_This script is based off a previous project of mine, see
[aur-pkg-scripts](//github.com/hv15/aur-pkg-scripts) for further details._

Purpose
-------

There are **a lot** of different AUR related scripts, however I didn't find any
suitable for my purposes, which are:

 * relatively straightforward way to automate building/distributing of packages
 * support an automated way to patch PKGBUILDs (and other files in AUR repository) before building
 * support sharing packages over LAN (and even Internet)

I tend to make certain modifications to some of the packages on the AUR (different build options,
changes to source code, etc.). Often I use these packages on more than one machine, the result
being that I duplicate a lot of work for myself.

I was inspired by projects like [aurto](https://github.com/alexheretic/aurto) and
[tomato](https://github.com/aji-prod/tomato) for this work, both of which are excellent solutions
for local AUR package management.

I make extensive use of [AladW](https://github.com/AladW)'s [aurutils](https://github.com/AladW/aurutils)
project here.

This is a _work-in-progress_, and will only be updated when/if I have the time/need.

Todo
----

 * documentation
 * add automatic way to remove package (currently it must all be done manually)
 * add SystemD Timers/Cronie job specs

Setup
-----

This script depends on `makepkg` and `aurutils`.

It is a good idea to have a dedicated build user with limited superuser rights
(via `sudo`). Here we refer to the user as `{BUILDUSER}`.

Create the repo database first:

```
sudo install -o {BUILDUSER} -d /var/cache/pacman/{REPO}/
sudo -u {BUILDUSER} repo-add /var/cache/pacman/{REPO}/{REPO}.db.tar
```

Interesting, hmmm
----------------

 * Guide on how to [leverage](https://disconnected.systems/blog/archlinux-repo-in-aws-bucket/#fetching-remote-changes)
   AWS S3 service to store the repo in the cloud.
 * [This](https://github.com/yujinakayama/pacman-repo) repo seems to be a valid ArchLinux package repository... maybe
   some GitHub-Pages magic like [NVIDIA repo](https://nvidia.github.io/nvidia-container-runtime/) for
   [nvidia-container-runtime](https://github.com/NVIDIA/nvidia-container-runtime)

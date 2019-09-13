An explanation of the organization and name scheme for the workspace \n
Version-control procedures
  We will be using Git. Each user story will be it's own small branch.
Tool stack description and setup procedure
Build instructions
Unit testing instructions
System testing instructions
Other development notes, as needed



# Fa19 CS2610 Lecture Notes Repository

These notes are an important means of communication from me to you.  You are
accountable for the information contained in these notes and are expected to
clone this repository to your computer to have instant access to this resource.

In addition to serving as a study guide throughout the semester, I will post
code written in class along with example programs and other important resources
to this repository.



## Creating a comprehensive study guide from individual lecture notes files

`concatenate.py` is a Python program written by Michael Hoffmann which
concatenates (joins) all lecture notes found in these directories into a
single, comprehensive file.  You may use this single file to easily find a
topic when you don't remember on which day it was covered or to create a study
guide for an exam.  Only lecture notes files are included; extra files such as
code, images and media are not included.

This program creates a read-only file called `all_notes.md`.  This file is
marked read-only to remind you to not make any important changes as they would
be destroyed the next time you ran this program.



## Instructions:

1. Run `git pull` to get the latest, most up-to-date lecture notes
2. Open a command shell in which Python is available (on Windows this is the
   Anaconda Prompt)
3. Run `python concatenate.py`
4. The resulting file is named `all_notes.md`

`concatenate.py` works best with Python 3, though it is backwards-compatible
with Python 2.

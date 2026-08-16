OverTheWire Bandit CTF --- Learning & Practical Write-Up

Overview

This repository documents my journey through the OverTheWire Bandit
CTF, a beginner-friendly Linux and cybersecurity challenge designed to
build practical command-line, Linux, SSH, file-system, scripting,
permissions, and Git skills.

The goal was not simply to collect passwords, but to understand how to
investigate a system, identify clues, choose the right command, and
solve problems step by step.

What I Learned

1. Linux Command Line Fundamentals

The Bandit levels provided hands-on practice with essential Linux
commands:

ls --- list files and directories

ls -la --- show hidden files and detailed permissions

cd --- navigate directories

pwd --- display the current directory

cat --- read file contents

file --- identify a file type

find --- search for files based on conditions

grep --- search text for patterns

sort --- sort lines

uniq --- identify repeated/unique lines

strings --- extract human-readable strings from binary files

head / tail --- inspect beginning/end of files

du --- inspect file/directory sizes

chmod --- change permissions

mkdir --- create directories

cp / mv --- copy and move files

rm --- remove files

echo --- print/write text

man --- read command documentation

The most important lesson was to inspect before acting:

ls -la
file filename
cat filename

2. Understanding Linux Permissions

I learned to interpret permission strings such as:

-rw-r----- 

Permissions are divided into:

owner | group | others

and include:

r = read
w = write
x = execute

I also encountered SUID binaries, where a program can execute with
the privileges of its owner.

A key lesson:

Always inspect ownership and permissions before assuming that a file
can be modified or executed.

Useful command:

ls -la

3. Searching for Hidden Information

Several Bandit levels required finding files that were not immediately
obvious.

Important techniques included:

find /path -type f
find /path -size 1033c
find /path -readable
find /path -not -executable

The important mindset was to convert the challenge description into
search conditions.

For example:

human-readable + specific size + not executable

becomes a find command using multiple conditions.

4. Working with Encoded Data

Bandit introduced several forms of encoding and transformation.

I learned that encoded data is not necessarily encrypted data.

Examples of concepts encountered:

Base64

Hexadecimal

ROT-style transformations

Character substitution

Compression

File format identification

A useful workflow was:

file filename

followed by the appropriate decoding/decompression tool.

The main lesson:

Identify the format first; then choose the tool.

5. Compression and Archives

I worked with files that were repeatedly compressed or wrapped inside
different archive formats.

Important tools/concepts included:

gzip
bzip2
tar
xxd
file

The general workflow was:

identify file
    ↓
rename/extract if necessary
    ↓
identify resulting file
    ↓
repeat

This taught me not to assume that a file's extension tells the truth
about its contents.

6. SSH and Remote Linux Systems

SSH became one of the most important skills throughout Bandit.

Basic connection:

ssh username@host -p 2220

I learned:

what SSH is

how remote authentication works

why the port matters

how usernames/passwords are used

how SSH keys can replace passwords

how to troubleshoot SSH connection problems

I also learned that Windows PowerShell can behave differently from Linux
shells in some CTF situations, and that Command Prompt or Git Bash
can be useful alternatives.

7. SSH Private Keys

One of the more challenging levels introduced an SSH private key.

The important workflow was:

obtain private key
      ↓
save it correctly
      ↓
use it with SSH
      ↓
authenticate as the next user

Example:

ssh -i private_key -p 2220 username@bandit.labs.overthewire.org

I also learned how to verify whether a private key is valid:

ssh-keygen -y -f private_key

A major troubleshooting lesson was that copying a key manually can
corrupt its format. Downloading the original key with scp was much
safer.

8. Understanding Shells

One of the later levels used a non-standard login shell.

I learned to investigate a user's shell with:

cat /etc/passwd | grep username

For example:

bandit26:x:...:/home/bandit26:/usr/bin/showtext

This showed that the user's shell was not the normal /bin/bash.

The challenge then became:

Understand what program is being used as the shell and find a way to
escape into a normal shell.

This was an important introduction to shell restrictions and escape
techniques.

9. SUID Programs

I encountered binaries that were owned by another user and had the SUID
permission set.

A typical permission might look like:

-rwsr-x---

The important character is:

s

Instead of blindly executing a suspicious-looking binary, I learned to
investigate what it does.

Useful commands:

ls -la
file program
strings program
./program

Some Bandit levels intentionally provided a SUID program that could
execute commands with another user's privileges.

10. Basic Binary Analysis

Bandit also introduced binaries that could not simply be read with
cat.

For example:

cat bandit27-do

produced unreadable binary data.

Using:

file bandit27-do

helps identify what the file actually is.

Using:

strings bandit27-do

can reveal human-readable strings inside a binary.

This taught me an important forensic habit:

When normal text tools fail, identify the file before deciding what to
do next.

11. Git

The final section of Bandit introduced Git-based challenges.

I learned the basic Git workflow:

clone
  ↓
inspect
  ↓
modify
  ↓
add
  ↓
commit
  ↓
push

Basic commands:

git clone <repository>
git status
git log
git show
git branch
git add
git commit
git push

12. Git History Can Contain Sensitive Information

One of the important lessons was that information does not necessarily
exist only in the current version of a file.

Git keeps history.

Useful commands:

git log
git show

This taught me to investigate:

current files
      +
commit history
      +
branches
      +
tags

when looking for accidentally committed information.

13. .gitignore and Forced Addition

One of the final levels required creating:

key.txt

with specific content.

However, .gitignore prevented the file from being tracked normally.

I learned that:

git add -f key.txt

means:

Force Git to add this file even though it is ignored.

The final workflow was:

echo "May I come in?" > key.txt
git add -f key.txt
git commit -m "Add key"
git push origin master

The remote repository then processed the submitted file and provided the
next credential.

14. Git Configuration Troubleshooting

During the final Git challenge, my first commit failed with:

Author identity unknown

The solution was to configure Git:

git config user.name "bandit31"
git config user.email "bandit31@example.com"

Then:

git commit -m "Add key"

This was a useful real-world Git lesson: Git commits require an author
identity.

15. Troubleshooting Lessons

Bandit taught me that errors are often clues rather than dead ends.

Examples:

Permission denied

Instead of repeatedly trying to write somewhere:

ls -la
pwd

Check who owns the directory and whether I have write permission.

SSH key invalid format

Instead of manually recreating a private key, obtain the original file
correctly.

Git repository already exists

Instead of cloning again:

cd repo

and inspect the existing repository.

Git says "Everything up-to-date"

Check:

git status
git log

because the intended changes may never have been committed.

Command not working

Read the error message carefully before changing random things.

Key Cybersecurity Mindset Developed

The biggest takeaway from Bandit was not memorizing commands.

It was learning a repeatable investigation process:

1. Read the challenge carefully
        ↓
2. Identify what information is being given
        ↓
3. Inspect the environment
        ↓
4. Identify files, permissions, users and processes
        ↓
5. Form a hypothesis
        ↓
6. Use the simplest appropriate command
        ↓
7. Read the output/error carefully
        ↓
8. Adjust the approach
        ↓
9. Verify the result
        ↓
10. Document what was learned

Important Commands Cheat Sheet

Navigation

pwd
ls
ls -la
cd

Files

cat
file
head
tail
strings
find
grep

Permissions

ls -la
chmod

Users / System

whoami
id
cat /etc/passwd

SSH

ssh user@host -p 2220
ssh -i keyfile user@host -p 2220
scp -P 2220 user@host:/remote/file .

Encoding / Transformation

base64
xxd
tr

Compression

gzip
bzip2
tar

Git

git clone
git status
git log
git show
git branch
git add
git commit
git push
git config

Skills Gained

By completing Bandit, I gained practical exposure to:

Linux command-line usage

Linux file systems

File permissions

User/group ownership

SUID binaries

SSH authentication

SSH private keys

Shell behavior

Restricted shells

File searching

Text processing

Encoding and decoding

Compression and archives

Basic binary analysis

Git repositories

Git history

.gitignore

Git commits and branches

Remote repositories

Troubleshooting authentication failures

Reading and interpreting command-line errors

CTF problem-solving methodology

Final Reflection

The OverTheWire Bandit CTF was my introduction to solving cybersecurity
problems through direct interaction with a Linux environment.

At the beginning, many commands such as find, grep, chmod, ssh,
and git were unfamiliar or confusing. As the levels progressed, I
learned to stop treating commands as isolated syntax and instead
understand why a particular command is useful in a particular
situation.

The most valuable lesson was the investigative mindset:

Don't guess. Inspect the system, understand the evidence, test your
hypothesis, and learn from the error messages.

Bandit provided a strong foundation for moving into more advanced
cybersecurity areas such as:

Linux security

Digital forensics

Network analysis

Web security

Privilege escalation

Penetration testing

Binary analysis

CTF competitions

Conclusion

Completing the Bandit CTF gave me practical confidence with Linux and
security fundamentals that cannot be gained from theory alone. Every
level required a combination of observation, command-line skills,
troubleshooting, and logical thinking.

The experience has strengthened my ability to approach unfamiliar
systems methodically and has provided a foundation for continuing into
more advanced cybersecurity and digital-forensics labs.

Bandit complete --- foundation built.

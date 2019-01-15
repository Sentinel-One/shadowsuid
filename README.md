# Linux Shadow SUID

This repository is part of SentinelOne's research done by Dor Dankner, of privilege persistance using `binfmt_misc`, which was named **Shadow SUID**.

Research Part I - https://www.sentinelone.com/blog/shadow-suid-for-privilege-persistence-part-1/
<br>
Research Part II - https://www.sentinelone.com/blog/shadow-suid-privilege-persistence-part-2/

The repository conatins the following files:

### locate_unique_suids.py

Looks for setuid file on your system, which has a unique 128 bytes header. That one can later be used as a legitimate setuid file for the shadow suid.

### shadow_suid.py

Install / Uninstall / List shadow suids.

Execute without paramteres to print the usage.

### interpreter_dummy.c

An example of a tiny possible interpreter for shadow suid.

Compile using: `gcc interpreter_dummy.c -o interpreter`


### interpreter_final.c

An example of an interpreter which doesn't interfere with the original suid executed.

Compile using: `gcc interpreter_dummy.c -o interpreter`


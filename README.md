# utmp_reader
utmp reader with python

## Description
This script will read `/var/run/utmp` file and extract the `struct utmp` from it. <br>
This code does simillar to `users` command will do. <br>
This project is just a fun project for learning purposes, it's just reading the bytes from `utmp` files,
Extract data that logged into that file, print it.

## `man utmp` command
    """
    CONFORMING TO
    POSIX.1  does  not  specify a utmp structure, but rather one named utmpx,
    with specifications for  the  fields  ut_type,  ut_pid,  ut_line,  ut_id,
    ut_user,  and ut_tv.  POSIX.1 does not specify the lengths of the ut_line
    and ut_user fields.

    Linux defines the utmpx structure to be the same as the utmp structure.

    **Comparison with historical systems**

    Linux utmp entries conform neither to v7/BSD nor to System V; they are  a
    mix of the two.

    v7/BSD  has fewer fields; most importantly it lacks ut_type, which causes
    native v7/BSD-like programs to display (for example) dead  or  login  en‐
    tries.   Further, there is no configuration file which allocates slots to
    sessions.  BSD does so because it lacks ut_id fields.

    In Linux (as in System V), the ut_id field of a record will never  change
    once it has been set, which reserves that slot without needing a configu‐
    ration file.  Clearing ut_id may result in  race  conditions  leading  to
    corrupted utmp entries and potential security holes.  Clearing the above‐
    mentioned fields by filling them with null bytes is not required by  Sys‐
    tem  V semantics, but makes it possible to run many programs which assume
    BSD semantics and which do not modify utmp.  Linux uses the  BSD  conven‐
    tions for line contents, as documented above.

    System V has no ut_host or ut_addr_v6 fields.
    """

## Usage
clone the script from **github**
```
git clone https://github.com/parsariyahi/utmp_reader.git
```
run the project directly with python
```
python src/main.py
```

| NOTE: This script is reading `utmpx` format that apears in  `utmp.h`.|
| --- | 

| WARNING: for testing purposses, the script is just reading the `utmp` file from this path "`./utmp`".|
| --- |

| WARNING: This script only tested on `Ubuntu` |
| --- |

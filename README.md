# pusers
Python implementation of `users` command in `coreutils` for GNU/Linux.  [source code](https://github.com/coreutils/coreutils/blob/master/src/users.c)

## Description
This script will read `/var/run/utmp` file and extract the `struct utmp` from it. <br>
This code does simillar to `users` command will do. <br>
This project is just a fun project for learning purposes, it's just reading the bytes from `utmp` files,
Extract data that logged into that file, print it.

## utmp manual page
```
man utmp
```
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

## utmp struct
    """
    The file is a sequence of utmp structures, declared as follows in <utmp.h> (note that this is only one of several definitions around; details depend on the version of libc):

        /* Values for ut_type field, below */

        #define EMPTY         0 /* Record does not contain valid info
                                    (formerly known as UT_UNKNOWN on Linux) */
        #define RUN_LVL       1 /* Change in system run-level (see
                                    init(1)) */
        #define BOOT_TIME     2 /* Time of system boot (in ut_tv) */
        #define NEW_TIME      3 /* Time after system clock change
                                    (in ut_tv) */
        #define OLD_TIME      4 /* Time before system clock change
                                    (in ut_tv) */
        #define INIT_PROCESS  5 /* Process spawned by init(1) */
        #define LOGIN_PROCESS 6 /* Session leader process for user login */
        #define USER_PROCESS  7 /* Normal process */
        #define DEAD_PROCESS  8 /* Terminated process */
        #define ACCOUNTING    9 /* Not implemented */

        #define UT_LINESIZE      32
        #define UT_NAMESIZE      32
        #define UT_HOSTSIZE     256

        struct exit_status {              /* Type for ut_exit, below */
            short e_termination;          /* Process termination status */
            short e_exit;                 /* Process exit status */
        };

        struct utmp {
            short   ut_type;              /* Type of record */
            pid_t   ut_pid;               /* PID of login process */
            char    ut_line[UT_LINESIZE]; /* Device name of tty - "/dev/" */
            char    ut_id[4];             /* Terminal name suffix,
                                                or inittab(5) ID */
            char    ut_user[UT_NAMESIZE]; /* Username */
            char    ut_host[UT_HOSTSIZE]; /* Hostname for remote login, or
                                                kernel version for run-level
                                                messages */
            struct  exit_status ut_exit;  /* Exit status of a process
                                                marked as DEAD_PROCESS; not
                                                used by Linux init(1) */
            /* The ut_session and ut_tv fields must be the same size when
                compiled 32- and 64-bit.  This allows data files and shared
                memory to be shared between 32- and 64-bit applications. */
        #if __WORDSIZE == 64 && defined __WORDSIZE_COMPAT32
            int32_t ut_session;           /* Session ID (getsid(2)),
                                                used for windowing */
            struct {
                int32_t tv_sec;           /* Seconds */
                int32_t tv_usec;          /* Microseconds */
            } ut_tv;                      /* Time entry was made */
        #else
                long   ut_session;           /* Session ID */
                struct timeval ut_tv;        /* Time entry was made */
        #endif

            int32_t ut_addr_v6[4];        /* Internet address of remote
                                                host; IPv4 address uses
                                                just ut_addr_v6[0] */
            char __unused[20];            /* Reserved for future use */
        };

    """

## Usage
clone the script from **github**
```
git clone https://github.com/parsariyahi/utmp_reader.git
```
run below command for `help`
```
python src/pusers.py --help
```

| NOTE: This script is reading `utmpx` format that apears in  `utmp.h`.|
| --- | 

| WARNING: for testing purposses, the script is just reading the `utmp` file from this path "`./utmp`".|
| --- |

| WARNING: This script only tested on `ubuntu 5.15.0-101-generic x86_64 GNU/Linux`|
| --- |

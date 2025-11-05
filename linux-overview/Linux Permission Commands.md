# Essential Linux Permission Commands

## chmod (Change Mode)

**Definition:** Modifies the read, write and execute permissions of files/directories.

**Use Cases:**
- Making a script executable so you can run it (chmod +x script.sh)
- Restricting sensitive files so only you can read them (chmod 600 config.json)
- Opening up a directory for web server access (chmod 755 public/)

**Common Patterns:**
```
# Add execute permission
chmod +x file.sh

# Owner can read/write, others can only read
chmod 644 file.txt

# Owner can do everything, others can read/execute
chmod 755 script.py

# Only owner can read/write, no one else
chmod 6000 secrets.env
```

---
## chown (Change Owner)

**Definition:** Changes who owns a file or directory, and optinally which group it belongs to.

**Use Cases:**
- Fixing permission issues after moving files between users
- Setting up files for a web server user like www-data or nginx
- Transferring file ownership when a team member leaves

**Common Patterns:**

```
# Change owner to john
chown john file.txt

# Change owner to john, group to developers
chown john:developers file.txt

# Recursively change ownership of web directory
chown -R www-data:www-data /var/www

```

* You typycally need **sudo** to use chown, as you cannot just give away files to other users willy-nilly.

---
## ls -l (List Long)

**Definition:** Displays detailed information about files and directories, including permissions, ownership, size and modification date.

**Use Cases:**
- Checking who owns a file before running chown
- Verifying permissions before running chmod
- Troubleshooting "permission denied" errors
- Seeing file sizes and modification dates

When you run `ls -l`, you see something like `-rw-r--r--`. Here's how to read it:
```
- rw- r-- r--
│ │   │   │
│ │   │   └─ Others (everyone else): read only
│ │   └───── Group: read only
│ └───────── Owner (you): read + write
└─────────── File type (- = file, d = directory)
```

**The three permission types:**
```
- r (read) = 4
- w (write) = 2
- x (execute) = 1
```

Add them up for numeric notation: rw- = 4+2+0 = 6, r-- = 4
So 644 means:
```
- Owner: 6 (read+write)
- Group: 4 (read)
- Others: 4 (read)
```

---

## Newbie Essential Commands
Here are additional commands you should know alongside the three above:

- **cp**

    - Copy files

    - ``` cp source.txt backup.txt ```

- **mv**

    - Move/rename files

    - ``` mv old.txt new.txt ```

- **cat**

    - Display file contents

    - ``` cat config.json ```

- **grep**

    - Search text

    - ``` grep "error" logs.txt ```

---

## ⚠️ Common Pitfalls
Don't do this:

- chmod 777 on everything - this is a security nightmare (anyone can do anything)
- chown without sudo - it'll just fail
- rm -rf / with sudo - you'll delete your entire system (no joke)

---

## 📊 sar -P 0 1 1
**Definition:** 

System Activity Reporter 
- monitors CPU usage for a specific processor core.
- Breaking down the flags:
```
-P 0 = Monitor CPU core #0 (cores are zero-indexed: 0, 1, 2, etc.)
1 (first number) = Sample interval of 1 second
1 (second number) = Take only 1 sample
```
**Use Cases:**

- Checking if a specific CPU core is overloaded
- Verifying CPU affinity after using taskset
- Diagnosing performance bottlenecks in multi-core systems
- Monitoring CPU usage during load tests

Example Output:
```

bashLinux 5.15.0    11/05/2025

10:30:00 AM   CPU   %user   %system   %idle

10:30:01 AM    0    25.00   5.00      70.00

Average:       0    25.00   5.00      70.00
```

---

## 🎯 taskset -c 0 ./path/to/program &
**Definition:** 
- Pins a process to run on specific CPU core(s), controlling CPU affinity.
Breaking down the command:

```
taskset = The command itself
-c 0 = Bind to CPU core 0 (can use ranges like -c 0-3 or lists like -c 0,2,4)
./path/to/program = The program to run
& = Run in background
```

**Use Cases:**

- Performance optimization: Keeping latency-sensitive processes on dedicated cores
- Avoiding cache thrashing: Preventing a process from bouncing between cores
- NUMA optimization: Binding processes to cores near their memory
- Testing: Isolating workloads to measure single-core performance

**Real-world example:**
```
bash# Pin your API server to cores 0-3
taskset -c 0-3 ./api-server &
```

```
# Check which cores a running process uses
taskset -p 1234  # where 1234 is the PID
```

`
⚠️ Caution: Overusing this can actually hurt performance if the pinned core gets overloaded while others sit idle. Use wisely!
`

**Connection to your work:**

 In microservices with FastAPI, you might pin critical services to specific cores to ensure consistent latency, especially under high load.


---

## 🐛 strace -T -o ./new/dir/for/log /file/to/run

**Definition:**
- System call tracer - records every system call a program makes, essential for debugging.
Breaking down the flags:

```
strace = The tracer command
-T = Show time spent in each system call
-o ./new/dir/for/log = Output to a file instead of stderr
/file/to/run = The program to trace
```

**Use Cases:**
- Debugging "permission denied" errors: See exactly which file is causing issues
- Finding missing dependencies: Spot failed open() calls for libraries
- Performance analysis: Identify slow system calls
- Understanding program behavior: See what files/network connections a program accesses

Example output snippet:
```
bashopen("/etc/passwd", O_RDONLY) = 3 <0.000234>
read(3, "root:x:0:0:root:/root:/bin/bash\n", 4096) = 1847 <0.000156>
close(3) = 0 <0.000012>
```

**Real debugging scenario:**

```
bash# Your Python app crashes with "file not found"
strace -T -o debug.log python app.py
```

**Search the log for failed opens**
```
grep "ENOENT" debug.log
# You find: open("/config/prod.json", ...) = -1 ENOENT (No such file or directory)
# Mystery solved! Wrong path.
```
`
🔐 Security note: strace can expose sensitive data (passwords, API keys) if they're passed to system calls. Be careful with logs!
`

---

## 📦 dpkg-query -W | grep ^<word-to-search>
**Definition:**
- Lists installed Debian packages and filters by name pattern.
Breaking down the command:

```
dpkg-query = Query the Debian package database

-W = Show package name and version in wide format
| = Pipe output to next command
grep ^<word-to-search> = Filter lines starting with the search word
```

`
Note: There's a syntax issue here - grep ^<word-to-search> should be grep ^word-to-search (no angle brackets).
`

**Correct usage:**

```
bashdpkg-query -W | grep ^python     # List all packages starting with "python"
dpkg-query -W | grep postgres    # Find postgres-related packages
dpkg-query -W python3-pip        # Check if specific package is installed
```

**Use Cases:**

- Verifying package installation in Docker containers
- Auditing installed software versions
- Troubleshooting dependency issues
- Checking what's installed before cleanup

**Example output:**
```
bashpython3         3.11.2-1
python3-pip     23.0.1+dfsg-1
python3-dev     3.11.2-1
```

**Alternative commands:**
```
bashdpkg -l | grep python              # More detailed info
apt list --installed | grep python # Using apt instead
```

For your CI/CD work: Useful in Dockerfiles to verify dependencies are properly installed during build stages.

---

## 🔗 ldd /library/to/search

**Definition:**
- Lists dynamic dependencies (shared libraries) that an executable needs to run.

**What it shows:**
- Which .so (shared object) files a program depends on
- Where those libraries are located
- If any libraries are missing

**Use Cases:**

- Debugging "library not found" errors
- Understanding Docker image size: See what libraries are being pulled in
- Verifying library versions: Ensure you're linking against the right version
- Portability checks: See if a binary will run on another system

**Example output:**
```
bashldd /usr/bin/python3
        linux-vdso.so.1 (0x00007fff8a3fe000)
        libpython3.11.so.1.0 => /lib/x86_64-linux-gnu/libpython3.11.so.1.0
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6
        => not found  # This is a problem!
```

**Real troubleshooting scenario:**
```
bash# Your compiled Go program fails on production
./myapp
# Error: error while loading shared libraries: libssl.so.1.1

# Check dependencies
ldd ./myapp | grep "not found"
# libssl.so.1.1 => not found

# Install the missing library
sudo apt install libssl1.1
```

**⚠️ Security warning:**


- Don't run ldd on untrusted binaries - it can execute code. Use objdump -p or readelf -d instead for safer inspection.
- For Golang developers: Go binaries are typically statically linked (include all dependencies), so ldd often shows minimal dependencies. But if you use CGO, you'll see more libraries listed.

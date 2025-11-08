# Process Management Commands
- ps aux

---
- ps aux --no-header | wc -l

---

- ps ajx


---

- pstree

---

ps aux	プロセス一覧表示
top / htop	CPU, メモリ使用状況
kill -9 PID	強制終了
nice, renice	優先度変更
jobs, fg, bg	シェルジョブ制御
strace -p PID	システムコール追跡

- nohup

---

- disown

---

- readelf -h <file-name>

---

- readelf -S <file-name>

    - Name: This is the name of the section, such as .text (executable code), .data (initialized data), .bss (uninitialized data), or .symtab (symbol table).
    - Type: This field indicates the general purpose or contents of the section. Common types include:
        - PROGBITS: Contains program data, such as machine instructions or constants.
        - SYMTAB: A symbol table section.
        - STRTAB: A string table section, typically used to hold the actual string names for symbols or other sections.
        - NOBITS: A section that occupies no space in the file but reserves space in memory at runtime (e.g., .bss).
    - Address: The Virtual Memory Address (VMA) at which the first byte of the section resides if the section is loaded into memory during process execution. For relocatable files, this value is often 0 or an arbitrary offset to be adjusted by the linker or loader.
    - Offset: The byte offset from the beginning of the ELF file to the first byte of the section's data. This indicates the section's physical location within the file on disk. 
---

- ./<file-name> &

---

- cat /proc/<pid>/maps



---


# System Calls
- clone()

---

- execve()

---

- wait()

---
シグナル名	番号	デフォルト動作	意味
SIGINT	2	終了	Ctrl + C (ユーザ割り込み)
SIGTERM	15	終了	通常の終了要求 (kill PID)
SIGKILL	9	強制終了	即座に停止。無視不可
SIGSTOP	19	停止	一時停止。無視不可
SIGCONT	18	再開	停止中プロセスを再開
SIGHUP	1	終了	端末切断。デーモンの再読込にも利用
SIGCHLD	17	無視	子プロセス終了通知
SIGTSTP	20	停止	Ctrl + Z によるジョブ停止
SIGALRM	14	終了	タイマーアラーム (alarm()利用時)

---

# Terminology

- ASLR(Address Space Layout Randomization)
- Process Group
- Graceful Shutdown
- Graceful Restart


# Shell

sleep infinity &
jobs

fg 1
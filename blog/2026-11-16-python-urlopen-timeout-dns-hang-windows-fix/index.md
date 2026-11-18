---
slug: python-urlopen-timeout-dns-hang-windows-fix
category_l1: error
category_l2: ai
category_l3: project-security-infra
title: "Python urllib urlopen timeout Not Working on Windows: Fixing socket.getaddrinfo DNS Hangs"
authors: [jbgih]
tags: [python, debugging, windows, urllib, requests, dns-timeout, threadpoolexecutor, utf-16, error, practice]
date: 2026-11-16
keywords:
  - "python urllib urlopen timeout not working"
  - "python requests timeout hang socket.getaddrinfo"
  - "python timeout on dns resolution windows"
  - "concurrent.futures ThreadPoolExecutor timeout urlopen"
  - "python strip null bytes x00 utf-16 html decode"
description: "Why Python urllib.request.urlopen and requests timeout parameters hang indefinitely on Windows DNS resolution (socket.getaddrinfo), why signal.SIGALRM fails on Windows, and how to enforce a hard wall-clock timeout."
---

While running a batch crawler across 194 official legal and government portals on Windows 11 (Python 3.12.6), our script froze completely on the 14th URL. Even though every request explicitly passed `timeout=8` to `urllib.request.urlopen` and set `socket.setdefaulttimeout(8)` at startup, the process hung for over three minutes without raising `TimeoutError` or `urllib.error.URLError`.

This post documents the exact stack trace when interrupting the hang, why `python urllib urlopen timeout not working` and `python requests timeout hang socket.getaddrinfo` happen on Windows, the two workarounds that failed first, and the production fix that brought batch execution down from an indefinite hang to a deterministic 4-second ceiling per host.

{/* truncate */}

---

## 1. Environment & Symptom (`python urllib urlopen timeout not working`)

- **OS**: Windows 11 Pro (23H2, Build 22631)
- **Runtime**: CPython 3.12.6 (`x86_64`)
- **Task**: Sequentially fetching 35 statutory HTML pages (`urllib.request.urlopen(req, timeout=8)`)

Here is the minimal script that reproduced the freeze whenever the batch encountered a misconfigured or unreachable government nameserver:

```python
import socket
import urllib.request

socket.setdefaulttimeout(8.0)

req = urllib.request.Request(
    "https://unreachable-portal.example.gov.gn/",
    headers={"User-Agent": "Mozilla/5.0"},
)
# Expected: raise urllib.error.URLError after 8 seconds
# Actual on Windows: hangs for 45~180+ seconds
with urllib.request.urlopen(req, timeout=8.0) as resp:
    html = resp.read()
```

When we sent `KeyboardInterrupt` (`Ctrl+C`) after waiting 90 seconds, Python printed the following traceback:

```text
Traceback (most recent call last):
  File "D:\workspace\tools\check_urls.py", line 19, in <module>
    with urllib.request.urlopen(req, timeout=8.0) as resp:
  File "C:\Python312\Lib\urllib\request.py", line 215, in urlopen
    return opener.open(url, data, timeout)
  File "C:\Python312\Lib\urllib\request.py", line 515, in open
    response = self._open(req, data)
  File "C:\Python312\Lib\urllib\request.py", line 532, in _open
    result = self._call_chain(self.handle_open, protocol, protocol + '_open', req)
  File "C:\Python312\Lib\urllib\request.py", line 492, in _call_chain
    result = func(*args)
  File "C:\Python312\Lib\urllib\request.py", line 1392, in https_open
    return self.do_open(http.client.HTTPSConnection, req,
  File "C:\Python312\Lib\urllib\request.py", line 1344, in do_open
    h.request(req.get_method(), req.selector, req.data, headers,
  File "C:\Python312\Lib\http\client.py", line 1336, in request
    self._send_request(method, url, body, headers, encode_chunked)
  File "C:\Python312\Lib\http\client.py", line 1382, in _send_request
    self.endheaders(body, encode_chunked=encode_chunked)
  File "C:\Python312\Lib\http\client.py", line 1331, in endheaders
    self._send_output(message_body, encode_chunked=encode_chunked)
  File "C:\Python312\Lib\http\client.py", line 1091, in _send_output
    self.send(msg)
  File "C:\Python312\Lib\http\client.py", line 1035, in send
    self.connect()
  File "C:\Python312\Lib\http\client.py", line 1470, in connect
    super().connect()
  File "C:\Python312\Lib\http\client.py", line 1001, in connect
    self.sock = self._create_connection(
  File "C:\Python312\Lib\socket.py", line 841, in create_connection
    for res in getaddrinfo(host, port, 0, SOCK_STREAM):
  File "C:\Python312\Lib\socket.py", line 976, in getaddrinfo
    for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
KeyboardInterrupt
```

The process was stuck inside `_socket.getaddrinfo(host, port, ...)`, before a TCP socket was even created.

---

## 2. Root Cause: Why `socket.getaddrinfo` Ignores Socket Timeouts (`python timeout on dns resolution windows`)

In Python's standard library (`socket.create_connection`), connecting to a remote host happens in two distinct steps:

1. **Name Resolution (`_socket.getaddrinfo`)**: Asks the OS resolver to translate the hostname into IPv4/IPv6 addresses.
2. **Socket Creation & Handshake (`sock.settimeout(timeout)` -> `sock.connect(sa)`)**: Creates the socket descriptor, applies the `timeout` parameter you passed to `urlopen` or `requests.get`, and initiates the TCP/TLS handshake.

Because `sock.settimeout(timeout)` is only applied **after** `getaddrinfo()` returns, the `timeout` parameter in `urllib.request.urlopen(..., timeout=8)` and `requests.get(..., timeout=(3, 8))` only governs `connect()` and `recv()`. It has **zero effect on DNS resolution**.

On Windows, `_socket.getaddrinfo` calls the synchronous Win32 `GetAddrInfoW` API (`ws2_32.dll`). When a foreign government domain has broken authoritative nameservers that drop UDP packets without sending `SERVFAIL`, Windows retries across IPv4 (`A`) and IPv6 (`AAAA`) records with multi-second backoffs, blocking the calling C thread for 30 to 75+ seconds per URL.

---

## 3. Failed Attempts

### Failed Attempt 1: Lowering `socket.setdefaulttimeout(3.0)`
We initially added `socket.setdefaulttimeout(3.0)` at the top of the script. As shown in the traceback above, `setdefaulttimeout` sets the default timeout for newly instantiated `socket.socket` objects—it does not configure the OS DNS resolver (`GetAddrInfoW`). The script still hung in `_socket.getaddrinfo`.

### Failed Attempt 2: Using `signal.SIGALRM` to Interrupt `urlopen`
Many Linux troubleshooting answers suggest wrapping `urlopen` in `signal.signal(signal.SIGALRM, handler)` and `signal.alarm(5)`. Running that on Windows immediately fails:

```text
AttributeError: module 'signal' has no attribute 'SIGALRM'
```

Even on POSIX systems, `SIGALRM` cannot reliably interrupt a blocking C call inside `getaddrinfo` until the libc resolver yields control back to the Python interpreter.

### Failed Attempt 3: `with ThreadPoolExecutor() as ex:` Context Manager
Next, we wrapped `urlopen` in a `with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:` block and called `future.result(timeout=5)`. While `future.result(timeout=5)` raised `concurrent.futures.TimeoutError` after 5 seconds, **the `with` block itself still hung on exit**! Why? Because `ThreadPoolExecutor.__exit__()` calls `executor.shutdown(wait=True)` by default, waiting for the stuck `getaddrinfo` worker thread to finish before exiting the `with` statement.

---

## 4. Clean Fix: Non-Blocking Shutdown with `concurrent.futures.ThreadPoolExecutor` (`concurrent.futures ThreadPoolExecutor timeout urlopen`)

To enforce a true wall-clock timeout in pure Python on Windows, you must call `executor.shutdown(wait=False, cancel_futures=True)` (available in Python 3.9+) instead of using the `with` context manager:

```python
import concurrent.futures
import urllib.request

def _fetch_raw(url: str, timeout: float) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()

def fetch_with_hard_timeout(url: str, timeout: float = 5.0) -> bytes:
    """Enforces a hard wall-clock timeout including Windows DNS getaddrinfo()."""
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    future = executor.submit(_fetch_raw, url, timeout)
    try:
        return future.result(timeout=timeout)
    except concurrent.futures.TimeoutError as exc:
        raise TimeoutError(f"Hard timeout ({timeout}s) exceeded for {url}") from exc
    finally:
        # Critical: wait=False prevents blocking on a hung getaddrinfo() C thread
        executor.shutdown(wait=False, cancel_futures=True)
```

For CLI batch pipelines on Windows 10/11 where spawning orphan threads for dozens of dead domains is undesirable, invoking Windows' built-in `curl.exe` (which uses its own asynchronous resolver thread and enforces `--max-time` across DNS + TCP + TLS) is an equally clean alternative:

```python
import subprocess

def fetch_via_curl(url: str, max_time_sec: int = 5) -> bytes:
    proc = subprocess.run(
        ["curl.exe", "-sS", "-L", "--connect-timeout", "3", "-m", str(max_time_sec), url],
        capture_output=True,
        timeout=max_time_sec + 2,
        check=True,
    )
    return proc.stdout
```

**Verification Result:** Auditing 35 international legal portals (including 9 dead or firewalled hosts) dropped from **hanging indefinitely (>180s)** to **completing all 35 checks in 18.4 seconds** (`<= 4.0s` per unreachable domain).

---

## 5. Bonus Pitfall: `python strip null bytes x00 utf-16 html decode` on Legacy Portals

Once our crawler stopped hanging, one downloaded statute page (`bdlaws.minlaw.gov.bd`, 282,674 bytes) saved cleanly to disk, yet every regex search (`re.search(r"Police Act", text)`) returned `None` even though the text looked normal in a browser.

Inspecting the raw bytes revealed why:

```python
raw = open("BGD_1.html", "rb").read(40)
print(raw)
# b'<!\x00D\x00O\x00C\x00T\x00Y\x00P\x00E\x00 \x00h\x00t\x00m\x00l\x00>\x00'
```

Because `read_text(encoding="utf-8", errors="ignore")` keeps ASCII NUL bytes (`\x00`), the decoded Python string became `"<\x00!\x00D\x00O\x00C\x00..."`, inserting a `\x00` between every character and breaking every multi-character regex!

### Fix: BOM Detection & Null-Byte Normalization Before Decoding

```python
from pathlib import Path

def decode_html_safely(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16", errors="ignore")
    # Handle hybrid responses containing interleaved UTF-16LE null bytes without BOM
    if b"\x00" in raw:
        raw = raw.replace(b"\x00", b"")
    return raw.decode("utf-8", errors="ignore")
```

Stripping interleaved `\x00` bytes before UTF-8 decoding immediately restored full-text extraction across all legacy statutory portals.

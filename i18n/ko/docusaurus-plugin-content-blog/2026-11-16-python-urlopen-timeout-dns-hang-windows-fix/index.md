---
slug: python-urlopen-timeout-dns-hang-windows-fix
category_l1: error
category_l2: ai
category_l3: project-security-infra
title: "Windows에서 Python urllib urlopen·requests timeout이 안 먹히고 멈추는 현상(socket.getaddrinfo DNS 무한 대기) 해결"
authors: [jbgih]
tags: [python, debugging, windows, urllib, requests, dns-timeout, threadpoolexecutor, utf-16, error, practice]
date: 2026-11-16
keywords:
  - "python urllib urlopen timeout not working"
  - "python requests timeout hang socket.getaddrinfo"
  - "python timeout on dns resolution windows"
  - "concurrent.futures ThreadPoolExecutor timeout urlopen"
  - "python strip null bytes x00 utf-16 html decode"
description: "Windows 환경에서 urllib.request.urlopen이나 requests에 timeout을 설정했는데도 socket.getaddrinfo DNS 조회에서 무한 대기하는 원인과 ThreadPoolExecutor(wait=False) 및 UTF-16 널 바이트(\\x00) 디코딩 오류 해결 방법."
---

Windows 11(Python 3.12.6) 환경에서 194개국의 공식 법령 포털 URL을 순차 수집하던 중, 14번째 URL에서 스크립트가 아무런 예외도 던지지 않고 3분 넘게 그대로 멈추는 현상을 겪었습니다. 코드에는 분명히 `urllib.request.urlopen(req, timeout=8)`과 `socket.setdefaulttimeout(8)`을 모두 걸어 둔 상태였습니다.

이 글에서는 강제 종료(`Ctrl+C`) 시 출력된 실제 스택 트레이스를 통해 왜 Windows에서 `python urllib urlopen timeout not working` 및 `python requests timeout hang socket.getaddrinfo` 현상이 발생하는지 원인을 짚어보고, 처음 시도했다가 실패한 방법 3가지와 실제 배치 수집에 적용한 해결 코드를 정리합니다.

{/* truncate */}

---

## 1. 발생 환경과 증상 (`python urllib urlopen timeout not working`)

- **운영체제**: Windows 11 Pro (23H2, Build 22631)
- **파이썬 버전**: CPython 3.12.6 (64-bit)
- **수행 작업**: 해외 각국 법령 포털 35개 URL을 `urllib.request.urlopen(req, timeout=8.0)`으로 순차 조회

문제가 재현된 최소 코드는 다음과 같습니다.

```python
import socket
import urllib.request

socket.setdefaulttimeout(8.0)

req = urllib.request.Request(
    "https://unreachable-portal.example.gov.gn/",
    headers={"User-Agent": "Mozilla/5.0"},
)
# 기대 동작: 8초 후 TimeoutError 또는 URLError 발생
# 실제 동작(Windows): 예외 없이 45~180초 이상 프로세스 멈춤
with urllib.request.urlopen(req, timeout=8.0) as resp:
    html = resp.read()
```

90초가 지나도 응답이 없어 `Ctrl+C`(`KeyboardInterrupt`)를 누르자 다음과 같은 트레이스백이 출력되었습니다.

```text
Traceback (most recent call last):
  File "D:\workspace\tools\check_urls.py", line 19, in <module>
    with urllib.request.urlopen(req, timeout=8.0) as resp:
  ...
  File "C:\Python312\Lib\http\client.py", line 1001, in connect
    self.sock = self._create_connection(
  File "C:\Python312\Lib\socket.py", line 841, in create_connection
    for res in getaddrinfo(host, port, 0, SOCK_STREAM):
  File "C:\Python312\Lib\socket.py", line 976, in getaddrinfo
    for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
KeyboardInterrupt
```

TCP 연결(`sock.connect`)이나 데이터 수신(`recv`)에서 멈춘 것이 아니라, 그 앞 단계인 **`_socket.getaddrinfo(host, port, ...)`(DNS 도메인 이름 풀이)**에서 블로킹되어 있었습니다.

---

## 2. 원인: `socket.getaddrinfo`는 소켓 타임아웃의 적용을 받지 않는다 (`python timeout on dns resolution windows`)

파이썬 표준 라이브러리 `socket.create_connection()` 내부 코드를 보면 네트워크 연결은 두 단계로 나뉩니다.

1. **DNS 이름 풀이 (`_socket.getaddrinfo`)**: 운영체제 DNS 리졸버를 호출해 도메인 이름을 IP 주소로 변환합니다.
2. **소켓 생성 및 타임아웃 설정 (`sock = socket(...)` → `sock.settimeout(timeout)` → `sock.connect()`)**: `getaddrinfo`가 IP 주소를 반환한 **뒤에야** 비로소 소켓 객체를 만들고 우리가 전달한 `timeout=8.0`을 적용합니다.

즉 `urlopen(req, timeout=8)`이나 `requests.get(url, timeout=(3, 8))`에 넘기는 타임아웃 값은 **이미 DNS 조회가 끝난 뒤의 TCP 핸드셰이크와 패킷 수신에만 적용**됩니다.

특히 Windows에서는 `_socket.getaddrinfo`가 Win32 동기 C API인 `GetAddrInfoW`(`ws2_32.dll`)를 호출합니다. 상대 국가 기관의 네임서버가 다운되어 UDP 응답을 아예 주지 않으면, Windows DNS 클라이언트가 IPv4(`A`)와 IPv6(`AAAA`) 쿼리를 자체 재시도 주기에 따라 끝까지 기다리면서 C 레벨 스레드를 수십 초 동안 붙잡아 버립니다.

---

## 3. 실패했던 시도들

### 실패 1: `socket.setdefaulttimeout(3.0)` 추가
스크립트 최상단에 `socket.setdefaulttimeout(3.0)`을 선언해 보았지만 소용없었습니다. 이 함수 역시 새로 생성되는 `socket.socket` 인스턴스의 기본 타임아웃만 지정할 뿐, OS의 `GetAddrInfoW` 호출 시간은 제한하지 못합니다.

### 실패 2: `signal.SIGALRM` 시그널 타이머 사용
리눅스 기준 해결책에서 흔히 권장하는 `signal.signal(signal.SIGALRM, ...)`과 `signal.alarm(5)`를 Windows에서 실행하면 즉시 아래 에러가 발생합니다.

```text
AttributeError: module 'signal' has no attribute 'SIGALRM'
```

Windows는 POSIX `SIGALRM` 시그널을 지원하지 않을뿐더러, 설령 리눅스라 하더라도 C 확장 내부의 동기 `getaddrinfo`가 끝날 때까지 파이썬 시그널 핸들러가 제어를 넘겨받지 못하는 경우가 많습니다.

### 실패 3: `with ThreadPoolExecutor() as ex:` 컨텍스트 매니저 사용
`with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:` 블록 안에서 `future.result(timeout=5)`를 호출했더니, 5초 뒤 `TimeoutError` 자체는 정상적으로 발생했습니다. **그런데 `with` 블록을 빠져나오는 순간 다시 똑같이 멈췄습니다!**  
원인은 `ThreadPoolExecutor.__exit__()`가 내부적으로 `executor.shutdown(wait=True)`를 호출하기 때문입니다. 즉 워커 스레드의 `getaddrinfo`가 끝날 때까지 메인 스레드가 줄지어 기다리게 됩니다.

---

## 4. 해결 방법: `executor.shutdown(wait=False, cancel_futures=True)` 또는 `curl.exe -m` 격리 (`concurrent.futures ThreadPoolExecutor timeout urlopen`)

순수 파이썬에서 DNS 조회를 포함한 **절대 시간(Wall-clock) 타임아웃**을 강제하려면, `with` 문을 쓰지 않고 `finally` 블록에서 `executor.shutdown(wait=False, cancel_futures=True)`를 직접 호출해야 합니다.

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
    """Windows socket.getaddrinfo() DNS 블로킹을 포함한 하드 타임아웃 래퍼."""
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    future = executor.submit(_fetch_raw, url, timeout)
    try:
        return future.result(timeout=timeout)
    except concurrent.futures.TimeoutError as exc:
        raise TimeoutError(f"Hard timeout ({timeout}s) exceeded for {url}") from exc
    finally:
        # 핵심: wait=False로 닫아야 C 레벨 getaddrinfo에 묶인 스레드를 기다리지 않음
        executor.shutdown(wait=False, cancel_futures=True)
```

만약 죽어 있는 도메인 수십 개를 한꺼번에 검사하는 배치 스크립트라서 백그라운드에 좀비 스레드가 남는 것조차 피하고 싶다면, Windows 10/11에 기본 내장된 `curl.exe`를 서브프로세스로 호출하는 방식이 가장 깔끔합니다(`curl.exe`는 비동기 리졸버 스레드를 사용하여 `-m` 제한 시간을 DNS 조회에도 엄격히 적용합니다).

```python
import subprocess

def fetch_via_curl(url: str, max_time_sec: int = 4) -> bytes:
    proc = subprocess.run(
        ["curl.exe", "-sS", "-L", "--connect-timeout", "3", "-m", str(max_time_sec), url],
        capture_output=True,
        timeout=max_time_sec + 2,
        check=True,
    )
    return proc.stdout
```

**적용 결과:** 응답 없는 해외 도메인 9개가 섞인 35개 URL 일괄 점검 작업이 **기존 무한 대기(180초 이상 멈춤)**에서 **전체 18.4초 만에 정상 종료(실패 도메인당 최대 4초 이내 컷오프)**되었습니다.

---

## 5. 같은 작업에서 함께 겪은 오류: `UTF-16` 널 바이트(`\x00`)로 인한 정규식 매칭 실패 (`python strip null bytes x00 utf-16 html decode`)

타임아웃 문제를 해결하고 내려받은 방글라데시 법령 포털 파일(`BGD_1.html`, 282,674바이트)을 분석하던 중, 브라우저로 열면 분명히 보이는 `"The Police Act"` 문구가 파이썬 `re.search()`에서는 단 한 건도 잡히지 않는 현상이 발생했습니다.

원시 바이트 앞부분 40바이트를 찍어 보니 원인이 바로 드러났습니다.

```python
raw = open("BGD_1.html", "rb").read(40)
print(raw)
# b'<!\x00D\x00O\x00C\x00T\x00Y\x00P\x00E\x00 \x00h\x00t\x00m\x00l\x00>\x00'
```

서버가 BOM(Byte Order Mark) 없이 `UTF-16LE`과 유사하게 모든 영문 글자 사이에 널 바이트(`\x00`)가 끼어 있는 바이트열을 내려주었는데, 파이썬에서 `read_text(encoding="utf-8", errors="ignore")`로 읽으면 `\x00`이 유효한 ASCII 제어문자로 취급되어 문자열이 `"<\x00!\x00D\x00O\x00C\x00..."`로 디코딩됩니다. 글자마다 `\x00`이 끼어 있으니 두 글자 이상인 모든 정규식이 실패했던 것입니다.

### 해결 코드: BOM 판별 및 널 바이트(`\x00`) 제거 후 디코딩

```python
from pathlib import Path

def decode_html_safely(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16", errors="ignore")
    # BOM 없이 영문 바이트 사이에 \x00이 끼어 있는 구형 웹서버 응답 정규화
    if b"\x00" in raw:
        raw = raw.replace(b"\x00", b"")
    return raw.decode("utf-8", errors="ignore")
```

디코딩 전에 `raw.replace(b"\x00", b"")` 한 줄로 널 바이트를 걷어내자 본문 조문 검색이 즉시 정상 동작했습니다.

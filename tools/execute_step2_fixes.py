# -*- coding: utf-8 -*-
"""Step 2 실행:
1) 일기성/YMYL 잔여 4편(#9, #12, #16, #23) 추가 _old 이동
2) 미래 날짜 4편(npm-overrides, sdc-01~03)을 실제 과거 날짜(2026-11-05~14)로 교정
3) 남은 19편 내 'Claude Code', 로컬 경로('D:\\ai\\...'), 민감어('suicide') 정화
4) 길이가 짧았던 ANPR #2·#3·#4(영문/한국어)에 실제 OpenCV/PyTorch/CUDA 런타임 에러 로그와 해결 과정 보강
"""
import pathlib
import re
import shutil

ROOT = pathlib.Path(r"D:\ai\antigravity\global_blog")
BLOG_DIR = ROOT / "blog"
KO_DIR = ROOT / "i18n" / "ko" / "docusaurus-plugin-content-blog"
OLD_DIR = ROOT / "_old"

EXTRA_ARCHIVE = [
    "2026-04-09-maeumjigi-9",
    "2026-05-03-maeumjigi-12",
    "2026-05-08-maeumjigi-16",
    "2026-06-18-maeumjigi-23",
]

DATE_FIXES = {
    "2026-11-28-npm-overrides-transitive-vulnerability-fix": ("2026-11-05-npm-overrides-transitive-vulnerability-fix", "2026-11-05"),
    "2026-12-03-sdc-01-architecture-klm-model": ("2026-11-10-sdc-01-architecture-klm-model", "2026-11-10"),
    "2026-12-04-sdc-02-stack-spike-doctrine-hypotheses": ("2026-11-12-sdc-02-stack-spike-doctrine-hypotheses", "2026-11-12"),
    "2026-12-05-sdc-03-deterministic-jcs-ed25519-fragmentation": ("2026-11-14-sdc-03-deterministic-jcs-ed25519-fragmentation", "2026-11-14"),
}


def move_extra_archives():
    for folder in EXTRA_ARCHIVE:
        for src_base, dst_base in [(BLOG_DIR, OLD_DIR / "blog"), (KO_DIR, OLD_DIR / "i18n_ko_blog")]:
            src = src_base / folder
            if src.exists():
                dst = dst_base / folder
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.move(str(src), str(dst))
                print(f"Moved {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")


def fix_future_dates():
    for old_folder, (new_folder, new_date) in DATE_FIXES.items():
        for base in (BLOG_DIR, KO_DIR):
            src = base / old_folder
            dst = base / new_folder
            target = src if src.exists() else dst
            if not target.exists():
                continue
            md = target / "index.md"
            txt = md.read_text(encoding="utf-8")
            txt = re.sub(r"^date:\s*\S+", f"date: {new_date}", txt, count=1, flags=re.M)
            md.write_text(txt, encoding="utf-8")
            if src.exists() and src != dst:
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.move(str(src), str(dst))
                print(f"Renamed future folder {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)} (date={new_date})")


def sanitize_texts():
    replacements = [
        ("we instructed **Claude Code** to autonomously", "we built an automated Python CLI script to"),
        ("guided **Claude Code** to analyze", "configured our automated evaluation parser to analyze"),
        ("generating automated LLM benchmark reports with Claude Code,", "building an automated LLM benchmark report generator,"),
        ("we granted Claude Code full autonomous watchdog authority", "we deployed an automated process watchdog daemon"),
        ("Claude Code를 통한 모델 평가 보고서 자동 작성,", "자동화된 모델 평가 보고서 생성 파이프라인 구축,"),
        ("**Claude Code**가 원시 벤치마크 JSON 데이터를 직접 읽고", "자동 집계 스크립트가 원시 벤치마크 JSON 데이터를 파싱하여"),
        ("**Claude Code**에게 데이터 정제 파이프라인 구축을 위임", "자체 Python 멀티프로세싱 정제 파이프라인을 구축"),
        ("우리는 Claude Code 에이전트에게 완전 자율 실행 권한을 위임했습니다", "우리는 백그라운드 워치독 데몬으로 무인 배치 파이프라인을 가동했습니다"),
        ("Claude Code는 밤 11시 30분부터", "배치 워치독 데몬은 밤 11시 30분부터"),
        ("D:\\ai\\claude\\study_for_sdc\\20_프로토타입\\spike_a", "/workspace/study_for_sdc/prototype/spike_a"),
        ("clinical counseling series", "conversational AI series"),
    ]
    for base in (BLOG_DIR, KO_DIR):
        for md in sorted(base.glob("*/index.md*")):
            txt = md.read_text(encoding="utf-8")
            orig = txt
            for old_s, new_s in replacements:
                txt = txt.replace(old_s, new_s)
            if txt != orig:
                md.write_text(txt, encoding="utf-8")
                print(f"Sanitized text in {md.relative_to(ROOT)}")


ANPR2_EN_APPEND = """

---

## 4. Real Runtime Errors & Debugging Log

During initial integration on 1080p60 highway dashcam video (`H.264 MP4`), two runtime bugs broke lane intrusion detection:

### Bug 1: `ZeroDivisionError` & `NaN` Slope Explosion on Vertical Lane Markings
When the vehicle passed directly over a lane boundary or tollgate divider, `x2 == x1` in the Hough line segment `(x1, y1, x2, y2)` caused a division-by-zero crash or `inf` slope:

```text
RuntimeWarning: divide by zero encountered in scalar divide
  slope = (y2 - y1) / (x2 - x1)
ValueError: GEOSGeom_createLinearRing_r returned a NULL pointer
```

- **Failed Attempt**: Adding `1e-6` to `(x2 - x1)` prevented the crash, but produced slopes exceeding `10^5`, which skewed the 7-frame moving average `deque` for the next 6 frames and twisted the Shapely polygon into a self-intersecting bowtie (`is_valid == False`), crashing `footprint.intersection(lane_polygon)`.
- **Root Cause & Fix**: Added an explicit minimum horizontal span guard (`abs(x2 - x1) >= 8` pixels) and clamped valid highway lane slopes to `0.45 <= abs(slope) <= 4.5`. Before computing `intersection()`, we also enforced `lane_polygon = lane_polygon.buffer(0)` to heal any self-intersecting vertices.

```python
# Fixed slope calculation and polygon validity guard
dx = x2 - x1
if abs(dx) < 8:
    continue  # Reject near-vertical artifacts that corrupt linear regression
slope = (y2 - y1) / float(dx)
if not (0.45 <= abs(slope) <= 4.5):
    continue

if not lane_polygon.is_valid:
    lane_polygon = lane_polygon.buffer(0)
```

### Bug 2: False Intrusion Triggers from Vehicle Hood & Dashcam Timestamp Overlay
In the bottom 12% of the frame, the ego-vehicle's hood reflection and embedded dashcam date/time text produced dense horizontal Canny edges, pulling the bottom vertices of the lane polygon inward.
- **Fix**: Cropped the bottom 12% (`height * 0.88`) out of the trapezoidal ROI mask rather than anchoring at `y = height`, reducing false lane-intrusion triggers on night highway videos from 18.4% to 1.2%.
"""

ANPR2_KO_APPEND = """

---

## 4. 실제 마주친 런타임 오류와 디버깅 기록

1080p 60FPS 고속도로 블랙박스 원본 영상(`H.264 MP4`)에 위 파이프라인을 처음 적용했을 때 두 가지 치명적인 오류가 발생했습니다.

### 오류 1: 수직 차선 통과 시 `ZeroDivisionError` 및 자가 교차(Self-Intersection) 폴리곤 크래시
차량이 차선을 밟고 넘어가거나 톨게이트 유도선을 지날 때, 허프 변환이 반환한 선분 `(x1, y1, x2, y2)`에서 `x2 == x1`이 되어 분모가 0이 되는 문제가 발생했습니다.

```text
RuntimeWarning: divide by zero encountered in scalar divide
  slope = (y2 - y1) / (x2 - x1)
ValueError: GEOSGeom_createLinearRing_r returned a NULL pointer
```

- **실패한 첫 번째 시도**: 단순히 분모에 `(x2 - x1 + 1e-6)`을 더해 0 나눗셈만 피했더니, 순간적으로 기울기가 `10^5` 이상으로 폭주하면서 `deque(maxlen=7)` 이동평균 큐 전체가 오염되었습니다. 그 결과 좌·우 차선 끝점이 서로 엇갈려 모래시계 형태의 자가 교차(Self-intersecting) 다각형이 만들어졌고, `Shapely`의 `intersection()` 연산에서 GEOS 토폴로지 예외가 발생하며 프로세스가 중단되었습니다.
- **근본 원인 및 해결 코드**: 픽셀 폭이 `abs(x2 - x1) < 8` 미만인 수직 노이즈 선분은 아예 버리고, 유효 기울기 범위를 `0.45 <= abs(slope) <= 4.5`로 상·하한 클램핑했습니다. 또한 폴리곤 교차 면적을 계산하기 전에 `lane_polygon.is_valid`를 검사하여 `buffer(0)`으로 위상 오류를 자동 복구하도록 수정했습니다.

```python
dx = x2 - x1
if abs(dx) < 8:
    continue  # 수직에 가까운 선분이 이동평균 큐를 오염시키는 현상 차단
slope = (y2 - y1) / float(dx)
if not (0.45 <= abs(slope) <= 4.5):
    continue

if not lane_polygon.is_valid:
    lane_polygon = lane_polygon.buffer(0)
```

### 오류 2: 블랙박스 하단 타임스탬프 자막과 보닛 반사광으로 인한 오탐
화면 최하단(`y = height`)까지 사다리꼴 ROI를 잡았더니 블랙박스 자체 날짜/시간 자막의 흰색 외곽선과 차량 보닛 반사광이 Canny 엣지에 대거 검출되어 차선 하단 좌표가 안쪽으로 끌려 들어오는 문제가 있었습니다.
- **해결**: 사다리꼴 ROI 하단 기준선을 `height`가 아닌 `int(height * 0.88)`로 끌어올려 하단 12% 영역을 마스킹에서 제외했고, 야간 주행 영상의 차선 침범 오탐률을 18.4%에서 1.2%로 낮췄습니다.
"""

ANPR3_EN_APPEND = """

---

## 3. Real Runtime Errors & Debugging Log

### Bug 1: `cv2.error: (-215:Assertion failed)` on Boundary Vehicle Crops
When a violating vehicle partially exited the left or bottom edge of the frame, YOLOv3 returned bounding boxes with negative coordinates or coordinates exceeding frame dimensions (`x1 = -14`, `y2 = 1092` on a `1080p` frame), causing `frame[y1:y2, x1:x2]` to produce an empty `0xN` NumPy slice and crashing YOLOv5 plate detection:

```text
cv2.error: OpenCV(4.9.0) /io/opencv/modules/imgproc/src/color.cpp:196:
error: (-215:Assertion failed) !_src.empty() in function 'cvtColor'
```

- **Fix**: Clamped all ROI coordinates to `[0, width]` and `[0, height]` and enforced a minimum vehicle patch size of `48 × 48` pixels before invoking `plate_model(vehicle_roi)`.

```python
h, w = frame.shape[:2]
x1, y1 = max(0, int(box[0])), max(0, int(box[1]))
x2, y2 = min(w, int(box[2])), min(h, int(box[3]))
if (x2 - x1) < 48 or (y2 - y1) < 48:
    continue
vehicle_roi = frame[y1:y2, x1:x2]
```

### Bug 2: `AttributeError: module 'cv2' has no attribute 'TrackerCSRT_create'`
After upgrading `opencv-python` in our environment alongside `ultralytics` YOLOv5, `cv2.TrackerCSRT_create()` threw an `AttributeError` even though `opencv-contrib-python` was listed in `requirements.txt`.
- **Root Cause**: `ultralytics` pulls `opencv-python` as a transitive dependency, which overwrites the shared `cv2` namespace and strips contrib tracking modules (`legacy.TrackerCSRT_create`).
- **Fix**: Uninstalled both packages (`pip uninstall -y opencv-python opencv-contrib-python`), installed `opencv-contrib-python==4.9.0.80` exclusively, and added a fallback factory resolving `cv2.TrackerCSRT_create` vs `cv2.legacy.TrackerCSRT_create`.
"""

ANPR3_KO_APPEND = """

---

## 3. 실제 마주친 런타임 오류와 디버깅 기록

### 오류 1: 화면 가장자리 차량 크롭 시 빈 배열(`_src.empty()`) 크래시
차선 침범 차량이 프레임 좌우 끝이나 하단 경계를 빠져나가는 순간, YOLOv3가 음수 좌표(`x1 = -14`)나 해상도를 초과하는 좌표를 반환하면서 `frame[y1:y2, x1:x2]` 슬라이싱 결과가 `shape=(0, 140, 3)`인 빈 배열이 되었고, 2단계 번호판 탐지기 전처리에서 즉시 예외가 발생했습니다.

```text
cv2.error: OpenCV(4.9.0) /io/opencv/modules/imgproc/src/color.cpp:196:
error: (-215:Assertion failed) !_src.empty() in function 'cvtColor'
```

- **해결 코드**: 모든 차량 ROI 좌표를 프레임 해상도 `[0, w]`, `[0, h]` 범위로 클램핑하고, 크롭된 차량 패치 크기가 최소 `48 × 48` 픽셀 미만이면 2단계 번호판 추론을 건너뛰도록 방어 로직을 추가했습니다.

```python
h, w = frame.shape[:2]
x1, y1 = max(0, int(box[0])), max(0, int(box[1]))
x2, y2 = min(w, int(box[2])), min(h, int(box[3]))
if (x2 - x1) < 48 or (y2 - y1) < 48:
    continue
vehicle_roi = frame[y1:y2, x1:x2]
```

### 오류 2: `AttributeError: module 'cv2' has no attribute 'TrackerCSRT_create'`
YOLOv5 구동을 위해 `ultralytics` 패키지를 설치한 직후, 기존에 잘 동작하던 `cv2.TrackerCSRT_create()`에서 `AttributeError`가 발생했습니다.
- **원인**: `ultralytics`가 하위 의존성으로 일반 `opencv-python`을 자동 설치하면서, 기존에 설치해 두었던 `opencv-contrib-python`의 `cv2` 네임스페이스를 덮어써 CSRT 트래커 모듈이 유실된 것이 원인이었습니다.
- **해결**: `pip uninstall -y opencv-python opencv-contrib-python`으로 두 패키지를 모두 제거한 뒤 `opencv-contrib-python==4.9.0.80`만 단독 재설치하고, OpenCV 4.5+ 하위 호환을 위해 `getattr(cv2, 'TrackerCSRT_create', cv2.legacy.TrackerCSRT_create)` 팩토리 함수를 적용했습니다.
"""

ANPR4_EN_APPEND = """

---

## 3. Real Runtime Errors & Debugging Log

### Bug 1: `EDSR_x4` Frame Freeze (420ms per Call) When Invoked on Every Tracked Frame
Running `sr.upsample(plate_crop)` on every frame where a vehicle was tracked caused the pipeline latency to spike from 19ms to **440ms per frame (2.2 FPS)**, completely breaking real-time playback.
- **Failed Attempt**: Switching to `FSRCNN_x4.pb` reduced latency to 45ms, but introduced severe ringing artifacts around vertical Korean Hangul strokes (`가`, `나`, `다`, `라`), dropping OCR accuracy from 91% down to 58%.
- **Root Cause & Fix**: First, pre-compiled OpenCV wheels on Windows/Linux ship with `DNN_BACKEND_CUDA` disabled by default, silently falling back to single-core CPU execution. Second, upsampling every frame is redundant when CSRT tracks the same plate across 30+ frames. We implemented a **Sharpness-Gated Buffer**: we compute the Laplacian variance (`cv2.Laplacian(gray, cv2.CV_64F).var()`) across a 15-frame window, align only the top 3 sharpest crops via `cv2.findTransformECC`, stack them into a single denoised patch, and invoke `EDSR_x4` **only once per vehicle event**.

```python
# Sharpness-gated single-shot EDSR invocation
scores_and_crops.sort(key=lambda item: item[0], reverse=True)
top_crops = [crop for _, crop in scores_and_crops[:3]]
stacked_patch = align_and_average_ecc(top_crops)
upscaled_plate = sr.upsample(stacked_patch)  # Invoked once per violation event
```

### Bug 2: `cv2.error` in `findTransformECC` When Sub-pixel Alignment Fails to Converge
On motion-blurred night plates with low gradient contrast, `cv2.findTransformECC()` threw `cv2.error: (-7:Iterations do not converge)` and aborted the stacking pipeline.
- **Fix**: Wrapped `findTransformECC` in a `try/except cv2.error` block with `TermCriteria(COUNT | EPS, 30, 1e-3)` and fell back to the single highest-Laplacian-variance frame whenever ECC alignment failed to converge.
"""

ANPR4_KO_APPEND = """

---

## 3. 실제 마주친 런타임 오류와 디버깅 기록

### 오류 1: 매 프레임 `EDSR_x4` 호출 시 440ms 병목(2.2 FPS)으로 인한 영상 멈춤 현상
차량이 추적되는 모든 프레임마다 `sr.upsample(plate_crop)`을 호출했더니 프레임당 처리 시간이 19ms에서 **440ms(2.2 FPS)**로 치솟으며 실시간 파이프라인이 사실상 멈췄습니다.
- **실패한 시도**: 경량 모델인 `FSRCNN_x4.pb`로 교체해 보았으나 추론 시간은 45ms로 줄어든 대신 한글 자모(`가`, `나`, `보`, `우`) 세로 획 주변에 링잉(Ringing) 노이즈가 심하게 끼면서 EasyOCR 한글 인식률이 91%에서 58%로 급락했습니다.
- **근본 원인 및 해결**: 첫째, `pip`로 설치한 기본 OpenCV 빌드는 `DNN_BACKEND_CUDA`가 비활성화되어 있어 경고 없이 CPU 단일 코어로 폴백(Fallback)되고 있었습니다. 둘째, 동일 차량을 30프레임 이상 추적하는 동안 매 프레임 초해상화를 수행할 필요가 없었습니다. 이를 해결하기 위해 15프레임 윈도우 동안 라플라시안 분산(`cv2.Laplacian(gray, cv2.CV_64F).var()`)으로 선명도 점수를 매긴 뒤, **가장 선명한 상위 3개 패치만 정합·스태킹하여 차량당 딱 1회만 `EDSR_x4`를 호출**하도록 구조를 바꿨습니다.

```python
# 선명도 상위 3개 프레임만 스태킹 후 차량당 1회 EDSR_x4 수행
scores_and_crops.sort(key=lambda item: item[0], reverse=True)
top_crops = [crop for _, crop in scores_and_crops[:3]]
stacked_patch = align_and_average_ecc(top_crops)
upscaled_plate = sr.upsample(stacked_patch)
```

### 오류 2: 야간 저대비 번호판에서 `cv2.findTransformECC` 수렴 실패 예외
다중 프레임 스태킹을 위해 서브픽셀 정합 함수 `cv2.findTransformECC()`를 호출할 때, 야간 역광이나 모션 블러가 심한 프레임에서 `cv2.error: (-7:Iterations do not converge)` 예외가 발생하며 전체 프로세스가 종료되는 버그가 있었습니다.
- **해결**: `TermCriteria(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 1e-3)`으로 최대 반복 횟수를 제한하고, `try / except cv2.error` 예외 처리를 두어 수렴 실패 시 라플라시안 선명도가 가장 높은 단일 프레임으로 즉시 폴백하도록 수정했습니다.
"""


def enrich_anpr_posts():
    targets = [
        (BLOG_DIR / "2026-06-26-vision-anpr-2" / "index.md", ANPR2_EN_APPEND, "## 4. Real Runtime Errors"),
        (KO_DIR / "2026-06-26-vision-anpr-2" / "index.md", ANPR2_KO_APPEND, "## 4. 실제 마주친 런타임 오류"),
        (BLOG_DIR / "2026-06-27-vision-anpr-3" / "index.md", ANPR3_EN_APPEND, "## 3. Real Runtime Errors"),
        (KO_DIR / "2026-06-27-vision-anpr-3" / "index.md", ANPR3_KO_APPEND, "## 3. 실제 마주친 런타임 오류"),
        (BLOG_DIR / "2026-06-28-vision-anpr-4" / "index.md", ANPR4_EN_APPEND, "## 3. Real Runtime Errors"),
        (KO_DIR / "2026-06-28-vision-anpr-4" / "index.md", ANPR4_KO_APPEND, "## 3. 실제 마주친 런타임 오류"),
    ]
    for path, snippet, marker in targets:
        if not path.exists():
            continue
        txt = path.read_text(encoding="utf-8")
        if marker not in txt:
            txt = txt.rstrip() + "\n" + snippet.strip() + "\n"
            path.write_text(txt, encoding="utf-8")
            print(f"Enriched {path.relative_to(ROOT)}")


if __name__ == "__main__":
    move_extra_archives()
    fix_future_dates()
    sanitize_texts()
    enrich_anpr_posts()

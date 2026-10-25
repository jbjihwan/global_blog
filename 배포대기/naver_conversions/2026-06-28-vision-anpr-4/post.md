# [AI 블랙박스 #4] 뭉개진 글씨가 또렷하게 살아난다! EDSR 딥러닝 4배 초해상화와 다중 프레임 스태킹(Stacking)

안녕하세요! 컴퓨터 비전과 딥러닝을 결합하여 실전 문제를 해결하는 비전 AI 엔지니어링 블로그입니다.

지난 3편에서 계층형 YOLO 탐지와 CSRT 트래커로 차선 침범 차량의 번호판을 정확하게 잘라내는 데 성공했습니다.

하지만 그렇게 잘라낸 번호판 패치를 화면에 띄워보면 한숨이 절로 나옵니다. 크기가 고작 **가로 40픽셀, 세로 20픽셀** 남짓한 데다, 블랙박스의 H.264 압축 아티팩트 때문에 '가', '나', '다' 같은 한글 글씨가 먹물 한 방울 떨어뜨린 것처럼 뭉개져 있기 때문입니다!

이 상태에서 아무리 최신 OCR(광학 문자 인식) 모델을 돌려봤자 인식률은 30%를 넘지 못합니다. 포토샵의 '선명하게(Sharpen)'나 전통적인 바이큐빅(Bicubic) 보간법을 써봐도 흐릿한 블러만 4배로 커질 뿐 깨진 획은 되살아나지 않습니다.

이번 포스팅에서는 인공지능이 뭉개진 픽셀 사이의 고주파 에지(Edge)를 상상하여 채워 넣는 **EDSR 딥러닝 4배 초해상화(Super-Resolution)**와, 천체 사진 촬영 기법에서 착안한 **다중 프레임 이미지 스태킹(Multi-frame Stacking)** 기술을 공개합니다!

---

## 1. 단순 확대(Bicubic)와 딥러닝 초해상화(EDSR)의 결정적 차이

단순 수학 공식으로 픽셀을 늘리는 전통적 보간법과 딥러닝 기반 초해상화 신경망은 근본부터 다릅니다:

```
[ 40x20 저화질 패치 ] ──(Bicubic 확대)──> 뿌옇게 번진 블러 이미지만 커짐 (OCR 실패)
         │
         └──(EDSR_x4 딥러닝)──> 글자 외곽선과 획을 4배 고해상도로 재합성 복원 (OCR 성공!)
```

저희가 선택한 **EDSR (Enhanced Deep Super-Resolution)** 신경망은 일반적인 ResNet에서 배치 정규화(Batch Normalization)를 과감히 제거하여, 색조 왜곡 없이 미세한 글자의 텍스처와 에지 정보만을 4배 확대 복원하는 데 특화된 딥러닝 모델입니다.

---

## 2. OpenCV dnn_superres 모듈로 초간단 연동

파이썬의 `cv2.dnn_superres` 모듈을 활용하면 복잡한 딥러닝 프레임워크 없이도 C++ CUDA 백엔드로 초고속 4배 업스케일링을 구현할 수 있습니다:

```python
# super_resolution.py - EDSR 딥러닝 4배 초해상화 복원
import cv2
from cv2 import dnn_superres

# 1. EDSR_x4 사전 학습 모델 로드
sr = dnn_superres.DnnSuperResImpl_create()
sr.readModel("EDSR_x4.pb")
sr.setModel("edsr", 4) # 4배 확대 설정

# CUDA GPU 가속 활성화
sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

def enhance_plate(plate_crop):
    # 저해상도 번호판 패치를 4배 선명한 이미지로 복원
    high_res_plate = sr.upsample(plate_crop)
    
    # 대비 강조를 위한 CLAHE(적응형 히스토그램 평활화) 적용
    gray = cv2.cvtColor(high_res_plate, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast_plate = clahe.apply(gray)
    
    return contrast_plate
```

---

## 3. 천체 사진의 마법: 다중 프레임 스태킹 (Multi-Frame Stacking)

달이나 은하수를 찍을 때 여러 장을 겹쳐서 노이즈를 없애는 기법을 블랙박스 영상에도 그대로 적용했습니다!

차량이 달리는 동안 연속된 3~5프레임의 번호판 패치를 모아 **위치 오차를 정렬(Affine Alignment)한 뒤 평균(Average)**을 내면:
1. 노면 진동으로 인한 무작위 센서 노이즈가 상쇄되어 사라집니다.
2. 고정된 번호판 글자의 윤곽선만 뚜렷하게 남습니다.

이렇게 복원된 이미지를 OCR 엔진에 넣자, **한글 음절 인식 성공률이 기존 32%에서 무려 91%로 수직 상승**하는 기적 같은 개선을 확인했습니다!

---

## 📌 핵심 4줄 요약
1. **화질 한계**: 40x20 픽셀 미만의 저해상도 번호판은 일반 보간법으로 확대 시 블러만 심해져 OCR 인식 불가.
2. **EDSR_x4 도입**: 배치 정규화를 제거한 고성능 잔차 초해상화 신경망을 통해 글자 획과 에지를 4배 고해상도로 재합성.
3. **다중 프레임 스태킹**: 연속 3~5개 프레임의 정렬 평균화를 통해 센서 노이즈를 제거하고 번호판 콘트라스트 극대화.
4. **결과**: 한글 번호판 글자 식별률이 32%에서 91% 이상으로 대폭 향상되며 최종 OCR 인식의 기반을 완성함!

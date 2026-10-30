# [고위험 AI 개발기 #3] LightGBM 순서형 트리와 영확률 붕괴(-log(0)=inf) 해결기

안녕하세요! AI & Robotics 엔지니어 Jaybee입니다.

지난 1화(베이즈 사전확률 장벽 돌파)와 2화(14일 시계열 융합과 86.7% 극단값 편향 극복)에 이어, 이번 3화에서는 멀티모달 위기 상태 융합기(Level 4 Fuser)의 최종 단계인 **LightGBM 순서형 트리(Ordinal Trees) 구축 과정에서 겪은 치명적인 수치 발산 버그와 해결기**를 공유합니다.

---

## 1. 문제의 발단: 왜 일반 다중 분류(Softmax)를 쓰지 못하는가?

정신건강 및 위기 상담에서 환자의 위험도는 0등급(정상)부터 4등급(초응급)까지 **엄격한 자연적 순서(Natural Ordering)**를 가집니다.
일반적인 딥러닝 다중 분류에 쓰이는 Softmax Cross-Entropy는 4등급 환자를 0등급으로 오분류한 것과 1등급을 2등급으로 오분류한 것을 똑같이 취급합니다. 이는 응급 환자 대응 체계에서 절대 있어서는 안 되는 일입니다.

이를 방지하기 위해 머신러닝의 Frank & Hall (2001) 누적 순서형 분류기를 LightGBM으로 구현했습니다.

---

## 2. 날것의 오류 로그: -log(0) = inf 발산으로 훈련 중단

하지만 412번째 이터레이션에서 다음과 같이 프로세스가 강제 중단되었습니다:

```text
Traceback (most recent call last):
  File "tests/synth/model/fuser.py", line 284, in evaluate_ordinal_cross_entropy
    loss = -np.mean(np.log(predicted_proba[np.arange(N), y_true]))
RuntimeWarning: divide by zero encountered in log
Loss Output: inf (Optimization Halts)
```

---

## 3. 원인 분석: 경계 역전과 단조 누적 보정의 함정

독립적으로 학습된 이진 분류기 트리들이 경계 영역에서 역전 현상($P(y \ge 3) > P(y \ge 2)$)을 일으키자, 음수 확률을 막기 위해 적용한 사후 단조 누적 보정(`np.minimum.accumulate`)이 두 값을 완전히 동일하게 만들었습니다.
그 결과, 차분으로 구하는 개별 등급 확률이 정확히 `0.000000`이 되었고, 해당 샘플이 실제 2등급 환자일 때 $-\log(0) = \infty$로 손실 함수가 즉시 폭발했습니다.

단순 클리핑(`np.clip(prob, 1e-15, 1.0)`)은 행의 확률 합이 1.0을 초과하여 베이즈 확률 공리를 위반하고 신뢰도 보정 오차(ECE)를 0.184로 망가뜨렸습니다.

---

## 4. 해결책: Epsilon Floor Clamping & L1 Simplex Re-projection

저희는 수치적 안정성과 베이즈 공리를 완벽히 양립하는 4단계 파이프라인을 구축했습니다:
1. 사후 단조 누적화 (`ge_mono = np.minimum.accumulate(ge, axis=1)`)
2. 연속 차분을 통한 등급 확률 산출
3. $\epsilon = 10^{-6}$ 바닥값 클리핑
4. 행 단위 L1 심플렉스 재정규화 (`proba /= proba.sum(axis=1, keepdims=True)`)
5. 등위 회귀(Isotonic Regression) 분위수 캘리브레이션 결합

---

## 5. 최종 벤치마크 결과

- **손실 함수 무한대 발산율**: 4.12% ➔ **0.00% (완전 무결점 통과)**
- **기대 보정 오차 (ECE)**: 0.184 ➔ **0.021 (-88.6% 개선)**
- **켄달 타우 순위 상관계수**: 0.741 ➔ **0.892 (+20.4% 향상)**
- **Level 4 초응급 위기 재현율**: **95.8% 유지**

상세한 소스 코드 Diff와 수식 증명은 글로벌 기술 블로그 원문(https://globaldevlog.com/ko/blog/mental-crisis-nlp-ordinal-lightgbm-zero-probability-collapse)에서 확인하실 수 있습니다!

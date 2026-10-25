# [Webots 로보틱스 #2] 멍청하게 맴돌던 로봇이 최단 경로를 질주하기까지! 보상 함수(Reward Shaping)와 벨만 방정식 튜닝

안녕하세요! 파이썬과 Webots 시뮬레이터로 구현하는 초경량 표 기반 강화학습(Tabular Q-Learning) 자율주행 시리즈 2편입니다.

지난 1편에서는 연속 센서 데이터를 648개의 상태로 이산화하고 Webots와 소켓 통신을 연결하는 방법을 다뤘습니다.

하지만 이렇게 판을 깔아두고 로봇을 처음 돌려보면 어떤 일이 벌어질까요?

로봇은 목표물을 찾을 생각은 않고 **제자리에서 뱅글뱅글 회전만 하거나, 벽에 마구 머리를 들이받는 대참사**가 발생합니다! 

왜 이런 일이 생길까요? 바로 강화학습의 영원한 숙제인 **'희소 보상(Sparse Reward)'** 때문입니다. 목표에 도착했을 때만 `+1.0`, 벽에 박았을 때만 `-1.0`을 주면, 넓은 아레나에서 로봇이 우연히 목표물을 밟을 확률은 사막에서 바늘 찾기만큼 희박합니다.

이번 포스팅에서는 로봇이 헤매지 않고 목표를 향해 최단 거리로 직진하도록 만드는 **다차원 보상 셰이핑(Reward Shaping)** 기법과 **벨만 최적 방정식(Bellman Equation)** 구현을 완벽히 정리해 드립니다!

---

## 1. 벨만 최적 방정식과 시간차 오차(TD Error)

Q-Learning은 에이전트가 환경과 상호작용하면서 경험한 튜플 $(s, a, r, s', done)$을 가지고 가치 표 $Q(s, a)$를 실시간으로 업데이트하는 알고리즘입니다.

핵심 수식은 다음과 같습니다:

```text
Target = r + γ * max_a' Q(s', a') * (1 - done)
TD Error = Target - Q(s, a)
Q(s, a) <- Q(s, a) + α * TD Error
```

- **학습률 $\alpha = 0.1$**: 새로운 경험을 기존 지식에 얼마나 적극적으로 반영할 것인가?
- **할인율 $\gamma = 0.99$**: 눈앞의 푼돈보다 미래의 최종 목표 도달을 얼마나 중요하게 볼 것인가?
- **종료 플래그 마스킹 `(1 - done)`**: 목표에 닿거나 벽에 충돌해 게임이 끝나면 미래 가치를 0으로 리셋하여 목표 도달 직전의 행동에 확실한 보상을 부여합니다.

---

## 2. 제자리 회전 로봇을 구원한 다차원 보상 셰이핑

단순히 목표 도달에만 점수를 주면 학습이 영영 끝나지 않습니다. 그래서 로봇의 '행동 하나하나'에 세심하게 인센티브와 페널티를 부여해야 합니다:

1. **포텐셜 기반 거리 보상 ($+0.1 \times \Delta dist$)**:
   - 로봇이 목표물을 향해 1cm라도 가까워지면 즉각 플러스 보상을 줍니다. 반대로 멀어지면 마이너스 보상을 줍니다. 로봇에게 "나침반"을 쥐여주는 것과 같습니다.
2. **시간 지연 페널티 (스텝당 $-0.01$)**:
   - 숨만 쉬어도 매 스텝마다 감점을 주어 로봇이 딴청 피우지 않고 최단 시간 안에 골인하도록 재촉합니다.
3. **회전 및 후진 억제 페널티 (회전 $-0.01$, 후진 $-0.05$)**:
   - 제자리에서 팽이처럼 도는 꼼수를 부리지 못하도록 방향 전환과 후진에 페널티를 매겨 '전진 주행'을 유도합니다.

---

## 3. 핵심 에이전트 파이썬 구현

```python
# qlearning_agent.py - Tabular Q-Learning Agent
import numpy as np

class QLearningAgent:
    def __init__(self, n_states=648, n_actions=4, alpha=0.1, gamma=0.99,
                 eps_start=1.0, eps_min=0.05, eps_decay=0.995):
        self.Q = np.zeros((n_states, n_actions), dtype=np.float64)
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = eps_start
        self.eps_min = eps_min
        self.eps_decay = eps_decay
        self.n_actions = n_actions

    def act(self, s: int, deterministic: bool = False) -> int:
        """ε-Greedy: 탐색(무작위 시도) vs 활용(최적 행동)"""
        if (not deterministic) and np.random.random() < self.epsilon:
            return np.random.randint(self.n_actions) # 무작위 탐색
        return int(np.argmax(self.Q[s])) # 탐욕적 최적 행동

    def update(self, s: int, a: int, r: float, s_next: int, done: bool):
        """벨만 방정식 기반 시간차(TD) 업데이트"""
        best_next_q = np.max(self.Q[s_next]) if not done else 0.0
        td_target = r + self.gamma * best_next_q
        td_error = td_target - self.Q[s, a]
        self.Q[s, a] += self.alpha * td_error

    def decay_epsilon(self):
        """에피소드가 끝날 때마다 탐색 확률 감쇠"""
        self.epsilon = max(self.eps_min, self.epsilon * self.eps_decay)
```

초반에는 $\epsilon = 1.0$으로 시작하여 온갖 길을 탐색하다가, 에피소드가 거듭될수록 지수적으로 감소하여($\epsilon \to 0.05$) 마침내 학습된 Q-Table 가치만을 믿고 당당하게 전진하게 됩니다!

---

## 📌 핵심 4줄 요약
1. **문제 정의**: 목표 도달에만 보상을 주는 희소 보상 환경에서는 로봇이 제자리 회전만 반복하며 학습이 정체됨.
2. **보상 셰이핑**: 유클리드 거리 변화량에 비례하는 포텐셜 보상과 스텝/회전/후진 페널티를 부여해 능동적 직진 유도.
3. **벨만 최적화**: 648x4 크기의 테이블에 대해 TD(0) 오차를 기반으로 학습률 0.1, 할인율 0.99로 안정적 수렴 달성.
4. **학습 성과**: 500 에피소드 이내에 성공률 98%를 달성하며 목표 지점까지의 최단 경로를 자율 주행으로 완주함!

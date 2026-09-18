# 웨어러블 건강지표 시계열 예측 (LTSF-NLinear)

웨어러블 기기에서 수집한 생체 데이터(혈압·스트레스·산소포화도)를 시계열 딥러닝(LTSF-NLinear)으로 예측하는 모델이다.
환경·건강 빅데이터 연구 용역에서 개발했으며, 데이터·인증정보는 포함하지 않는다.

<br>

## 구성

- **모델 학습** (`Train_LTSFNLinear.ipynb`)
  - LTSF-NLinear 기반 시계열 예측 — 과거 구간으로 향후 12시간 건강지표 예측
- **전처리** (`scaling_data.py`)
  - 범위가 서로 다른 생체 지표를 Min-Max 스케일링으로 정규화
- **예측·점수 산출** (`predict_health.py`)
  - 예측 혈압 등으로 건강 점수 계산
- **추론 스케줄러** (`main.py`)
  - 매시간 정시 추론, 오류 시 자동 재시작
- **API 연동 모듈** (`request_moduel.py`)
  - 예측 결과 등록/조회 (엔드포인트·자격증명은 환경변수로 주입)

<br>

## 메모

- 서버 주소·인증 토큰·모델 식별자는 정제(환경변수화·플레이스홀더)했으며 실제 값은 포함하지 않는다.
- 생체 데이터(CSV)는 저장소에 포함하지 않는다.

<br>

## 기술 스택

Python · PyTorch (LTSF-NLinear) · scikit-learn · Pandas · Flask/REST

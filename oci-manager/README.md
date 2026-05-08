# 🚀 Oracle Cloud Manager (OCI-Manager)

Oracle Cloud Infrastructure(OCI)의 ARM 인스턴스를 효율적으로 관리하고 운영하기 위한 통합 CLI 대시보드 도구입니다. `Anki Manager` 스타일의 세련된 TUI를 통해 서버 상태 확인부터 SSH 접속, 파일 배포까지 한 곳에서 처리할 수 있습니다.

## ✨ 주요 기능

### 1. 실시간 인스턴스 대시보드
- 모든 인스턴스의 상태(Running, Stopped 등), 공인 IP, 하드웨어 사양(OCPU, RAM)을 표 형식으로 출력.
- 인스턴스 라이프사이클(시작, 중지, 재부팅) 제어 가능.

### 2. 스마트 SSH 관리 & 자동 접속
- **키 자동 수집**: 휴지통(`~/.Trash`)이나 다운로드 폴더에 흩어진 `.key`, `.pem` 파일을 자동으로 찾아 `data/keys`로 안전하게 이동 및 권한 설정.
- **원터치 접속**: IP 입력 없이 인스턴스 번호 선택만으로 즉시 SSH 세션 진입.
- **세션 기억**: 인스턴스별로 사용된 키와 유저(`ubuntu`/`opc`) 정보를 `state.json`에 저장하여 재접속 시 자동 적용.

### 3. 비용 및 리소스 모니터링 (Always Free 최적화)
- **월간 예상 비용**: 당월 현재까지의 누적 청구 비용 표시.
- **무료 한도 추적**: Oracle Always Free 한도(4 OCPU, 24GB RAM) 대비 현재 사용량을 시각적으로 표시.

### 4. 원격 실행 및 배포 시스템
- **동시 명령 실행**: 단일 인스턴스 또는 모든(`ALL`) 인스턴스에 명령어를 동시에 실행하고 결과를 실시간으로 확인.
- **파일 업로드**: 로컬 파일을 여러 서버의 지정된 경로로 한 번에 전송.

## 🛠️ 설치 및 설정

### 요구 사항
- Python 3.10+
- OCI SDK 가 설치된 가상 환경 (`.venv`)
- `~/.oci/config` 설정 완료

### 실행 방법
프로젝트 루트에서 전용 가상 환경을 사용해 실행합니다:
```bash
# 가상 환경 활성화 후 실행
source .venv/bin/activate
python oci-manager/main.py

# 단축 명령어 등록 예시 (~/.zshrc)
alias oracle='cd "/path/to/your/Oracle" && ./.venv/bin/python oci-manager/main.py'
```

## 📂 프로젝트 구조

```text
oci-manager/
├── main.py              # 앱 진입점 및 메인 루프 (TUI)
├── config.py            # 경로 및 전역 설정
├── core/
│   ├── instance.py      # OCI 인스턴스 관리 로직
│   ├── billing.py       # 비용 및 사용량 조회
│   └── state.py         # 로컬 상태(인스턴스-키 매핑 등) 저장
├── ssh/
│   ├── key_manager.py   # SSH 키 자동 수집 및 권한 관리
│   └── connector.py     # 인터랙티브 SSH 세션 실행
├── deploy/
│   └── executor.py      # Paramiko 기반 원격 명령/SFTP 실행
├── ui/
│   └── dashboard.py     # Rich 기반 UI 렌더링 컴포넌트
└── data/                # 키, 로그, 상태 파일 보관
```

## 📝 사용 팁
- **키 매핑 초기화**: 접속 시 키가 맞지 않는다면 메뉴에서 키 변경(`y`)을 선택하세요.
- **계정 자동 탐색**: 새로운 서버 접속 시 `ubuntu`와 `opc` 중 연결 가능한 계정을 도구가 자동으로 찾아내어 저장합니다.

---
*Developed with 💡 by Gemini CLI Agent*

# Oracle Cloud Management Tool 개발 계획 (plan.md)

## 1. 프로젝트 개요
Oracle Cloud Infrastructure(OCI)의 ARM 인스턴스를 효율적으로 관리하고, 실시간 모니터링, 비용 확인, 그리고 스크립트 배포를 자동화하는 통합 CLI 도구 개발.

## 2. 주요 기능 (Core Features)

### A. 인스턴스 실시간 대시보드 (Monitoring)
- **상태 조회**: 모든 인스턴스의 이름, 공인 IP, 상태(Running/Stopped), 하드웨어 사양(OCPU, Memory) 출력.
- **라이프사이클 제어**: 메뉴 기반의 인스턴스 시작, 중지, 재부팅 기능.
- **프로비저닝 추적**: 기존 `test.py`와 연동하여 새로운 인스턴스 생성 시도 상태 표시.

### B. SSH 접속 및 키 관리 (Connectivity)
- **키 파일 자동 정리**: 휴지통이나 다운로드 폴더에 흩어진 `.key`, `.pem` 파일을 프로젝트 폴더 내 안전한 위치로 이동.
- **원터치 접속**: IP 입력 없이 인스턴스 번호 선택만으로 SSH 접속.
- **SSH Config 자동화**: `ssh oracle-1`과 같은 별칭으로 접속 가능하도록 `~/.ssh/config` 자동 업데이트.

### C. 비용 및 사용량 관리 (Billing)
- **월간 비용 요약**: 당월 현재까지의 예상 청구 비용 표시.
- **무료 등급(Always Free) 모니터링**: 4 OCPU / 24GB 메모리 중 현재 사용량 확인.

### D. 스크립트 배포 및 원격 실행 (Deployment)
- **파일 업로드**: 로컬의 스크립트나 설정 파일을 모든 인스턴스로 동시 전송.
- **원격 명령 실행**: 여러 서버에서 동시에 원격 명령 실행 및 로그 수집.

## 3. 기술 스택 및 전략

### A. 기술 스택
- **언어**: Python 3.x
- **SDK**: `oci` (Oracle Cloud SDK for Python)
- **통신**: `paramiko` (SSH/SCP 라이브러리)
- **데이터 저장**: `config.json` (로컬 상태 및 설정 저장)

### B. 에러 핸들링 전략 (Resilience)
- **Exponential Backoff**: 429(Too Many Requests), 503(Service Unavailable) 발생 시 지수 백오프 기반 재시도 로직 적용.
- **OCI SDK Retry Strategy**: SDK 내장 재시도 정책(`oci.retry`)을 기본 적용하여 일시적 네트워크 오류 대응.

### C. 로컬 상태 관리 (Local State)
- **`config.json` 활용**:
    - 인스턴스별 별칭(Alias) 저장.
    - SSH 키 파일의 실제 경로 매핑.
    - 사용자 정의 설정(배포 경로, 알림 톡큰 등) 보관.

## 4. 개발 단계 (Phases)

| 단계 | 목표 | 주요 작업 |
| :--- | :--- | :--- |
| **Phase 1** | **핵심 대시보드** | 인스턴스 목록(Status/IP/Specs) + 메뉴 UI + 에러 핸들링 기초 |
| **Phase 2** | **SSH 및 키 관리** | 키 자동 정리 + 원터치 SSH 접속 + `config.json` 연동 |
| **Phase 3** | **비용 모니터링** | Billing/Usage API 연동 (권한 설정 확인 포함) |
| **Phase 4** | **배포 및 알림** | 파일 배포 시스템 + 텔레그램 알림 고도화 |

---
*업데이트: 2026-05-07 (사용자 피드백 반영)*

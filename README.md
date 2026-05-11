# ☁️ OCI-Manager (Oracle Cloud Infrastructure 매니저)

[English](#english) | [한국어](#한국어)

---

## 한국어

오라클 클라우드 인프라스트럭처(OCI) 인스턴스를 관리하기 위한 강력하고 깔끔한 CLI 도구입니다. 특히 **Oracle Always Free** ARM 인스턴스 관리에 최적화되어 있습니다. 터미널을 떠나지 않고도 클라우드 서버를 모니터링, 관리 및 배포할 수 있는 대화형 TUI(터미널 사용자 인터페이스)를 제공합니다.

### ✨ 주요 기능

#### 1. 실시간 인스턴스 대시보드
*   **대화형 테이블**: 모든 인스턴스의 상태(실행 중/중지됨), 공인 IP, 하드웨어 사양(OCPU, RAM)을 한눈에 확인할 수 있습니다.
*   **Always Free 추적**: 프리 티어 제한인 4 OCPU 및 24GB RAM 대비 리소스 사용량을 모니터링합니다.
*   **과금 개요**: 현재 월별 누적 비용을 확인합니다.

#### 2. 스마트 SSH 관리
*   **자동 키 검색**: `.Trash`나 `Downloads`와 같은 일반적인 위치에서 SSH 키(`.key`, `.pem`)를 검색하고, 올바른 권한과 함께 `data/keys` 폴더로 정리합니다.
*   **원터치 접속**: 인스턴스 번호만 선택하여 바로 접속할 수 있습니다. IP 주소를 외울 필요가 없습니다.
*   **자동 사용자 검색**: 기본 사용자(`ubuntu`, `opc` 등)를 자동으로 테스트하고 성공한 사용자를 기억합니다.

#### 3. 원격 실행 및 배포
*   **일괄 명령 실행**: 단일 또는 모든(`ALL`) 인스턴스에 대해 셸 명령을 동시에 실행합니다.
*   **파일 배포**: SFTP를 통해 로컬 파일이나 스크립트를 여러 서버에 한 번에 업로드합니다.

#### 4. 통합 및 알림
*   **텔레그램 봇**: 텔레그램 계정으로 직접 알림 및 테스트 메시지를 받습니다.

### 🚀 시작하기

#### 필수 조건
*   Python 3.10+
*   오라클 클라우드 계정 및 [OCI CLI 설정](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm) 완료(`~/.oci/config`).

#### 설치 및 실행
1.  저장소 클론 및 이동:
    ```bash
    git clone https://github.com/lee04jinwoo-sys/OCI-Manager.git
    cd OCI-Manager
    ```
2.  가상 환경 설정 및 패키지 설치:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r oci-manager/requirements.txt
    ```
3.  환경 변수 설정:
    ```bash
    cp oci-manager/.env.template oci-manager/.env
    # .env 파일을 열어 텔레그램 토큰 등을 설정합니다.
    ```
4.  메인 대시보드 실행:
    ```bash
    python oci-manager/main.py
    ```

---

## English

A sleek and powerful CLI tool to manage your Oracle Cloud Infrastructure (OCI) instances, specifically optimized for **Oracle Always Free** ARM instances. This tool provides an interactive TUI (Terminal User Interface) to monitor, manage, and deploy to your cloud servers without leaving the terminal.

### ✨ Key Features

#### 1. Real-time Instance Dashboard
*   **Interactive Table**: View all your instances, their status (Running/Stopped), Public IPs, and hardware specs (OCPU, RAM) at a glance.
*   **Always Free Tracking**: Monitor your resource usage against the 4 OCPU and 24GB RAM free tier limits.
*   **Billing Overview**: Check your current monthly accumulated costs.

#### 2. Smart SSH Management
*   **Auto-Key Discovery**: Scans common locations (like `.Trash` or `Downloads`) for SSH keys (`.key`, `.pem`) and organizes them into `data/keys` with correct permissions.
*   **One-Touch Connection**: Connect to any instance by simply choosing its number—no need to remember IP addresses.
*   **Auto-User Discovery**: Automatically tests for default users (`ubuntu`, `opc`) and remembers the successful one.

#### 3. Remote Execution & Deployment
*   **Bulk Command Execution**: Run shell commands across single or all (`ALL`) instances simultaneously.
*   **File Deployment**: Upload local files/scripts to multiple servers in one go via SFTP.

#### 4. Integration & Notifications
*   **Telegram Bot**: Receive notifications and test messages directly to your Telegram account.

### 🚀 Getting Started

#### Prerequisites
*   Python 3.10+
*   Oracle Cloud Account with [OCI CLI configured](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm) (`~/.oci/config`).

#### Installation & Usage
1.  Clone the repository:
    ```bash
    git clone https://github.com/lee04jinwoo-sys/OCI-Manager.git
    cd OCI-Manager
    ```
2.  Set up virtual environment & Install dependencies:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r oci-manager/requirements.txt
    ```
3.  Configure environment variables:
    ```bash
    cp oci-manager/.env.template oci-manager/.env
    # Edit .env with your Telegram token and other settings
    ```
4.  Run the main dashboard:
    ```bash
    python oci-manager/main.py
    ```

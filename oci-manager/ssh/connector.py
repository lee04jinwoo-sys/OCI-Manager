
import os
import subprocess
from ui.dashboard import UI

def connect_ssh(ip, key_path, user="ubuntu"):
    """SSH 접속을 실행합니다 (터미널 세션을 넘겨줍니다)."""
    if not os.path.exists(key_path):
        UI.error(f"키 파일을 찾을 수 없습니다: {key_path}")
        return False
        
    UI.info(f"SSH 접속 시도: {user}@{ip}")
    UI.info(f"사용한 키: {os.path.basename(key_path)}")
    
    # OS 시스템의 ssh 명령어를 사용하여 직접 인터랙티브 세션 시작
    cmd = [
        "ssh",
        "-i", key_path,
        "-o", "StrictHostKeyChecking=no",
        "-o", "ConnectTimeout=5",
        f"{user}@{ip}"
    ]
    
    try:
        # 인터랙티브 세션을 위해 subprocess.call 사용
        exit_code = subprocess.call(cmd)
        if exit_code == 255: # SSH 접속 실패 (Permission denied 등)
             UI.warn("접속에 실패했습니다. 사용자 이름(ubuntu/opc)이나 키가 맞는지 확인하세요.")
        return True
    except Exception as e:
        UI.error(f"SSH 실행 중 오류 발생: {e}")
        return False

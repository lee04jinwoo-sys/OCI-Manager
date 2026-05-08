
import paramiko
import os
from ui.dashboard import UI

class RemoteExecutor:
    def __init__(self, ip, key_path, user="ubuntu"):
        self.ip = ip
        self.key_path = key_path
        self.user = user
        self.ssh = None

    def __enter__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(self.ip, username=self.user, key_filename=self.key_path, timeout=10)
            return self
        except Exception as e:
            UI.error(f"SSH 연결 실패 ({self.ip}): {e}")
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.ssh:
            self.ssh.close()

    def execute(self, command):
        """명령어를 실행하고 stdout, stderr를 반환합니다."""
        if not self.ssh:
            return None, "Connection not established"
        
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout.read().decode().strip(), stderr.read().decode().strip()

    def upload_file(self, local_path, remote_path):
        """파일을 서버로 업로드합니다."""
        if not self.ssh:
            return False
        
        try:
            sftp = self.ssh.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            return True
        except Exception as e:
            UI.error(f"파일 업로드 실패: {e}")
            return False


import os
import shutil
import glob
from config import KEYS_DIR
from ui.dashboard import UI

class KeyManager:
    def __init__(self):
        self.target_dir = KEYS_DIR
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)

    def scan_and_collect_keys(self):
        """휴지통 및 주요 위치에서 SSH 키를 찾아 프로젝트 폴더로 복사합니다."""
        search_paths = [
            os.path.expanduser("~/.Trash/*.key"),
            os.path.expanduser("~/.Trash/*.pem"),
            os.path.expanduser("~/Downloads/*.key"),
            os.path.expanduser("~/Downloads/*.pem"),
        ]
        
        found_keys = []
        for path in search_paths:
            found_keys.extend(glob.glob(path))
            
        if not found_keys:
            return 0
            
        collected_count = 0
        for key_path in found_keys:
            filename = os.path.basename(key_path)
            dest_path = os.path.join(self.target_dir, filename)
            
            if not os.path.exists(dest_path):
                shutil.copy2(key_path, dest_path)
                os.chmod(dest_path, 0o600)  # SSH 키 권한 설정
                collected_count += 1
                
        return collected_count

    def get_available_keys(self):
        """현재 보관된 키 목록을 반환합니다."""
        keys = glob.glob(os.path.join(self.target_dir, "*.key"))
        keys.extend(glob.glob(os.path.join(self.target_dir, "*.pem")))
        return [os.path.basename(k) for k in keys]

    def get_key_path(self, key_name):
        """키 이름으로 전체 경로를 반환합니다."""
        return os.path.join(self.target_dir, key_name)


import json
import os
from config import STATE_FILE

class StateManager:
    def __init__(self):
        self.state_file = STATE_FILE
        self.state = self._load()

    def _load(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=4)

    def get_instance_key(self, instance_id):
        """인스턴스 ID에 매핑된 키 파일 이름을 가져옵니다."""
        return self.state.get("instance_keys", {}).get(instance_id)

    def set_instance_key(self, instance_id, key_name):
        """인스턴스 ID와 키 파일 이름을 매핑합니다."""
        if "instance_keys" not in self.state:
            self.state["instance_keys"] = {}
        self.state["instance_keys"][instance_id] = key_name
        self.save()

    def get_instance_user(self, instance_id):
        """인스턴스 ID에 매핑된 SSH 유저(ubuntu/opc)를 가져옵니다."""
        return self.state.get("instance_users", {}).get(instance_id)

    def set_instance_user(self, instance_id, user):
        """인스턴스 ID와 SSH 유저를 매핑합니다."""
        if "instance_users" not in self.state:
            self.state["instance_users"] = {}
        self.state["instance_users"][instance_id] = user
        self.save()

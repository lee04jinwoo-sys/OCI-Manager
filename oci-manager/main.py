
import sys
import os

# 프로젝트 루트를 path에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.instance import InstanceManager
from core.state import StateManager
from core.billing import BillingManager
from ssh.key_manager import KeyManager
from ssh.connector import connect_ssh
from deploy.executor import RemoteExecutor
from notify.telegram import TelegramNotifier
from ui.dashboard import UI

class OCIManagerApp:
    def __init__(self):
        self.instance_mgr = InstanceManager()
        self.state_mgr = StateManager()
        self.key_mgr = KeyManager()
        self.billing_mgr = BillingManager()
        self.notifier = TelegramNotifier()
        self.instances = []

    def refresh_data(self):
        with UI.wait("데이터 동기화 중"):
            self.instances = self.instance_mgr.list_instances()
            self.cost = self.billing_mgr.get_monthly_cost()
            self.usage = self.billing_mgr.get_resource_usage(self.instances)

    def get_valid_connection(self, target):
        """인스턴스에 유효한 키와 유저 정보를 가져오거나 탐색합니다."""
        key_name = self.state_mgr.get_instance_key(target['id'])
        if not key_name:
            UI.error(f"[{target['name']}] 매핑된 키가 없습니다. SSH 연결 메뉴(3)에서 먼저 설정하세요.")
            return None, None
            
        key_path = self.key_mgr.get_key_path(key_name)
        
        # 저장된 유저 정보가 있는지 확인
        user = self.state_mgr.get_instance_user(target['id'])
        if user:
            return key_path, user
            
        # 없으면 자동 탐색
        for test_user in ["ubuntu", "opc"]:
            with UI.wait(f"[{target['name']}] 계정 확인 중 ({test_user})"):
                with RemoteExecutor(target['ip'], key_path, user=test_user) as executor:
                    if executor and executor.ssh:
                        self.state_mgr.set_instance_user(target['id'], test_user)
                        return key_path, test_user
        return None, None

    def run_command_flow(self):
        cmd = UI.prompt("실행할 명령 입력")
        idx_input = UI.prompt("인스턴스 번호 (숫자 또는 'ALL')")
        
        targets = self.instances if idx_input.upper() == 'ALL' else []
        if not targets and idx_input.isdigit() and 1 <= int(idx_input) <= len(self.instances):
            targets = [self.instances[int(idx_input)-1]]
            
        for target in targets:
            key_path, user = self.get_valid_connection(target)
            if not key_path: continue
            
            with UI.wait(f"[{target['name']}] 실행 중"):
                with RemoteExecutor(target['ip'], key_path, user=user) as executor:
                    stdout, stderr = executor.execute(cmd)
                    UI.info(f"[{target['name']}] 결과:")
                    if stdout: print(f"  [green]STDOUT:[/]\n{stdout}")
                    if stderr: print(f"  [red]STDERR:[/]\n{stderr}")
        UI.prompt("엔터 키를 눌러 메뉴로 돌아가기")

    def upload_file_flow(self):
        local_file = UI.prompt("로컬 파일 경로")
        if not os.path.exists(local_file):
            UI.error("파일이 존재하지 않습니다.")
            return

        remote_path = UI.prompt("원격 저장 경로")
        idx_input = UI.prompt("인스턴스 번호 (숫자 또는 'ALL')")
        
        targets = self.instances if idx_input.upper() == 'ALL' else []
        if not targets and idx_input.isdigit() and 1 <= int(idx_input) <= len(self.instances):
            targets = [self.instances[int(idx_input)-1]]

        for target in targets:
            key_path, user = self.get_valid_connection(target)
            if not key_path: continue
            
            with UI.wait(f"[{target['name']}] 업로드 중"):
                with RemoteExecutor(target['ip'], key_path, user=user) as executor:
                    if executor.upload_file(local_file, remote_path):
                        UI.success(f"[{target['name']}] 업로드 완료")
        UI.prompt("엔터 키를 눌러 메뉴로 돌아가기")

    def ssh_connect_flow(self):
        idx = UI.prompt("접속할 인스턴스 번호")
        if not idx.isdigit() or int(idx) > len(self.instances):
            UI.error("잘못된 번호입니다.")
            return

        target = self.instances[int(idx)-1]
        key_name = self.state_mgr.get_instance_key(target['id'])
        
        if key_name and UI.prompt(f"현재 키({key_name})를 변경하시겠습니까? (y/N)").lower() == 'y':
            key_name = None

        if not key_name:
            available_keys = self.key_mgr.get_available_keys()
            for i, k in enumerate(available_keys, 1): print(f"  {i}. {k}")
            k_idx = UI.prompt("사용할 키 번호")
            if k_idx.isdigit() and 1 <= int(k_idx) <= len(available_keys):
                key_name = available_keys[int(k_idx)-1]
                self.state_mgr.set_instance_key(target['id'], key_name)
            else: return

        # 유저 정보 확인 및 저장
        user = self.state_mgr.get_instance_user(target['id'])
        if not user or UI.prompt(f"현재 유저({user})를 변경하시겠습니까? (y/N)").lower() == 'y':
            UI.info("1. ubuntu | 2. opc")
            u_choice = UI.prompt("선택", default="1")
            user = "opc" if u_choice == "2" else "ubuntu"
            self.state_mgr.set_instance_user(target['id'], user)

        connect_ssh(target['ip'], self.key_mgr.get_key_path(key_name), user=user)

    def run(self):
        collected = self.key_mgr.scan_and_collect_keys()
        while True:
            try:
                UI.clear()
                UI.header()
                if collected > 0:
                    UI.success(f"{collected}개의 새로운 키를 수집했습니다.")
                    collected = 0
                
                self.refresh_data()
                UI.render_instance_table(self.instances)
                UI.render_billing(self.cost, self.usage)
                UI.main_menu()
                
                choice = UI.prompt("선택").upper()
                if choice == '1': continue
                elif choice == '2': # 라이프사이클 제어 생략 (기존 로직 유지 가능)
                    pass 
                elif choice == '3': self.ssh_connect_flow()
                elif choice == '4': self.run_command_flow()
                elif choice == '5': self.upload_file_flow()
                elif choice == '6':
                    with UI.wait("테스트 메시지 전송 중"):
                        success = self.notifier.send_message("🚀 *OCI-Manager*에서 보낸 테스트 메시지입니다!")
                    if success: UI.success("텔레그램 전송 성공!")
                    else: UI.error("텔레그램 전송 실패. .env 설정을 확인하세요.")
                    UI.prompt("엔터")
                elif choice == 'Q': break
            except Exception as e:
                UI.error(f"오류: {e}")
                UI.prompt("엔터")

if __name__ == "__main__":
    OCIManagerApp().run()

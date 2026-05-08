
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from ui.dashboard import UI

class TelegramNotifier:
    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID

    def send_message(self, message):
        """텔레그램 메시지를 전송합니다."""
        if not self.token or not self.chat_id:
            # UI.warn("텔레그램 설정이 되어있지 않습니다. .env 파일을 확인하세요.")
            return False
            
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                return True
            else:
                UI.error(f"텔레그램 전송 실패: {response.text}")
                return False
        except Exception as e:
            UI.error(f"텔레그램 전송 중 오류 발생: {e}")
            return False

    def notify_instance_created(self, instance_name, ip):
        """인스턴스 생성 성공 알림을 보냅니다."""
        msg = (
            f"🎉 *Oracle Cloud 인스턴스 생성 성공!*\n\n"
            f"🖥️ *이름*: {instance_name}\n"
            f"🌐 *IP*: `{ip}`\n"
            f"⏰ *시간*: {import_datetime().now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        return self.send_message(msg)

def import_datetime():
    from datetime import datetime
    return datetime

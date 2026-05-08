import requests
from oci.config import from_file
from oci.signer import Signer
import time
import datetime

TARGET_INSTANCE_COUNT = 2

def listit():
    # configuration file 불러오기
    config = from_file("/Users/leejinwoo/.oci/config", "DEFAULT")

    # request의 auth 부분 생성
    auth = Signer(
        tenancy=config['tenancy'],
        user=config['user'],
        fingerprint=config['fingerprint'],
        private_key_file_location=config['key_file']
    )

    # endpoint
    endpoint = 'https://iaas.ap-chuncheon-1.oraclecloud.com/20160918/instances/'

    # body
    body = {
      	"compartmentId": config['tenancy']
    }

    # request 보내기, 해당 API는 get method를 요구합니다.
    response = requests.get(endpoint, params=body, auth=auth)
    
    instances = response.json()
    # TERMINATED 상태가 아닌 활성 인스턴스만 필터링
    active_instances = [i for i in instances if i.get('lifecycleState') != 'TERMINATED']
    print(f"현재 활성 인스턴스 개수: {len(active_instances)} (전체 목록: {len(instances)})")
    
    return len(active_instances)

def makeit():
    # configuration file 불러오기
    config = from_file("/Users/leejinwoo/.oci/config", "DEFAULT")

    # request의 auth 부분 생성
    auth = Signer(
        tenancy=config['tenancy'],
        user=config['user'],
        fingerprint=config['fingerprint'],
        private_key_file_location=config['key_file']
    )

    # endpoint
    endpoint = 'https://iaas.ap-chuncheon-1.oraclecloud.com/20160918/instances/'

    # body
    body = {"availabilityDomain":"MZoR:AP-CHUNCHEON-1-AD-1","compartmentId":config['tenancy'],"metadata":{"ssh_authorized_keys":"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCw+ghNY84xzbM9HOpfnT6OdRfYWi2qzufnYhOvw2PwR4WirSgTmABGBWHwmcEoPm0sgeHC7tnN0k+oNlR3yW976Pg7KpW/wNxe+zXkqeOr5oyKZ2UNuIfoV9BrvFKlwAcxhOHMY1E/oGiW2Kglh4b9cLCpPCSsFm5SoMx7QLxIYr2v1bUZUNpvY+VuIy5uo+K3IGEA9/f5bakXm3M9L402LcL3DNWfjd6XPedMWbpR6nPUtXy+XvR3j0ecpM4e//Y13rw3EC0sgDbZOQfcqk+T5dmy+aJMg9lPPpayq9TwlPFGv0+tHnm2SXJc3dcbP4PVc17GCW0cCe7KyGjAnToD ssh-key-2026-05-05"},"displayName":"instance-20260503-0934","sourceDetails":{"sourceType":"image","imageId":"ocid1.image.oc1.ap-chuncheon-1.aaaaaaaarsxbxzwhedbxyi5wxg2tlahgymysvhejzvktg52r7tt77qizvwra"},"shape":"VM.Standard.A1.Flex","shapeConfig":{"ocpus":1,"memoryInGBs":6},"createVnicDetails":{"assignPublicIp":True,"subnetId":"ocid1.subnet.oc1.ap-chuncheon-1.aaaaaaaau6aqetn4ctpgrlznqwafyenim4wgoy6dtij6z6j3uyszyabehk4q","assignPrivateDnsRecord":True,"assignIpv6Ip":False},"isPvEncryptionInTransitEnabled":True,"instanceOptions":{"areLegacyImdsEndpointsDisabled":True},"definedTags":{},"freeformTags":{},"availabilityConfig":{"recoveryAction":"RESTORE_INSTANCE"},"agentConfig":{"pluginsConfig":[{"name":"WebLogic Management Service","desiredState":"DISABLED"},{"name":"Vulnerability Scanning","desiredState":"DISABLED"},{"name":"Oracle Java Management Service","desiredState":"DISABLED"},{"name":"OS Management Hub Agent","desiredState":"DISABLED"},{"name":"Management Agent","desiredState":"DISABLED"},{"name":"Fleet Application Management Service","desiredState":"DISABLED"},{"name":"Custom Logs Monitoring","desiredState":"ENABLED"},{"name":"Compute RDMA GPU Monitoring","desiredState":"DISABLED"},{"name":"Compute Instance Run Command","desiredState":"ENABLED"},{"name":"Compute Instance Monitoring","desiredState":"ENABLED"},{"name":"Compute HPC RDMA Auto-Configuration","desiredState":"DISABLED"},{"name":"Compute HPC RDMA Authentication","desiredState":"DISABLED"},{"name":"Cloud Guard Workload Protection","desiredState":"ENABLED"},{"name":"Block Volume Management","desiredState":"DISABLED"},{"name":"Bastion","desiredState":"DISABLED"}],"isMonitoringDisabled":False,"isManagementDisabled":False}}

    # request 보내기, 해당 API는 post method를 요구합니다.
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 인스턴스 생성을 요청합니다...")
    response = requests.post(endpoint, json=body, auth=auth)
    return response

if __name__=='__main__':
    print(f"인스턴스 생성 자동 시도를 시작합니다. (목표 개수: {TARGET_INSTANCE_COUNT})")
    
    while True:
        try:
            print(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 상태 확인 중...")
            current_count = listit()
            
            if current_count < TARGET_INSTANCE_COUNT:
                response = makeit()
                status = response.status_code
                
                if 200 <= status < 300:
                    print(f"🎉 성공! 상태 코드: {status}")
                    print(response.json())
                    break
                elif status == 429:
                    print("⚠️ 429 Too Many Requests 발생. 5분간 대기합니다...")
                    time.sleep(300)
                    continue
                else:
                    print(f"실패 (상태 코드: {status})")
                    try:
                        print(response.json())
                    except:
                        print(response.text)
            else:
                print(f"목표한 인스턴스 개수({TARGET_INSTANCE_COUNT}개)에 도달하여 종료합니다.")
                break
                
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
        
        print("1분 후 재시도합니다...")
        time.sleep(90)

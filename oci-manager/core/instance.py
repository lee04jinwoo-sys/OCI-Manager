
import oci
from oci.retry import DEFAULT_RETRY_STRATEGY
from config import OCI_CONFIG_PATH, OCI_CONFIG_PROFILE

class InstanceManager:
    def __init__(self):
        self.config = oci.config.from_file(OCI_CONFIG_PATH, OCI_CONFIG_PROFILE)
        self.compute_client = oci.core.ComputeClient(self.config, retry_strategy=DEFAULT_RETRY_STRATEGY)
        self.vnic_client = oci.core.VirtualNetworkClient(self.config, retry_strategy=DEFAULT_RETRY_STRATEGY)
        self.compartment_id = self.config['tenancy']

    def list_instances(self):
        """인스턴스 목록과 기본 정보를 조회합니다."""
        instances = self.compute_client.list_instances(compartment_id=self.compartment_id).data
        result = []
        for inst in instances:
            if inst.lifecycle_state == 'TERMINATED':
                continue
            
            # VNIC 정보를 통해 공인 IP 추출
            public_ip = "N/A"
            vnic_attachments = self.compute_client.list_vnic_attachments(
                compartment_id=self.compartment_id, 
                instance_id=inst.id
            ).data
            
            if vnic_attachments:
                vnic = self.vnic_client.get_vnic(vnic_attachments[0].vnic_id).data
                public_ip = vnic.public_ip or "N/A"
            
            result.append({
                "id": inst.id,
                "name": inst.display_name,
                "state": inst.lifecycle_state,
                "ip": public_ip,
                "shape": inst.shape,
                "cpus": inst.shape_config.ocpus,
                "ram": inst.shape_config.memory_in_gbs,
                "created": inst.time_created.strftime("%Y-%m-%d %H:%M")
            })
        return result

    def control_instance(self, instance_id, action):
        """인스턴스 전원 제어 (START, STOP, SOFTRESET)"""
        return self.compute_client.instance_action(instance_id, action)

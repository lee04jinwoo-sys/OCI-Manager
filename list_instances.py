
import oci
import os

def get_instances():
    config = oci.config.from_file()
    compute_client = oci.core.ComputeClient(config)
    
    # Get all instances in the compartment
    compartment_id = config['tenancy']
    instances = compute_client.list_instances(compartment_id=compartment_id).data
    
    # For each instance, get its public IP
    vnic_client = oci.core.VirtualNetworkClient(config)
    
    print(f"{'Name':<30} {'State':<15} {'Public IP':<15} {'Created':<25}")
    print("-" * 85)
    
    for instance in instances:
        if instance.lifecycle_state == 'TERMINATED':
            continue
            
        public_ip = "N/A"
        # Get VNIC attachments to find public IP
        vnics = compute_client.list_vnic_attachments(compartment_id=compartment_id, instance_id=instance.id).data
        if vnics:
            vnic = vnic_client.get_vnic(vnics[0].vnic_id).data
            public_ip = vnic.public_ip or "N/A"
            
        print(f"{instance.display_name:<30} {instance.lifecycle_state:<15} {public_ip:<15} {instance.time_created}")

if __name__ == "__main__":
    try:
        get_instances()
    except Exception as e:
        print(f"Error: {e}")

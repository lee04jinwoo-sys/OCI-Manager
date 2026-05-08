
import oci
from datetime import datetime, timedelta
from oci.retry import DEFAULT_RETRY_STRATEGY
from config import OCI_CONFIG_PATH, OCI_CONFIG_PROFILE

class BillingManager:
    def __init__(self):
        self.config = oci.config.from_file(OCI_CONFIG_PATH, OCI_CONFIG_PROFILE)
        self.usage_client = oci.usage_api.UsageapiClient(self.config, retry_strategy=DEFAULT_RETRY_STRATEGY)
        self.tenancy_id = self.config['tenancy']

    def get_monthly_cost(self):
        """이번 달 현재까지의 대략적인 예상 비용을 가져옵니다."""
        try:
            now = datetime.utcnow()
            first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            request = oci.usage_api.models.RequestSummarizedUsagesDetails(
                tenant_id=self.tenancy_id,
                time_usage_started=first_day,
                time_usage_ended=now + timedelta(days=1),
                granularity='MONTHLY',
                query_type='COST',
                group_by=['currency']
            )
            
            response = self.usage_client.request_summarized_usages(request)
            items = response.data.items
            
            if not items:
                return "₩0 (No data yet)"
            
            total_cost = sum(item.computed_amount for item in items if item.computed_amount)
            currency = items[0].currency if items else "USD"
            
            return f"{currency} {total_cost:.2f}"
        except oci.exceptions.ServiceError as e:
            if e.status == 404:
                return "₩0 (New Account)"
            return f"Auth Error (Check Policy)"
        except Exception as e:
            return f"Error: {type(e).__name__}"

    def get_resource_usage(self, instances):
        """Always Free 한도(4 OCPU, 24GB RAM) 대비 현재 사용량을 계산합니다."""
        total_ocpus = 0
        total_ram = 0
        
        for inst in instances:
            if inst['state'] == 'RUNNING':
                total_ocpus += inst['cpus']
                total_ram += inst['ram']
                
        return {
            "ocpus": total_ocpus,
            "ram": total_ram,
            "ocpu_pct": (total_ocpus / 4.0) * 100 if total_ocpus <= 4 else 100,
            "ram_pct": (total_ram / 24.0) * 100 if total_ram <= 24 else 100
        }

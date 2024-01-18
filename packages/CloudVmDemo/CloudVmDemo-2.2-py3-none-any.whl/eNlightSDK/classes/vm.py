from typing import Any, Optional
import requests
import json
from classes.caller import caller, get_error_message


class VM:
    def __init__(self, session: str, host: str):
        self.session = session
        self.host = host

    def get_by_id(self, vm_guid: str):
        try:
            api_endpoint = "vms"
            api_call = f"http://{self.host}:30157/{api_endpoint}/{vm_guid}"
            method = "GET"
            response = caller(self.session, api_call, method)
            return response
            
        except Exception as e:
            print(e)

    def get_list(
        self, vm_guid: Optional[str] = None, get_utilization: Optional[bool] = None, vmm_ip: Optional[str] = None, vmm_id: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None, search_text: Optional[str] = None, encryption_text: Optional[str] = None, compute_name: Optional[str] = None, vm_group: Optional[str] = None, vm_status: Optional[str] = None, from_date: Optional[str] = None, to_date: Optional[str] = None, export_type: Optional[str] = None, tools_installed: Optional[str] = None, filter_tag: Optional[str] = None, call_from: Optional[str] = None, hsgcombo: Optional[str] = None, status: Optional[str] = None, power_state: Optional[str] = None, compute_type: Optional[str] = None, is_hsg_vm: Optional[str] = None, data_from_date: Optional[str] = None, data_to_date: Optional[str] = None
    ) -> None:
        try:
            api_endpoint = "vms"
            api_call_url = f"http://{self.host}:30157/{api_endpoint}"
            method = "GET"

            params = {
                "vm_guid": vm_guid,
                "get_utilization": get_utilization,
                "vmm_ip": vmm_ip,
                "vmm_id": vmm_id,
                "limit": limit,
                "offset": offset,
                "search_text": search_text,
                "encryption_text": encryption_text,
                "compute_name": compute_name,
                "vm_group": vm_group,
                "vm_status": vm_status,
                "from_date": from_date,
                "to_date": to_date,
                "export_type": export_type,
                "tools_installed": tools_installed,
                "filter_tag": filter_tag,
                "call_from": call_from,
                "hsgcombo": hsgcombo,
                "status": status,
                "power_state": power_state,
                "compute_type": compute_type,
                "is_hsg_vm": is_hsg_vm,
                "data_from_date": data_from_date,
                "data_to_date": data_to_date
            }

            response = caller(self.session, api_call_url, method, params)
            return response

        except Exception as e:
            print(e)  

    def create_vm(self, data):
        try:
            api_endpoint = "vms"
            api_call = f"http://{self.host}:30157/{api_endpoint}"
            method = "POST"
            response = caller(self.session, api_call, method, data=data)
            return response
            
        except Exception as e:
            print(e)

    def update_vm(self, vm_guid: str, data):
        try:
            api_endpoint = "vms"
            api_call = f"http://{self.host}:30157/{api_endpoint}/{vm_guid}"
            method = "PUT"
            response = caller(self.session, api_call, method, data=data)
            return response
            
        except Exception as e:
            print(e)

    def delete(self, vm_guid: str, delete_mode: str, schedule: Optional[str] = None, request_id: Optional[str] = None, request_ip: Optional[str] = 'UNKNOWN', call_from: Optional[str] = None, service_type: Optional[str] = None) -> None:
        try:
            api_endpoint = "vms"
            api_call_url = f"http://{self.host}:30157/{api_endpoint}/{vm_guid}"
            method = "DELETE"

            params = {
                "delete_mode": delete_mode,
                "schedule": schedule,
                "REQUESTID": request_id,
                "request_ip": request_ip,
                "call_from": call_from,
                "service_type": service_type
                # Add other parameters as needed
            }

            response = caller(self.session, api_call_url, method, params)
            return response

        except Exception as e:
            raise RuntimeError(f"Error in VM.delete: {e}")

    def vm_actions(self, vm_guid: str, schedule: str, action: str, call_from: Optional[str] = None, service_type: Optional[str] = None, request_id: Optional[str] = None) -> None:
        try:
            api_endpoint = f"vms/actions/{vm_guid}"
            api_call_url = f"http://{self.host}:30157/{api_endpoint}"
            method = "PUT"

            headers = {
                'Authorization': f'Bearer {self.session}',
                'Content-Type': 'application/x-www-form-urlencoded',  # form data content-type
                'Accept': 'application/json',
                'cache-control': 'no-cache'
            }

            data = {
                "schedule": schedule,
                "action": action,
                "call_from": call_from,
                "service_type": service_type,
                "REQUESTID": request_id
                # Add other parameters as needed
            }

            response = requests.put(api_call_url, headers=headers, data=data, verify=False)

            if response.ok:
                return response.text
            else:
                print(response.text)
                error_msg = get_error_message(response)
                return error_msg

        except Exception as e:
            raise RuntimeError(f"Error in VM.vm_actions: {e}")




    # def vm_actions(self, vm_guid: Optional[str] = None, schedule: Optional[str] = None, action: Optional[str] =None, call_from: Optional[str] = None, service_type: Optional[str] = None, request_id: Optional[str] = None) -> None:
    #     try:
    #         api_endpoint = f"vms/actions/{vm_guid}"
    #         api_call_url = f"http://{self.host}:30157/{api_endpoint}"
    #         method = "PUT"

    #         data = {
    #             "schedule": schedule,
    #             "action": action,
    #             "call_from": call_from,
    #             "service_type": service_type,
    #             "REQUESTID": request_id
    #             # Add other parameters as needed
    #         }

    #         response = caller(self.session, api_call_url, method, data=data)
    #         return response

    #     except Exception as e:
    #         raise RuntimeError(f"Error in VM.vm_actions: {e}")






# def get_error_message(api_response):
#     if api_response.text:
#         error_data = json.loads(api_response.text)
#         if 'message' in error_data:
#             return error_data['message']
#         elif 'message_list' in error_data:
#             return error_data['message_list'][0]['message']
#     return "Error: Something went wrong!"

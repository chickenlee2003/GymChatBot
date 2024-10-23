from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionFetchFitnessPackagesByType(Action):

    def name(self) -> Text:
        return "action_fetch_fitness_packages_by_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Lấy type_id từ slot
        type_id = tracker.get_slot('type_id')

        if not type_id:
            dispatcher.utter_message(text="Bạn chưa cung cấp mã loại dịch vụ. Vui lòng cung cấp ID hợp lệ")
            return []

        try:
            # Gửi yêu cầu API để lấy gói fitness theo type_id
            response = requests.get(f"http://localhost:3001/fitness-packages/by-type/{type_id}", verify=False)

            if response.status_code == 200:
                fitness_packages = response.json()

                if fitness_packages:
                    message = f"Các gói dịch vụ của loại có mã {type_id} là:"
                    for package in fitness_packages:
                        package_info = package['servicePackage']
                        message += f"\n - Gói: {package_info['name']} (ID: {package_info['id']}), Mô tả: {package_info['description']}"
                else:
                    message = f"Không có gói dịch vụ nào cho loại có mã {type_id}."
                
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text="Không thể lấy thông tin gói dịch vụ.")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text="Có lỗi xảy ra khi kết nối với máy chủ.")
            print(f"Lỗi yêu cầu API: {e}")

        return []



class ActionFetchServiceTypes(Action):

    def name(self) -> Text:
        return "action_fetch_service_types"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            # Gửi yêu cầu để lấy loại dịch vụ
            response = requests.get("http://localhost:3001/service-package-types")

            # Kiểm tra phản hồi thành công
            if response.status_code == 200:
                # Phân tích dữ liệu JSON
                service_types = response.json()

                # In ra dữ liệu lấy được để kiểm tra
                print("Dữ liệu lấy từ API:", service_types)

                # Chuẩn bị tin nhắn để hiển thị các loại dịch vụ và gói dịch vụ
                if service_types:
                    message = "Các loại dịch vụ gói tập hiện có:"
                    for service_type in service_types:
                        # print("Xử lý loại dịch vụ:", service_type['type'])  # In loại dịch vụ
                        message += f"\n --- (mã: {service_type['id']}) {service_type['type']} "
                        # Hiển thị từng gói dịch vụ thuộc loại
                        # for package in service_type.get('servicePackages', []):
                        #     print("Xử lý gói dịch vụ:", package['name'])  # In gói dịch vụ
                        #     message += f"  - Gói: {package['name']} (ID: {package['id']}), Mô tả: {package['description']}"
                else:
                    message = "Không có loại dịch vụ nào."

                # In nội dung tin nhắn trước khi gửi
                print("Tin nhắn gửi đi:", message)

                # Gửi phản hồi cho người dùng
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text="Đã có lỗi xảy ra khi lấy thông tin dịch vụ.")

        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text="Có lỗi xảy ra khi kết nối với máy chủ, vui lòng thử lại sau.")
            print(f"Yêu cầu thất bại: {e}")

        return []


class ActionGetBranches(Action):

    def name(self) -> Text:
        return "action_ask_about_branches"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try: 
            response = requests.get("http://localhost:3001/branches/count")

            if response.status_code == 200:
                data = response.json()
                num_branches = data.get('num_branches', 0) if data else 0
                dispatcher.utter_message(text=f"Số lượng chi nhánh hiện tại: {num_branches}")
            else:
                dispatcher.utter_message(text="Could not retrieve branches information.")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text="Có lỗi xảy ra khi kết nối với máy chủ, vui lòng thử lại sau.")
            print(f"Yêu cầu thất bại: {e}")

        return []
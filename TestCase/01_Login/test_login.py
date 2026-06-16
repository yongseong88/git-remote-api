# import pytest
#
# from Common.common_data import Commondata
# from Utilities.configreaderutil import Filereadutil
# from ApiClient.Base_API import User_api, ApiClient
# import logging
#
# logger = logging.getLogger(__name__)
#
#
# @pytest.mark.usefixtures("base_url")
# class TestLogin():
#
#     # @pytest.mark.regression
#     def test_login_success_v2(self, base_url):
#
#         try:
#             api_client = ApiClient(base_url)
#             common_data = Commondata(base_url)
#             user_account = common_data.account_config()
#
#             valid_id = user_account['valid_id']
#             valid_pwd = user_account['valid_pwd']
#
#             login_status = api_client.user.login_api_v2(valid_id, valid_pwd)
#             assert login_status.status_code == 200, print(f" 로그인 실패: {login_status.status_code}")
#             logger.info(f"✅ 로그인 성공 - status: {login_status.status_code}")
#
#         except AssertionError as e:
#             print(f"AssertionError: {e}")
#
#     # @pytest.mark.regression
#     def test_login_id_failure_v2(self, base_url):
#
#         try:
#             user_api = User_api(base_url)
#             common_data = Commondata(base_url)
#             user_account = common_data.account_config()
#
#             invalid_id = user_account['invalid_id']
#             valid_pwd = user_account['valid_pwd']
#
#             login_status = user_api.login_api_v2(invalid_id, valid_pwd)
#
#             if login_status.status_code != 200:
#                 longin_json = login_status.json()
#                 msg = longin_json.get('errors', [{}])[0].get('msg', None)
#
#             assert login_status.status_code != 200, print(f" 로그인 실패: {login_status.status_code}")
#             logger.info(f"✅ 로그인 실패 - status: {login_status.status_code}. {msg}")
#
#         except AssertionError as e:
#             print(f"AssertionError: {e}")
#
#     # @pytest.mark.regression
#     def test_login_pwd_failure_v2(self, base_url):
#
#         try:
#             user_api = User_api(base_url)
#             common_data = Commondata(base_url)
#             user_account = common_data.account_config()
#
#             valid_id = user_account['valid_id']
#             invalid_pwd = user_account['invalid_pwd']
#
#             login_status = user_api.login_api_v2(valid_id, invalid_pwd)
#             if login_status.status_code != 200:
#                 longin_json = login_status.json()
#                 msg = longin_json.get('errors', [{}])[0].get('msg', None)
#
#             assert login_status.status_code != 200, print(f" 로그인 실패: {login_status.status_code}")
#             logger.info(f"✅ 로그인 실패 - status: {login_status.status_code}. {msg}")
#
#         except AssertionError as e:
#             print(f"AssertionError: {e}")
#
#
#     # @pytest.mark.regression
#     def test_login_success_v1(self, base_url):
#         try:
#             user_api = User_api(base_url)
#             common_data = Commondata(base_url)
#             user_account = common_data.account_config()
#
#             valid_id = user_account['valid_id']
#             valid_pwd = user_account['valid_pwd']
#
#             login_status = user_api.login_api_v1(valid_id, valid_pwd)
#             assert login_status.status_code == 200, print(f" 로그인 실패: {login_status.status_code}")
#             logger.info(f"✅ 로그인 성공 - status: {login_status.status_code}")
#
#         except AssertionError as e:
#             print(f"AssertionError: {e}")
#
#
#     # @pytest.mark.regression
#     def test_login_id_failure_v1(self, base_url):
#         try:
#             user_api = User_api(base_url)
#             common_data = Commondata(base_url)
#             user_account = common_data.account_config()
#
#             invalid_id = user_account['invalid_id']
#             valid_pwd = user_account['valid_pwd']
#
#             login_status = user_api.login_api_v1(invalid_id, valid_pwd)
#
#             if login_status.status_code != 200:
#                 longin_json = login_status.json()
#                 msg = longin_json.get('errors', [{}])[0].get('msg', None)
#
#             assert login_status.status_code != 200, print(f" 로그인 실패: {login_status.status_code}")
#             logger.info(f"✅ 로그인 실패 - status: {login_status.status_code}. {msg}")
#
#         except AssertionError as e:
#             print(f"AssertionError: {e}")
#
#
#     # @pytest.mark.regression
#     def test_login_pwd_failure_v1(self, base_url):
#         try:
#             user_api = User_api(base_url)
#             common_data = Commondata(base_url)
#             user_account = common_data.account_config()
#
#             valid_id = user_account['valid_id']
#             invalid_pwd = user_account['invalid_pwd']
#
#             login_status = user_api.login_api_v1(valid_id, invalid_pwd)
#             if login_status.status_code != 200:
#                 longin_json = login_status.json()
#                 msg = longin_json.get('errors', [{}])[0].get('msg', None)
#
#             assert login_status.status_code != 200, print(f" 로그인 실패: {login_status.status_code}")
#             logger.info(f"✅ 로그인 실패 - status: {login_status.status_code}. {msg}")
#
#         except AssertionError as e:
#             print(f"AssertionError: {e}")

# # from ApiClient.Base_API import ApiClient
# from Common.common_data import Commondata
# from Utilities.configreaderutil import Filereadutil
#
# class CommonAction():
#     def __init__(self, base_url):
#         self.base_url = base_url
#         self.common_data = Commondata(base_url)
#         # self.api_client = ApiClient(base_url)
#         self.File_read_util = Filereadutil()
#
#
#         if "dev" in base_url:
#             self.env = "dev"
#         elif "beta" in base_url:
#             self.env = "beta"
#         else:
#             self.env = "prod"
#
#     def set_braille(self):
#         try:
#             test_result = []
#
#             brl_lst = self.common_data.braille_lists()
#
#             for idx, bd in enumerate(brl_lst):
#                 try:
#
#                     if not bd:
#                         continue
#
#                     braille = bd.strip()
#                     braille_info = self.common_data.parse_braille_info(braille)
#
#                     if not braille_info:
#                         print(f"⚠️ braille_info 없음 - 스킵: {braille}")
#                         continue
#
#                     lang_data = braille_info.get("language", "")
#                     grade_data = braille_info.get("language_grade", "")
#
#                     braille_change = self.api_client.user.braille_language_change_api(lang_data, grade_data)
#                     print(f"braille_change.status_code: {braille_change.status_code}")
#
#                     if braille_change.status_code <= 200:
#                         test_result.append(braille_change.status_code)
#
#                     else:
#                         pass
#
#                 except Exception:
#                     print(f"⚠️brl_lst Exception 발생 - 스킵: {braille}")
#                     continue
#
#             return test_result
#
#         except Exception as e:
#             print(f"root_file_open error: {e}")
#             return None
#
#     def set_spacing(self):
#         try:
#             test_result = []
#
#             brl_lst = self.common_data.braille_lists()
#
#             for idx, bd in enumerate(brl_lst):
#                 try:
#
#                     if not bd:
#                         continue
#
#                     braille = bd.strip()
#                     braille_info = self.common_data.parse_braille_info(braille)
#
#                     if not braille_info:
#                         print(f"⚠️ braille_info 없음 - 스킵: {braille}")
#                         continue
#
#                     lang_data = braille_info.get("language", "")
#                     grade_data = braille_info.get("language_grade", "")
#
#                     braille_change = self.api_client.user.braille_language_change_api(lang_data, grade_data)
#                     print(f"braille_change.status_code: {braille_change.status_code}")
#
#                     for cnt in range(4):
#                         letter_spacing_change = self.api_client.user.braille_letter_change_api(cnt)
#
#                     if letter_spacing_change.status_code <= 200:
#                         test_result.append(letter_spacing_change.status_code)
#
#                     else:
#                         pass
#
#                 except Exception:
#                     print(f"⚠️brl_lst Exception 발생 - 스킵: {braille}")
#                     continue
#
#             return test_result
#
#         except Exception as e:
#             print(f"root_file_open error: {e}")
#             return None
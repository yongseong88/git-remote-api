# # from ApiClient.Base_API import ApiClient
# from Utilities.configreaderutil import Filereadutil
#
#
# class Commondata():
#     def __init__(self, base_url):
#         self.base_url = base_url
#         self.File_read_util = Filereadutil()
#         self.api_client = ApiClient(base_url)
#
#         if "dev" in base_url:
#             self.env = "dev"
#         elif "beta" in base_url:
#             self.env = "beta"
#         else:
#             self.env = "prod"
#
#     def account_config(self):
#
#         try:
#             # env = "dev" if "dev" in self.base_url else "prod"
#
#             return {
#                 "valid_id": self.File_read_util.readConfig("Account", f"{self.env}_id"),
#                 "valid_pwd": self.File_read_util.readConfig("Account", f"{self.env}_password"),
#                 "invalid_id": self.File_read_util.readConfig("Account", "invalid_id"),
#                 "invalid_pwd": self.File_read_util.readConfig("Account", "invalid_pwd")
#
#             }
#
#         except AssertionError as e:
#             print(f"AssertionError: {e}")
#
#
#     def parse_braille_info(self, braille_element):
#         try:
#
#             """점자 언어 요소에서 언어와 grade 정보를 추출"""
#             if "-" in braille_element:
#                 braille_text = braille_element[0:(braille_element.find("-") - 1)].strip()
#                 braille_grade = braille_element[(braille_element.find("-")) + 1:].strip()
#
#             else:
#                 braille_text = braille_element.strip()
#                 braille_grade = "Grade".strip()
#
#             braille_json_path = self.File_read_util.read_filepath("Config/braille_info", "braille_data.json")
#             json_read = self.File_read_util.read_file(braille_json_path)
#             braille_items = json_read.get('braille_info', [])
#
#             for item in braille_items:
#                 if braille_text in item and "language_option" in item[braille_text]:
#                     brl_lang = item[braille_text]['language']
#
#                     # ✅ KeyError 방지
#                     brl_grade = item[braille_text]['language_option'].get(braille_grade.strip())
#
#                     if not brl_grade:
#                         print(f"⚠️ grade 매핑 실패: {braille_grade}")
#                         continue
#
#                     return {
#                         'text': braille_text,
#                         'grade': braille_grade,
#                         'language': brl_lang,
#                         'language_grade': brl_grade
#                     }
#
#             print(f"[경고] 점자 매핑 실패: {braille_text} - {braille_grade}")
#             return None
#
#         except Exception as e:
#             print(f"parse_braille_info Exception: {e}")
#
#
#     def braille_lists(self):
#         try:
#             braille_txt_path = self.File_read_util.read_filepath("Config/braille_info", "target_braille_info.txt")
#             braille_txt_data = self.File_read_util.read_file(braille_txt_path)
#             return braille_txt_data
#         except Exception as e:
#             print(f"⚠braille Exception 발생 - 스킵: {e}")
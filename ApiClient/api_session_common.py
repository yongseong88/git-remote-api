import requests

# from ApiClient.Base_API import User_api, Drive_api, Braille_api


# class Apisession:
#     def __init__(self, base_url):
#         # ✅ session 하나만 생성
#         self.session = requests.Session()
#
#         # ✅ 모든 api 인스턴스 생성
#         self.user = User_api(base_url)
#         self.drive = Drive_api(base_url)
#         self.braille = Braille_api(base_url)
#
#         # ✅ 모든 api session 공유
#         for api in [self.user, self.drive, self.braille]:
#             api.session = self.session
#
#         # ✅ braille_api에 user_api 주입
#         self.braille.set_user_api(self.user)
#
#     def login(self):
#         id = self.user.read_util.readConfig("Account", f"{self.user.env}_id")
#         pwd = self.user.read_util.readConfig("Account", f"{self.user.env}_password")
#         login_response = self.user.login_and_verify(id, pwd)
#         return self.user.token_check(login_response)
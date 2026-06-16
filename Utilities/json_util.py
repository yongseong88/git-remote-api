import json
import math
import os
from datetime import datetime

import pytest

from Utilities.configreaderutil import Filereadutil
import requests


class BaseApi:
    def __init__(self, base_url):
        self.base_url = base_url
        if "dev" in base_url:
            self.env = "dev"
        elif "beta" in base_url:
            self.env = "beta"
        else:
            self.env = "prod"
        # self.env = "dev" if "dev" in base_url else "prod"
        self.read_util = Filereadutil()
        self.config = self._load_config()
        self.session = requests.Session()

    def _load_config(self):

        return {
            "SITE_NO": self.read_util.readConfig("USER_INFO", f"{self.env}_SITE_NO"),
            "USER_NO": self.read_util.readConfig("USER_INFO", f"{self.env}_USER_NO"),
            "COMP_NO": self.read_util.readConfig("USER_INFO", "COMP_NO")
        }

    def _build_url(self):
        return f"{self.base_url}"


    def request(self, method, url, base_url, **kwargs):
        """API 호출 + 토큰 만료 자동 체크 래퍼"""
        try:
            # 1. API 호출
            response = getattr(self.session, method)(url=url, **kwargs) #  getattr로 함수 꺼내오고 (url=url, **kwargs)는 함수의 파라미터
            # → self.session.post(url=url, **kwargs) 로 쓰인 다고 생각 하면 됨

            # 2. 토큰 만료 체크
            if response.status_code in [401, 412]:
                print(f"⚠️ 토큰 만료 감지 - status: {response.status_code} → 갱신 시도")

                if self.token_refresh(base_url):
                    # 3. 갱신 성공 → 재시도
                    print("✅ 토큰 갱신 성공 → 재시도")
                    response = getattr(self.session, method)(url=url, **kwargs)

                else:
                    # 4. 갱신 실패 → 재로그인 후 재시도
                    print("❌ 갱신 실패 → 재로그인 시도")
                    self.login_and_verify(base_url)
                    response = getattr(self.session, method)(url=url, **kwargs)

            return response

        except Exception as e:
            print(f"request Exception: {e}")
            return None

    def token_refresh(self, base_url):
        """토큰 갱신"""
        try:
            apps_url = [x for x in base_url.split("/") if x]
            domain = apps_url[1] if len(apps_url) >= 2 else ""
            refresh_url = f"https://account.{domain}/user-app/v2/auth/token/refresh"

            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'ko,hr;q=0.9,ja;q=0.8,pl;q=0.7,ru;q=0.6,sv;q=0.5,nl;q=0.4,sr;q=0.3,de;q=0.2,sh;q=0.1',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Origin': f'https://{domain}',
                'Referer': f'https://{domain}/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"'
            }

            data = {
                "SITE_NO": self.config['SITE_NO'],
                "COMP_NO": self.config['COMP_NO']
            }

            response = self.session.post(url=refresh_url, headers=headers, json=data, timeout=30)

            if response.status_code == 200:
                new_token = self.session.cookies.get('ACCESS_TOKEN')
                if new_token:
                    print("✅ 토큰 갱신 성공")
                    return True
                else:
                    print("❌ 토큰 갱신 실패 - 새 토큰 없음")
                    return False
            else:
                print(f"❌ 토큰 갱신 실패 - status: {response.status_code}")
                return False

        except Exception as e:
            print(f"token_refresh Exception: {e}")
            return False


    def login_and_verify(self):
        """로그인 + 토큰 체크 한세트 - 모든 하위 클래스 공통 사용"""
        try:
            id = self.read_util.readConfig("Account", f"{self.env}_id")
            pwd = self.read_util.readConfig("Account", f"{self.env}_password")
            print(f"login_and_verify base_url: {self.base_url}")

            apps_url = [x for x in self.base_url.split("/") if x]
            domain = apps_url[1] if len(apps_url) >= 2 else ""
            login_url = f"https://account.{domain}/user-app/v2/auth/login"

            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ja;q=0.7',
                'Content-Type': 'application/json',
                'Origin': f'https://account.{domain}',
                'Referer': login_url,
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
            }

            data = {
                'USER_ID': id,
                'PASSWD': pwd,
                "SITE_NO": self.config['SITE_NO'],
                "COMP_NO": self.config['COMP_NO']
            }

            # 1. 로그인 요청
            login_response = self.session.post(url=login_url, headers=headers, json=data, timeout=10)

            # 2. status code 체크
            # if login_response.status_code != 200:
            #     print(f"❌ 로그인 실패 - status: {login_response.status_code}")
            #     return False
            #
            # # 3. 토큰 체크
            # if not self.session.cookies.get('ACCESS_TOKEN'):
            #     print("❌ 토큰 없음")
            #     return False
            #
            # print("✅ 로그인 + 토큰 확인 완료")
            return login_response

        except Exception as e:
            print(f"login_and_verify Exception: {e}")
            return False





class User_api(BaseApi):
    def login_check_v2_api(self):
        # 로그인 체크 V2

        try:
            login_info = self.login_and_verify()
            # apps_url = [x for x in self.base_url.split("/") if x]
            # domain = apps_url[1] if len(apps_url) >= 2 else ""
            # login_url = f"https://account.{domain}/user-app/v2/auth/login"
            #
            # headers = {
            #     'Accept': 'application/json, text/plain, */*',
            #     'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ja;q=0.7',
            #     'Content-Type': 'applssication/json',
            #     'Origin': f'https://account.{domain}.com',
            #     'Referer': login_url,
            #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
            # }
            #
            # data = {
            #     'USER_ID': id,
            #     'PASSWD': pwd,
            #     "SITE_NO": self.config['SITE_NO'],
            #     "COMP_NO": self.config['COMP_NO']
            # }
            #
            # login_info = self.session.post(url=login_url, headers=headers, json=data, timeout=10)

            # 쿠키 확인
            # res_cookies = login_info.cookies.get_dict()
            #
            # if res_cookies:
            #     print("\n[서버 발급 쿠키 목록]")
            #     for c_name, c_value in res_cookies.items():
            #         print(f"쿠키명: {c_name} | 값: {c_value[:10]}...")
            #
            #     if 'ACCESS_TOKEN' in res_cookies:
            #         print("✅ ACCESS_TOKEN 획득 완료 - 이후 요청에 자동 포함됩니다")
            #
            #     else:
            #         print("⚠️ ACCESS_TOKEN 없음 - 쿠키 목록 확인 필요")
            #
            # else:
            #     print("\n❌ 응답에 설정된 쿠키가 없습니다.")

            return login_info


        except Exception as e:
            print(f"login_and_verify Exception: {e}")
            return False

    def authenticated_check(self):
        """쿠키에 토큰 있는지 체크"""
        return bool(self.session.cookies.get('ACCESS_TOKEN'))


    def login_check_api(self, id, pwd):
        # 로그인 체크 V1

        if "dev" in self.env:
            login_url = f"https://dev-account.dotincorp.com/user-app/v1/sites/{self.config['SITE_NO']}-{self.config['COMP_NO']}/login"
        else:
            login_url = f"https://account.dotincorp.com/user-app/v1/sites/{self.config['SITE_NO']}-{self.config['COMP_NO']}/login"

        data = {
            'USER_ID': id,
            'PASSWD': pwd
        }


        return self.session.post(url=login_url, data=data)


    def user_status_api(self, base_url):
        user_url = f"{base_url}/user-app/v1/sites/{self.config['SITE_NO']}-{self.config['COMP_NO']}/users/{self.config['USER_NO']}/language"

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ko,hr;q=0.9,ja;q=0.8,pl;q=0.7,ru;q=0.6,sv;q=0.5,nl;q=0.4,sr;q=0.3,de;q=0.2,sh;q=0.1',
            'priority': 'u=1, i',
            'referer': f'{base_url}',
            'sec-ch-ua': '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36'
        }

        param_info = {
            "USER_NO": self.config['USER_NO'],
            "SITE_NO": self.config['SITE_NO'],
            "COMP_NO": self.config['COMP_NO'],
            "LANGUAGE_TYPE": "1"
        }

        return self.request('get', user_url, base_url, headers=headers, params=param_info)


    def menus_api(self, base_url):

        menus_url = f"{base_url}/site-app/v1/sites/{self.config['SITE_NO']}-{self.config['COMP_NO']}/users/{self.config['USER_NO']}/menus"

        return self.request('get', menus_url, base_url)



    def braille_language_change_api(self, base_url):

        try:
            user_status = self.user_status_api(base_url)
            user_info = user_status.json()

            change_data = {
                "USER_NO": self.config['USER_NO'],
                "SITE_NO": self.config['SITE_NO'],
                "COMP_NO": self.config['COMP_NO'],
                "ENGINE": user_info.get('ENGINE', ""),
                "LANGUAGE_TYPE": "1",
                "LANGUAGE": user_info.get('LANGUAGE', ""),
                "LANGUAGE_OPTION": user_info.get('LANGUAGE_OPTION', ""),
                "PIN": user_info.get('PIN', 0)
            }

            brl_language_url = f"{base_url}/user-app/v1/sites/{self.config['SITE_NO']}-{self.config['COMP_NO']}/users/{self.config['USER_NO']}/language"
            headers = {"Content-Type": "application/json"}

            # ✅ request 래퍼로 변경
            return self.request('put', brl_language_url, base_url, json=change_data, headers=headers)

        except Exception as e:
            print(f"❌ API 요청 중 예외 발생: {e}")
            return None


class Drive_api(BaseApi):

    def filebrowser_list_api(self, base_url, page_no, group_no, value_type=None):

        try:
            file_list_url = f"{base_url}/drive-app/v1/dtms/groups"

            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'ko,ja;q=0.9,pl;q=0.8,ru;q=0.7,sv;q=0.6,nl;q=0.5,sr;q=0.4,de;q=0.3,sh;q=0.2,es;q=0.1',
                'Connection': 'keep-alive',
                'Referer': f'https://{"dev-" if "dev" in self.env else ""}dot.apps-dotincorp.com/cloud',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"'
            }

            param_info = {
                "PAGE_NO": page_no,
                # "PAGE_SIZE": 9,
                "PARENT_GROUP_NO": group_no,
                "COMP_NO": self.config['COMP_NO'],
                "DRIVER_KIND": "P",
                "USER_NO": self.config['USER_NO']
            }

            # type 없을 경우 (캔버스 내 filebrowser)
            if not value_type:
                param_info["PAGE_SIZE"] = 9

            else:
                param_info["PAGE_SIZE"] = 18
                param_info["APP_TYPE"] = "A"

            # ✅ request 래퍼로 변경
            response = self.request('get', file_list_url, base_url, params=param_info, headers=headers)

            if response and response.status_code == 200:
                return response

            else:
                print(f"❌ 파일 목록 조회 실패 - status: {response.status_code if response else 'None'}")
                return None

        except Exception as e:
            print(f"filebrowser_list_api Exception 오류: {e}")

    def file_open_api(self, base_url, filekey, cell_kind):
        try:
            file_open_url = f"{base_url}/drive-app/v1/dtm/images/{filekey}/device/{cell_kind}/to-dtms"

            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ja;q=0.7',
                'Connection': 'keep-alive',
                'Referer': f'{base_url}/canvas?redirect=/canvas',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"'
            }

            # ✅ request 래퍼로 변경
            response = self.request('get', file_open_url, base_url, headers=headers)

            if response and response.status_code == 200:
                # print(f"✅ 파일 열기 성공 - status: {response.status_code}")
                return response
            else:
                print(f"❌ 파일 열기 실패 - status: {response.status_code if response else 'None'}")
                return None


        except Exception as e:
            print(f"file_open_api Exception: {e}")
            return None


    def file_key_search(self, base_url, file_name, folder_in_filename=None):
        try:
            filebrowser_response = self.filebrowser_list_api(base_url, 1, 'ROOT')

            if not filebrowser_response:
                print("❌ filebrowser_list_api 실패")
                return None

            filelist_cnt = filebrowser_response.json()
            total_count = max(1, filelist_cnt.get('TOTAL_COUNT', 0))
            file_len = math.ceil((total_count / 9))
            page_nums = list(range(1, (file_len + 1)))

            for p_nums in page_nums:
                filelists_response = self.filebrowser_list_api(base_url, p_nums, 'ROOT')
                if not filelists_response:
                    continue

                file_items = filelists_response.json().get('items', [])

                for fi in file_items:
                    if fi['FILE_NAME'] == file_name and 'D' in fi['FILE_KEY']:
                        return fi['FILE_KEY'], fi['DEVICE_KIND']

                    elif fi['FILE_NAME'] == file_name and 'G' in fi['FILE_KEY']:
                        folder_response = self.filebrowser_list_api(base_url, p_nums, fi['FILE_KEY'])
                        if not folder_response:
                            continue

                        folder_lists = folder_response.json()
                        total_count = max(1, folder_lists.get('TOTAL_COUNT', 0))
                        folder_in_file_len = math.ceil((total_count / 9))
                        folder_in_page_nums = list(range(1, (folder_in_file_len + 1)))

                        for fp_nums in folder_in_page_nums:
                            folder_in_response = self.filebrowser_list_api(base_url, fp_nums, fi['FILE_KEY'])
                            if not folder_in_response:
                                continue

                            folder_in_file_items = folder_in_response.json().get('items', [])

                            for fl in folder_in_file_items:
                                if fl['FILE_NAME'] == folder_in_filename:
                                    return fi['FILE_KEY'], fl['FILE_KEY'], fl['DEVICE_KIND']

            print(f"file_key 정보가 없습니다.")
            return None

        except Exception as e:
            print(f"file_key_search error: {e}")
            return None

    def audio_upload_check(self, base_url, file_key, file_path):

        try:
            """
                DTM_NO 정보와 오디오 파일을 multipart/form-data 형식으로 전송하는 테스트입니다.
            """
            # 1. 설정 정보 (실제 환경에 맞게 수정 필요)
            audio_url = f"{base_url}/drive-app/v1/dtma/audio"

            # 전송할 텍스트 데이터 (DTM_NO)
            payload = {'DTM_NO': file_key}

            # 테스트 안정성을 위해 파일 존재 여부 체크
            if not os.path.exists(file_path):
                print(f"파일이 존재하지 않습니다: {file_path}")
                return None

            file_name = os.path.basename(file_path)
            extension = os.path.splitext(file_name)[1].lower()

            # 확장자에 따른 MIME 타입 설정
            if extension == '.mp3':
                mime_type = 'audio/mpeg'

            elif extension == '.m4a':
                mime_type = 'audio/mp4'

            else:
                # 그 외 기본 타입 설정
                mime_type = 'application/octet-stream'

            print(f"📂 파일 확인 성공: {file_name} (타입: {mime_type})")

            # 3. 파일 스트림 열기 및 전송
            # 'rb' (read binary) 모드로 파일을 열어야 합니다.
            with open(file_path, 'rb') as audio_file:

                files = {'DTMS_AUDIO': (file_name, audio_file, mime_type)}

                return self.request('post', audio_url, base_url, data=payload, files=files, timeout=30)

        except Exception as e:
            print(f"audio_upload_check Exception: {e}")

    def dtms_save_api(self, base_url, file_no, cell_kind, file_name, folder_no=None):
        try:
            file_open_response = self.file_open_api(base_url, file_no, cell_kind)
            if not file_open_response:
                print("❌ file_open_api 실패")
                return None

            dtms_info = file_open_response.json()

            if file_no is None:
                print("파일 키를 찾을 수 없습니다.")
                return None

            header = {"Content-Type": "application/json"}
            dtms_json = dtms_info['DTMS_JSON']
            save_url = f"{base_url}/drive-app/v1/dtm/images/{file_no}/from-dtms"

            if not folder_no:
                save_data = {
                    "COMP_NO": self.config['COMP_NO'],
                    "DEVICE_KIND": cell_kind,
                    "DTMS_GROUP_NO": "ROOT",
                    "DTMS_JSON": dtms_json,
                    "DTMS_TYPE": "dtms",
                    "DTM_DESC": "",
                    "DTM_GROUP_NO": "ROOT",
                    "DTM_NAME": file_name,
                    "SITE_NO": self.config['SITE_NO'],
                    "USER_NO": self.config['USER_NO']
                }

            else:
                save_data = {
                    "USER_NO": self.config['USER_NO'],
                    "COMP_NO": self.config['COMP_NO'],
                    "SITE_NO": self.config['SITE_NO'],
                    "DTM_GROUP_NO": folder_no,
                    "DTMS_JSON": dtms_json,
                    "DTM_NAME": file_name,
                    "DTM_DESC": "",
                    "DEVICE_KIND": cell_kind,
                    "DTMS_TYPE": "dtms",
                    "DTMS_GROUP_NO": file_no
                }

            # ✅ request 래퍼로 변경
            return self.request('post', save_url, base_url, json=save_data, headers=header)

        except Exception as e:
            print(f"dtms_save_api Exception: {e}")
            return None

    def cloud_group_path_api(self, base_url):
        # cloud 페이지 진입 시 group path 확인 하는 api
        cloud_group_path_url = f"{base_url}/drive-app/v1/dtms/group/path"

        param_info = {
            "DRIVER_KIND": "P",
            "USER_NO": self.config['USER_NO']
        }

        # ✅ request 래퍼로 변경
        return self.request('get', cloud_group_path_url, base_url, params=param_info)

    def cloud_group_list_api(self, base_url, current_page, group_no):
        # cloud 페이지 진입 시 파일 확인 하는 api
        cloud_group_list_url = f"{base_url}/drive-app/v1/dtms/groups"

        param_info = {
            "PAGE_NO": current_page,
            "PAGE_SIZE": "18",
            "COMP_NO": self.config['COMP_NO'],
            "PARENT_GROUP_NO": group_no,
            "DRIVER_KIND": "P",
            "USER_NO": self.config['USER_NO'],
            "APP_TYPE": "A"
        }

        # ✅ request 래퍼로 변경
        return self.request('get', cloud_group_list_url, base_url, params=param_info)


    def audio_sync(self, base_url, file_no):
        try:
            audio_sync_url = f"{base_url}/drive-app/v1/dtma/audio/sync"

            headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'ko,hr;q=0.9,ja;q=0.8,pl;q=0.7,ru;q=0.6,sv;q=0.5,nl;q=0.4,sr;q=0.3,de;q=0.2,sh;q=0.1',
                'priority': 'u=1, i',
                'referer': f'{base_url}',
                'sec-ch-ua': '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36'
            }

            param_info = {"DTM_NO": file_no}

            response = self.request('get', audio_sync_url, base_url, headers=headers, params=param_info)

            if response.status_code == 200:
                return response

            else:
                print(f"❌ audio_sync 실패 - status: {response.status_code if response else 'None'}")
                return None

        except Exception as e:
            print(f"audio_sync Exception: {e}")
            return None




class Braille_api(BaseApi):

    def __init__(self, base_url):
        super().__init__(base_url)
        self.user_api = None  # ✅ 미리 선언

    def set_user_api(self, user_api):
        """user_api 주입"""
        self.user_api = user_api

    def multiline_api(self, base_url, text):
        try:
            if not self.user_api:
                print("❌ user_api가 없습니다. set_user_api()를 먼저 호출하세요.")
                return None

            user_info = self.user_api.user_status_api(base_url)
            if not user_info:
                print("❌ user_info 실패")
                return None

            user_status = user_info.json()

            brl_engine = user_status.get('ENGINE', "")
            user_brl = user_status.get('LANGUAGE', "")
            user_brl_lang = user_status.get('LANGUAGE_OPTION', "")
            user_line_space = user_status.get('LINE_SPACING', 0)
            user_letter_space = user_status.get('LETTER_SPACING', 0)
            braille_pin = user_status.get('PIN', 0)

            if brl_engine == "0":
                translation_multiline_url = f"{base_url}/braille-app/v1/braille/translation-multiline"
            else:
                translation_multiline_url = f"{base_url}/braille-app/v1/braille/translation-liblouis-multiline"

            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'ko,hr;q=0.9,ja;q=0.8,pl;q=0.7,ru;q=0.6,sv;q=0.5,nl;q=0.4,sr;q=0.3,de;q=0.2,sh;q=0.1',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Origin': f'{base_url}',
                'Referer': f'{base_url}',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"'
            }

            # ✅ user_status에서 가져오도록 수정
            data = {
                "LANGUAGE": user_brl,
                "OPTION": user_brl_lang,
                "TEXT": text,
                "PIN": str(braille_pin),
                "PADDING": user_line_space,
                "HEIGHT": 10
            }

            # ✅ SPACING, CELL 조건 분기
            if user_letter_space == 1:
                data["SPACING"] = "true"
                data["CELL"] = "20"
            else:
                data["SPACING"] = "false"
                data["CELL"] = "30"

            print(f"multiline_data: {data}")

            # ✅ data → json으로 변경 (Content-Type: application/json)
            return self.request('post', translation_multiline_url, base_url, headers=headers, json=data)

        except Exception as e:
            print(f"multiline_api Exception: {e}")
            return None


    def braille_translation_api(self, base_url, description):
        try:
            if not self.user_api:
                print("❌ user_api가 없습니다. set_user_api()를 먼저 호출하세요.")
                return None

            user_info = self.user_api.user_status_api(base_url)
            if not user_info:
                print("❌ user_info 실패")
                return None

            user_status = user_info.json()

            brl_engine = user_status.get('ENGINE', "")
            user_brl = user_status.get('LANGUAGE', "")
            user_brl_lang = user_status.get('LANGUAGE_OPTION', "")
            user_line_space = user_status.get('LINE_SPACING', 0)
            user_letter_space = user_status.get('LETTER_SPACING', 0)
            braille_pin = user_status.get('PIN', 0)

            if brl_engine == "0":
                translation_url = f"{base_url}/braille-app/v1/braille/translation-console"
            else:
                translation_url = f"{base_url}/braille-app/v1/braille/translation-liblouis"


            translation_data = {
                "LANGUAGE": user_brl,
                "OPTION": user_brl_lang,
                "PADDING": user_line_space,
                "TEXT": description
            }

            if not (brl_engine == "0" and "chinese" in user_brl):
                translation_data["PIN"] = braille_pin

            if user_letter_space == 1:
                translation_data["SPACING"] = "true"
                translation_data["CELL"] = 20

            else:
                translation_data["SPACING"] = "false"
                translation_data["CELL"] = 30

            # print(f"translation_data: {translation_data}")

            # ✅ request 래퍼로 변경
            return self.request('post', translation_url, base_url, data=translation_data)

        except Exception as e:
            print(f"braille_translation_api Exception: {e}")
            return None




    def pad_conn_multiline_api(self, base_url, text):
        try:
            if not self.user_api:
                print("❌ user_api가 없습니다. set_user_api()를 먼저 호출하세요.")
                return None

            user_info = self.user_api.user_status_api(base_url)
            if not user_info:
                print("❌ user_info 실패")
                return None

            user_status = user_info.json()

            user_brl = user_status.get('LANGUAGE', "")
            user_line_space = user_status.get('LINE_SPACING', 0)
            user_letter_space = user_status.get('LETTER_SPACING', 0)
            braille_pin = user_status.get('PIN', 0)

            translation_multiline_url = f"{base_url}/braille-app/v1/braille/translation-liblouis-multiline"

            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'ko,hr;q=0.9,ja;q=0.8,pl;q=0.7,ru;q=0.6,sv;q=0.5,nl;q=0.4,sr;q=0.3,de;q=0.2,sh;q=0.1',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Origin': f'{base_url}',
                'Referer': f'{base_url}/cloud',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"'
            }

            # ✅ user_status에서 가져오도록 수정
            data = {
                "LANGUAGE": user_brl,
                "OPTION": "1",
                "TEXT": text,
                "PIN": str(braille_pin),
                "PADDING": user_line_space,
                "HEIGHT": 10
            }

            # ✅ SPACING, CELL 조건 분기
            if user_letter_space == 1:
                data["SPACING"] = "true"
                data["CELL"] = "20"
            else:
                data["SPACING"] = "false"
                data["CELL"] = "30"

            print(f"multiline_data: {data}")

            # ✅ data → json으로 변경 (Content-Type: application/json)
            return self.request('post', translation_multiline_url, base_url, headers=headers, json=data)

        except Exception as e:
            print(f"multiline_api Exception: {e}")
            return None


class ApiClient:
    def __init__(self, base_url):
        # ✅ session 하나만 생성
        self.session = requests.Session()

        # ✅ 모든 api 인스턴스 생성
        self.user = User_api()
        self.drive = Drive_api(base_url)
        self.braille = Braille_api(base_url)

        # ✅ 모든 api session 공유
        for api in [self.user, self.drive, self.braille]:
            api.session = self.session

        # ✅ braille_api에 user_api 주입
        self.braille.set_user_api(self.user)














    # def open_file_info(self, base_url, file_name, folder_in_filename=None):
    #
    #     filelist_cnt = self.filebrowser_list_api(base_url, 1, 'ROOT').json()
    #     total_count = filelist_cnt.get('TOTAL_COUNT', 0)
    #
    #     if total_count == 0:
    #         total_count +=1
    #
    #     file_len = math.ceil(total_count / 9)
    #     page_nums = list(range(1, (file_len + 1)))
    #
    #     filelist_json = self.filebrowser_list_api(base_url, 'ROOT').json()
    #
    #     for key in filelist_json:
    #         if type(filelist_json[key]) is list:
    #             for item in filelist_json[key]:
    #                 # 선택한게 파일인지 폴더인지 구분 하는 로직
    #                 if item['FILE_NAME'] == file_name and 'D' in item['FILE_KEY'] and 'audioPath' in folder_in_item['DTMS_JSON'] and \
    #                                             folder_in_item['DTMS_JSON']['audioPath'] == "":
    #                     print(f"ROOT 내 파일: {item['FILE_NAME']}")
    #                     return "dtm", item['FILE_KEY'], item['DEVICE_KIND']
    #
    #                 elif item['FILE_NAME'] == file_name and 'D' in item['FILE_KEY'] and 'audioPath' in folder_in_item['DTMS_JSON'] and \
    #                                             folder_in_item['DTMS_JSON']['audioPath'] != "":
    #                     print(f"ROOT 내 파일: {item['FILE_NAME']}")
    #                     return "dtma", item['FILE_KEY'], item['DEVICE_KIND']
    #
    #                 elif item['FILE_NAME'] == file_name and 'G' in item['FILE_KEY']:
    #
    #                     folder_json = self.filebrowser_list_api(base_url, item['FILE_KEY']).json()
    #
    #                     # 폴더 내 파일 클릭 했을 때의 status 값
    #                     for key in folder_json:
    #                         if type(folder_json[key]) is list:
    #                             for folder_in_item in folder_json[key]:
    #                                 if folder_in_item['FILE_NAME'] == folder_in_filename and 'audioPath' in folder_in_item['DTMS_JSON'] and \
    #                                             folder_in_item['DTMS_JSON']['audioPath'] == "":
    #                                     print(f"우히히 폴더명: {item['FILE_NAME']}")
    #                                     print(f"폴더 내 파일명: {folder_in_item['FILE_NAME']}")
    #                                     return "dtm", folder_in_item['FILE_KEY'], folder_in_item['DEVICE_KIND']
    #
    #                                 elif folder_in_item['FILE_NAME'] == folder_in_filename and 'audioPath' in folder_in_item['DTMS_JSON'] and \
    #                                             folder_in_item['DTMS_JSON']['audioPath'] != "":
    #                                     print(f"우히히 폴더명: {item['FILE_NAME']}")
    #                                     print(f"폴더 내 파일명: {folder_in_item['FILE_NAME']}")
    #                                     return "dtma", folder_in_item['FILE_KEY'], folder_in_item['DEVICE_KIND']
    #
    #                                 else:
    #                                     pass
    #
    # def file_openman_api(self, base_url, file_type, file_key, canvas_size):
    #
    #     # file_info = self.open_file_info(base_url, root_file, folder_in_file)
    #
    #     # dtm 부분과 device/뒤 패드 사이즈 동적으로 처리 필요
    #     file_open_url = f"{base_url}/drive-app/v1/{file_type}/images/{file_key}/device/{canvas_size}/to-dtms"
    #
    #     file_open_api = requests.get(url=file_open_url)
    #
    #     return file_open_api

    # for key in filelist_json:
    #     if type(filelist_json[key]) is list:
    #         for item in filelist_json[key]:
    #             # 선택한게 파일인지 폴더인지 구분 하는 로직
    #             if item['FILE_NAME'] == file_name and 'D' in item['FILE_KEY']:
    #                 print(f"ROOT 내 파일: {item['FILE_NAME']}")
    #
    #                 return item['FILE_KEY']
    #
    #             elif item['FILE_NAME'] == file_name and 'G' in item['FILE_KEY']:
    #                 # print(f"폴더명: {item['FILE_NAME']}")
    #
    #                 folder_json = self.filebrowser_list_api(base_url, item['FILE_KEY']).json()
    #
    #                 # 폴더 내 파일 클릭 했을 때의 status 값
    #                 for key in folder_json:
    #                     if type(folder_json[key]) is list:
    #                         for folder_in_item in folder_json[key]:
    #                             if folder_in_item['FILE_NAME'] == folder_in_filename:
    #                                 print(f"우히히 폴더명: {item['FILE_NAME']}")
    #                                 print(f"폴더 내 파일명: {folder_in_item['FILE_NAME']}")
    #                                 return item['FILE_KEY'], folder_in_item['FILE_KEY']
    #                             else:
    #                                 pass

    # def dtms_data(self, base_url, file_key, cell_kind):
    #     dtms_info = self.file_open_api(base_url, file_key, cell_kind).json()
    #
    #     return dtms_info['DTMS_JSON']






# class File_group_api(BaseApi):
#     def cloud_group_path_api(self, base_url):
#         cloud_group_path_url = f"{base_url}/drive-app/v1/dtms/group/path"
#
#         param_info = {
#             "DRIVER_KIND": "P",
#             "USER_NO": self.config['USER_NO']
#         }
#
#         cloud_group_path_url_api = self.session.get(url=cloud_group_path_url, params=param_info)
#
#         return cloud_group_path_url_api
#
#         # if "dev" in base_url:
#         #     cloud_group_path_url = "{}/drive-app/v1/dtms/group/path".format(base_url)
#         #
#         #     param_info = {
#         #         "DRIVER_KIND": "P",
#         #         "USER_NO": "dev_USER_NO"
#         #     }
#         #
#         # elif "dev" not in base_url:
#         #     cloud_group_path_url = "{}/drive-app/v1/dtms/group/path".format(base_url)
#         #
#         #     param_info = {
#         #         "DRIVER_KIND": "P",
#         #         "USER_NO": "prod_USER_NO"
#         #     }
#
#
#
#     def cloud_group_list_api(self, base_url, current_page, group_no):
#         cloud_group_list_url = f"{base_url}/drive-app/v1/dtms/groups"
#
#         param_info = {
#             "PAGE_NO": current_page,
#             "PAGE_SIZE": "18",
#             "COMP_NO": self.config['COMP_NO'],
#             "PARENT_GROUP_NO": group_no,
#             "DRIVER_KIND": "P",
#             "USER_NO": self.config['USER_NO'],
#             "APP_TYPE": "A"
#         }
#
#         cloud_group_list_url_api = self.session.get(url=cloud_group_list_url, params=param_info)
#
#         return cloud_group_list_url_api

        # if "dev" in base_url:
        #     cloud_group_list_url = "{}/drive-app/v1/dtms/groups".format(base_url)
        #
        #     param_info = {
        #         "PAGE_NO": "1",
        #         "PAGE_SIZE": "18",
        #         "COMP_NO": readConfig("USER_INFO", "COMP_NO"),
        #         "PARENT_GROUP_NO": "ROOT",
        #         "DRIVER_KIND": "P",
        #         "USER_NO": readConfig("USER_INFO", "dev_USER_NO"),
        #         "APP_TYPE": "A"
        #     }
        #
        # elif "dev" not in base_url:
        #     cloud_group_list_url = "{}/drive-app/v1/dtms/groups".format(base_url)
        #
        #     param_info = {
        #         # "PAGE_NO": "1",
        #         # "PAGE_SIZE": "18",
        #         "COMP_NO": readConfig("USER_INFO", "COMP_NO"),
        #         "PARENT_GROUP_NO": "ROOT",
        #         "DRIVER_KIND": "P",
        #         "USER_NO": readConfig("USER_INFO", "prod_USER_NO"),
        #         "APP_TYPE": "A"
        #     }




























    # filelist_json = filebrowser_list_api('ROOT').json()
    # time1 = None
    #
    # for key in filelist_json:
    #     if type(filelist_json[key]) is list:
    #         for item in filelist_json[key]:
    #             if item['FILE_NAME'] in file_name and save_path == 'ROOT':
    #                 time_str1 = item['MOD_DATE']
    #                 time2 = datetime.strptime(time_str1, "%Y-%m-%d %H:%M:%S.%f")
    #
    #                 if time1 is None or time1 < time2:
    #                     time1 = time2
    #                     latest_item = item
    #                     print(f"time1: {time1} 이 최근입니다.")
    #                     time_str = datetime.strftime(time1, "%Y-%m-%d %H:%M:%S.") + str(time1.microsecond)[:1]
    #                     print(f"time_str: {time_str}")
    #                     print(f"파일명: {item['FILE_NAME']}")
    #                 else:
    #                     print("파일이 없습니다.")
    #
    #             elif save_path != 'ROOT':
    #                 if item['FILE_NAME'] in save_path:
    #                     time_str1 = item['REG_DATE']
    #                     time2 = datetime.strptime(time_str1, "%Y-%m-%d %H:%M:%S.%f")
    #
    #                     if time1 is None or time1 < time2:
    #                         time1 = time2
    #                         # latest_item = item
    #                         print(f"time1: {time1} 이 최근입니다.")
    #                         time_str = datetime.strftime(time1, "%Y-%m-%d %H:%M:%S.") + str(time1.microsecond)[:1]
    #                         print(f"time_str: {time_str}")
    #                         print(f"폴더명: {item['FILE_NAME']}")
    #                     else:
    #                         print("파일이 없습니다.")
    #
    #                     folder_json = filebrowser_list_api(item['FILE_KEY']).json()
    #
    #                     for key in folder_json:
    #                         if type(folder_json[key]) is list:
    #                             for folder_in_item in folder_json[key]:
    #                                 if folder_in_item['FILE_NAME'] in file_name:
    #                                     print(f"폴더 filekey: {item['FILE_KEY']}")
    #                                     time_str1 = folder_in_item['MOD_DATE']
    #                                     time2 = datetime.strptime(time_str1, "%Y-%m-%d %H:%M:%S.%f")
    #
    #                                     if time1 is None or time1 < time2:
    #                                         time1 = time2
    #                                         latest_item = folder_in_item
    #                                         print(f"time1: {time1} 이 최근입니다.")
    #                                         time_str = datetime.strftime(time1, "%Y-%m-%d %H:%M:%S.") + str(
    #                                             time1.microsecond)[:1]
    #                                         print(f"time_str: {time_str}")
    #                                     else:
    #                                         print("파일이 없습니다.")
    #                                 else:
    #                                     pass

                    # save_url = 'https://dev-apps.dotincorp.com/drive-app/v1/dtm/images/{}/from-dtms'.format(item['FILE_KEY'])
                    #
                    # save_data = {
                    #     "USER_NO": readConfig("USER_INFO", "USER_NO"),
                    #     "DTM_GROUP_NO": "ROOT",
                    #     "DTMS_JSON": item['DTMS_JSON'],
                    #     "DTM_NAME": file_name,
                    #     "DTM_DESC": "",
                    #     "DEVICE_KIND": "300",
                    #     "DTMS_TYPE": "dtms",
                    #     "DTMS_GROUP_NO": "ROOT"
                    #
                    # }
                    #
                    # print(f"최신 시간_post200: {time_str}")
                    # print(f"최신 파일명_post200: {item['FILE_NAME']}")
                    # print(f"최신 파일 DTMS_JSON값_post200: {item['DTMS_JSON']}")
                    # print(f"최신 파일 저장 시간_post200: {item['MOD_DATE']}")

                    # save_info = requests.post(url=save_url, data=save_data)
                    # return save_info



                    # save_url = 'https://dev-apps.dotincorp.com/drive-app/v1/dtm/images/{}/from-dtms'.format(folder_in_item['FILE_KEY'])
                    #
                    # save_data = {
                    #     "USER_NO": readConfig("USER_INFO", "USER_NO"),
                    #     "DTM_GROUP_NO": item['FILE_KEY'],
                    #     "DTMS_JSON": folder_in_item['DTMS_JSON'],
                    #     "DTM_NAME": file_name,
                    #     "DTM_DESC": "",
                    #     "DEVICE_KIND": "300",
                    #     "DTMS_TYPE": "dtms",
                    #     "DTMS_GROUP_NO": item['FILE_KEY']
                    #
                    # }
                    #
                    # print(f"최신 시간_post200: {time_str}")
                    # print(f"최신 파일명_post200: {item['FILE_NAME']}")
                    # print(f"최신 파일 DTMS_JSON값_post200: {item['DTMS_JSON']}")
                    # print(f"최신 파일 저장 시간_post200: {item['MOD_DATE']}")

    # if latest_item:
    #
    #     if save_path == 'ROOT':
    #
    #         save_url = 'https://dev-apps.dotincorp.com/drive-app/v1/dtm/images/{}/from-dtms'.format(latest_item['FILE_KEY'])
    #
    #         save_data = {
    #             "USER_NO": readConfig("USER_INFO", "USER_NO"),
    #             "DTM_GROUP_NO": "ROOT",
    #             "DTMS_JSON": latest_item['DTMS_JSON'],
    #             "DTM_NAME": latest_item['FILE_NAME'],
    #             "DTM_DESC": "",
    #             "DEVICE_KIND": "300",
    #             "DTMS_TYPE": "dtms",
    #             "DTMS_GROUP_NO": "ROOT"
    #
    #         }
    #
    #         print(f"최신 시간_post200: {time1}")
    #         print(f"최신 파일명_post200: {latest_item['FILE_NAME']}")
    #         print(f"최신 파일 DTMS_JSON값_post200: {latest_item['DTMS_JSON']}")
    #         print(f"최신 파일 저장 시간_post200: {latest_item['MOD_DATE']}")
    #
    #     elif save_path != 'ROOT':
    #
    #         save_url = 'https://dev-apps.dotincorp.com/drive-app/v1/dtm/images/{}/from-dtms'.format(latest_item['FILE_KEY'])
    #
    #         save_data = {
    #                     "USER_NO": readConfig("USER_INFO", "USER_NO"),
    #                     "DTM_GROUP_NO": item['FILE_KEY'],
    #                     "DTMS_JSON": latest_item['DTMS_JSON'],
    #                     "DTM_NAME": latest_item['FILE_NAME'],
    #                     "DTM_DESC": "",
    #                     "DEVICE_KIND": "300",
    #                     "DTMS_TYPE": "dtms",
    #                     "DTMS_GROUP_NO": item['FILE_KEY']
    #
    #         }
    #
    #         print(f"최신 시간_post200: {time1}")
    #         print(f"최신 파일명_post200: {latest_item['FILE_NAME']}")
    #         print(f"최신 파일 DTMS_JSON값_post200: {latest_item['DTMS_JSON']}")
    #         print(f"최신 파일 저장 시간_post200: {latest_item['MOD_DATE']}")
    #
    # else:
    #     print("최신 항목이 없습니다.")
    #
    # save_info = requests.post(url=save_url, data=save_data)
    # return save_info



    # if latest_item:
    #     print(f"최신 시간_post200: {time_str}")
    #     print(f"최신 파일명_post200: {latest_item['FILE_NAME']}")
    #     print(f"최신 파일 DTMS_JSON값_post200: {latest_item['DTMS_JSON']}")
    #     print(f"최신 파일 저장 시간_post200: {latest_item['MOD_DATE']}")
    #
    #     save_url = 'https://dev-apps.dotincorp.com/drive-app/v1/dtm/images/{}/from-dtms'.format(latest_item['FILE_KEY'])
    #
    #     save_data = {
    #         "USER_NO": readConfig("USER_INFO", "USER_NO"),
    #         "DTM_GROUP_NO": file_path,
    #         "DTMS_JSON": latest_item['DTMS_JSON'],
    #         "DTM_NAME": file_name,
    #         "DTM_DESC": "",
    #         "DEVICE_KIND": "300",
    #         "DTMS_TYPE": "dtms",
    #         "DTMS_GROUP_NO": file_path
    #
    #     }
    # else:
    #     pass

    # save_info = requests.post(url=save_url, data=save_data)
    # return save_info

    # for key in filelist_json:
    #     if type(filelist_json[key]) is list:
    #         for item in filelist_json[key]:
    #             if file_name in item['FILE_NAME']:
    #                 # print("FILE_NAME값: {}".format(item['FILE_NAME']))
    #                 # print("DTMS_JSON값: {}".format(item['DTMS_JSON']))
    #                 # print("REG_DATE값: {}".format(item['REG_DATE']))
    #
    #                 time_str1 = item['REG_DATE']
    #                 time2 = datetime.strptime(time_str1, "%Y-%m-%d %H:%M:%S.%f")
    #
    #                 if time1 is None or time1 < time2:
    #                     time1 = time2
    #                     latest_item = item
    #                     print(f"time1: {time1} 이 최근입니다.")
    #
    #                 time_str = datetime.strftime(time1, "%Y-%m-%d %H:%M:%S.") + str(time1.microsecond)[:1]
    #                 print(f"time_str: {time_str}")
    #
    #             else:
    #                 pass
    #
    # if latest_item:
    #     print(f"최신 시간_post200: {time_str}")
    #     print(f"최신 파일명_post200: {latest_item['FILE_NAME']}")
    #     print(f"최신 파일 DTMS_JSON값_post200: {latest_item['DTMS_JSON']}")
    #     print(f"최신 파일 저장 시간_post200: {latest_item['REG_DATE']}")
    #
    #     save_url = 'https://dev-apps.dotincorp.com/drive-app/v1/dtm/images/{}/from-dtms'.format(item['FILE_KEY'])
    #
    #     save_data = {
    #         "USER_NO": readConfig("USER_INFO", "USER_NO"),
    #         "DTM_GROUP_NO": file_path,
    #         "DTMS_JSON": item['DTMS_JSON'],
    #         "DTM_NAME": file_name,
    #         "DTM_DESC": "",
    #         "DEVICE_KIND": "300",
    #         "DTMS_TYPE": "dtms",
    #         "DTMS_GROUP_NO": file_path
    #
    #     }
    # else:
    #     pass
    #
    #
    # save_info = requests.post(url=save_url, data=save_data)
    # return save_info

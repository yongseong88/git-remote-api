import logging
import pytest
# from ApiClient.Braille.braiile_action import BrailleAction
# from ApiClient.api_session_common import Apisession
from board.post import PostsAction

# from Common.common_action import CommonAction
# from Common.common_data import Commondata
# from Utilities.configreaderutil import Filereadutil
# from ApiClient.Base_API import User_api, ApiClient

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("base_url")
class TestMain():

    @pytest.mark.regression
    def test_posts_lists(self, base_url):
        try:
            posts_action = PostsAction(base_url)
            posts_action.specific_user_post_api()
            # posts_action.specific_post_api()
            # posts = posts_action.posts_api()
            # print(f"posts: {posts.json()}")

            # if letter_input_result is None:
            #     raise ValueError(f"'{letter_input_result}없음.")
            #
            # # 1. 성공 건수 계산 및 출력 (정보 보고)
            # success_count = sum(1 for code in letter_input_result if 200 <= code < 300)
            # total_count = len(letter_input_result)
            #
            # print(f"✅ 총 {total_count}건 중 {success_count}건이 200번대 응답을 받았습니다.")
            #
            # # 2. 실패 코드만 분류 (검증 기준 준비)
            # failed_codes = [code for code in letter_input_result if code >= 400 or code < 200]
            #
            # # 3. ⭐️ 최종 assert (검증 수행)
            # assert len(failed_codes) == 0, f"HTTP 상태 코드 검증 실패. 실패 건수: {len(failed_codes)}건. 실패 코드 목록: {failed_codes}"

        except AssertionError as e:
            print(f"test_letter_input AssertionError: {e}")



    # @pytest.mark.regression
    # def test_user_info(self, base_url):
    #     try:
    #         api_client = ApiClient(base_url)
    #         common_data = Commondata(base_url)
    #         user_account = common_data.account_config()
    #
    #         valid_id = user_account['valid_id']
    #         valid_pwd = user_account['valid_pwd']
    #
    #         api_client.user.login_and_verify(valid_id, valid_pwd)
    #         user_info_http = api_client.user.get_user_me()
    #
    #         assert user_info_http.status_code <= 200, f"✅ 유저 조회 실패 - status: {user_info_http.status_code}"
    #         logger.info(f"✅ 유저 조회 성공 - status: {user_info_http.status_code}")
    #
    #     except AssertionError as e:
    #         print(f"AssertionError: {e}")
    #
    # # @pytest.mark.regression
    # def test_user_status(self, base_url):
    #     try:
    #         api_client = ApiClient(base_url)
    #         common_data = Commondata(base_url)
    #         user_account = common_data.account_config()
    #
    #         valid_id = user_account['valid_id']
    #         valid_pwd = user_account['valid_pwd']
    #
    #         api_client.user.login_and_verify(valid_id, valid_pwd)
    #         user_status_http = api_client.user.user_status_api()
    #
    #         assert user_status_http.status_code <= 200, f"✅ 유저 설정 정보 조회 실패 - status: {user_status_http.status_code}"
    #         logger.info(f"✅ 유저 설정 정보 조회 성공 - status: {user_status_http.status_code}")
    #
    #     except AssertionError as e:
    #         print(f"AssertionError: {e}")
    #
    # # @pytest.mark.regression
    # def test_gnb_menus(self, base_url):
    #     try:
    #         api_client = ApiClient(base_url)
    #         common_data = Commondata(base_url)
    #         user_account = common_data.account_config()
    #
    #         valid_id = user_account['valid_id']
    #         valid_pwd = user_account['valid_pwd']
    #
    #         api_client.user.login_and_verify(valid_id, valid_pwd)
    #         gnb_menu_http = api_client.user.menus_api()
    #
    #         assert gnb_menu_http.status_code <= 200, f"✅ 유저 설정 정보 조회 실패 - status: {gnb_menu_http.status_code}"
    #         logger.info(f"✅ 메뉴 조회 성공 - status: {gnb_menu_http.status_code}")
    #
    #     except AssertionError as e:
    #         print(f"AssertionError: {e}")
    #
    #
    # # @pytest.mark.regression
    # def test_braille_input(self, base_url):
    #     try:
    #         braille_action = BrailleAction(base_url)
    #         braille_input_result = braille_action.set_braille()
    #
    #         if braille_input_result is None:
    #             raise ValueError(f"'{braille_input_result}없음.")
    #
    #         # 1. 성공 건수 계산 및 출력 (정보 보고)
    #         success_count = sum(1 for code in braille_input_result if 200 <= code < 300)
    #         total_count = len(braille_input_result)
    #
    #         print(f"✅ 총 {total_count}건 중 {success_count}건이 200번대 응답을 받았습니다.")
    #
    #         # 2. 실패 코드만 분류 (검증 기준 준비)
    #         failed_codes = [code for code in braille_input_result if code >= 400 or code < 200]
    #
    #         # 3. ⭐️ 최종 assert (검증 수행)
    #         assert len(failed_codes) == 0, f"HTTP 상태 코드 검증 실패. 실패 건수: {len(failed_codes)}건. 실패 코드 목록: {failed_codes}"
    #
    #         # assert braille_input_http.status_code <= 200, f"✅ 점자 설정 실패 - status: {braille_input_http.status_code}"
    #         # logger.info(f"✅ 점자 설정 성공 - status: {braille_input_http.status_code}")
    #
    #     except AssertionError as e:
    #         print(f"AssertionError: {e}")
    #
    # # @pytest.mark.regression
    # def test_line_input(self, base_url):
    #     try:
    #         braille_action = BrailleAction(base_url)
    #         line_input_result = braille_action.set_line()
    #
    #         if line_input_result is None:
    #             raise ValueError(f"'{line_input_result}없음.")
    #
    #         # 1. 성공 건수 계산 및 출력 (정보 보고)
    #         success_count = sum(1 for code in line_input_result if 200 <= code < 300)
    #         total_count = len(line_input_result)
    #
    #         print(f"✅ 총 {total_count}건 중 {success_count}건이 200번대 응답을 받았습니다.")
    #
    #         # 2. 실패 코드만 분류 (검증 기준 준비)
    #         failed_codes = [code for code in line_input_result if code >= 400 or code < 200]
    #
    #         # 3. ⭐️ 최종 assert (검증 수행)
    #         assert len(failed_codes) == 0, f"HTTP 상태 코드 검증 실패. 실패 건수: {len(failed_codes)}건. 실패 코드 목록: {failed_codes}"
    #
    #     except AssertionError as e:
    #         print(f"test_line_input AssertionError: {e}")
    #
    # # @pytest.mark.regression
    # def test_letter_input(self, base_url):
    #     try:
    #         braille_action = BrailleAction(base_url)
    #         letter_input_result = braille_action.set_letter()
    #
    #         if letter_input_result is None:
    #             raise ValueError(f"'{letter_input_result}없음.")
    #
    #         # 1. 성공 건수 계산 및 출력 (정보 보고)
    #         success_count = sum(1 for code in letter_input_result if 200 <= code < 300)
    #         total_count = len(letter_input_result)
    #
    #         print(f"✅ 총 {total_count}건 중 {success_count}건이 200번대 응답을 받았습니다.")
    #
    #         # 2. 실패 코드만 분류 (검증 기준 준비)
    #         failed_codes = [code for code in letter_input_result if code >= 400 or code < 200]
    #
    #         # 3. ⭐️ 최종 assert (검증 수행)
    #         assert len(failed_codes) == 0, f"HTTP 상태 코드 검증 실패. 실패 건수: {len(failed_codes)}건. 실패 코드 목록: {failed_codes}"
    #
    #     except AssertionError as e:
    #         print(f"test_letter_input AssertionError: {e}")
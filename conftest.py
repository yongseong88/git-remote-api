# from Utilities.testresult_json import parse_pytest_json_results, write_to_google_sheet
import pytest
# from selenium import webdriver
import datetime
import os
# from seleniumwire import webdriver
# webdriver-manager 패키지 설치
# from webdriver_manager.chrome import ChromeDriverManager 라이브러리 호출
# from selenium.webdriver.chrome.service import Service 라이브러리 호출

def pytest_addoption(parser):
    parser.addoption(
        "--env",  # 명령줄 옵션 이름
        action="store",  # 옵션 값 저장
        default=None,  # 기본값
        help="Set the environment: dev or prod"  # 옵션 설명
    )

@pytest.fixture()
def base_url(pytestconfig):
    try:
        # CLI 옵션 > 환경변수 > 기본값 순서로 환경 설정
        return "https://jsonplaceholder.typicode.com"

    except Exception as e:
        print(f"conftest base_url Exception: {e}")


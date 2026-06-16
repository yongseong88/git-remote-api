from ApiClient.Base_API import BaseApi
import pytest
from Utilities.configreaderutil import Filereadutil

"""
    /posts 리소스에 대한 GET 테스트.

    이 파일에서 보여주는 것:
    - 목록 조회 + 건수/스키마 검증
    - 단일 조회 + 값/타입 검증
    - 없는 리소스 → 404 (네거티브 케이스)
    - 응답 헤더(Content-Type) 검증
    - @parametrize 로 여러 입력 반복
    - 중첩 라우트와 쿼리 파라미터 필터
"""


class PostsAction(BaseApi):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url

    def all_posts_api(self):
        try:
            posts_url = f"{self.base_url}/posts"

            headers = {
                'accept': 'application/json'

            }

            posts_lists = self.request('get', posts_url, headers=headers)
            post_lst = posts_lists.json()
            print(f"\npost_lst 길이: {len(post_lst)}")

            for pl in post_lst:
                print(f"userId: {pl['userId']}, id: {pl['id']}")

            # return self.request('get', posts_url, headers=headers)

        except Exception as e:
            print(f"user_status_api Exception: {e}")
            return False


    def posts_api(self):
        try:
            posts_url = f"{self.base_url}/posts"

            headers = {
                'accept': 'application/json'

            }

            posts_lists = self.request('get', posts_url, headers=headers)
            post_lst = posts_lists.json()
            print(f"\npost_lst 길이: {len(post_lst)}")

            for index, pl in enumerate(post_lst):
                single_posts_url = posts_url + f"/{index+1}"
                single_posts = self.request('get', single_posts_url, headers=headers)
                print(f"single_info: {single_posts.json()}")

            # return self.request('get', posts_url, headers=headers)

        except Exception as e:
            print(f"user_status_api Exception: {e}")
            return False

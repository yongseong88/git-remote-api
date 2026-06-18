from ApiClient.Base_API import BaseApi


class CommentsAction(BaseApi):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url

    def all_comments_api(self):
        try:
            comments_url = f"{self.base_url}/comments"

            headers = {
                'accept': 'application/json'

            }

            comments_lists = self.request('get', comments_url, headers=headers)
            comments_lst = comments_lists.json()
            print(f"\npost_lst 길이: {len(comments_lst)}")

            for cl in comments_lst:
                print(f"userId: {cl['postId']}, id: {cl['id']}")

        except Exception as e:
            print(f"user_status_api Exception: {e}")
            return False

    def specific_comments_api(self):
        try:
            comments_url = f"{self.base_url}/comments"

            headers = {
                'accept': 'application/json'

            }

            comments_lists = self.request('get', comments_url, headers=headers)
            comment_json = comments_lists.json()
            print(f"\ncomment_json 길이: {len(comment_json)}")

            post_ids = sorted({cl['postId'] for cl in comment_json})

            for cl in post_ids:
                specific_comments_url = f"{self.base_url}/posts/{cl}/comments"
                specific_comments = self.request('get', specific_comments_url, headers=headers)
                specific_comments_dict = specific_comments.json()

                for scd in specific_comments_dict:
                    print(f"{scd['postId']}번째 글, id: {scd['id']}, 게시글 내 댓글 status_code: {specific_comments.status_code}")

        except Exception as e:
            print(f"specific_comments_api Exception: {e}")
            return False
# import datetime
# import pandas as pd
# import json
# import pytest
# from google.oauth2.service_account import Credentials
# import gspread
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
#
#
# def parse_pytest_json_results(json_report):
#     with open(json_report, 'r') as f:
#         json_data = json.load(f)
#     data = []
#     for test in json_data['tests']:
#         name = test['nodeid']
#         outcome = test['outcome']
#         duration = test['call']['duration']
#         message = test.get('longrepr', None)
#         data.append({
#             'Test Case': name,
#             'Status': outcome,
#             'Time': duration,
#             'Failure Message': message if outcome == 'failed' else None
#         })
#     df = pd.DataFrame(data)
#
#     return df
#
# # Google Sheets API 인증
# def authenticate_google_apis():
#     credentials = Credentials.from_service_account_file(
#         '/Users/park-yongseong/Documents/DCW_Automation/Config/automation-spreadsheet-437715-ad655cd2a639.json',  # 서비스 계정 JSON 파일 경로
#         scopes=[
#             'https://spreadsheets.google.com/feeds',
#             'https://www.googleapis.com/auth/drive'
#         ]
#     )
#     # client = gspread.authorize(creds)
#     return credentials
#
#
# # Google 스프레드시트와 Google Drive API 사용 클라이언트 생성
# def create_google_clients():
#     credentials = authenticate_google_apis()
#
#     # Google Sheets API 클라이언트 생성
#     gspread_client = gspread.authorize(credentials)
#
#     # Google Drive API 클라이언트 생성
#     drive_client = build('drive', 'v3', credentials=credentials)
#
#     return gspread_client, drive_client
#
# # Google 스프레드시트에 데이터를 쓰고 Google Drive에서 파일 정보 가져오는 함수
# def write_to_google_sheet(df, spreadsheet_name=None):
#     gspread_client, drive_client = create_google_clients()
#
#     try:
#         # 스프레드시트를 엽니다 (만약 없다면 새로 생성)
#         spreadsheet = gspread_client.open(spreadsheet_name)
#
#         # worksheet 추가
#         worksheet = spreadsheet.add_worksheet(title=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), rows=100, cols=100)
#         worksheet.update([df.columns.values.tolist()] + df.values.tolist())
#
#     except gspread.SpreadsheetNotFound:
#         today = datetime.datetime.now().strftime('%Y_%m')
#         # today = date.today().strftime('%Y_%m')
#         spreadsheet_metadata = {
#             'name': today + '_DCW_Automation_Results',
#             'mimeType': 'application/vnd.google-apps.spreadsheet',
#             'parents': ['1zg62JRbQHLOt6xNgOpQ6Es4ql_Hd7b93']  # 공유 드라이브 ID
#             # 'parents': ['0AIo8tZ88_blKUk9PVA']  # 공유 드라이브 ID
#         }
#
#         # 6. Google Drive에 스프레드시트 파일 생성
#         file = drive_client.files().create(body=spreadsheet_metadata, fields='id', supportsAllDrives=True).execute()
#
#         # 새로 생성된 스프레드시트 ID를 확인
#         spreadsheet_id = file.get('id')
#         print(f'\r\nSpreadsheet created with ID: {spreadsheet_id}')
#
#         # 생성된 스프레드시트 열기
#         spreadsheet = gspread_client.open_by_key(spreadsheet_id)
#
#         # 스프레드시트 공유 설정 (이메일 추가하여 수정 권한 부여)
#         spreadsheet.share('yspark@dotincorp.com', perm_type='user', role='writer')
#
#         # 첫 번째 워크시트에 데이터 업데이트
#         worksheet = spreadsheet.get_worksheet(0) # 첫번째 워크시트 설
#         worksheet.update_title(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) # 워크시트명 변경
#         worksheet.update([df.columns.values.tolist()] + df.values.tolist())
#
#     except HttpError as error:
#         print(f"오류 발생: {error}")
#
#
#         # spreadsheet = gspread_client.create(spreadsheet_name)
#         # Google Drive에서 스프레드시트 파일 정보를 가져옴
#         # file_id = spreadsheet.id
#         # file_metadata = drive_client.files().get(fileId=file_id).execute()
#         #
#         # print(f"\r\n스프레드시트가 Google Drive에 생성되었습니다. 파일 ID: {file_id}")
#         # print(f"Google Drive에서의 파일 정보: {file_metadata}")
#

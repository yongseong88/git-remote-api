import pandas as pd
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
import gspread

try:
    # JSON 파일 읽기
    with open('/Users/park-yongseong/Documents/DCW_Automation/Result_Report/report.json') as f:
        data = json.load(f)

    # 테스트 결과에서 필요한 정보 추출
    tests = data['tests']

    # 필요한 데이터를 정리해서 pandas 데이터프레임으로 변환
    df = pd.DataFrame([
        {
            'name': test['nodeid'],
            'outcome': test['outcome'],
            'duration': test['call']['duration']

        }
        for test in tests
    ])

    print(df)

    # 2. Google Sheets API에 연결
    # OAuth 2.0 자격 증명 파일 경로
    creds_file = '/Users/park-yongseong/Documents/DCW_Automation/Config/automation-spreadsheet-437715-ad655cd2a639.json'  # credentials JSON 파일 경로 지정

    # Google Sheets API 범위
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # 자격 증명 생성 및 인증
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
    client = gspread.authorize(creds)

    # Google Drive API 클라이언트 생성
    drive_service = build('drive', 'v3', credentials=creds)

    # 3. Google 스프레드시트 생성
    spreadsheet_metadata = {
        'name': 'Automation_Results22',
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'parents': ['0AIo8tZ88_blKUk9PVA']  # 공유 드라이브 ID
    }

    # 6. Google Drive에 스프레드시트 파일 생성
    file = drive_service.files().create(body=spreadsheet_metadata, fields='id', supportsAllDrives=True).execute()

    # 새로 생성된 스프레드시트 ID를 확인
    spreadsheet_id = file.get('id')
    print(f'Spreadsheet created with ID: {spreadsheet_id}')

    # 생성된 스프레드시트 열기
    spreadsheet = client.open_by_key(spreadsheet_id)

    # 3. 새로운 Google 스프레드시트 생성
    # spreadsheet = client.create('Automation_Results')  # 'pytest Results'라는 이름으로 스프레드시트 생성

    # 스프레드시트 공유 설정 (이메일 추가하여 수정 권한 부여)
    spreadsheet.share('yspark@dotincorp.com', perm_type='user', role='writer')

    # 첫 번째 워크시트 선택
    worksheet = spreadsheet.get_worksheet(0)

    # 4. pandas 데이터프레임을 Google 스프레드시트에 기록
    # 헤더 추가
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

    print('데이터가 성공적으로 스프레드시트에 작성되었습니다.')
except HttpError as error:
    print(f"오류 발생: {error}")
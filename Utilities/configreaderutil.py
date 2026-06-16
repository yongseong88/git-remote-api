import filecmp
import json
import os
import pathlib
from configparser import ConfigParser

class Filereadutil():
    def readConfig(self, section, key):

        config = ConfigParser() #객체 생성
        config.read("/Users/park-yongseong/Documents/DCW_Automation/Config/config.ini") #ini 파일 읽어오기
        return config.get(section, key) #section과 key로 value 리턴

    def write_file(self, input_file_path, file_data):

        try:
            # file_data = self.read_file(input_file_path)

            if file_data is None:
                print("file_data가 없어요")
                return  # 읽기 실패 시 종료

            source_folder_path = os.path.dirname(input_file_path)  # '/Users/data' 폴더 경로
            file_name_with_ext = os.path.basename(input_file_path)  # 'doc.json' 파일 경로
            file_extension = os.path.splitext(file_name_with_ext)[1].lower() # 확장자 구분

            # 3. 임시 저장 경로 설정
            # 비교를 위해 원본 파일과 동일한 내용의 임시 파일을 생성할 경로
            # temp_file_path = os.path.join(source_folder_path, f".temp_{file_name_with_ext}")

            if file_extension == '.json':

                # 4. 임시 파일에 새 내용을 저장
                os.makedirs(source_folder_path, exist_ok=True)

                with open(input_file_path, 'w', encoding="utf-8") as file:
                    # 새로운 내용을 임시 파일에 JSON 형식으로 저장
                    json.dump(file_data, file, indent=4, ensure_ascii=False)

            else:
                print(f"⚠️ 쓰기 작업을 지원하지 않는 파일 형식입니다: {file_extension}")

        except FileNotFoundError:
            print(f"❌ 파일을 찾을 수 없습니다: {input_file_path}")

        except Exception as e:
            print(f"❌ 파일 쓰기 중 오류 발생: {e}")


    def read_file(self, file_path):
        # 파일 경로에서 확장자 추출 (예: "data.json" -> ".json")
        file_extension = os.path.splitext(file_path)[1].lower()

        try:

            if not os.path.exists(file_path):
                print(f"파일을 찾을 수 없습니다: {file_path}")
                return None

            if os.path.getsize(file_path) == 0:
                print(f"⚠️ 파일이 비어 있습니다: {file_path}")
                return [] if file_extension == '.json' else None  # JSON이면 빈 리스트 반환 등 대응

            with open(file_path, 'r', encoding="utf-8") as file:

                if file_extension == '.json':
                    # JSON 파일인 경우: json.load()를 사용하여 데이터 구조를 로드
                    data = json.load(file)
                    # print(f"✅ JSON 데이터 로드 완료: {file_path}")
                    return data
                    # data = json.load(file)
                    # # print("JSON 데이터:", data)
                    # return data

                elif file_extension == '.txt':
                    multiline_list = []

                    # TXT 파일인 경우: 파일의 내용을 문자열로 읽어옴
                    # data = file.read()
                    lines = file.readlines()
                    print(f"✅ 텍스트 파일 내용 로드 완료: {file_path}")

                    for line in lines:
                        multiline_list.append(line.strip())
                        # print(line.strip())

                    return multiline_list

                else:
                    print(f"⚠️ 지원하지 않는 파일 형식입니다: {file_extension}")
                    return None

        except FileNotFoundError:
            print(f"파일을 찾을 수 없습니다: {file_path}")
            return None

        except json.JSONDecodeError:
            print(f"JSON 디코딩 오류가 발생했습니다: {file_path}")
            return None

    def multi_line(self, lang):

        multiline_text_file = f"/Users/park-yongseong/Documents/DCW_Automation/Config/translations/{lang}_translations.txt"
        # multiline_text_file = "/Users/park-yongseong/Documents/DCW_Automation/Config/multiline.txt"

        multiline_list = []

        # 파일을 열고 파일 객체를 변수에 저장
        with open(multiline_text_file, 'r') as file:  # with 문을 사용하여 파일을 열고, 파일 객체를 file 변수에 저장. with 문을 사용하면 파일을 다 사용한 후 자동으로 닫힙니다.
            # lines = file.read()  # 파일 내용을 읽어오기
            lines = file.readlines()  # 파일 내용을 읽어옵니다

        for line in lines:
            multiline_list.append(line.strip())
            # print(line.strip())

        return multiline_list


    def read_filepath(self, root_dir, file_name):

        """

            현재 스크립트의 위치를 기준으로 절대 경로를 계산하여 반환합니다.

            (root_dir="Config", file_name="upload_file.json")

        """




        # 1. 현재 파일의 폴더 경로 (.../DCW_Automation/Utilities)

        # [디버깅 추가] 현재 작업 디렉토리를 찍어봅니다.
        # print(f"🔍 [Debug] 현재 작업 디렉토리(CWD): {os.getcwd()}")

        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = str(pathlib.Path(current_script_dir).parent)
        # print(f"🔍 [Debug] 스크립트 파일 위치: {current_script_dir}")

        # current_script_dir = pathlib.Path(__file__).resolve().parent

        full_file_path = os.path.join(base_dir, root_dir, file_name)

        # if not full_file_path.exists():
        #     # 로그를 남기거나 예외를 발생시켜 디버깅을 돕습니다.
        #     print(f"WARNING: 파일을 찾을 수 없습니다 -> {full_file_path}")

        return full_file_path

        # # 1. 현재 파일의 위치 (.../DCW_Automation/Utilities)
        # current_script_dir = os.path.dirname(os.path.abspath(__file__))
        #
        # # 2. 상위 폴더로 이동 (.../DCW_Automation)
        # base_dir_pathlib = pathlib.Path(current_script_dir)
        # base_dir_candidate = base_dir_pathlib.parent
        #
        # # 3. ⭐️ 수정 포인트: root_dir 안에 있는 슬래시를 분리해서 join하거나,
        # # root_dir 자체가 "Config/braille_info"인 경우 아래처럼 결합하는 게 가장 안전합니다.
        # full_file_path = os.path.join(base_dir_candidate, root_dir, file_name)
        #
        # # 4. 🚨 에러 확인을 위한 출력 (에러 시 이 경로를 확인해 보세요)
        # if not os.path.exists(full_file_path):
        #     print(f"\n[경로 에러] 파일을 찾을 수 없습니다!")
        #     print(f"찾으려 한 경로: {full_file_path}\n")
        #
        # return full_file_path



        # 예시: 유틸리티 파일이 Config 폴더에 있다면 base_dir은 상위 폴더입니다.
        # DCW_Automation/Config/upload_file.json 경로를 기준으로 가정하면:
        # 3. 인자로 받은 상대 경로를 base_dir과 결합합니다.
        # - root_dir: "Config"
        # - file_name: "upload_file.json"
        # 🚨 경로의 복잡성을 제거하기 위해 os.path.join을 사용합니다.

        # full_file_path = os.path.join(base_dir_candidate, root_dir, file_name)
        # return full_file_path
        # full_file_path = os.path.join(root_dir, current_folder, file_name)
        # return full_file_path


def multi_line(lang):

    multiline_text_file = "/Users/park-yongseong/Documents/DCW_Automation/Config/translations/"+lang+"_translations.txt"
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





# print("텍스트 파일 경로: {}".format(multiline_text_file))
# print(lines)  # 파일 내용을 출력
# print('-' * 10)  # 결과 사이 경계선
# for line in lines:  # readlines() 사용 할 경우
#     print(line.strip())  # 줄 끝의 개행 문자를 제거한 후 출력




import pymysql

# 데이터베이스 연결 설정
conn = pymysql.connect(
    host='python_mysql_mysql',  # 컨테이너 이름 또는 IP
    user='cocolabhub',
    password='cocolabhub',
    db='python_mysql',  # 데이터베이스 이름
)

def pose_problem():
    problem_type = input("문제 유형을 입력하세요. : ") # 4 지선다
    problem_count = input("문항 수를 입력하세요. : ")  # 5 문항
    
    Question_id = 1     # QUESTION_ID
    Choice_id = 1       # CHOICE_ID

    for i in range(int(problem_count)):
        # 문제 INSERT
        print("문제와 선택지를 입력하세요 : ")
        Question_title = input("문항{} : ".format(i+1))

        sql = "INSERT INTO QUESTION (QUESTION_ID, QUESTION_TITLE) VALUES (%s, %s)"
        cursor.execute(sql, (Question_id, Question_title))
        conn.commit()


        # 선택지 INSERT
        print("선택지 : ")
        Choice_num = 1
        for j in range(int(problem_type)):
            Choice_choice = input("{}. ".format(j+1))
        
            sql = "INSERT INTO CHOICE (CHOICE_ID, QUESTION_ID, CHOICE_CHOICE, CHOICE_NUM) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (Choice_id, Question_id, Choice_choice, Choice_num))
            conn.commit()
            
            Choice_id += 1       # CHOICE_ID
            Choice_num += 1


        Question_score = int(input("점수 : "))
        Question_answer = int(input("정답 : "))


        # 문제 점수 UPDATE
        sql = "UPDATE QUESTION SET QUESTION_SCORE = %s WHERE QUESTION_ID = %s"
        cursor.execute(sql, (Question_score, Question_id))
        conn.commit()

        # 선택지 정답 UPDATE
        sql = "UPDATE CHOICE SET CHOICE_CORRECT = %s WHERE QUESTION_ID = %s AND CHOICE_NUM = %s"
        cursor.execute(sql, ('정답', Question_id, Question_answer))
        conn.commit()

        Question_id += 1

def solving_problem():
    User_id = 1        # USER_ID
    Result_id = 1        # RESULT_ID

    while True:
        
        # 응시자 이름 INSERT
        User_name = input("응시자 이름을 입력하세요: ")
        
        sql = "INSERT INTO USER (USER_ID, USER_NAME) VALUES (%s, %s)"
        cursor.execute(sql, (User_id, User_name))
        conn.commit()

        # 문제 풀기
        print("문제를 풀어주세요:")

        # QUESTION_TITLE SELECT
        sql = "SELECT QUESTION_TITLE, QUESTION_ID FROM QUESTION"
        cursor.execute(sql)
        datas = cursor.fetchall()
        num_count_q = 1       # 문항 번호COUNT
        for data in datas:
            print("문항{}: {}".format(num_count_q, data[0]))
            Question_id = data[1]

            
            num_count_c = 1       # 선택지 번호 COUNT
            print("선택지: ")
            sql = "SELECT CHOICE_CHOICE FROM CHOICE WHERE QUESTION_ID = %s"
            cursor.execute(sql, (Question_id))
            choices = cursor.fetchall()
            for choice in choices:
                print("{}. {}".format(num_count_c, choice[0]))
                num_count_c += 1       # 선택지 번호 COUNT
            
            
            # 응시자 정답 입력 후 RESULT TABLE에 INSERT
            User_choice = input("답 :")
            sql = "INSERT INTO RESULT (RESULT_ID, USER_ID, QUESTION_ID, CHOICE_ID) VALUES (%s, (SELECT USER_ID FROM USER WHERE USER_ID = %s), %s, %s)"
            cursor.execute(sql, (Result_id, User_id, Question_id, User_choice))
            conn.commit()

            num_count_q += 1       # 문항 번호COUNT
            Result_id += 1        # RESULT_ID
        User_id += 1        # USER_ID
        
        # 계속 진행 여부
        user_end = input("다음 응시자가 있나요? (계속: c, 종료: x): ")
        # x 입력 시 break
        if user_end == 'x':
            break
            
def result():

    print("각 문항 정답 : ")
    sql = "SELECT CHOICE_NUM FROM CHOICE WHERE CHOICE_CORRECT = '정답' ORDER BY QUESTION_ID"
    cursor.execute(sql)
    choices = cursor.fetchall()
    for choice in choices:
        print("{} ".format(choice[0]))


    # 응시자별 채점 결과
    # RESULT테이블의 QUETSION_ID, CHOICE_ID
    # CHOICE 테이블의 QUETSION_ID, CHOICE_NUM 두개가 일치하는 것의
    # CHOICE_CORRECT가 '정답'이면 QUESTION테이블의 QUESTION_SCORE의 숫자를 SUM
    # '정답'이 아니라 NULL값이면 SUMx
    average = 0
    print("응시자별 채점 결과: ")
    sql = "SELECT USER.USER_NAME, USER.USER_ID, SUM(CASE WHEN CHOICE.CHOICE_CORRECT = '정답' THEN QUESTION.QUESTION_SCORE ELSE 0 END) AS TOTAL_SCORE FROM USER LEFT JOIN RESULT ON USER.USER_ID = RESULT.USER_ID LEFT JOIN CHOICE ON RESULT.QUESTION_ID = CHOICE.QUESTION_ID AND RESULT.CHOICE_ID = CHOICE.CHOICE_NUM LEFT JOIN QUESTION ON RESULT.QUESTION_ID = QUESTION.QUESTION_ID GROUP BY USER.USER_ID, USER.USER_NAME"
    cursor.execute(sql)
    users = cursor.fetchall()
    for user in users:
        print("{}: {}점".format(user[0], user[2]))
        average += user[2]

    print("과목 평균 점수: {}점".format(average//len(users)))



try:
    with conn.cursor() as cursor:

        # 문제 내기        
        # pose_problem()
        print("—--------------------------------------------------")

        # 문제 풀기
        # solving_problem()
        print("—--------------------------------------------------")

        # 채점 결과
        result()

        # # Delete
        # sql = "DELETE FROM TableName WHERE pk_id=%s"
        # cursor.execute(sql, (1,))
        # conn.commit()

finally:
    conn.close()

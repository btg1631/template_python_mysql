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
    
    Question_id = 1
    Choice_id = 1 

    for i in range(int(problem_type)):
    
        print("문제와 선택지를 입력하세요 : ")
        Question_title = input("문항{} : ".format(i+1))
        # 문제 INSERT
        sql = "INSERT INTO QUESTION (QUESTION_ID, QUESTION_TITLE) VALUES (%s, %s)"
        cursor.execute(sql, (Question_id, Question_title))
        conn.commit()

        print("선택지 : ")

        Choice_num = 1
        for j in range(int(problem_count)):
            Choice_choice = input("{}. ".format(j+1))
            # 선택지 INSERT
            sql = "INSERT INTO CHOICE (CHOICE_ID, QUESTION_ID, CHOICE_CHOICE, CHOICE_NUM) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (Choice_id, Question_id, Choice_choice, Choice_num))
            conn.commit()
            Choice_id += 1
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


try:
    with conn.cursor() as cursor:
        # 문제 내기        
        # pose_problem()

        User_id = 1
        # 응시자 문제풀기
        User_name = input("응시자 이름을 입력하세요: ")
        sql = "INSERT INTO USER (USER_ID, USER_NAME) VALUES (%s, %s)"
        cursor.execute(sql, (User_id, User_name))
        conn.commit()
        print("문제를 풀어주세요:")

        
        
        sql = "SELECT QUESTION_TITLE, QUESTION_ID FROM QUESTION"
        cursor.execute(sql)
        datas = cursor.fetchall()

        for i in range(len(datas)):
            for data in datas:
                print("문항{}: {}".format(i+1, data[0]))  # 각 행 출력
                Question_id = data[1]
                
                print("선택지: ")
                sql = "SELECT CHOICE_CHOICE FROM CHOICE WHERE QUESTION_ID = %s"
                cursor.execute(sql, (Question_id))
                choices = cursor.fetchall()

                for j in range(len(choices)):
                    for choice in choices:
                        print("{}. {}".format(j+1, choice[0]))  # 각 행 출력
                    input("답 :")


            User_id += 1


        # # Delete
        # sql = "DELETE FROM TableName WHERE pk_id=%s"
        # cursor.execute(sql, (1,))
        # conn.commit()



# # 종료 여부 입력 function
# def End(collection, collection1, collection2):           # hint collection 추가
#     user_end = 'q'           # hint
#     while True:
#         # c 입력 시 Todos() 다시 실행
#         if user_end == "c":
#             print("")
#             Todos(user_id, collection1, collection2)
#         # q 입력 시 User_name() 실행 후 Todos() 다시 실행
#         elif user_end == "q":
#             print("")
#             print("------------------------")
#             user_id = User_name(collection)
#             Todos(user_id, collection1, collection2)
#         # x 입력 시 프로그램 종료
#         else:
#             break

#         print("c, q, x 중 하나를 입력하세요.")
#         user_end = input("진행 여부: ")

#     print("------------------------")
#     print("프로그램이 종료되었습니다.")

finally:
    conn.close()

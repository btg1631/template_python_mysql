import pymysql

# 데이터베이스 연결 설정
conn = pymysql.connect(
    host='python_mysql_mysql',  # 컨테이너 이름 또는 IP
    user='cocolabhub',
    password='cocolabhub',
    db='python_mysql',  # 데이터베이스 이름
)

try:
    with conn.cursor() as cursor:

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

            # -----------------------------------------




finally:
    conn.close()

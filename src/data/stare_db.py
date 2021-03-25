import mysql.connector;

'''
Notice python convention상 시작 글자를 대문자로 시작하는게 일반적이지만, 우리는 C개발자 출신이 다수이기에 일반적인 C Convention에 따른다. 
'''
class stare_db():

    def __init__(self):
        # 클래스 외부 접근이 힘들도록 private 선언
        self.__dbconn = None
        self.__enable_cashing = False

    def is_connect(self):
        if self.__dbconn == None:
            return 0;
        return 1;

    def enable_cash(self):
        self.__enable_cashing = True

    def disable_cash(self):
        self.__enable_cashing = False

    def connect(self, **config):
        try:
            self.__dbconn = mysql.connector.connect(**config);
        except Exception as e:
            raise e

    # DATABASE 및 TABLE 생성 메소드
    def create(self, query):
        try:
            # 메모리에 버퍼 사용 (캐싱 기능)
            cursor = self.__dbconn.cursor(buffered=self.__enable_cashing)
            cursor.execute(query)
            self.dbconn.commit()
        except Exception as e:
            self.__dbconn.rollback()
            raise e
    # SELECT 함수
    def select(self, query):
        try:
            # 메모리에 버퍼 사용 (캐싱 기능)
            cursor = self.__dbconn.cursor(buffered=self.__enable_cashing)
            cursor.execute(query)
            resultlist = cursor.fetchall()
        except Exception as e:
            raise e
        return resultlist

    # insert, update, delete 용 메소드
    def execute(self, query, value):
        try:
            # 메모리에 버퍼 사용 (캐싱 기능)
            cursor = self.__dbconn.cursor(buffered=self.__enable_cashing)
            cursor.execute(query, value)
            self.__dbconn.commit()
        except Exception as e:
            self.__dbconn.rollback()
            raise e

    # insert, update, delete bulk 용 메소드 (DML)
    def bulk_execute(self, query, value):
        try:
            # 메모리에 버퍼 사용 (캐싱 기능)
            cursor = self.__dbconn.cursor(buffered=self.__enable_cashing)
            cursor.executemany(query, value)
            self.__dbconn.commit()
        except Exception as e:
            self.__dbconn.rollback()
            raise e

    # static method (select 용 메소드)
    @staticmethod
    def select_simple(query, **config):
        try:
            # 메모리에 버퍼 사용 (캐싱 기능)
            dbconn = mysql.connector.connect(**config);
            cursor = dbconn.cursor()
            cursor.execute(query)
            resultlist = cursor.fetchall()
        except Exception as e:
            raise e

        dbconn.close()
        return resultlist

    # static method (DML 용)
    @staticmethod
    def execute_simple(query, value, **config):
        try:
            dbconn = mysql.connector.connect(**config);
            cursor = dbconn.cursor()
            cursor.execute(query, value)
            dbconn.commit()
        except Exception as e:
            self.dbconn.rollback()
            raise e

        dbconn.close()
        return 0

    def __del__(self):
        self.__dbconn.close()

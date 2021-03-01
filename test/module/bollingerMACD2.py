#-*- coding: utf-8 -*-
import sys
sys.path.append("../")
from testInterface import testInterface

class bollingerMACD2(testInterface):
    def __init__(self, info):
        self.comment="볼린저 + MACD 전략 시험2\n매수 비율, 매도 비율 조정시험"
        #info에 포함
        self.stateDate=''
        self.endDate=''
        #기타 필요한 설정
        self.setUse()


    def load(self):
        print("해당 시점에 볼린저 / MACD 정보 로드")

    def calc(self):
        print("수익률 계산")


    def run(self):
        self.load()
        self.calc()
        print("bollinggerMACD2 완료")

if __name__ == "__main__":
    info = None
    bm1 = bollingerMACD2(info)
    bm1.run()


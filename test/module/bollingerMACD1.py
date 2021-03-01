#-*- coding: utf-8 -*-
import sys
sys.path.append("../")
from testInterface import testInterface

class bollingerMACD1(testInterface):
    def __init__(self, info):
        self.comment="볼린저 + MACD 전략 시험\n주 전략은 볼린저 신호 매수시점과 MACD 매수시점이 AND 되는 상황에서 매수 시도\n매도는 XXXX 시점에 매도"
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
        print("bollinggerMACD1 완료")

if __name__ == "__main__":
    info = None
    bm1 = bollingerMACD1(info)
    bm1.run()


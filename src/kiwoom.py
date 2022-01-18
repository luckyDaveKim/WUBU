import datetime
import sys
import time

from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *

TR_REQ_TIME_INTERVAL = 1


class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()


    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)

    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def _event_connect(self, err_code):
        if err_code == 0:
            print("connected")
        else:
            print("disconnected")

        self.login_event_loop.exit()

    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market)
        code_list = code_list.split(';')
        return code_list[:-1]

    def get_master_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    def get_master_listed_stock_cnt(self, code):
        stock_cnt = self.dynamicCall("GetMasterListedStockCnt(QString)", code)
        return stock_cnt

    def get_master_construction(self, code):
        return self.dynamicCall("GetMasterConstruction(QString)", code)

    def get_master_listed_stock_date(self, code):
        return self.dynamicCall("GetMasterListedStockDate(QString)", code)

    def get_master_stock_state(self, code):
        return self.dynamicCall("GetMasterStockState(QString)", code)

    def get_branch_code_name(self):
        return self.dynamicCall("GetBranchCodeName()")

    def get_future_list(self):
        return self.dynamicCall("GetFutureList()")

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        # ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString", code,
        #                        real_type, field_name, index, item_name)

        ret = self.dynamicCall("GetCommData(QString, QString, int, QString", code,
                               field_name, index, item_name)
        return ret.strip()

    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        print('화면번호 : {}'.format(screen_no))
        print('사용자 구분 : {}'.format(rqname))
        print('TR 이름 : {}'.format(trcode))
        print('레코드 이름 : {}'.format(record_name))

        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10080_req":
            self._opt10080(rqname, trcode)
        elif rqname == "opt10081_req":
            self._opt10081(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def _opt10080(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)

        for i in range(data_cnt):
            date = self._comm_get_data(trcode, "", rqname, i, "체결시간")
            date = datetime.datetime.strptime(date, '%Y%m%d%H%M%S')
            volume = self._comm_get_data(trcode, "", rqname, i, "거래량")
            open = self._comm_get_data(trcode, "", rqname, i, "시가")
            close = self._comm_get_data(trcode, "", rqname, i, "현재가")
            high = self._comm_get_data(trcode, "", rqname, i, "고가")
            low = self._comm_get_data(trcode, "", rqname, i, "저가")

            # if i == 0:
            #     webhook_url = 'https://hooks.slack.com/services/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'
            #     slack_data = json.dumps(
            #         {"blocks":
            #             [
            #                 {
            #                     "type": "section",
            #                     "text": {
            #                         "type": "mrkdwn",
            #                         "text": "체결시간 : " + str(date)
            #                     }
            #                 },
            #                 {
            #                     "type": "divider"
            #                 },
            #                 {
            #                     "type": "section",
            #                     "text": {
            #                         "type": "mrkdwn",
            #                         "text": f"*거래량* : {volume}\n*시가* : {open}\n*현재가* : {close}\n*고가* : {high}\n*저가* : {low}"
            #                     }
            #                 }
            #             ]
            #         }
            #     )
            #     response = requests.post(webhook_url, data=slack_data, headers={'Content-Type': 'application/json'})

            if (i == 0) or (i % 100) == 0:
                print('체결시간', '\t\t', '거래량', '\t\t', '시가', '\t\t', '현재가', '\t\t', '고가', '\t\t', '저가')
                print(date, '\t\t', volume, '\t\t', open, '\t\t', close, '\t\t', high, '\t\t', low)

            self._insert('005930', volume, close, open, high, low, date.strftime('%Y-%m-%d %H:%M:%S'))

    def _insert(self, stock_code, volume, cur_price, start_price, high_price, low_price, datetime):
        sql = "INSERT INTO stock_min_history (stock_code, volume, cur_price, start_price, high_price, low_price, datetime) VALUES ('{stock_code}', {volume}, {cur_price}, {start_price}, {high_price}, {low_price}, '{datetime}')"
        sql = sql.format(stock_code=stock_code, volume=volume, cur_price=cur_price, start_price=start_price, high_price=high_price, low_price=low_price, datetime=datetime)
        try:
            self.cur.execute(sql)
        except Exception as e:
            print(e)
            print(sql)
        self.conn.commit()


    def _opt10081(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)

        for i in range(data_cnt):
            transaction_price = self._comm_get_data(trcode, "", rqname, i, "거래대금")
            date = self._comm_get_data(trcode, "", rqname, i, "일자")
            date = datetime.datetime.strptime(date, '%Y%m%d')
            open = self._comm_get_data(trcode, "", rqname, i, "시가")
            high = self._comm_get_data(trcode, "", rqname, i, "고가")
            low = self._comm_get_data(trcode, "", rqname, i, "저가")
            close = self._comm_get_data(trcode, "", rqname, i, "현재가")
            volume = self._comm_get_data(trcode, "", rqname, i, "거래량")

            self._insert_day('005930', volume, transaction_price, close, open, high, low, date.strftime('%Y-%m-%d'))

    def _insert_day(self, market_code, volume, transaction_price, cur_price, start_price, high_price, low_price, date):
        sql = "INSERT INTO market_history_per_day (market_code, volume, transaction_price, cur_price, start_price, high_price, low_price, date) VALUES ('{market_code}', {volume}, {cur_price}, {start_price}, {high_price}, {low_price}, '{date}')"
        sql = sql.format(market_code=market_code, volume=volume, transaction_price=transaction_price, cur_price=cur_price, start_price=start_price, high_price=high_price, low_price=low_price, date=date)
        try:
            self.cur.execute(sql)
        except Exception as e:
            print(e)
            print(sql)
        self.conn.commit()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     kiwoom = Kiwoom()
#     kiwoom.comm_connect()
#
#     # opt10081 TR 요청
#     # kiwoom.set_input_value("종목코드", "039490")
#     # kiwoom.set_input_value("기준일자", "20170224")
#     # kiwoom.set_input_value("수정주가구분", 1)
#     # kiwoom.comm_rq_data("opt10081_req", "opt10081", 0, "0101")
#     #
#     # while kiwoom.remained_data == True:
#     #     print('요청')
#     #     time.sleep(TR_REQ_TIME_INTERVAL)
#     #     kiwoom.set_input_value("종목코드", "039490")
#     #     kiwoom.set_input_value("기준일자", "20170224")
#     #     kiwoom.set_input_value("수정주가구분", 1)
#     #     kiwoom.comm_rq_data("opt10081_req", "opt10081", 2, "0101")
#
#     # kiwoom.set_input_value("종목코드", "005930")
#     # kiwoom.set_input_value("틱범위", 1)
#     # kiwoom.set_input_value("수정주가구분", 1)
#     # kiwoom.comm_rq_data("opt10080_req", "opt10080", 0, "1999")
#     #
#     # while (kiwoom.remained_data == True):
#     #     print('==================요청=========================')
#     #     time.sleep(TR_REQ_TIME_INTERVAL)
#     #     kiwoom.set_input_value("종목코드", "005930")
#     #     kiwoom.set_input_value("틱범위", 1)
#     #     kiwoom.set_input_value("수정주가구분", 1)
#     #     kiwoom.comm_rq_data("opt10080_req", "opt10080", 2, "1999")
#
#     # print(kiwoom.get_code_list_by_market(''))
#     markets = kiwoom.get_code_list_by_market('')
#     for market in markets:
#         print(kiwoom.get_master_code_name(market))


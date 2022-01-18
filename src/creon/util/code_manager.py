from enum import Enum, auto

import win32com.client

from src.creon.result.result import Result


class CodeManager:
    def __init__(self):
        self.__client = win32com.client.Dispatch('CpUtil.CpCodeMgr')

    def code_to_name(self, code):
        value = self.__client.CodeToName(code)
        return Result(value, '주식/선물/옵션종목명')

    def get_stock_buy_margin_rate(self, code):
        value = self.__client.GetStockMarginRate(code)
        return Result(value, '주식 매수 증거금율')

    def get_stock_trading_count(self, code):
        value = self.__client.GetStockMemeMin(code)
        return Result(value, '주식 매매 거래단위 주식수')

    def get_stock_market_kind(self, code):
        value = self.__client.GetStockMarketKind(code)
        return MarketKindResult.of(value)


# class MarketKind(Enum):
#     NULL = Result(0, '구분없음')
#     KOSPI = Result(1, '거래소')
#     KOSDAQ = Result(2, '코스닥')
#     FREEBOARD = Result(3, 'K-OTC')
#     KRX = Result(4, 'KRX')
#     KONEX = Result(5, 'KONEX')
#
#     def __init__(self, result):
#         self.__result = result
#
#     @staticmethod
#     def of(value):
#         for marketKind in MarketKind:
#             if marketKind.value.get_value() == value:
#                 return marketKind
#
#     def get_value(self):
#         return self.value.get_value()
#
#     def get_description(self):
#         return self.value.get_description()


class EnumResult(Result, Enum):
    def __init__(self, result):
        super().__init__(result.get_value(), result.get_description())

    def _generate_next_value_(self, start, count, last_values):
        return self

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class MarketKindResult(EnumResult):
    NULL = Result(0, '구분없음')
    KOSPI = Result(1, '거래소')
    KOSDAQ = Result(2, '코스닥')
    FREEBOARD = Result(3, 'K-OTC')
    KRX = Result(4, 'KRX')
    KONEX = Result(5, 'KONEX')

    @staticmethod
    def of(value):
        for market_kind_result in MarketKindResult:
            if market_kind_result.value.get_value() == value:
                return market_kind_result

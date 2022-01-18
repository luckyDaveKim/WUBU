class Wallet:
    def __init__(self, money=0):
        self.__base_money = money
        self.__money = money
        self.__stock = 0

    def get_money(self):
        return self.__money

    def get_stock(self):
        return self.__stock

    def __buy(self, price, count=1):
        if self.__money < price * count:
            return False

        self.__money -= price * count
        self.__stock += count
        return True

    def buy(self, price, count=1):
        if self.__money < price * count:
            for i in reversed(range(int(count))):
                if self.__buy(price, i):
                    print(f"Can't buy; money:{self.__money}, price:{price}, stock:{i}")
                    return

        self.__money -= price * count
        self.__stock += count
        print(f"[BUY] ===> totalMoney:{self.__money + (self.__stock * price)}\n, price:{price}, stock:{count}")

    def __sell(self, price, count=1):
        if self.__stock <= 0:
            return False

        self.__money += price * count
        self.__stock -= count
        return True

    def sell(self, price, count=1):
        if self.__stock < count:
            for i in reversed(range(int(count))):
                if self.__sell(price, i):
                    return

        self.__money += price * count
        self.__stock -= count

        # if (self.__money + (self.__stock * price)) < self.__base_money:
        #     print(self.__money + (self.__stock * price))
        print(f"[SELL] ===> totalMoney:{self.__money + (self.__stock * price)}\n, price:{price}, stock:{count}")

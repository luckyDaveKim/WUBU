from src.creon.util.code_manager import CodeManager

codeManager = CodeManager()

result = codeManager.code_to_name('A005930')

print(result.get_value())
print(result.get_description())

print(codeManager.get_stock_market_kind('A005930'))
# 需求
写一个银行账户类，包含存款、取款、查询余额，要求考虑异常处理。

# 设计文档
## 设计文档
1. 包含 BankAccount 类。
2. 提供 deposit, withdraw, get_balance 方法。
3. 异常处理：取款金额大于余额时抛出 ValueError。

# 最终代码
```python
class BankAccount:
    def __init__(self):
        self.balance = 0
    def deposit(self, amount):
        self.balance += amount
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError('余额不足')
        self.balance -= amount
    def get_balance(self):
        return self.balance
```

# 审查意见
【PASS】
代码逻辑正确，异常处理完善，符合设计文档要求。

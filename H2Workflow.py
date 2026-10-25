import os, json, urllib.request, urllib.error

API_KEY = "mock_key_for_test"
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"

USE_MOCK = True


def call_llm(system_prompt, user_prompt):
    if USE_MOCK:
        if "需求分析师" in system_prompt:
            return "## 设计文档\n1. 包含 BankAccount 类。\n2. 提供 deposit, withdraw, get_balance 方法。\n3. 异常处理：取款金额大于余额时抛出 ValueError。"
        elif "开发工程师" in system_prompt:
            return "class BankAccount:\n    def __init__(self):\n        self.balance = 0\n    def deposit(self, amount):\n        self.balance += amount\n    def withdraw(self, amount):\n        if amount > self.balance:\n            raise ValueError('余额不足')\n        self.balance -= amount\n    def get_balance(self):\n        return self.balance"
        elif "审查员" in system_prompt:
            return "【PASS】\n代码逻辑正确，异常处理完善，符合设计文档要求。"
        else:
            return "【PASS】\n代码已按要求修复。"

    url = BASE_URL.rstrip("/") + "/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + API_KEY
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        return "Error: " + str(e)


class WorkflowState:
    def __init__(self, requirement):
        self.requirement = requirement
        self.design = ""
        self.code = ""
        self.review = ""
        self.passed = False


class RequirementAgent:
    def run(self, state):
        print(">>> [需求 Agent] 正在分析需求...")
        system_prompt = "你是一个资深需求分析师。请根据用户的初步需求，输出一份简洁的软件设计文档（包含功能点、接口定义）。"
        state.design = call_llm(system_prompt, state.requirement)
        print(">>> [需求 Agent] 设计文档生成完毕。\n")


class CodingAgent:
    def run(self, state):
        print(">>> [编码 Agent] 正在根据设计编写代码...")
        system_prompt = "你是一个高级 Python 开发工程师。请根据设计文档编写 Python 代码，只输出代码，不要包含任何解释文字。"
        state.code = call_llm(system_prompt, state.design)
        print(">>> [编码 Agent] 代码编写完毕。\n")


class ReviewAgent:
    def run(self, state):
        print(">>> [审查 Agent] 正在审查代码...")
        system_prompt = "你是一个严格的代码审查员。如果代码有严重问题，请第一行输出【FAIL】，并给出原因。如果代码没问题，第一行输出【PASS】。"
        state.review = call_llm(system_prompt, state.code)
        
        if "【PASS】" in state.review:
            state.passed = True
            print(">>> [审查 Agent] 审查通过！\n")
        else:
            state.passed = False
            print(">>> [审查 Agent] 审查未通过，需要修复。原因：" + state.review[:50] + "...\n")


class WorkflowEngine:
    def __init__(self):
        self.req_agent = RequirementAgent()
        self.coding_agent = CodingAgent()
        self.review_agent = ReviewAgent()

    def run(self, requirement):
        print("=" * 40)
        print("Workflow 开始执行")
        print("=" * 40)
        
        state = WorkflowState(requirement)
        
        self.req_agent.run(state)
        self.coding_agent.run(state)
        
        max_retries = 2
        for attempt in range(max_retries):
            self.review_agent.run(state)
            if state.passed:
                break
            else:
                print(">>> [系统] 触发条件分支：要求编码 Agent 修复代码...")
                state.code = call_llm("你是一个高级 Python 开发工程师。请修复代码中的问题，只输出代码。", state.review)
        
        print("=" * 40)
        print("Workflow 执行结束")
        print("=" * 40)
        
        project_dir = os.path.dirname(os.path.abspath(__file__))
        out_path = os.path.join(project_dir, "final_output.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("# 需求\n" + state.requirement + "\n\n")
            f.write("# 设计文档\n" + state.design + "\n\n")
            f.write("# 最终代码\n```python\n" + state.code + "\n```\n\n")
            f.write("# 审查意见\n" + state.review + "\n")
        print("结果已保存到 " + out_path)


if __name__ == "__main__":
    engine = WorkflowEngine()
    engine.run("写一个银行账户类，包含存款、取款、查询余额，要求考虑异常处理。")
from zhipuai import ZhipuAI


class AgentZhipuAI:
    def __init__(self, client =ZhipuAI(api_key="a8f63606c4dd11d501aa6ffee9be16d6.icUQlh0I0DFFaD7s") , model_name="glm-4",system_info = ""):
        self.client = client  # 可以使用你自己key定义的chient
        self.model_name = model_name
        if system_info == "":
            self.history = []
        else:
            self.history = [{"role": "system", "content": system_info}]


    def __call__(self, prompt="", role="user") -> str:
        """_call"""
        # construct query
        prompt_json = {
            "role": role,
            "content": prompt
        }
        self.history.append(prompt_json)
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=self.history,
        )
        # 直接获取 message 字段，这里假设它是一个 CompletionMessage 实例
        choices = response.choices[0].message

        # 直接访问属性而不是作为字典键
        response_content = choices.content
        response_role = choices.role
        tool_calls = choices.tool_calls

        response_json = {
            "role": response_role,
            "content": response_content
        }
        self.history.append(response_json)

        return response_content


if __name__ == '__main__':
    llm = AgentZhipuAI()

    response = llm("你好")
    print(response)

    response = llm("南京是哪里的省会")
    print(response)

    response = llm("那里有什么好玩的地方")
    print(response)

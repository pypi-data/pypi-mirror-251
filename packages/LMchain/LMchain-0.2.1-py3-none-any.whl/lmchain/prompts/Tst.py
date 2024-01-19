class PromptTemplate:
    def __init__(self, input_variables, template):
        self.input_variables = input_variables
        self.template = template

    def format(self, **kwargs):
        # 确保所有输入变量都有对应的值
        for var in self.input_variables:
            if var not in kwargs:
                raise ValueError(f"Missing input variable: {var}")

        # 使用提供的值填充模板
        filled_template = self.template.format(**kwargs)
        return filled_template




if __name__ == '__main__':
    prompt = PromptTemplate(
        input_variables=["location", "obj"],
        template="请问{location}有什么{obj}的地方"
    )

    # 使用关键字参数调用 format 方法
    new_prompt = prompt.format(location="南京", obj="好玩")
    print(new_prompt)

    # 使用字典解包的方式调用 format 方法
    params = {"location": "南京", "obj": "好吃"}
    new_prompt = prompt.format(params)
    print(new_prompt)
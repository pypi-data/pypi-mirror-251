
class SubQuestChain:
    def __init__(self, llm):
        self.llm = llm

    def __call__(self, query=""):
        if query == "":
            raise "query需要填入查询问题"

        decomp_template = """
            用中文回答下面问题：
            You are a domain expert. Your task is to break down a complex question into simpler sub-parts.

            USER QUESTION
            {user_question}

            ANSWER FORMAT
            ["sub-questions_1","sub-questions_2","sub-questions_3",...]
            """

        from lmchain.prompts import PromptTemplate
        prompt = PromptTemplate(
            input_variables=["user_question"],
            template=decomp_template,
        )

        from lmchain.chains import LLMChain
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run({"user_question": query})

        return response

    def run(self, query):
        sub_list = self.__call__(query)
        return sub_list


if __name__ == '__main__':
    from lmchain.agents import llmMultiAgent

    llm = llmMultiAgent.AgentZhipuAI()
    subQC = SubQuestChain(llm)
    response = subQC.run(query="工商银行财报中，2024财年Q1与Q2 之间，利润增长了多少？")
    print(response)
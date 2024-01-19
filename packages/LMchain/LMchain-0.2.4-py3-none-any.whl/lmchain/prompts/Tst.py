from zhipuai import ZhipuAI


client = ZhipuAI(api_key="a8f63606c4dd11d501aa6ffee9be16d6.icUQlh0I0DFFaD7s") # 填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4v",  # 填写需要调用的模型名称
    messages=[
       {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "图里有什么"
          },
          {
            "type": "image_url",
            "image_url": {
                "url" : "https://k.sinaimg.cn/n/sinacn/w660h956/20180312/4502-fyscsmu6088133.jpg/w700d1q75cms.jpg"
            }
          }
        ]
      }
    ]
)
print(response.choices[0].message.content)
#
# api_key="a8f63606c4dd11d501aa6ffee9be16d6.icUQlh0I0DFFaD7s"
# from zhipuai import ZhipuAI
#
# client = ZhipuAI(api_key=api_key)  # 请填写您自己的APIKey
#
# response = client.images.generations(
#     model="cogview",  # 填写需要调用的模型名称
#     prompt="一只可爱的小猫咪",
# )
# print(response.data[0].url)


import requests
from PIL import Image
from io import BytesIO

# 在线图像的URL
url = "https://sfile.chatglm.cn/testpath/684abfb2-cc94-5aed-b6dd-5ae8f43b4c7a_0.png"

# 发送HTTP请求获取图像数据
response = requests.get(url)
response.raise_for_status()  # 确保请求成功

# 使用PIL来打开并显示图像
image = Image.open(BytesIO(response.content))
import numpy as np
_image = np.array(image)
print(_image.shape)
image.show()
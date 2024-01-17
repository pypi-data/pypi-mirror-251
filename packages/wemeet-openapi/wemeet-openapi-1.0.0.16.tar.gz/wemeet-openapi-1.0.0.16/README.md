# 简介
欢迎使用腾讯会议开发者工具套件（SDK）1.1.0，为方便 Python 开发者调试和接入腾讯云会议 API，这里向您介绍适用于 Python 的腾讯会议开发工具包，并提供首次使用开发工具包的简单示例。让您快速获取腾讯会议 Python SDK 并开始调用。
# 依赖环境
1. 依赖环境：Python 3.7 版本及以上。
2. 购买腾讯会议企业版获取 SecretID、SecretKey，接入的企业 AppId。

# 获取安装
在第一次使用云API之前，用户首先需要在腾讯云控制台上申请安全凭证，安全凭证包括 SecretID 和 SecretKey，SecretID 是用于标识 API 调用者的身份，SecretKey 是用于加密签名字符串和服务器端验证签名字符串的密钥 SecretKey 必须严格保管，避免泄露。

## 通过源码包安装
1. 前往 [Github 代码托管地址](https://git.code.tencent.com/open_sdk/openapi-sdk-python) 下载源码压缩包；
2. 解压源码包到您项目合适的位置；
3. 引用方法可参考示例。

# 示例

以创建会议接口为例：
```Python
import random
import time

import wemeet_openapi

# crete_meeting_demo 创建会议请求demo
def crete_meeting_demo():

    # 1.构造 client 客户端(jwt 鉴权需要配置 appId sdkId secretID 和 secretKey)
    client = wemeet_openapi.Client(app_id="2****46", sdk_id="2****50",
                                   secret_id="Zk*****J8h",
                                   secret_key="Y2z*****WRsVksn")

    # 2.构造请求体
    request = wemeet_openapi.ApiV1MeetingsPostRequest(
        body=wemeet_openapi.V1MeetingsPostRequest(
            instanceid=2,
            meeting_type=0,
            subject="测试会议",
            type=1,
            userid="userid",
            start_time="1651334400",
            end_time="1651377600"
        )
    )

    # 3.构造 JWT 鉴权器
    authenticator_builder = wemeet_openapi.JWTAuthenticator(
        nonce=random.randrange(0, 2 ** 64),
        timestamp=str(int(time.time()))
    ).options_build()

    # 4.发送对应的请求
    try:
        response = client.meetings_api.v1_meetings_post(
            request=request,
            authenticator_options=[authenticator_builder])

        print(f"Response from `MeetingsApi.V1MeetingsPost`: {vars(response)}\n")
    except wemeet_openapi.ClientException as e:
        print(f"Error when calling `MeetingsApi.V1MeetingsPost`: {e}\n")

    except wemeet_openapi.ServiceException as svrErr:
        print(f"Error when calling `MeetingsApi.V1MeetingsPost`: {svrErr}\n")
        print(f"Full HTTP response: {str(svrErr.api_resp.raw_body)}\n")


# 调用入口点函数
if __name__ == "__main__":
    crete_meeting_demo()
```

# WechatSpider
<<<<<<< HEAD
api结构基本按照spiderapi文档完成，但是由于公众号特性，在获取文章内容的api上，参数设置为url和username（这两个参数都可以从上一步获取文章列表中得到）
```shell
python -m uvicorn main:wechatCreeper --reload --port 8001
```
=======
api结构基本按照spiderapi文档完成，但是由于公众号特性，在获取文章内容的api上，参数设置为url和username（这两个参数都可以从上一步获取文章列表中得到），文章列表不得不返回url（公众号的文章url拼不出来）
现在有test.http了
>>>>>>> 75cb1fa790e063837d3d0e804e5c1eb2dd2942f3

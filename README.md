# WechatSpider

api结构基本按照spiderapi文档完成，但是由于公众号特性，在获取文章内容的api上，参数设置为url和username（这两个参数都可以从上一步获取文章列表中得到）
```shell
python -m uvicorn main:wechatCreeper --reload --port 8001
```


# WechatSpider
api结构基本按照spiderapi文档完成，但是由于公众号特性，在获取文章内容的api上，参数设置为url和username（这两个参数都可以从上一步获取文章列表中得到），文章列表不得不返回url（公众号的文章url拼不出来）
现在有test.http了
get /api/search/author/｛username｝
查询微信公众号
返回：
{
    “ret”：{
        "username":"公众号名称"
        "id":"fakeid"
}

}
get /api/passage/{username}/{page}
查询文章列表
返回:
{
    "ret":
[
        {
        "aid":"文章id"
        "title":"标题"
        "url":"推文url"
        "create_time"："发布时间"
        "time_stamp":"时间戳"
  


}
]
}
get /api/passage/{username}/{id}
{

   "ret":{
    passage
}




}

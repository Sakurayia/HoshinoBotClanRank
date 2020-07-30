# HoshinoBotClanRank

一个用来查询会战排名以及定时播报排名的 [HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot) 插件，适配V2

A plugin for [HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot) that can search PCR clan rank and automatically broadcast your favored clan's rank per hour.

## 插件介绍

本插件基于HoshinoBot V2，需搭配机器人本体使用。用户可在群内通过指令查询公会会战排名，以及设置定时推送来每小时自动获取关注的公会排名。

## 数据来源

本插件数据来源 [镜华 - 公会战排名查询](https://kengxxiao.github.io/Kyouka/) ，**请不要滥用该插件给原作者带来困扰**！

## 指令介绍

本插件分为两个模块：clanrank及clanrank-reminder

+ *clanrank* 会战查询
  + **查询排名**：通过机器人后台查询指定名次的公会信息
  + **查询公会**：通过机器人后台查询指定公会名称的公会信息，通过正则表达式匹配，可能返回多个结果，其中数据量大于5时返回简版结果
  + **查询会长**：通过机器人后台查询指定会长名称的公会信息，通过正则表达式匹配，可能返回多个结果，其中数据量大于5时返回简版结果
  + **查询分数**：通过机器人后台查询指定分数的公会信息 (~~不过接口似乎有问题~~)
  + **查询档线**：通过机器人后台查询最新各档分数情况
+ *clanrank-reminder* 会战推送  **※本功能默认关闭，如需启用请手动开启**
  + **关注公会**：向后台数据库插入待查询的公会名称，之后会在每小时指定时间查询本群关注的所有公会的排名情况
  + **删除关注**：从后台数据库删除关注的公会，不再定时推送该公会信息
  + **更新关注**：从后台数据库更新关注的公会
  + **查看关注**：查看本群关注的所有公会

## 使用方式

1. clone或download zip
2. 将clanrank文件夹放入`hoshino/modules/`文件夹中
3. 在`query.py`文件的55行设置自定义`Custom-Source`
4. 在`__bot__.py`文件的`MODULES_ON`中添加`'clanrank'`

## 更新日志

`v1.3`

+ 查询公会信息时新增进度显示
+ 定时推送中新增排名和分数变化显示
+ 更改了数据库结构

`v1.2`

+ 新增Custom-Source请求头

`v1.1`

+ 更改了部分触发指令及回复内容

`v1.0`

+ 初版发布


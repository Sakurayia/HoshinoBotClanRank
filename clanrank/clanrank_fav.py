import random

import hoshino
from hoshino import Service, priv
from hoshino.util import FreqLimiter

from .clanfavdb import ClanFav
from . import query

sv_help = '''
[关注公会] 接公会名称 每小时自动推送该公会排名
[删除关注] 接公会名称 删除关注的该公会
[更新关注] 接待更新公会名称 新公会名称
[查看关注] 查看当前群关注的公会
'''.strip()
svfav = Service('clanrank-reminder', enable_on_default=False, bundle='pcr排名', help_=sv_help)

lmt = FreqLimiter(10)


@svfav.scheduled_job('cron', minute='15')  # 可在此修改定时播报的方式
async def rank_poller():
    bot = hoshino.get_bot()
    await send_rank(bot)


async def get_rank(list):
    msg = ""
    for item in list:
        name = item[0]
        # 执行查询
        svfav.logger.info('Doing query...')
        res = await query.do_query(0, name, 2)
        svfav.logger.info('Got response!')

        # 处理查询结果
        if res is None:
            msg = "\n".join([
                msg,
                f"=={name}==\n查询出错"
            ])
            continue
        if not len(res[0]):
            msg = "\n".join([
                msg,
                f"=={name}==\n没有查询到相关结果"
            ])
            continue
        data = res[0]
        data = data[:1]  # 仅保留第一条记录
        ts = res[1]

        details = ["\n".join([
            f"=={e['clan_name']}==",
            f"公会排名：{e['rank']}",
            f"公会伤害：{e['damage']}",
            f"公会会长：{e['leader_name']}",
            f"公会人数：{e['member_num']}"
        ]) for e in data]

        msg = "\n".join([
            msg,
            details[0],
        ])
    return msg, ts


async def send_rank(bot):
    glist = await svfav.get_enable_groups()
    db = ClanFav()
    for gid, selfids in glist.items():
        try:
            name_list = db._find(int(gid))
            if len(name_list) == 0:
                continue
            res = await get_rank(name_list)
            message = res[0]
            ts = res[1]
            msg = "\n".join([
                f'自动查询：{query.calculate_ts(ts)}',
                message,
                '※数据来源：kengxxiao.github.io'
            ])
            await bot.send_group_msg(self_id=random.choice(selfids), group_id=gid, message=msg)
            svfav.logger.info(f"群{gid} 自动推送成功")
        except Exception as e:
            svfav.logger.error(f"群{gid} 自动推送失败：{type(e)}")
            svfav.logger.exception(e)


@svfav.on_prefix(('关注公会', '收藏公会'))
async def add_fav(bot, ev):
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.finish(ev, '抱歉，只有管理员才能使用该指令~', at_sender=True)

    # 处理输入数据
    name = ev.message.extract_plain_text()
    if len(name) == 0:
        await bot.finish(ev, "请发送'关注公会+公会名称'进行关注，无需+号", at_sender=True)

    try:
        db = ClanFav()
        gid = int(ev.group_id)
        all_record = db._find(gid)
        if len(all_record) >= 5:
            await bot.finish(ev, "已经关注5个工会啦，请删除部分关注后再添加~", at_sender=True)
        record = db._find_by_name(gid, name)
        if record:
            await bot.finish(ev, "该记录已经存在了哦~", at_sender=True)

        if db._insert(gid, name):
            await bot.send(ev, "关注成功！", at_sender=True)
    except:
        await bot.send(ev, "关注失败，请联系维护组或稍后再试", at_sender=True)


@svfav.on_prefix(('删除关注', '删除收藏'))
async def delete_fav(bot, ev):
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.finish(ev, '抱歉，只有管理员才能使用该指令~', at_sender=True)

    # 处理输入数据
    name = ev.message.extract_plain_text()
    if len(name) == 0:
        await bot.finish(ev, "请发送'删除关注+公会名称'进行删除，无需+号", at_sender=True)

    try:
        db = ClanFav()
        gid = int(ev.group_id)
        record = db._find_by_name(gid, name)
        if not record:
            await bot.finish(ev, "未找到该记录哦~", at_sender=True)

        if db._delete(gid, name):
            await bot.send(ev, "删除成功！", at_sender=True)
    except:
        await bot.send(ev, "删除失败，请联系维护组或稍后再试", at_sender=True)


@svfav.on_prefix(('更新关注', '更新收藏'))
async def delete_fav(bot, ev):
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.finish(ev, '抱歉，只有管理员才能使用该指令~', at_sender=True)

    # 处理输入数据
    msg = ev.message.extract_plain_text().split()
    if len(msg) != 2:
        await bot.finish(ev, "请发送'更新关注+待更新名称+更新名称'进行更新，无需+号", at_sender=True)

    prename = msg[0]
    name = msg[1]

    try:
        db = ClanFav()
        gid = int(ev.group_id)
        record = db._find_by_name(gid, prename)
        if not record:
            await bot.finish(ev, "未找到该记录哦~", at_sender=True)

        if db._update(gid, name, prename):
            await bot.send(ev, "更新成功！", at_sender=True)
    except:
        await bot.send(ev, "更新失败，请联系维护组或稍后再试", at_sender=True)


@svfav.on_fullmatch(('查看关注', '查询关注', '查看收藏', '查询收藏'))
async def query_fav(bot, ev):
    uid = ev.user_id

    if not lmt.check(uid):
        await bot.finish(ev, '您查询得过于频繁，请稍等片刻~', at_sender=True)

    lmt.start_cd(uid)

    try:
        db = ClanFav()
        gid = int(ev.group_id)
        record = db._find(gid)
        if len(record) == 0:
            await bot.finish(ev, "暂无关注记录哦~快去添加吧！", at_sender=True)

        details = [" ".join([
            f"{e[0]}",
        ]) for e in record]

        msg = "\n".join([
            f"群{gid}关注公会一览：",
            *details
        ])

        await bot.send(ev, msg, at_sender=True)
    except:
        await bot.send(ev, "查询失败，请联系维护组或稍后再试", at_sender=True)


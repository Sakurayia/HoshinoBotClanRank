from hoshino import Service
from hoshino.util import FreqLimiter

sv_help = '''
[查询排名] 接排名 查询最新该排名公会
[查询公会] 接公会名称 查询最新该公会
[查询会长] 接会长名称 查询最新该会长公会
[查询分数] 接分数 查询最新该分数公会
[查询档线] 查询最新各档线分数
'''.strip()
sv = Service('clanrank', enable_on_default=True, bundle='pcr排名', help_=sv_help)

from . import query

lmt = FreqLimiter(10)


@sv.on_prefix(('查询公会', '公会查询'))
async def name_query(bot, ev):
    uid = ev.user_id

    if not lmt.check(uid):
        await bot.finish(ev, '您查询得过于频繁，请稍等片刻', at_sender=True)

    # 处理输入数据
    name = ev.message.extract_plain_text()
    if len(name) == 0:
        await bot.finish(ev, "请发送'查询排名+行会名称'进行查询，无需+号", at_sender=True)

    lmt.start_cd(uid)

    # 执行查询
    sv.logger.info('Doing query...')
    res = await query.do_query(0, name, 2)
    sv.logger.info('Got response!')

    # 处理查询结果
    if res is None:
        await bot.finish(ev, '查询出错，请联系维护组调教\n请先移步kengxxiao.github.io进行查询', at_sender=True)
    if not len(res[0]):
        await bot.finish(ev, '抱歉没有查询到相关结果', at_sender=True)
    data = res[0]
    data = data[:min(20, len(data))]
    ts = res[1]

    if len(data) > 5:
        details = [" ".join([
            f"{e['clan_name']}：{e['rank']}"
        ]) for e in data]
    else:
        details = ["\n".join([
            f"公会名称：{e['clan_name']}",
            f"公会排名：{e['rank']}",
            f"公会伤害：{e['damage']}",
            f"公会会长：{e['leader_name']}",
            f"公会人数：{e['member_num']}",
            f"----------"
        ]) for e in data]

    msg = [
        f'更新时间：{query.calculate_ts(ts)}',
        f'----------',
        *details,
        '※数据来源：kengxxiao.github.io'
    ]

    sv.logger.debug('Rank sending result...')
    await bot.send(ev, '\n'.join(msg))
    sv.logger.debug('Rank result sent!')


@sv.on_prefix(('查询会长', '会长查询'))
async def leader_query(bot, ev):
    uid = ev.user_id

    if not lmt.check(uid):
        await bot.finish(ev, '您查询得过于频繁，请稍等片刻', at_sender=True)

    # 处理输入数据
    name = ev.message.extract_plain_text()
    if len(name) == 0:
        await bot.finish(ev, "请发送'查询会长+会长名称'进行查询，无需+号", at_sender=True)

    lmt.start_cd(uid)

    # 执行查询
    sv.logger.info('Doing query...')
    res = await query.do_query(0, name, 3)
    sv.logger.info('Got response!')

    # 处理查询结果
    if res is None:
        await bot.finish(ev, '查询出错，请联系维护组调教\n请先移步kengxxiao.github.io进行查询', at_sender=True)
    if not len(res[0]):
        await bot.finish(ev, '抱歉没有查询到相关结果', at_sender=True)
    data = res[0]
    data = data[:min(20, len(data))]
    ts = res[1]

    if len(data) > 5:
        details = [" ".join([
            f"{e['clan_name']}：{e['rank']}"
        ]) for e in data]
    else:
        details = ["\n".join([
            f"公会会长：{e['leader_name']}",
            f"公会名称：{e['clan_name']}",
            f"公会排名：{e['rank']}",
            f"公会伤害：{e['damage']}",
            f"公会人数：{e['member_num']}",
            f"----------"
        ]) for e in data]

    msg = [
        f'更新时间：{query.calculate_ts(ts)}',
        f'----------',
        *details,
        '※数据来源：kengxxiao.github.io'
    ]

    sv.logger.debug('Rank sending result...')
    await bot.send(ev, '\n'.join(msg))
    sv.logger.debug('Rank result sent!')


@sv.on_prefix(('查询排名', '排名查询'))
async def rank_query(bot, ev):
    uid = ev.user_id

    if not lmt.check(uid):
        await bot.finish(ev, '您查询得过于频繁，请稍等片刻', at_sender=True)

    # 处理输入数据
    rank = ev.message.extract_plain_text()
    if len(rank) == 0:
        await bot.finish(ev, "请发送'查询排名+排名'进行查询，无需+号", at_sender=True)
    rank = int(rank)

    lmt.start_cd(uid)

    # 执行查询
    sv.logger.info('Doing query...')
    res = await query.do_query(rank, "", 1)
    sv.logger.info('Got response!')

    # 处理查询结果
    if res is None:
        await bot.finish(ev, '查询出错，请联系维护组调教\n请先移步kengxxiao.github.io进行查询', at_sender=True)
    if not len(res[0]):
        await bot.finish(ev, '抱歉没有查询到相关结果', at_sender=True)
    data = res[0]
    data = data[:min(20, len(data))]
    ts = res[1]

    details = ["\n".join([
        f"公会会长：{e['leader_name']}",
        f"公会名称：{e['clan_name']}",
        f"公会排名：{e['rank']}",
        f"公会伤害：{e['damage']}",
        f"公会人数：{e['member_num']}",
        f"----------"
    ]) for e in data]

    msg = [
        f'更新时间：{query.calculate_ts(ts)}',
        f'----------',
        *details,
        '※数据来源：kengxxiao.github.io'
    ]

    sv.logger.debug('Rank sending result...')
    await bot.send(ev, '\n'.join(msg))
    sv.logger.debug('Rank result sent!')


@sv.on_prefix(('查询分数', '分数查询'))
async def score_query(bot, ev):
    uid = ev.user_id

    if not lmt.check(uid):
        await bot.finish(ev, '您查询得过于频繁，请稍等片刻', at_sender=True)

    # 处理输入数据
    rank = ev.message.extract_plain_text()
    if len(rank) == 0:
        await bot.finish(ev, "请发送'查询分数+分数'进行查询，无需+号", at_sender=True)
    rank = int(rank)

    lmt.start_cd(uid)

    # 执行查询
    sv.logger.info('Doing query...')
    res = await query.do_query(rank, "", 4)
    sv.logger.info('Got response!')

    # 处理查询结果
    if res is None:
        await bot.finish(ev, '查询出错，请联系维护组调教\n请先移步kengxxiao.github.io进行查询', at_sender=True)
    if not len(res[0]):
        await bot.finish(ev, '抱歉没有查询到相关结果', at_sender=True)
    data = res[0]
    data = data[:min(20, len(data))]
    ts = res[1]

    details = ["\n".join([
        f"公会会长：{e['leader_name']}",
        f"公会名称：{e['clan_name']}",
        f"公会排名：{e['rank']}",
        f"公会伤害：{e['damage']}",
        f"公会人数：{e['member_num']}",
        f"----------"
    ]) for e in data]

    msg = [
        f'更新时间：{query.calculate_ts(ts)}',
        f'----------',
        *details,
        '※数据来源：kengxxiao.github.io'
    ]

    sv.logger.debug('Rank sending result...')
    await bot.send(ev, '\n'.join(msg))
    sv.logger.debug('Rank result sent!')


@sv.on_fullmatch(('查询档线', '档线查询'))
async def line_query(bot, ev):
    uid = ev.user_id

    if not lmt.check(uid):
        await bot.finish(ev, '您查询得过于频繁，请稍等片刻', at_sender=True)

    lmt.start_cd(uid)

    # 执行查询
    sv.logger.info('Doing query...')
    res = await query.do_query(0, "", 5)
    sv.logger.info('Got response!')

    # 处理查询结果
    if res is None:
        await bot.finish(ev, '查询出错，请联系维护组调教\n请先移步kengxxiao.github.io进行查询', at_sender=True)
    if not len(res[0]):
        await bot.finish(ev, '抱歉没有查询到相关结果', at_sender=True)
    data = res[0]
    ts = res[1]

    details = [" ".join([
        f"{e['rank']}：{e['damage']}",
    ]) for e in data]

    msg = [
        f'更新时间：{query.calculate_ts(ts)}',
        f'----------',
        f'排名：分数',
        f'----------',
        *details,
        '※数据来源：kengxxiao.github.io'
    ]

    sv.logger.debug('Rank sending result...')
    await bot.send(ev, '\n'.join(msg))
    sv.logger.debug('Rank result sent!')

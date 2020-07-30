import time

from hoshino import aiorequests, config, util

from .clanrank import sv

try:
    import ujson as json
except:
    import json

logger = sv.logger

async def do_query(rank, name, mode):
    apiUrl = "https://service-kjcbcnmw-1254119946.gz.apigw.tencentcs.com/"

    # 查询排名
    if mode == 1:
        payload = {
            "history": 0
        }
        url = apiUrl + "/rank/" + str(rank)
    # 查询分数
    elif mode == 4:
        payload = {
            "history": 0
        }
        url = apiUrl + "/score/" + str(rank)
    # 查询公会
    elif mode == 2:
        payload = {
            "history": 0,
            "clanName": name
        }
        url = apiUrl + "/name/" + "0"
    # 查询会长
    elif mode == 3:
        payload = {
            "history": 0,
            "leaderName": name
        }
        url = apiUrl + "/leader/" + "0"
    # 查询档线
    elif mode == 5:
        payload = {
            "history": 0
        }
        url = apiUrl + "/line"
    else:
        return None

    headers = {
        "Content-Type": "application/json",
        "Origin": 'https://kengxxiao.github.io',
        "Referer": 'https://kengxxiao.github.io/Kyouka/',
        "Custom-Source": ""  #请设置一个自定义的Custom-Source头来标识来源，且不要将其设置为KyoukaOfficial以和直接请求区分。
    }
    logger.debug(f'Rank query {payload=}')
    try:
        resp = await aiorequests.post(url, headers=headers, json=payload, timeout=10)
        res = await resp.json()
        logger.debug(f'len(res)={len(res)}')
    except Exception as e:
        logger.exception(e)
        return None

    if res['code']:
        logger.error(f"Rank query failed.\nResponse={res}\nPayload={payload}")
        return None

    return res['data'], res['ts']

def calculate_ts(ts):
    querytime = time.localtime(ts)
    formaltime = time.strftime("%Y-%m-%d %H:%M", querytime)
    return formaltime




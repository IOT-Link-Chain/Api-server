import requests
import config
import math
import json


def get_logo(name):
    cache_fix = 5

    if name == "ILC":
        return f"https://api.iotlinkchain.com/static/logo/iotlink.svg?{cache_fix}"

    elif name == "ARTL":
        return f"https://api.iotlinkchain.com/static/logo/artl.svg?{cache_fix}"

    elif name == "CCA":
        return f"https://api.iotlinkchain.com/static/logo/cca.svg?{cache_fix}"

    elif name == "MEC":
        return f"https://api.iotlinkchain.com/static/logo/mec.svg?{cache_fix}"

    elif name == "SERG":
        return f"https://api.iotlinkchain.com/static/logo/serg.svg?{cache_fix}"

    elif name == "PAPT":
        return f"https://api.iotlinkchain.com/static/logo/papt.svg?{cache_fix}"

    elif name == "CCA/USDT":
        return f"https://api.iotlinkchain.com/static/logo/cca_usdt.svg?{cache_fix}"

    elif name == "MEC/HOWLING2":
        return (
            f"https://api.iotlinkchain.com/static/logo/mec_howling2.svg?{cache_fix}"
        )

    elif name == "PLB":
        return f"https://api.iotlinkchain.com/static/logo/plb.svg?{cache_fix}"

    elif name == "NMO":
        return f"https://api.iotlinkchain.com/static/logo/nmo.svg?{cache_fix}"

    elif name == "NOL":
        return f"https://api.iotlinkchain.com/static/logo/nol.svg?{cache_fix}"

    elif name == "GND":
        return f"https://api.iotlinkchain.com/static/logo/gnd.svg?{cache_fix}"

    elif name == "CCL":
        return f"https://api.iotlinkchain.com/static/logo/ccl.svg?{cache_fix}"

    elif name == "DZTB":
        return f"https://api.iotlinkchain.com/static/logo/dztb.png?{cache_fix}"

    elif name == "DHTB":
        return f"https://api.iotlinkchain.com/static/logo/dhtb.png?{cache_fix}"

    boring_name = name.replace("/", ":")

    return f"https://source.boringavatars.com/bauhaus/120/{boring_name}?colors=264653,2a9d8f,e9c46a,f4a261,e76f51"


def dead_response(message="Invalid Request", rid=config.rid):
    return {"error": {"code": 404, "message": message}, "id": rid}


def response(result, error=None, rid=config.rid, pagination=None):
    result = {"error": error, "id": rid, "result": result}

    if pagination:
        result["pagination"] = pagination

    return result


def make_request(method, params=[]):
    headers = {"content-type": "text/plain;"}
    data = json.dumps({"id": config.rid, "method": method, "params": params})

    try:
        return requests.post(config.endpoint, headers=headers, data=data).json()
    except Exception:
        return dead_response()


def reward(height):
    halvings = height // 525960

    if halvings >= 10:
        return 0

    return int(satoshis(4) // (2**halvings))


def supply(height):
    premine = satoshis(2100000000)
    reward = satoshis(4)
    halvings = 525960
    halvings_count = 0
    supply = premine + reward

    while height > halvings:
        total = halvings * reward
        reward = reward / 2
        height = height - halvings
        halvings_count += 1

        supply += total

        if halvings > 10:
            reward = 0
            break

    supply = supply + height * reward

    return {
        "halvings": int(halvings_count),
        # "supply": int(supply),
        # ToDo: fix supply calculation
        "supply": satoshis(1_000_000_000),
    }


def satoshis(value):
    return int(float(value) * math.pow(10, 8))


def amount(value, decimals=8):
    return round(float(value) / math.pow(10, decimals), decimals)

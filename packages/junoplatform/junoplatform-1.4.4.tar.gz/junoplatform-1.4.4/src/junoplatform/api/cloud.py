__author__ = 'Bruce.Lu'
__mail__ = 'lzbgt@icloud.com'
__create_time__ = '2023/11/07'
__version__ = '0.0.1'

from junoplatform.io.utils import junoconfig
from junoplatform.io import Storage
import yaml
import os
import logging
import requests
import json
import datetime

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(filename)s %(lineno)d - %(message)s')


def info_package(package_id: str = ""):
    '''info packages
    returns: 
        tuple(code, data)
            code: 0 - success; otherwise - failure
            data: when(code==0) - dict; otherwise - errmsg(str)
    '''
    api = f'{junoconfig["cloud"]["api"]}/package/info'
    params = {}
    if not package_id:
        package_id = junoconfig["package_id"]

    params["package_id"] = package_id
    r = requests.get(api, params=params, headers={
                     "Authorization": f"Bearer {junoconfig['cloud']['token']}"})
    if r.status_code != 200:
        msg = f"faild fetch packages"
        if "detail" in r.json():
            msg += ". detail: " + r.json()["detail"]
        return 1, msg
    else:
        data = r.json()
        data["config"] = json.loads(data["config"])
        # data["status"] = statusmap.get(data["status"])
        return 0, data


def list_packages(plant, module):
    '''list packages
    returns: 
        tuple(code, data)
            code: 0 - success; otherwise - failure
            data: when(code==0) - list[dict]; otherwise - errmsg(str)
    '''
    api = f"{junoconfig['cloud']['api']}/packages"
    params = {}
    if plant:
        params["plant"] = plant
    if module:
        params["module"] = module

    logging.info(f"list packages with params:\n{params}")
    r = requests.get(api, params=params, headers={
                     "Authorization": f"Bearer {junoconfig['cloud']['token']}"})
    if r.status_code != 200:
        msg = f"faild fetch packages "
        if "detail" in r.json():
            msg += r.json()["detail"]
        return 1, msg
    else:
        res = []
        for x in r.json():
            x["config"] = json.loads(x["config"])
            # x["status"] = statusmap.get(x["status"])
            res.append(x)
        res.reverse()
        return 0, res


def deploy_package(package_id: str, kind: int, keep_field_cfg: int):
    '''deploy a package
    kind: int, # 0: deploy , 1 rollback, 2: reconfig, 3: cloud api rollback
    returns: 
        tuple(code, data)
            code: 0 - success; otherwise - failure
            data: when(code==0) - None; otherwise - errmsg(str)
    '''
    api = f"{junoconfig['cloud']['api']}/deploy"
    params = {}
    params["package_id"] = package_id
    params["kind"] = kind
    params["keep_spec_cfg"] = keep_field_cfg
    r = requests.post(api, params=params, headers={
                      "Authorization": f"Bearer {junoconfig['cloud']['token']}"})
    if r.status_code != 200:
        msg = f"faild fetch packages "
        if "detail" in r.json():
            msg += r.json()["detail"]
        return 1, msg
    else:
        return 0, None


def rollback(package_id: str = ""):
    '''rollback a package to previous version or specific id[optional]
    returns: 
        tuple(code, data)
            code: 0 - success; otherwise - failure
            data: when(code==0) - new package_id(str); otherwise - errmsg(str)
    '''
    token = junoconfig['cloud']['token']
    if not package_id:
        try:
            package_id = junoconfig["package_id"]
        except:
            logging.error("no package id")
            exit(1)
    code, res = info_package(package_id=package_id)
    if code:
        logging.error(f"failed to get package info: {str}")
        return 1, res
    else:
        code, res = list_packages(res["plant"], res["module"])
        if code:
            logging.error(res)
            return 2, res
        else:
            res.reverse()
            target_idx = -1
            for idx, x in enumerate(res):
                if x["package_id"] == package_id:
                    target_idx = idx + 1

            if target_idx < len(res):
                while res[target_idx]["status"] != 1:
                    target_idx += 1
                    if target_idx >= len(res):
                        break
                if target_idx < len(res):
                    new_id = res[target_idx]["package_id"]
                    code, res = deploy_package(new_id, 3, 1)
                    if not code:
                        logging.info(
                            f"rollback from {package_id} to {new_id} submitted")
                        return 0, {new_id}
                    else:
                        logging.error(res)
                        return 3, res

            msg = f"no available package to rollback for {package_id}"
            logging.error(msg)
            return 4, msg


def send_notification(storage: Storage, func_key: str, msg: str, ban_minutes: int = 30):
    key = f'system.ai.notification.{junoconfig["plant"]}.{junoconfig["module"]}.{func_key}'
    try:
        scr = storage.local.read(key, cast=dict)
    except:
        storage.local.io.delete(key)

    if scr and (datetime.datetime.now().timestamp() - scr["ts"])/60 < ban_minutes and ban_minutes > 0:
        logging.warning(
            f"skip notification, since this module called in {ban_minutes} minutes already")
        return -1
    else:
        message = {
            "name": "junoplatform",
            "message": msg,
            "ts": datetime.datetime.now().timestamp()
        }
        storage.cloud.write(
            'juno-svc-notification', message, raw_table=True)
        storage.local.write(key, message)
        return 0


def get_func_key(mod: str, func_key: str):
    return f'system.ai.{mod}.{junoconfig["plant"]}.{junoconfig["module"]}.{func_key}'


call_record_map_default = {}


def smartcall(storage: Storage, func_key: str, fault: str, ban_minutes: int = 120):
    key = f'system.ai.smartcall.{junoconfig["plant"]}.{junoconfig["module"]}.{func_key}'
    scr = None
    try:
        scr = storage.local.read(key, cast=dict)
    except Exception as e:
        logging.error(f"failed to read redis {str(e)}")
        storage.local.io.delete(key)

    now = datetime.datetime.now()
    today = now.date()
    midnight = datetime.datetime.combine(today, datetime.datetime.min.time())
    sixoc = midnight + datetime.timedelta(hours=6)

    isInMidNight = (now > midnight) and (now < sixoc)
    isInBan = True if scr and (
        (now.timestamp() - scr["params"]["ts"])/60 < ban_minutes) else False

    if isInMidNight or isInBan:
        logging.warn(
            f"skip smartcall voice call, in ban time or midnight")
        return -1
    elif "smartcall" in junoconfig and "token" in junoconfig["smartcall"] and "api" in junoconfig["smartcall"] and "numbers" in junoconfig["smartcall"]:

        # in case redis down, fallback to memory record
        if not scr:
            if key in call_record_map_default and (call_record_map_default[key] + ban_minutes * 60) < now.timestamp():
                logging.warn("skip smartcall in ban time")
                return -1
            # store memory record
        call_record_map_default[key] = now.timestamp()

        calldata = {
            "number": "xxx",
            "params": {
                "plant": f'{junoconfig["plant"]}, 水厂',
                "module": f'{junoconfig["module"]}, 算法模块, ',
                "fault": fault,
                "ts": now.timestamp()
            }
        }
        storage.local.write(key, calldata)

        for number in junoconfig["smartcall"]["numbers"]:
            calldata["number"] = number
            r = requests.post(junoconfig["smartcall"]["api"], json=calldata, headers={
                "Authorization": f'Bearer {junoconfig["smartcall"]["token"]}'
            })
            logging.info("smartcall result: " + r.text)
        return 0
    else:
        logging.warning("smart call not configured")
        return -2


def fetch_latest_config(r):

    plant = r["plant"]
    module = r["module"]
    if "cloud" in r:
        cloud = r["cloud"]
        api = f"{cloud['api']}/deploys/current"
        token = cloud["token"]
    else:
        cloud = junoconfig["cloud"]
        api = f"{cloud['api']}/deploys/current"
        token = cloud["token"]

    logging.info(f"api: {api}, token: {token}")

    params = {}
    params["plant"] = plant
    params["module"] = module

    logging.info(f"list current deployments with params:\n{params}")
    r = requests.get(api, params=params, headers={
                     "Authorization": f"Bearer {token}"})
    if r.status_code != 200:
        msg = f"faild fetch packages "
        if "detail" in r.json():
            msg += r.json()["detail"]
        return msg
    else:
        r.encoding = "utf-8"
        data = r.json()
        data.reverse()
        return data

# coding=utf-8
import datetime
import logging as log

import docker

from management import utils, distr_controller
from management.kv_store import DBController
from management.models.nvme_device import NVMeDevice
from management.models.storage_node import StorageNode
from management.rpc_client import RPCClient
from management.snode_client import SNodeClient

logger = log.getLogger()


def check_cluster(cluster_id):
    db_controller = DBController()
    st = db_controller.get_storage_nodes()
    data = []
    for node in st:
        # check if node is online, unavailable, restarting
        ret = check_node(node.get_id())
        print("*"*100)
        data.append({
            "Kind": "Node",
            "UUID": node.get_id(),
            "Status": "ok" if ret else "failed"
        })

    for lvol in db_controller.get_lvols():
        ret = check_lvol(lvol.get_id())
        print("*" * 100)
        data.append({
            "Kind": "LVol",
            "UUID": lvol.get_id(),
            "Status": "ok" if ret else "failed"
        })
    print(utils.print_table(data))
    return True


def check_node(node_id):
    db_controller = DBController()
    snode = db_controller.get_storage_node_by_id(node_id)
    if not snode:
        logger.error("node not found")
        return False

    logger.info(f"Checking node {node_id}, status: {snode.status}")

    print("*" * 100)

    passed = True
    res = utils.ping_host(snode.mgmt_ip)
    if res:
        logger.info(f"Ping host: {snode.mgmt_ip}... OK")
    else:
        logger.error(f"Ping host: {snode.mgmt_ip}... Failed")
        passed = False

    print("*" * 100)

    try:
        rpc_client = RPCClient(
            snode.mgmt_ip, snode.rpc_port,
            snode.rpc_username, snode.rpc_password,
            timeout=3, retry=1)
        ret = rpc_client.get_version()
        if ret:
            logger.info(f"SPDK RPC ... ok")
            logger.debug(f"SPDK version: {ret['version']}")

            ret = rpc_client.get_bdevs()
            logger.info(f"SPDK BDevs count: {len(ret)}")
        else:
            logger.info(f"SPDK RPC ... failed")
            passed = False

    except Exception as e:
        logger.error(f"Failed to connect to node's SPDK: {e}")
        passed = False

    print("*" * 100)

    try:
        node_docker = docker.DockerClient(base_url=f"tcp://{snode.mgmt_ip}:2375", version="auto")
        containers_list = node_docker.containers.list(all=True)
        for cont in containers_list:
            name = cont.attrs['Name']
            state = cont.attrs['State']

            if name in ['/spdk', '/spdk_proxy', '/SNodeAPI'] or name.startswith("/app_"):
                logger.debug(state)
                if state['Status'] != "running":
                    continue
                since = ""
                try:
                    start = datetime.datetime.fromisoformat(state['StartedAt'].split('.')[0])
                    since = str(datetime.datetime.now() - start).split('.')[0]
                except:
                    pass
                clean_name = name.split(".")[0].replace("/", "")
                logger.info(f"Container: {clean_name}, Status: {state['Status']}, Since: {since}")

    except Exception as e:
        logger.error(f"Failed to connect to node's docker: {e}")
        passed = False

    print("*" * 100)

    logger.info(f"Node device: {len(snode.nvme_devices)}")
    for dev in snode.nvme_devices:
        ret = check_device(dev.get_id())
        passed |= ret
        print("*" * 100)

    try:
        snode_api = SNodeClient(f"{snode.mgmt_ip}:5000")
        node_info, _ = snode_api.info()
        if node_info:
            logger.info("Connecting to node's API ... ok")
            logger.debug(f"Node API={snode.mgmt_ip}:5000")
            logger.debug(node_info)
        else:
            logger.error("Connecting to node's API ... failed")
            passed = False
    except Exception as e:
        logger.error("Connecting to node's API ... failed")
        passed = False

    return passed


def check_device(device_id):
    db_controller = DBController()
    device = db_controller.get_storage_devices(device_id)
    if not device:
        logger.error("device not found")
        return False

    snode = db_controller.get_storage_node_by_id(device.node_id)
    if not snode:
        logger.error("node not found")
        return False

    passed = True
    try:
        rpc_client = RPCClient(
            snode.mgmt_ip, snode.rpc_port,
            snode.rpc_username, snode.rpc_password,
            timeout=3, retry=1)

        bdevs_stack = [device.nvme_bdev, device.testing_bdev, device.alceml_bdev, device.pt_bdev]
        logger.info(f"Checking Device: {device_id}, status:{device.status}")
        problems = 0
        for bdev in bdevs_stack:
            ret = rpc_client.get_bdevs(bdev)
            if ret:
                logger.debug(f"Checking bdev: {bdev} ... ok")
            else:
                logger.error(f"Checking bdev: {bdev} ... not found")
                problems += 1
                passed = False
                # return False
        logger.info(f"Checking Device's BDevs ... ({(len(bdevs_stack)-problems)}/{len(bdevs_stack)})")

        ret = rpc_client.subsystem_list(device.nvmf_nqn)
        logger.debug(f"Checking subsystem: {device.nvmf_nqn}")
        if ret:
            logger.info(f"Checking subsystem ... ok")
        else:
            logger.info(f"Checking subsystem: ... not found")
            passed = False

        if device.status == NVMeDevice.STATUS_ONLINE:
            logger.info("Checking other node's connection to this device...")
            ret = check_remote_device(device_id)
            passed |= ret

        # logger.info("All good")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to node's SPDK: {e}")
        passed = False

    return passed


def check_remote_device(device_id):
    db_controller = DBController()
    device = db_controller.get_storage_devices(device_id)
    if not device:
        logger.error("device not found")
        return False
    snode = db_controller.get_storage_node_by_id(device.node_id)
    if not snode:
        logger.error("node not found")
        return False

    # if device.status is not NVMeDevice.STATUS_ONLINE:
    #     logger.error("device is not online")
    #     return False

    for node in db_controller.get_storage_nodes():
        if node.status == StorageNode.STATUS_ONLINE:
            if node.get_id() == snode.get_id():
                continue
            logger.info(f"Connecting to node: {node.get_id()}")
            rpc_client = RPCClient(node.mgmt_ip, node.rpc_port, node.rpc_username, node.rpc_password)
            name = f"remote_{device.alceml_bdev}n1"
            ret = rpc_client.get_bdevs(name)
            if ret:
                logger.info(f"Checking bdev: {device.alceml_bdev} ... ok")
            else:
                logger.info(f"Checking bdev: {device.alceml_bdev} ... not found")
                # return False
    # logger.info("All good")
    return True


def check_lvol_on_node(lvol_id, node_id):

    db_controller = DBController()
    lvol = db_controller.get_lvol_by_id(lvol_id)
    if not lvol:
        logger.error(f"lvol not found: {lvol_id}")
        return False

    snode = db_controller.get_storage_node_by_id(node_id)
    rpc_client = RPCClient(
        snode.mgmt_ip, snode.rpc_port,
        snode.rpc_username, snode.rpc_password)

    passed = True
    for bdev_info in lvol.bdev_stack:
        bdev_name = bdev_info['name']
        ret = rpc_client.get_bdevs(bdev_name)
        if ret:
            logger.info(f"Checking LVol: {lvol_id} ... ok")
        else:
            logger.error(f"Checking LVol: {lvol_id} ... failed")
            passed = False

        ret = rpc_client.subsystem_list(lvol.nqn)
        if ret:
            logger.info(f"Checking subsystem ... ok")
        else:
            logger.info(f"Checking subsystem ... not found")
            passed = False

    logger.info("Checking Distr map ...")
    rpc_client = RPCClient(snode.mgmt_ip, snode.rpc_port, snode.rpc_username, snode.rpc_password)
    ret = rpc_client.distr_get_cluster_map(lvol.base_bdev)
    results, is_passed = distr_controller.parse_distr_cluster_map(ret)
    print(utils.print_table(results))
    passed |= is_passed
    return passed



def check_lvol(lvol_id):
    db_controller = DBController()

    lvol = db_controller.get_lvol_by_id(lvol_id)
    if not lvol:
        logger.error(f"lvol not found: {lvol_id}")
        return False

    if lvol.ha_type == 'single':
        ret = check_lvol_on_node(lvol_id, lvol.node_id)
        return ret

    elif lvol.ha_type == "ha":
        passed = True
        for nodes_id in lvol.nodes:
            ret = check_lvol_on_node(lvol_id, nodes_id)
            if not ret:
                passed = False
        return passed

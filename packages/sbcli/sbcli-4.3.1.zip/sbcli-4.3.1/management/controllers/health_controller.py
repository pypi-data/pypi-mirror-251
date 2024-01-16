# coding=utf-8
import datetime
import logging as log

import docker

from management import utils
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
        ret = check_node(node.get_id())
        for dev in node.nvme_devices:
            ret = check_device(dev.get_id())
            ret = check_remote_device(dev.get_id())

        for lvol_id in node.lvols:
            ret = check_lvol(lvol_id)

    return True


def check_node(node_id):
    db_controller = DBController()
    snode = db_controller.get_storage_node_by_id(node_id)
    if not snode:
        logger.error("node not found")
        return False

    logger.info(f"Checking node {node_id}")
    try:
        res = utils.ping_host(snode.mgmt_ip)
        if res:
            logger.info(f"Ping host: {snode.mgmt_ip}... OK")
        else:
            logger.error(f"Ping host: {snode.mgmt_ip}... Failed")

        node_docker = docker.DockerClient(base_url=f"tcp://{snode.mgmt_ip}:2375", version="auto")
        containers_list = node_docker.containers.list(all=True)
        for cont in containers_list:
            name = cont.attrs['Name']
            state = cont.attrs['State']

            if name in ['/spdk', '/spdk_proxy', '/SNodeAPI'] or name.startswith("/app_"):
                logger.debug(state)
                since = ""
                try:
                    start = datetime.datetime.fromisoformat(state['StartedAt'].split('.')[0])
                    since = str(datetime.datetime.now()-start).split('.')[0]
                except:
                    pass
                clean_name = name.split(".")[0].replace("/", "")
                logger.info(f"Container: {clean_name}, Status: {state['Status']}, Since: {since}")

    except Exception as e:
        logger.error(f"Failed to connect to node's docker: {e}")

    try:
        logger.info("Connecting to node's SPDK")
        rpc_client = RPCClient(
            snode.mgmt_ip, snode.rpc_port,
            snode.rpc_username, snode.rpc_password,
            timeout=3, retry=1)

        ret = rpc_client.get_version()
        logger.info(f"SPDK version: {ret['version']}")

        ret = rpc_client.get_bdevs()
        logger.info(f"SPDK BDevs count: {len(ret)}")
        for bdev in ret:
            name = bdev['name']
            product_name = bdev['product_name']
            driver = ""
            for d in bdev['driver_specific']:
                driver = d
                break
            # logger.info(f"name: {name}, product_name: {product_name}, driver: {driver}")

        logger.info(f"getting device bdevs")
        for dev in snode.nvme_devices:
            nvme_bdev = rpc_client.get_bdevs(dev.nvme_bdev)
            testing_bdev = rpc_client.get_bdevs(dev.testing_bdev)
            alceml_bdev = rpc_client.get_bdevs(dev.alceml_bdev)
            pt_bdev = rpc_client.get_bdevs(dev.pt_bdev)

            subsystem = rpc_client.subsystem_list(dev.nvmf_nqn)

            # dev.testing_bdev = test_name
            # dev.alceml_bdev = alceml_name
            # dev.pt_bdev = pt_name
            # # nvme.nvmf_nqn = subsystem_nqn
            # # nvme.nvmf_ip = IP
            # # nvme.nvmf_port = 4420

    except Exception as e:
        logger.error(f"Failed to connect to node's SPDK: {e}")

    try:
        logger.info("Connecting to node's API")
        snode_api = SNodeClient(f"{snode.mgmt_ip}:5000")
        node_info, _ = snode_api.info()
        logger.info(f"Node info: {node_info['hostname']}")

    except Exception as e:
        logger.error(f"Failed to connect to node's SPDK: {e}")


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

    try:
        logger.info("Connecting to node's SPDK")
        rpc_client = RPCClient(
            snode.mgmt_ip, snode.rpc_port,
            snode.rpc_username, snode.rpc_password,
            timeout=3, retry=1)

        for bdev in [device.nvme_bdev, device.testing_bdev, device.alceml_bdev, device.pt_bdev]:
            ret = rpc_client.get_bdevs(bdev)
            if ret:
                logger.info(f"Checking bdev: {bdev} ... ok")
            else:
                logger.info(f"Checking bdev: {bdev} ... not found")
                # return False

        ret = rpc_client.subsystem_list(device.nvmf_nqn)
        if ret:
            logger.info(f"Checking subsystem: {device.nvmf_nqn} ... ok")
        else:
            logger.info(f"Checking subsystem: {device.nvmf_nqn} ... not found")
            # return False

        if device.status == NVMeDevice.STATUS_ONLINE:
            logger.info("Checking other node's connection to this device...")
            ret = check_remote_device(device_id)

        # logger.info("All good")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to node's SPDK: {e}")


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

    if device.status is not NVMeDevice.STATUS_ONLINE:
        logger.error("device is not online")
        return False

    for node in db_controller.get_storage_nodes():
        if node.status == StorageNode.STATUS_ONLINE:
            if node.get_id() == snode.get_id():
                continue
            logger.info(f"Connecting to node: {node.get_id()}")
            rpc_client = RPCClient(node.mgmt_ip, node.rpc_port, node.rpc_username, node.rpc_password)
            ret = rpc_client.subsystem_list(device.nvmf_nqn)
            if ret:
                logger.info(f"Checking subsystem: {device.nvmf_nqn} ... ok")
            else:
                logger.info(f"Checking subsystem: {device.nvmf_nqn} ... not found")
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

    for bdev_info in lvol.bdev_stack:
        bdev_name = bdev_info['name']
        ret = rpc_client.get_bdevs(bdev_name)
        if ret:
            logger.info(f"Checking bdev: {bdev_name} ... ok")
        else:
            logger.info(f"Checking bdev: {bdev_name} ... not found")

        ret = rpc_client.subsystem_list(lvol.nqn)
        if ret:
            logger.info(f"Checking subsystem: {lvol.nqn} ... ok")
        else:
            logger.info(f"Checking subsystem: {lvol.nqn} ... not found")
            # return False
    # logger.info("All good")


def check_lvol(lvol_id):
    db_controller = DBController()

    lvol = db_controller.get_lvol_by_id(lvol_id)
    if not lvol:
        logger.error(f"lvol not found: {lvol_id}")
        return False

    if lvol.ha_type == 'single':
        ret = check_lvol_on_node(lvol_id, lvol.node_id)
        # if not ret:
        #     return False
    elif lvol.ha_type == "ha":
        for nodes_id in lvol.nodes:
            ret = check_lvol_on_node(lvol_id, nodes_id)
            # if not ret:
            #     return False

    # logger.info("All good")
    return True

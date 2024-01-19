import os
import sys
import time
import signal
import subprocess, multiprocessing
import json
import platform
import math
from pathlib import Path
from urllib.parse import *
import socket
import calendar
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
from threading import Thread, current_thread, Lock
import pkg_resources
from pkg_resources import get_distribution
import websocket

from mecord import store
from mecord import xy_pb
from mecord import task 
from mecord import utils
from mecord import taskUtils
from mecord import progress_monitor
from mecord import mecord_widget

thisFileDir = os.path.dirname(os.path.abspath(__file__)) 
def on_message(ws, message):
    print("Received message:", message)

    pb_rsp = xy_pb.rpcinput_pb2.RPCOutput()
    pb_rsp.ParseFromString(message)
    if pb_rsp.ret == 0:
        rsp = xy_pb.aigc_ext_pb2.TaskInfoRes()
        rsp.ParseFromString(pb_rsp.rsp)
        if rsp.taskStatus < 3:
            print("==========")
        elif rsp.taskStatus == 3:
            print(json.loads(rsp.taskResult))
        elif rsp.taskStatus == 4:
            print(pb_rsp.failReason)
        # rsp = xy_pb.aigc_ext_pb2.GetTaskRes()
        # rsp.ParseFromString(pb_rsp.rsp)
        # datas = []
        # for it in rsp.list:
        #     datas.append({
        #         "taskUUID": it.taskUUID,
        #         "pending_count": rsp.count - rsp.limit,
        #         "config": it.config,
        #         "data": it.data,
        #     })
        # print(f"receive ! {datas}")
    

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, status_code, close_msg):
    print(f"Connection closed status_code={status_code} msg={close_msg}")
    reconnect()

def reconnect():
    time.sleep(5)
    print("reconnect...")
    ws.run_forever()

def send():
    while True:
        # gettaskReq = xy_pb.aigc_ext_pb2.GetTaskReq()
        # gettaskReq.version = xy_pb.constant.app_version
        # gettaskReq.DeviceKey = utils.generate_unique_id()
        # map = store.widgetMap()
        # for it in map:
        #     if isinstance(map[it], (dict)):
        #         if map[it]["isBlock"] == False:
        #             gettaskReq.widgets.append(it)
        #     else:
        #         gettaskReq.widgets.append(it)
        # gettaskReq.token = xy_pb.real_token()
        # gettaskReq.limit = store.multitaskNum()
        # gettaskReq.extend = xy_pb._extend()
        # req = gettaskReq.SerializeToString()
        
        taskinfoReq = xy_pb.aigc_ext_pb2.TaskInfoReq()
        taskinfoReq.taskUUID = "b2ad550e-a07e-5b92-9efc-2058001bbb56"
        taskinfoReq.findTaskResult = True
        req = taskinfoReq.SerializeToString()
        opt = {
            "lang": "zh-Hans",
            "region": "CN",
            "appid": "80",
            "application": "mecord",
            "version": "1.0",
            "X-Token": xy_pb.real_token(),
            "uid": "1",
        }
        input_req = xy_pb.rpcinput_pb2.RPCInput(obj="mecord.aigc.AigcExtObj", func="TaskInfo", req=req, opt=opt)
        binary_data = input_req.SerializeToString()
        ws.send_bytes(binary_data)
        print("send success")
        time.sleep(60)
        

def on_open(ws):
    print("Connection opened")
    def send_heartbeat():
        while True:
            heartbeat_data = { "type": "heartbeat" }
            binary_data = json.dumps(heartbeat_data).encode()
            ws.send_bytes(binary_data)
            time.sleep(5)
    heartbeat_thread = Thread(target=send_heartbeat)
    heartbeat_thread.start()
    send_thread = Thread(target=send)
    send_thread.start()

if __name__ == "__main__":
    url = "wss://mecord-beta.2tianxin.com/proxymsg/ws"    
    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
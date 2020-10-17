#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import json
import subprocess, shlex
import os
import signal


import psutil


def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

class Status:
    STATUS = "idle"
    
    BBB_URL = None
    BBB_MEETING_ID = None
    BBB_SECRET = None
    BBB_STREAM_URL = None
    BBB_MEETING_NAME = None
    process = None
    STREAM_COMMAND = 'xvfb-run -n 122 --server-args="-screen 0 1360x768x24" python3 stream.py -s {BBB_URL} -p {BBB_SECRET} -i {BBB_MEETING_ID} -t {BBB_STREAM_URL} -u BBBStreamer -m -sc 122 '



async def send_status_to_all():
    for ws in cwebsockets:
        try:
            await get_status(ws)
        except:
            print("Cant send to", ws)

async def get_status(websocket):
    await websocket.send(json.dumps({"command":"status", "status": Status.STATUS}))

async def start_stream(websocket, msg):
    if Status.STATUS != "busy":
        print(msg)
        Status.BBB_URL = msg['bbb_url']
        Status.BBB_MEETING_ID = msg['bbb_meeting_id']
        Status.BBB_SECRET = msg['bbb_secret']
        Status.BBB_STREAM_URL = msg['bbb_stream_url']
        Status.BBB_MEETING_NAME = msg['bbb_meeting_name']
        
        cmd = shlex.split(Status.STREAM_COMMAND.format(BBB_URL=Status.BBB_URL,BBB_SECRET=Status.BBB_SECRET,BBB_MEETING_ID=Status.BBB_MEETING_ID,BBB_STREAM_URL=Status.BBB_STREAM_URL))
        print(cmd)
        Status.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=False, preexec_fn=os.setsid)
        Status.STATUS = "busy"
    await send_status_to_all()
    #print(STREAM_COMMAND.format(**locals()))

async def get_stream_details(websocket, msg):
    if Status.STATUS == "busy":
        await websocket.send(json.dumps({"command": "get_details", "bbb_url": Status.BBB_URL, "bbb_meeting_id": Status.BBB_MEETING_ID, "bbb_stream_url": Status.BBB_STREAM_URL, "bbb_meeting_name":Status.BBB_MEETING_NAME}))
    else:
        await get_status(websocket)

async def close_stream(websocket, msg):
    if Status.STATUS == "busy":
        Status.STATUS="idle"
        Status.BBB_URL = None
        Status.BBB_MEETING_ID = None
        Status.BBB_SECRET = None
        Status.BBB_STREAM_URL = None
        kill(Status.process.pid)
    await send_status_to_all()
    

async def get_ffmpeg_out(websocket, msg):
    if Status.STATUS == "busy":
        if os.path.exists('ffmpeg.log'):
            stdout = open('ffmpeg.log').read()

            await websocket.send(json.dumps({"command": "get_output","stdout":stdout}))



cwebsockets = []

async def handle_websocket(websocket, path):
    cwebsockets.append(websocket)
    while True:
        msg = await websocket.recv()
        msg = json.loads(msg)
        command = msg['command']
        print(msg)     
        if command == "status":
            await get_status(websocket)
        if command == "start_stream":
            await start_stream(websocket, msg)
        if command == "get_details":
            await get_stream_details(websocket, msg)
        if command == "close_stream":
            await close_stream(websocket, msg)
        if command == "get_output":
            await get_ffmpeg_out(websocket, msg)
        #await websocket.send(json.dumps(msg))
        
start_server = websockets.serve(handle_websocket, "0.0.0.0", 8989)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

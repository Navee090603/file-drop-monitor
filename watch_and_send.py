# watch_and_send.py
import os, time, requests
from datetime import datetime

FOLDER_TO_WATCH = r"C:\Users\naveent\Downloads\File_Droping"
SERVER_URL = "http://127.0.0.1:5000/update"
TOKEN = "1234"

def find_largest(folder):
    largest=None; size=-1
    for r,_,fs in os.walk(folder):
        for f in fs:
            p=os.path.join(r,f)
            try: s=os.path.getsize(p)
            except: continue
            if s>size:
                size=s; largest=f
    if largest is None: return None
    return largest, size

while True:
    res=find_largest(FOLDER_TO_WATCH)
    if res:
        fn, sz = res
        ts = datetime.utcnow().isoformat()+"Z"
        payload={"filename":fn,"size_bytes":sz,"timestamp_iso":ts}
        headers={"X-File-Drop-Token":TOKEN,"Content-Type":"application/json"}
        print("SENDING:", payload)
        try:
            r=requests.post(SERVER_URL,json=payload,headers=headers)
            print("REPLY:", r.status_code, r.text)
        except Exception as e:
            print("ERR:", e)
    time.sleep(5)

import asyncio,json,os,random,time
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_socketio import SocketManager
from fastapi.responses import HTMLResponse, JSONResponse
from threading import Timer

from openpibo.device import Device
from openpibo.motion import Motion
from openpibo.audio import Audio
from openpibo.speech import Speech

# speech.SAPI_HOST = 'https://oe-sapi.circul.us/v1'
VOLUME = 100
PLAY = False

app = FastAPI()
sio = SocketManager(app=app, cors_allowed_origins=[], mount_location="/ws/socket.io", socketio_path="")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/', response_class=HTMLResponse)
async def f(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})

@app.on_event('startup')
async def startup_event():
  print('startup')
  global audio, motion, device, speech
  os.system('mkdir -p mp3')
  audio = Audio()
  motion = Motion()
  device = Device()
  speech = Speech()  
  asyncio.create_task(touch_sensor_monitor())

@app.sio.on('connect')
async def connect(sid, environ):
  print(f"Client connected: {sid}")

@app.sio.on('disconnect')
async def disconnect(sid):
  print(f"Client disconnected: {sid}")

@app.sio.on('play')
async def handle_play(sid, data):
    global VOLUME
    volume = data.get('volume')
    try:
        if isinstance(volume, (int, float)) and 0 <= volume <= 100:
            VOLUME = volume
        else:
            raise ValueError("입력값이 0에서 100 사이여야 합니다.")
    except (TypeError, ValueError) as e:
        print("에러:", e)
        VOLUME = 100  # 모든 에러 발생 시 VOLUME을 100으로 설정

    # 정상 처리 후 실행
    await handle_touch_event()

async def touch_sensor_monitor():
  motion.set_motion('stop')
  device.eye_on(50,255,255)
  while True:
    if device.get_touch() == 'touch':
      await handle_touch_event()
      await asyncio.sleep(1)
    else:
      await asyncio.sleep(0.2)

async def talk(string, filepath, actions):
#   speech.tts(string=string, filename=filepath, voice='main', lang='ko')
#   await asyncio.sleep(0.1)
#   print("[TTS]:", string)
  device.eye_on(random.randint(100,255),random.randint(100,255),random.randint(100,255))
  if actions != None:
    motion_timer = Timer(0, motion.set_motion, args=(random.choice(actions),))
    motion_timer.start()
  audio.play(filepath, VOLUME, background=False)
  device.eye_off()
  await asyncio.sleep(0.5)
    
# 터치 이벤트 처리 함수
async def handle_touch_event():
  global PLAY
  if PLAY == True:
#   print("already run")
    return
  PLAY = True
  await talk('이 곳에는 디지털 새-싹들이 발굴한, 보물 들을 만나볼 수 있는데요.', 'mp3/tts2_1.mp3', ["yes_h", "no_h", "bow"])
  await talk('이 보물 들은 전국 코드 대회에서 빛난 열 개 팀의 놀라운 아이디어의 결과물 이-에요.', 'mp3/tts2_2.mp3', ["yes_h", "no_h", "bow"])
  await talk('여러 분도  나도 한 번 해볼까? 하는 생각이 들죠?', 'mp3/tts2_3.mp3', ["yes_h", "no_h", "bow"])
  motion.stop()
  await asyncio.sleep(3)
  motion.set_motors([0,0,-70,-25,0,0,0,0,70,25], 2000)
  PLAY = False

if __name__ == "__main__":
  import uvicorn
  uvicorn.run('demo_b:app', host='0.0.0.0', port=10001, access_log=False)

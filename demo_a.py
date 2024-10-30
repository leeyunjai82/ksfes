import random,time,os
from threading import Timer

from openpibo.device import Device
from openpibo.motion import Motion
from openpibo.audio import Audio
from openpibo.speech import Speech

audio = Audio()
motion = Motion()
device = Device()
speech = Speech()
# speech.SAPI_HOST = 'https://oe-sapi.circul.us/v1'
VOLUME = 100
PLAY = False
os.system('mkdir -p mp3')

def talk(string, filepath, actions):
#   speech.tts(string=string, filename=filepath, voice='main', lang='ko')
#   time.sleep(0.1)
#   print("[TTS]:", string)
  device.eye_on(random.randint(100,255),random.randint(100,255),random.randint(100,255))
  if actions != None:
    motion_timer = Timer(0, motion.set_motion, args=(random.choice(actions),))
    motion_timer.start()
  #audio.play(filepath, VOLUME, background=False)
  os.system(f'amixer -q -c Device sset Speaker 100%;play -q -V1 -v 1.0 "{filepath}"')
  device.eye_off()
  time.sleep(0.5)

def check_touch():
  global PLAY
  while True:
    if device.get_touch() == 'touch':
      PLAY = False if PLAY else True
      print("Change to RUN:", PLAY)
      time.sleep(2)
    time.sleep(0.2)    
    
motion.set_motion('stop')

timer = Timer(0, check_touch)
timer.daemon = True
timer.start()

while True:
  device.eye_on(50,255,255)

  PLAY and talk('어서 오세요, 미래의 디지털 탐험가 여러분, 디지털 새-싹, - 아이스 랜드에 오신 것을 환영합니다.', 'mp3/tts1_1.mp3', ["greeting"])
  PLAY and talk('저는, 여러분의 여정을 안내할, 인공지능 로봇 파이-보 에요.', 'mp3/tts1_2.mp3', ["clapping1", "clapping2"])
  PLAY and talk('디지털 새-싹, 홍보관, - 아이스 랜드 는, 임팩트, 크리에이티비티, 익스피어리언쓰, 세가지 테마로 되어 있어요.', 'mp3/tts1_3.mp3', ["speak_r1","speak_r2", "speak_l1","speak_l2"])
  PLAY and talk('여정을 통해 지난 삼 년 간의 디지털 새-싹이 이뤄왔던 멋진 성과와 디지털 새-싹이 꿈꾸는 멋진 미래를 알아볼 수 있어요.', 'mp3/tts1_4.mp3', ["speak_r1","speak_r2", "speak_l1","speak_l2"])   
  PLAY and talk('그리고, 우리의 귀여운 친구 ‘누룽찌’도 만나서 재미있는 대화도 나눌 수 있어요.', 'mp3/tts1_5.mp3', ["speak_r1","speak_r2", "speak_l1","speak_l2"])
  PLAY and talk('누룽찌 매력에 푹 빠져보세요.', 'mp3/tts1_6.mp3', ["clapping1", "clapping2"])
  PLAY and talk('잠깐, 이 여정에는 다양한 미쎤이 있습니다.', 'mp3/tts1_7.mp3', ["yes_h", "no_h"])
  PLAY and talk('인공지능 과의 두뇌 대결, 로봇 배달 미션 수행, 나만의 인공지능 캐릭터 만들기 등, 흥미진진한 체험들이 여러분을 기다립니다.', 'mp3/tts1_8.mp3', ["speak_r1","speak_r2", "speak_l1","speak_l2"])
  PLAY and talk('자, 이제 신나는 디지털 모험을 떠나볼까요? - 출 발 ', 'mp3/tts1_9.mp3', ["hand1", "hand2", "hand3", "hand4"])
    
  PLAY and motion.set_motion('greeting')
  motion.set_motors([0,0,-70,-25,0,0,0,0,70,25], 2000)
  time.sleep(2)

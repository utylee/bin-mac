#import winsound
import asyncio
#from PIL import Image
import os, glob
import subprocess
import datetime

#import pillow

class Handle():
    def __init__(self):
        self.file_flag = 0
        self.file_flag_car = 0

    async def handle(self, reader, writer):
        #data = yield from reader.read(100)
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print("Received %r from %r" % (message, addr))

        # message가 coming 이 들어오면 Beep 발생
        if(message == "coming"):
            try:
                # Beep
                for i in range(0, 5):
                    #winsound.Beep(300 + i*100, 60)
                    print('\a')
                    #winsound.Beep(300 , 60)
                    await asyncio.sleep(0.7)
            except:
                pass
                #print('Beep failed!')
        # message가 차량용블랙박스로부터 comingcar  들어오면 Beep 발생
        if(message == "comingcar"):
            try:
                # Beep
                for i in range(0, 3):
                    #winsound.Beep(300 + i*100, 60)
                    #winsound.Beep(700 , 60)
                    print('\a')
                    await asyncio.sleep(0.7)
            except:
                pass
                #print('Beep failed!')
        # motion from car 가 종료되었을 때 날아오는 메세지 
        elif(message == "endedcar"):
            # 거래시간인 오전에는 이미지 표시는 pass하도록 합니다
            n = datetime.datetime.now()
            current_hour = int(n.strftime('%H'))
            weekday = n.weekday()
            # 평일일 경우(토요일, 일요일이 아닌 경우)
            if (weekday != 0) or (weekday !=6):
                if (current_hour >= 8) and (current_hour <= 11):
                    return

            try:
                # 파일 생성까지 시간이 좀 걸리므로 3초 딜레이를 줘봅니다
                #loop.call_later(3, self.showcar)
                # 맥에서는 사진보여주기 보다는 그냥 알람만 울리도록 합니다.
                print('\a')
            except:
                pass
                
        # motion 이 종료되었을 때 날아오는 메세지 
        elif(message == "ended"):
            # 거래시간인 오전에는 이미지 표시는 pass하도록 합니다
            n = datetime.datetime.now()
            current_hour = int(n.strftime('%H'))
            weekday = n.weekday()
            # 평일일 경우(토요일, 일요일이 아닌 경우)
            if (weekday != 0) or (weekday !=6):
                if (current_hour >= 8) and (current_hour <= 11):
                    return

            try:
                # 파일 생성까지 시간이 좀 걸리므로 3초 딜레이를 줘봅니다
                #loop.call_later(3, self.show)
                # 맥에서는 사진보여주기 보다는 그냥 알람만 울리도록 합니다.
                print('\a')
            except:
                pass


h = Handle()
loop = asyncio.get_event_loop()
coro = asyncio.start_server(h.handle, '0.0.0.0', 8899, loop = loop)

server = loop.run_until_complete(coro)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

#print('interrupted')
# Close Server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()


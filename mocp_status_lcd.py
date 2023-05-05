import lcddriver
import subprocess
from time import time
from time import sleep
from datetime import datetime

lcd_line_len = 16
lcd = lcddriver.lcd()

s_char = 0
while True:
  try:
    mocp_info = subprocess.check_output(['mocp', '-i']).decode('ascii').split('\n')
    mocp_status = mocp_info[0].split(':')[1].strip()
    if mocp_status == 'STOP':
      lcd.clear()
      lcd.display_string("mocp is STOPPED", 1)
      sleep(.2)
      continue
    mocp_song = mocp_info[1].split(':')[1].split('/')[-1]
    mocp_song_len = mocp_info[8].split(':')[1].strip()
    progress_sec = round(int(mocp_song_len)/lcd_line_len)
    mocp_song_played = mocp_info[10].split(':')[1].strip()
    progress_chars = round(int(mocp_song_played)/progress_sec)
    progress_bar = "*" * progress_chars
    e_char = s_char+16
    if e_char > len(mocp_song):
      e_char = len(mocp_song) 
    disp_string = mocp_song[s_char:e_char]
    if len(disp_string) < 16:
        chars_to_add = 16-(len(disp_string) +1)
        disp_string+=" "
        disp_string+=mocp_song[0:chars_to_add]
    lcd.clear()
    lcd.display_string(disp_string, 1)
    if mocp_status == "PAUSE":
      lcd.display_string(mocp_status, 2)
    else:
       lcd.display_string(progress_bar, 2)
    sleep(.2)
    s_char+=1
    if s_char > len(mocp_song):
      s_char=0
  except Exception as e:
    print(e)
    continue

import time
import cv2
from Crypto.Cipher import AES
from Crypto import Random
import numpy as np
from moviepy.editor import *

KEY = Random.new().read(AES.key_size[0])

def encrypt_frame(frame):
   if frame.size % 16 > 0:
      row = img.shape[0]
      pad = 16 - (row % 16)
      frame = np.pad(img, ((0, pad), (0, 0), (0, 0)))
      frame[-1, -1, 0] = pad
   frame_bytes = frame.tobytes()
   encrypted_bytes = AES.new(KEY, AES.MODE_ECB).encrypt(frame_bytes)
   encrypted_frame = np.frombuffer(encrypted_bytes, np.uint8).reshape(frame.shape)
   return encrypted_frame

if __name__ == "__main__":
   vidcap = cv2.VideoCapture('suzuki.mp4')
   print((vidcap.get(cv2.CAP_PROP_FRAME_WIDTH),vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
   fourcc = cv2.VideoWriter_fourcc(*'MP4V')
   out = cv2.VideoWriter('output.mp4',fourcc,vidcap.get(cv2.CAP_PROP_FPS),
                         (int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
   success,frame = vidcap.read()
   count = 0
   while success:
      frame = encrypt_frame(frame)
      out.write(frame)
      success,frame = vidcap.read()
      count +=1
      print(str(count / vidcap.get(cv2.CAP_PROP_FRAME_COUNT)*100) + "%")

   vidcap.release()
   out.release()

   clip_1 = VideoFileClip("output.mp4")
   clip_2 = VideoFileClip("suzuki.mp4")
   final_clip = clips_array([[clip_1,clip_2]])
   final_clip.write_videofile("final.mp4")

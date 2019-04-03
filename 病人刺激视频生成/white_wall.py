# 获得灰色的背景
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('white_wall.mp4',fourcc, 25.0, (960,540)) # 帧数可调, 注意后面的尺寸大小要一致

for white_wall_num in range(int(9.5*25)):
          white_wall = np.zeros([540,960,3])+200
          white_wall = white_wall.astype('u1')
          out.write(white_wall)

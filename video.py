# import cv2
# from fps import FPS

# fps = FPS()
# fps.start()
# cap = cv2.VideoCapture(0)
# frame_counter = 0
# while(True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     frame_counter += 1

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Display the resulting frame
#     cv2.imshow('frame', gray)
#     fps.update()
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#     if fps._numFrames == 300:
#         break
# # When everything done, release the capture
# fps.stop()
# print(fps.fps())
# cap.release()
# cv2.destroyAllWindows()

# import cv2
# from multiprocessing import Process, Queue
# from fps import FPS


# class VideoIn(Process):
#     def __init__(self, source, frames_q):
#         Process.__init__(self)
#         self.source = source
#         self.frames_q = frames_q
#         self.fps = FPS()

#     def run(self):
#         cap = cv2.VideoCapture(self.source)
#         # cap.set(3, 640)
#         # cap.set(4, 640)
#         self.fps.start()
#         while True:
#             ret, frame = cap.read()
#             self.frames_q.put(frame)
#             self.fps.update()
#             print('Reader FC = ', self.fps._numFrames)
#             if self.fps._numFrames == 300:
#                 self.fps.stop()
#                 print('For reader', self.fps.fps())
#                 break


# class VideoOut(Process):
#     def __init__(self, frames_q):
#         Process.__init__(self)
#         self.frames_q = frames_q
#         self.fps = FPS()

#     def run(self):
#         self.fps.start()
#         while True:
#             frame = None
#             if not self.frames_q.empty():
#                 frame = self.frames_q.get(False)
#             else:
#                 import time
#                 time.sleep(0.005)

#             if frame is not None:
#                 cv2.imshow('Video', frame)
#                 print('Writer FC = ', self.fps._numFrames)
#                 self.fps.update()
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#         self.fps.stop()
#         print('For writer', self.fps.fps())
#         cv2.destroyAllWindows()


# frames = Queue(1)
# inp = VideoIn(0, frames)
# out = VideoOut(frames)
# inp.start()
# out.start()
# inp.join()
# out.join()

import cv2
from multiprocessing import Manager, Process
from fps import FPS


class VideoPlayer:
    def __init__(self, source=0, dest=None):
        self._source = source
        self._dest = dest
        self._frame = None
        self._playing = False
        self._fps = FPS()

    def start(self):
        self._cap = cv2.VideoCapture(self._source)
        self._cap.set(3, 640)
        self._cap.set(4, 640)
        if self._dest is not None:
            width = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
            height = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
            fps = int(self._cap.get(cv2.CAP_PROP_FPS))
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self._out = cv2.VideoWriter(
                self._dest, fourcc, fps, (width, height))
        self._playing = True
        self._fps.start()
        while self._playing:
            self.read_frame()
            self.process_frame()
            self.write_frame()
        self._fps.stop()
        print(self._fps.fps())

    def stop(self):
        self._playing = False
        self._cap.release()
        self._out.release()
        cv2.destroyAllWindows()

    def read_frame(self):
        ret, frame = self._cap.read()
        self._frame = frame
        self._fps.update()

    def process_frame(self):
        pass

    def write_frame(self):
        self.show_frame()
        if self._dest is not None:
            self.save_frame()

    def show_frame(self):
        cv2.imshow('Video', self._frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.stop()

    def save_frame(self):
        self._out.write(self._frame)


player = VideoPlayer(dest='vid.mp4')
player.start()

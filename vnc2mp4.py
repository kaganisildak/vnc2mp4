import sys, time, os, signal
import numpy as np
from PIL import Image, ImageDraw
import cv2
from vncdotool import api


def record(output,host,fps,password=None):
    print("Start Recording")
    pid = 0
    retval = 0
    cli = api.connect(host,password=password)
    cli.refreshScreen(False)
    videodims = cli.screen.size
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')    
    frame = int(fps)
    video = cv2.VideoWriter(output,fourcc, frame,videodims)
    p_start = time.time()
    try:
        def sigint_handler(sig, frame):
            raise KeyboardInterrupt
        signal.signal(signal.SIGINT, sigint_handler)
        count = 0
        try:
            while 1:
                elapse = int()
                start = time.time()
                for i in range(0,frame):          
                    cli.refreshScreen(False)
                    imtemp = cli.screen.copy()
                    video.write(cv2.cvtColor(np.array(imtemp), cv2.COLOR_RGB2BGR))
                stop = time.time()
                elapse = stop-start
                print("Frame Process : " + str(elapse))
                if elapse < 1:
                    time.sleep(1-elapse)
                count +=1
        finally:
            p_stop = time.time()
            print(p_stop-p_start)
            video.release()
            cli.disconnect()
            print("Stop Recording")
    except KeyboardInterrupt:
        pass
    if pid:
        os.killpg(os.getpgid(pid), signal.SIGTERM)

    return retval

def main(args):
    # python3 vnc2mp4.py output.mp4 host:port fps password[OPTIONAL]
    if len(args) < 3:
        print("Missing parameters")
        sys.exit()
    else:    
        output = args[0]
        host = args[1]
        fps = args[2]
        password = None
        if len(args) == 4 : password=args[3]
    record(output=output,host=host,fps=fps,password=password)


if __name__ == "__main__": sys.exit(main(sys.argv[1:]))
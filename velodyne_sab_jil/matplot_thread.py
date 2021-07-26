import matplotlib.pyplot as plt
import time
from multiprocessing import Queue
import threading

def TapHistplots():
    ##  for item in ['str1']:
# # it behaves as expected if the line above is used instead of the one below
    for item in ['str1','str2']:
        otheritem = 1
        TapHistQueue.put((item, otheritem))
        makeTapHist().start()

class makeTapHist(threading.Thread):
    def run(self):
        item, otheritem = TapHistQueue.get()
        fig = FigureQueue.get()
        FigureQueue.put(fig+1)
        print( item+':'+str(fig)+'\n',)
        time.sleep(1.3)
        plt.figure(fig) # comment out this line and it behaves as expected
        plt.close(fig)

TapHistQueue = Queue.Queue(0)
FigureQueue = Queue.Queue(0)
def main():
    start = time.time()
    """Code in here runs only when this module is run directly"""
    FigureQueue.put(1)
    TapHistplots()
    while threading.activeCount()>1:
        time.sleep(1)
        print('waiting on %d threads\n' % (threading.activeCount()-1)),
    print( '%ds elapsed' % (time.time()-start))

if __name__ == '__main__':
    main()
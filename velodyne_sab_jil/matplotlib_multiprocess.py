# Library packages needed
import numpy as np
import datetime
import sys
import queue
import multiprocessing

# Plot related packages
import matplotlib.pyplot as plt


def showImage(img: np.ndarray, title: str = str(datetime.datetime.today())):
    """Show an image in a new process without blocking. Usefull for debugging.

    Args:
        img (np.ndarray): Image to be shown
        title (str, optional): Title to be shown. Defaults to
    str(datetime.datetime.today()).
    """

    def plot(q, title):
        fig = plt.figure()
        fig.suptitle(title)
        try:
            q.get(True, 2.0)  # Wait a couple of seconds
        except queue.Empty:
            print('Not image received to plot...quitting')
            sys.exit()

        plt.imshow(img)
        plt.show()
        sys.exit()

    # Create a queue to share data between process
    q = multiprocessing.Queue()

    # Create and start the process
    proc = multiprocessing.Process(None, plot, args=(q, title))
    proc.start()
    q.put(img)
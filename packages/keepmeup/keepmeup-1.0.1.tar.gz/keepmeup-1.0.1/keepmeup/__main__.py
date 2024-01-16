import multiprocessing
from keepui import KeepUI

if __name__ == '__main__':
    p1 = multiprocessing.Process(target = KeepUI)
    p1.start()
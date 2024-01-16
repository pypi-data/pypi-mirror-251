import multiprocessing
from keepui import KeepUI

p1 = multiprocessing.Process(target = KeepUI)
p1.start()
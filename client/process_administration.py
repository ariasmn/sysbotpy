import psutil

class Process:

    def __init__(self, name, mem):
        self.name = name
        self.mem = mem


def sendProcesses():
    running_process_list = []
    for proc in psutil.process_iter():
      p = Process(proc.name(), proc.memory_percent())
      running_process_list.append(p)
    running_process_list.sort(key=lambda x: x.mem, reverse=True)
    return running_process_list
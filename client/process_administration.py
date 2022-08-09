import psutil


class Process:

    def __init__(self, name, mem):
        self.name = name
        self.mem = mem


def send_processes():
    running_process_list = []
    for proc in psutil.process_iter():
        p = Process(proc.name(), proc.memory_percent())
        running_process_list.append(p)
        # what to sort from. Using lambda function so you don´t have to define
        # another function.
    running_process_list.sort(key=lambda x: x.mem, reverse=True)
    return running_process_list[:10]

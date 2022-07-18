from os.path import isfile, isdir, split, join as pjoin
from os import listdir
from fnmatch import filter
from render import RenderGames

class SensorCom:
    """
    Basic constructs for shaping data.
    """

    def read_file(self, file_path: str) -> str:
        """
        Read data from file and return string
        """
        sys_file = open(file_path, "r")
        data = str(sys_file.readline())
        sys_file.close()
        return data

    def get_cpu_temp(self, file_path: str) -> float:
        """
        Read cpu temperature
        """
        return float(round(int(self.read_file(file_path))/1000, 2))

    def get_freq(self, file_path: str) -> int:
        """
        Read gpu/cpu frequency in kHz
        """
        return int(self.read_file(file_path))/1000

    def list_dir(self, dir_path: str, pattern: str) -> list:
        """
        Return list of directories in given path
        """
        return filter([d for d in listdir(dir_path) if isdir(pjoin(dir_path, d))], pattern)


class SensorData:
    """
    class that actually gets data from specified paths.
    Setting custom paths is possible.
    """

    def __init__(self):
        self.sc = SensorCom()
        self.cpu_freq_dir = '/sys/devices/system/cpu'
        self.thermal_dir = '/sys/class/thermal'
        self.gpu_dir = '/sys/class/devfreq'

    def gpu_freq(self) -> list:
        """
        Return GPU freq array min/cur/max in MHz
        """
        if not isdir(self.gpu_dir):
            print('Error: GPU parent dir not found')
            return

        gpu_list = self.sc.list_dir(self.gpu_dir, '*.gpu')
        gpu_list.sort()
        gpu_freq = [
            'min_freq',
            'cur_freq',
            'max_freq',
            ]
        gpu = []
        for g in gpu_list:
            gpu_line = []
            gpu_line.append(g)

            for i in gpu_freq:
                gpu_line.append(self.sc.get_freq(pjoin(self.gpu_dir, g, i))/1000)
            gpu.append(gpu_line)

        return gpu

    def cpu_freq(self) -> list:
        """
        List all cpus
        get min/cur/max frequencies
        return 2d array of above
        """
        cpu_features = [
            'cpufreq/cpuinfo_min_freq',
            'cpufreq/cpuinfo_cur_freq',
            'cpufreq/cpuinfo_max_freq',
        ]

        cpu_list = self.sc.list_dir(self.cpu_freq_dir, 'cpu[0-9]*')
        cpu_list.sort()
        cpu = []
        for c in cpu_list:
            cpu_line = []
            cpu_line.append(c)
            for cf in cpu_features:
                cpu_line.append(
                    self.sc.get_freq(
                        pjoin(self.cpu_freq_dir, c, cf)
                    )
                )
            cpu.append(cpu_line)
        return cpu
            
    def get_thermal(self) -> list:
        """
        Get list of all thermal devices
        """
        thermal_list = self.sc.list_dir(self.thermal_dir, 'thermal_zone[0-9]*')
        thermal_list.sort()
        thermal = []
        for t in thermal_list:
            thermal_line = []
            thermal_line.append(t)
            thermal_line.append(
                    self.sc.get_cpu_temp(pjoin(self.thermal_dir, t, 'temp'))
            )
            thermal.append(thermal_line)
        return thermal


import logging

def main():
    logging.basicConfig(
            level=logging.DEBUG,
            format="[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
    )
    template_path = pjoin('html', 'template.html')
    style_path = pjoin('html', 'style.css')
    sd = SensorData()
    rg = RenderGames()
    body = ""
    for l in [sd.gpu_freq(), sd.cpu_freq(), sd.get_thermal()]:
        body += rg.render_list(l)
    rg.merge_template(template_path, style_path, body, 'System stats')

if __name__ == '__main__':
    main()


import os
import platform
import socket
import re
import uuid
import time
import subprocess

def get_windows_logo():
    return r"""


                               ,,,        ,,,                                     
                             ,WWWW,    ,WWWW,                                  
                             WWWWWW,  ,WWWWWW                                  
                             WWWWWW,  ,WWWWWW                                  
                             WWWWWW,  ,WWWWWW                                  
                             WWWWWW,  ,WWWWWW                                  
                             WWWWWW,  ,WWWWWW                                  
                             WWWWWW,  ,WWWWWW                                  

                             ,WWWW,    ,WWWW,                                  
                             WWWWWW,  ,WWWWWW                                  
                             WWWWWW,  ,WWWWWW                                  
                             WWWWWW,  ,WWWWWW                                  
                             WWWWWW,  ,WWWWWW                                  
                             WWWWWW,  ,WWWWWW                                  
                             'YVYY'    'YVYY'                                  


"""

def type_text(text, delay=0.001):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def get_centered_text(text, width):
    lines = text.split('\n')
    centered_lines = [line.center(width) for line in lines]
    return '\n'.join(centered_lines)

def get_system_info():
    info = {}
    info['OS'] = f"{platform.system()} {platform.release()} {platform.version()}"
    info['Architecture'] = platform.machine()
    info['Hostname'] = socket.gethostname()

    try:
        cpu_info = subprocess.check_output('wmic cpu get name', shell=True).decode().strip().split('\n')[1]
        info['CPU'] = cpu_info
    except Exception:
        info['CPU'] = platform.processor()

    info['CPU Cores'] = os.cpu_count()

    try:
        ram_info = subprocess.check_output('wmic computersystem get totalphysicalmemory', shell=True).decode().strip().split('\n')[1]
        total_ram_gb = round(int(ram_info) / (1024**3), 2)
        free_ram_info = subprocess.check_output('wmic os get freephysicalmemory', shell=True).decode().strip().split('\n')[1]
        free_ram_gb = round(int(free_ram_info) / (1024**2), 2)
        info['RAM'] = f"{total_ram_gb} GB (Free: {free_ram_gb} GB)"
    except Exception:
        info['RAM'] = 'N/A'

    try:
        disk_info = subprocess.check_output('wmic logicaldisk get size,freespace,caption', shell=True).decode().strip().split('\n')
        disks = []
        for line in disk_info[1:]:
            if line.strip():
                parts = line.split()
                drive = parts[0]
                free_gb = round(int(parts[1]) / (1024**3), 2)
                size_gb = round(int(parts[2]) / (1024**3), 2)
                disks.append(f"{drive} {size_gb} GB (Free: {free_gb} GB)")
        info['Disk'] = ', '.join(disks)
    except Exception:
        info['Disk'] = 'N/A'

    return info

def main():
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80

    logo = get_windows_logo()
    centered_logo = get_centered_text(logo, terminal_width)
    type_text(centered_logo)

    info = get_system_info()
    info_text = "\n".join([f"{key}: {value}" for key, value in info.items()])
    centered_info = get_centered_text(info_text, terminal_width)
    
    type_text(centered_info)

if __name__ == "__main__":
    main()

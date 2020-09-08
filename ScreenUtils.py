import os
import numpy as np
from PIL import Image
from config import config


def get_screen():
    device_id_flag = f'-s {config.device}' if config.device is not None else ''
    cmd_prefix = f'adb {device_id_flag}'
    filename = config.adb['filename']
    os.system(f'{cmd_prefix} shell screencap -p /sdcard/{filename}')
    os.system(f'{cmd_prefix} pull /sdcard/{filename} . > /dev/null')
    return np.asarray(Image.open(filename))[config.yTop:config.yBottom, config.xLeft:config.xRight, :3]

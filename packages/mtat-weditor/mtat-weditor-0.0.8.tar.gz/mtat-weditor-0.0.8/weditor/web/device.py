# coding: utf-8
#

import abc

import adbutils
import uiautomator2 as u2
import wda
from logzero import logger
from PIL import Image
from tidevice import Usbmux, ConnectionType

from . import uidumplib
from .proto import PlatformEnum


class DeviceMeta(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def screenshot(self) -> Image.Image:
        pass

    def dump_hierarchy(self) -> str:
        pass

    @abc.abstractproperty
    def device(self):
        pass


class _AndroidADB(DeviceMeta):
    def __init__(self, device_url: str):
        if not device_url:
            self._d = adbutils.device()
        else:
            self._d = adbutils.device(device_url)
    
    def screenshot(self) -> Image:
        return self._d.screenshot()
    
    def dump_hierarchy(self) -> str:
        return self._d.dump_hierarchy()
    
    def dump_hierarchy2(self):
        current = self._d.app_current()
        page_xml = self._d.dump_hierarchy()
        page_json = uidumplib.android_hierarchy_to_json(
            page_xml.encode('utf-8'))
        return {
            "xmlHierarchy": page_xml,
            "jsonHierarchy": page_json,
            "activity": current.activity,
            "packageName": current.package,
            "windowSize": self._d.window_size(),
        }

    @property
    def device(self):
        return self._d
        
class _AndroidUiautomatorDevice(DeviceMeta):
    def __init__(self, device_url):
        d = u2.connect(device_url)
        # 登陆界面无法截图，就先返回空图片
        d.settings["fallback_to_blank_screenshot"] = True
        self._d = d

    def screenshot(self):
        return self._d.screenshot()

    def dump_hierarchy(self):
        return uidumplib.get_android_hierarchy(self._d)

    def dump_hierarchy2(self):
        current = self._d.app_current()
        page_xml = self._d.dump_hierarchy(pretty=True)
        # 临时增加测试
        # import adbutils
        page_json = uidumplib.android_hierarchy_to_json(
            page_xml.encode('utf-8'))
        return {
            "xmlHierarchy": page_xml,
            "jsonHierarchy": page_json,
            "activity": current['activity'],
            "packageName": current['package'],
            "windowSize": self._d.window_size(),
        }

    @property
    def device(self):
        return self._d


class _AppleDevice(DeviceMeta):
    def __init__(self, device_url):
        logger.info("ios connect: %s", device_url)
        if device_url.startswith('http'):
            c = wda.Client(device_url)
        elif device_url != "":
            c = wda.USBClient(device_url)
        else:
            c = wda.USBClient()
        self._client = c
        # 使用截图尺寸和屏幕大小来获取实际的缩放比例
        # 不使用 c.scale，在部分设备上会出现获取的缩放比例是错误的
        self.__scale = max(c.screenshot().size) / max(c.window_size())
        self.__device_url = device_url

    def screenshot(self):
        self.check_wda()
        try:
            return self._client.screenshot(format='pillow')
        except:
            import tidevice
            return tidevice.Device().screenshot()

    def dump_hierarchy(self):
        self.check_wda()
        return uidumplib.get_ios_hierarchy(self._client, self.__scale)

    def dump_hierarchy2(self):
        self.check_wda()
        return {
            "jsonHierarchy":
            uidumplib.get_ios_hierarchy(self._client, self.__scale),
            "windowSize":
            self._client.window_size(),
        }

    def check_wda(self):
        try:
            self._client.status()
        except:
            if not self.__device_url.startswith('http'):
                logger.info("ios connect: %s", self.__device_url)
                c = wda.USBClient(self.__device_url)
                self._client = c
                self.__scale = c.scale

    @property
    def device(self):
        return self._client


cached_devices = {}


def connect_device(platform: PlatformEnum, device_url: str):
    """
    Returns:
        deviceId (string)
    """
    device_id = platform + ":" + device_url
    if platform == PlatformEnum.AndroidUIAutomator2:
        d = _AndroidUiautomatorDevice(device_url)
    elif platform == PlatformEnum.AndroidADB:
        d = _AndroidADB(device_url)
    elif platform == PlatformEnum.IOS:
        d = _AppleDevice(device_url)
    else:
        raise ValueError("Unknown platform", platform)

    cached_devices[device_id] = d
    return device_id


def get_device(id):
    d = cached_devices.get(id)
    if d is None:
        platform, uri = id.split(":", maxsplit=1)
        connect_device(platform, uri)
    return cached_devices[id]


def get_devices(platform):
    if platform == 'android' or platform == 'androidadb':
        ds = adbutils.adb.device_list()
        ds = [info.serial for info in ds]
    elif platform == 'ios':
        ds = Usbmux().device_list()
        ds = [info.udid for info in ds if info.conn_type == ConnectionType.USB]
    return ds



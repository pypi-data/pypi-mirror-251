import inspect
import os
import pytest
from kytest.utils.log import logger
from kytest.utils.config import config


class TestMain(object):
    """
    Support for app、web、http
    """

    def __init__(
            self,
            path: str = None,
            api_host: str = None,
            headers: dict = None,
            package: str = None,
            serial: str = None,
            bundle_id: str = None,
            udid: str = None,
            ocr_api: str = None,
            start: bool = True,
            web_host: str = None,
            cookies: list = None,
            state: str = None,
            browser: str = None,
            headless: bool = False,
            maximized: bool = False,
            window_size: list = None,
            rerun: int = 0,
            xdist: bool = False
    ):
        """
        @param path: 用例路径
        @param api_host: 域名，用于接口测试和web测试
        @param headers: 请求头，用于接口测试和web测试
        @param package: 安卓包名，通过adb shell pm list packages | grep 'xxx'获取
        @param serial：安卓设备序列号，通过adb devices获取
        @param bundle_id：IOS应用包名，通过tidevice applist | grep 'xxx'获取
        @param udid：IOS设备uuid，通过tidevice list获取
        @param ocr_api: ocr识别服务api，用于安卓和ios测试
        @param start: 是否自动启动应用，用于安卓和ios测试
        @param web_host: 域名，用于接口测试和web测试
        @param cookies: 用于带上登录态
        @param state: 用户带上登录态，其实就是把cookies存到一个文件中
        @param browser: 浏览器类型，支持chrome、webkit、firefox
        @param headless: 是否开启无头模式，默认不开启
        @param maximized: 浏览器是否全屏
        @param window_size: 屏幕分辨率，[1920, 1080]
        @param rerun: 失败重试次数
        @param xdist: 是否并发执行，应该是多进程
        """
        # 公共参数保存
        common_data = {
            "base_url": api_host,
            "web_base_url": web_host,
            "headers": headers,
            "ocr_service": ocr_api
        }
        config.set_common_dict(common_data)
        # app参数保存
        app_data = {
            "udid": udid,
            "bundle_id": bundle_id,
            "serial": serial,
            "package": package,
            "auto_start": start
        }
        config.set_app_dict(app_data)
        # web参数保存
        web_data = {
            "cookies": cookies,
            "state_file": state,
            "browser_name": browser,
            "headless": headless,
            "maximized": maximized,
            "window_size": window_size
        }
        config.set_web_dict(web_data)

        # 执行用例
        cmd_list = [
            '-sv',
            '--reruns', str(rerun),
            '--alluredir', 'report', '--clean-alluredir'
        ]

        if path is None:
            stack_t = inspect.stack()
            ins = inspect.getframeinfo(stack_t[1][0])
            file_dir = os.path.dirname(os.path.abspath(ins.filename))
            file_path = ins.filename
            if "\\" in file_path:
                this_file = file_path.split("\\")[-1]
            elif "/" in file_path:
                this_file = file_path.split("/")[-1]
            else:
                this_file = file_path
            path = os.path.join(file_dir, this_file)

        cmd_list.insert(0, path)

        if xdist:
            cmd_list.insert(1, '-n')
            cmd_list.insert(2, 'auto')

        logger.info(cmd_list)
        pytest.main(cmd_list)

        # 公共参数保存
        common_data = {
            "base_url": None,
            "web_base_url": None,
            "headers": None,
            "ocr_service": None
        }
        config.set_common_dict(common_data)
        # app参数保存
        app_data = {
            "udid": None,
            "bundle_id": None,
            "serial": None,
            "package": None,
            "auto_start": False
        }
        config.set_app_dict(app_data)
        # web参数保存
        web_data = {
            "cookies": None,
            "state_file": None,
            "browser_name": None,
            "headless": False,
            "maximized": False,
            "window_size": None
        }
        config.set_web_dict(web_data)


main = TestMain

if __name__ == '__main__':
    main()

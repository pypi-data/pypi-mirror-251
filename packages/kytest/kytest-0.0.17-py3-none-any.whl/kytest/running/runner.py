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
            rerun: int = 0,
            xdist: bool = False
    ):
        """
        @param path: 用例路径
        @param api_host: 域名，用于接口测试和web测试
        @param headers: 请求头，用于接口测试和web测试
        @param ocr_api: ocr识别服务api，用于安卓和ios测试
        @param start: 是否自动启动应用，用于安卓和ios测试
        @param web_host: 域名，用于接口测试和web测试
        @param cookies: 用于带上登录态
        @param state: 用户带上登录态，其实就是把cookies存到一个文件中
        @param browser: 浏览器类型，支持chrome、webkit、firefox
        @param headless: 是否开启无头模式，默认不开启
        @param rerun: 失败重试次数
        @param xdist: 是否并发执行，应该是多进程
        """
        # 公共参数保存
        config.set_common("base_url", api_host)
        config.set_common("web_base_url", web_host)
        config.set_common("headers", headers)
        config.set_common("ocr_service", ocr_api)
        # app参数保存
        config.set_app("udid", udid)
        config.set_app("bundle_id", bundle_id)
        config.set_app("serial", serial)
        config.set_app("package", package)
        config.set_app("auto_start", start)
        # web参数保存
        config.set_web("cookies", cookies)
        config.set_web("state_file", state)
        config.set_web("browser_name", browser)
        config.set_web("headless", headless)

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

        # api参数保存
        config.set_common("base_url", None)
        config.set_common("web_base_url", None)
        config.set_common('headers', None)
        config.set_common("ocr_service", None)
        # app参数保存
        config.set_app("udid", None)
        config.set_app("bundle_id", None)
        config.set_app("serial", None)
        config.set_app("package", None)
        config.set_app("auto_start", False)
        # web参数保存
        config.set_web("cookies", None)
        config.set_web("state_file", None)
        config.set_web("browser_name", None)
        config.set_web("headless", False)


main = TestMain

if __name__ == '__main__':
    main()

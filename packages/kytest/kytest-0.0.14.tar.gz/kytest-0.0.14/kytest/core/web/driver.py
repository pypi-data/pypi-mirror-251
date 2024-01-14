"""
@Author: kang.yang
@Date: 2023/5/12 20:49
"""
from kytest.utils.log import logger
from kytest.utils.common import screenshot_util
from playwright.sync_api import sync_playwright, expect


class WebDriver:

    def __init__(self, browserName: str, headless: bool = False, state: dict = None):
        logger.info("初始化playwright驱动")

        self.browserName = browserName
        self.headless = headless
        self.playwright = sync_playwright().start()
        if browserName == 'firefox':
            self.browser = self.playwright.firefox.launch(headless=headless)
        elif browserName == 'webkit':
            self.browser = self.playwright.webkit.launch(headless=headless)
        else:
            self.browser = self.playwright.chromium.launch(headless=headless)
        if state:
            self.context = self.browser.new_context(storage_state=state,
                                                    no_viewport=True)
        else:
            self.context = self.browser.new_context(no_viewport=True)
        self.page = self.context.new_page()

    def switch_tab(self, locator):
        logger.info("开始切换tab")
        with self.page.expect_popup() as popup_info:
            locator.click()
        self.page = popup_info.value

    def open(self, url):
        logger.info(f"访问页面: {url}")
        self.page.goto(url)

    def storage_state(self, path=None):
        logger.info("保存浏览器状态信息")
        if not path:
            raise ValueError("路径不能为空")
        self.context.storage_state(path=path)

    @property
    def page_content(self):
        """获取页面内容"""
        logger.info("获取页面内容")
        content = self.page.content()
        logger.info(content)
        return content

    def set_cookies(self, cookies: list):
        logger.info("添加cookie并刷新页面")
        self.context.add_cookies(cookies)
        self.page.reload()

    def screenshot(self, file_name=None):
        return screenshot_util(self.page,
                               file_name=file_name)

    def close(self):
        logger.info("关闭浏览器")
        self.page.close()
        self.context.close()
        self.browser.close()
        self.playwright.stop()

    def assert_title(self, title: str, timeout: int = 5):
        logger.info(f"断言页面标题等于: {title}")
        expect(self.page).to_have_title(title,
                                        timeout=timeout * 1000)

    def assert_url(self, url: str, timeout: int = 5):
        logger.info(f"断言页面url等于: {url}")
        expect(self.page).to_have_url(url,
                                      timeout=timeout * 1000)


if __name__ == '__main__':
    pass



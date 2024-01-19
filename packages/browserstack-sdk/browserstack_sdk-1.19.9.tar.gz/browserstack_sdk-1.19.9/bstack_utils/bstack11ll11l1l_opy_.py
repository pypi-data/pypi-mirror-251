# coding: UTF-8
import sys
bstack1l1ll_opy_ = sys.version_info [0] == 2
bstack1l1llll_opy_ = 2048
bstack1l1ll11_opy_ = 7
def bstack111111l_opy_ (bstack111lll_opy_):
    global bstack1l1ll1l_opy_
    bstack1ll1l_opy_ = ord (bstack111lll_opy_ [-1])
    bstack1llll_opy_ = bstack111lll_opy_ [:-1]
    bstack1lllll1_opy_ = bstack1ll1l_opy_ % len (bstack1llll_opy_)
    bstack11lll11_opy_ = bstack1llll_opy_ [:bstack1lllll1_opy_] + bstack1llll_opy_ [bstack1lllll1_opy_:]
    if bstack1l1ll_opy_:
        bstack11lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1llll_opy_ - (bstack1llll11_opy_ + bstack1ll1l_opy_) % bstack1l1ll11_opy_) for bstack1llll11_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack11lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l1llll_opy_ - (bstack1llll11_opy_ + bstack1ll1l_opy_) % bstack1l1ll11_opy_) for bstack1llll11_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack11lll1l_opy_)
class bstack1lll1l111_opy_:
    def __init__(self, handler):
        self._11111ll1l1_opy_ = None
        self.handler = handler
        self._11111ll111_opy_ = self.bstack11111ll1ll_opy_()
        self.patch()
    def patch(self):
        self._11111ll1l1_opy_ = self._11111ll111_opy_.execute
        self._11111ll111_opy_.execute = self.bstack11111ll11l_opy_()
    def bstack11111ll11l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack111111l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࠢᏯ"), driver_command)
            response = self._11111ll1l1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack111111l_opy_ (u"ࠣࡣࡩࡸࡪࡸࠢᏰ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._11111ll111_opy_.execute = self._11111ll1l1_opy_
    @staticmethod
    def bstack11111ll1ll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver
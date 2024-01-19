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
import sys
class bstack1l11l11l1l_opy_:
    def __init__(self, handler):
        self._11ll1l1ll1_opy_ = sys.stdout.write
        self._11ll1l1l11_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11ll1l1lll_opy_
        sys.stdout.error = self.bstack11ll1l1l1l_opy_
    def bstack11ll1l1lll_opy_(self, _str):
        self._11ll1l1ll1_opy_(_str)
        if self.handler:
            self.handler({bstack111111l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨຜ"): bstack111111l_opy_ (u"ࠪࡍࡓࡌࡏࠨຝ"), bstack111111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬພ"): _str})
    def bstack11ll1l1l1l_opy_(self, _str):
        self._11ll1l1l11_opy_(_str)
        if self.handler:
            self.handler({bstack111111l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫຟ"): bstack111111l_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬຠ"), bstack111111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨມ"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11ll1l1ll1_opy_
        sys.stderr.write = self._11ll1l1l11_opy_
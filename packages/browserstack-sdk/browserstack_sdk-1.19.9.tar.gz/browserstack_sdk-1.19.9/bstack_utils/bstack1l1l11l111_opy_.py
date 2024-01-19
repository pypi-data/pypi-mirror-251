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
from collections import deque
from bstack_utils.constants import *
class bstack1ll1111l11_opy_:
    def __init__(self):
        self._111l1111l1_opy_ = deque()
        self._111l11l11l_opy_ = {}
        self._111l111ll1_opy_ = False
    def bstack111l1111ll_opy_(self, test_name, bstack111l111l1l_opy_):
        bstack1111llll1l_opy_ = self._111l11l11l_opy_.get(test_name, {})
        return bstack1111llll1l_opy_.get(bstack111l111l1l_opy_, 0)
    def bstack111l111l11_opy_(self, test_name, bstack111l111l1l_opy_):
        bstack111l111lll_opy_ = self.bstack111l1111ll_opy_(test_name, bstack111l111l1l_opy_)
        self.bstack111l11111l_opy_(test_name, bstack111l111l1l_opy_)
        return bstack111l111lll_opy_
    def bstack111l11111l_opy_(self, test_name, bstack111l111l1l_opy_):
        if test_name not in self._111l11l11l_opy_:
            self._111l11l11l_opy_[test_name] = {}
        bstack1111llll1l_opy_ = self._111l11l11l_opy_[test_name]
        bstack111l111lll_opy_ = bstack1111llll1l_opy_.get(bstack111l111l1l_opy_, 0)
        bstack1111llll1l_opy_[bstack111l111l1l_opy_] = bstack111l111lll_opy_ + 1
    def bstack1l11ll1l_opy_(self, bstack111l11l111_opy_, bstack111l11l1l1_opy_):
        bstack1111lllll1_opy_ = self.bstack111l111l11_opy_(bstack111l11l111_opy_, bstack111l11l1l1_opy_)
        bstack111l111111_opy_ = bstack11ll11l11l_opy_[bstack111l11l1l1_opy_]
        bstack1111llllll_opy_ = bstack111111l_opy_ (u"ࠤࡾࢁ࠲ࢁࡽ࠮ࡽࢀࠦ᎖").format(bstack111l11l111_opy_, bstack111l111111_opy_, bstack1111lllll1_opy_)
        self._111l1111l1_opy_.append(bstack1111llllll_opy_)
    def bstack11111lll_opy_(self):
        return len(self._111l1111l1_opy_) == 0
    def bstack1lllllll11_opy_(self):
        bstack111l11l1ll_opy_ = self._111l1111l1_opy_.popleft()
        return bstack111l11l1ll_opy_
    def capturing(self):
        return self._111l111ll1_opy_
    def bstack1111l111l_opy_(self):
        self._111l111ll1_opy_ = True
    def bstack1l1ll1l1l1_opy_(self):
        self._111l111ll1_opy_ = False
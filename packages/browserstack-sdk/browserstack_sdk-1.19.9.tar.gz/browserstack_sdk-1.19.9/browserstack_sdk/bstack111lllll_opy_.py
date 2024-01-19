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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack1ll111l1l1_opy_ as bstack1lll111lll_opy_
from browserstack_sdk.bstack1l1111ll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1111l1111_opy_
class bstack11l11ll11_opy_:
    def __init__(self, args, logger, bstack1l11111111_opy_, bstack11llll1ll1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1l11111111_opy_ = bstack1l11111111_opy_
        self.bstack11llll1ll1_opy_ = bstack11llll1ll1_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1lll1lll1_opy_ = []
        self.bstack11lllll111_opy_ = None
        self.bstack11l111ll_opy_ = []
        self.bstack11lllllll1_opy_ = self.bstack1ll1ll11l1_opy_()
        self.bstack1ll1l1l1_opy_ = -1
    def bstack11llll11l_opy_(self, bstack11lllll11l_opy_):
        self.parse_args()
        self.bstack11lllll1l1_opy_()
        self.bstack11llll11ll_opy_(bstack11lllll11l_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    def bstack11llll1l11_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1ll1l1l1_opy_ = -1
        if bstack111111l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭෣") in self.bstack1l11111111_opy_:
            self.bstack1ll1l1l1_opy_ = int(self.bstack1l11111111_opy_[bstack111111l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ෤")])
        try:
            bstack1l1111111l_opy_ = [bstack111111l_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪ෥"), bstack111111l_opy_ (u"ࠩ࠰࠱ࡵࡲࡵࡨ࡫ࡱࡷࠬ෦"), bstack111111l_opy_ (u"ࠪ࠱ࡵ࠭෧")]
            if self.bstack1ll1l1l1_opy_ >= 0:
                bstack1l1111111l_opy_.extend([bstack111111l_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ෨"), bstack111111l_opy_ (u"ࠬ࠳࡮ࠨ෩")])
            for arg in bstack1l1111111l_opy_:
                self.bstack11llll1l11_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11lllll1l1_opy_(self):
        bstack11lllll111_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11lllll111_opy_ = bstack11lllll111_opy_
        return bstack11lllll111_opy_
    def bstack11111l11l_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            import importlib
            bstack11llllll11_opy_ = importlib.find_loader(bstack111111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨ෪"))
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1111l1111_opy_)
    def bstack11llll11ll_opy_(self, bstack11lllll11l_opy_):
        bstack1111ll1ll_opy_ = Config.bstack11l11l1ll_opy_()
        if bstack11lllll11l_opy_:
            self.bstack11lllll111_opy_.append(bstack111111l_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ෫"))
            self.bstack11lllll111_opy_.append(bstack111111l_opy_ (u"ࠨࡖࡵࡹࡪ࠭෬"))
        if bstack1111ll1ll_opy_.bstack11lllll1ll_opy_():
            self.bstack11lllll111_opy_.append(bstack111111l_opy_ (u"ࠩ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ෭"))
            self.bstack11lllll111_opy_.append(bstack111111l_opy_ (u"ࠪࡘࡷࡻࡥࠨ෮"))
        self.bstack11lllll111_opy_.append(bstack111111l_opy_ (u"ࠫ࠲ࡶࠧ෯"))
        self.bstack11lllll111_opy_.append(bstack111111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠪ෰"))
        self.bstack11lllll111_opy_.append(bstack111111l_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨ෱"))
        self.bstack11lllll111_opy_.append(bstack111111l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧෲ"))
        if self.bstack1ll1l1l1_opy_ > 1:
            self.bstack11lllll111_opy_.append(bstack111111l_opy_ (u"ࠨ࠯ࡱࠫෳ"))
            self.bstack11lllll111_opy_.append(str(self.bstack1ll1l1l1_opy_))
    def bstack11llllllll_opy_(self):
        bstack11l111ll_opy_ = []
        for spec in self.bstack1lll1lll1_opy_:
            bstack1l1llll1ll_opy_ = [spec]
            bstack1l1llll1ll_opy_ += self.bstack11lllll111_opy_
            bstack11l111ll_opy_.append(bstack1l1llll1ll_opy_)
        self.bstack11l111ll_opy_ = bstack11l111ll_opy_
        return bstack11l111ll_opy_
    def bstack1ll1ll11l1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11lllllll1_opy_ = True
            return True
        except Exception as e:
            self.bstack11lllllll1_opy_ = False
        return self.bstack11lllllll1_opy_
    def bstack1llll1l1l1_opy_(self, bstack11llllll1l_opy_, bstack11llll11l_opy_):
        bstack11llll11l_opy_[bstack111111l_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩ෴")] = self.bstack1l11111111_opy_
        multiprocessing.set_start_method(bstack111111l_opy_ (u"ࠪࡷࡵࡧࡷ࡯ࠩ෵"))
        if bstack111111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ෶") in self.bstack1l11111111_opy_:
            bstack1l1l11l1l1_opy_ = []
            manager = multiprocessing.Manager()
            bstack1lll11l11_opy_ = manager.list()
            for index, platform in enumerate(self.bstack1l11111111_opy_[bstack111111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ෷")]):
                bstack1l1l11l1l1_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack11llllll1l_opy_,
                                                           args=(self.bstack11lllll111_opy_, bstack11llll11l_opy_, bstack1lll11l11_opy_)))
            i = 0
            bstack11llll1lll_opy_ = len(self.bstack1l11111111_opy_[bstack111111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ෸")])
            for t in bstack1l1l11l1l1_opy_:
                os.environ[bstack111111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ෹")] = str(i)
                os.environ[bstack111111l_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩ෺")] = json.dumps(self.bstack1l11111111_opy_[bstack111111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ෻")][i % bstack11llll1lll_opy_])
                i += 1
                t.start()
            for t in bstack1l1l11l1l1_opy_:
                t.join()
            return list(bstack1lll11l11_opy_)
    @staticmethod
    def bstack1ll1l1l11l_opy_(driver, bstack1lll1ll1l_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack111111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ෼"), None)
        if item and getattr(item, bstack111111l_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪ࠭෽"), None) and not getattr(item, bstack111111l_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࡡࡧࡳࡳ࡫ࠧ෾"), False):
            logger.info(
                bstack111111l_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠤࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡸࡲࡩ࡫ࡲࡸࡣࡼ࠲ࠧ෿"))
            bstack11llll1l1l_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1lll111lll_opy_.bstack111l11111_opy_(driver, bstack11llll1l1l_opy_, item.name, item.module.__name__, item.path, bstack1lll1ll1l_opy_)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
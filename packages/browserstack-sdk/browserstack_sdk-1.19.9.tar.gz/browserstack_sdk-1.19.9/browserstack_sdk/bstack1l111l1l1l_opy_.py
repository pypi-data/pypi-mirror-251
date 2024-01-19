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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1l11111111_opy_, bstack11llll1ll1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1l11111111_opy_ = bstack1l11111111_opy_
        self.bstack11llll1ll1_opy_ = bstack11llll1ll1_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l1111l1ll_opy_(bstack11llll1111_opy_):
        bstack11llll11l1_opy_ = []
        if bstack11llll1111_opy_:
            tokens = str(os.path.basename(bstack11llll1111_opy_)).split(bstack111111l_opy_ (u"ࠢࡠࠤ฀"))
            camelcase_name = bstack111111l_opy_ (u"ࠣࠢࠥก").join(t.title() for t in tokens)
            suite_name, bstack1l1l1lll1l_opy_ = os.path.splitext(camelcase_name)
            bstack11llll11l1_opy_.append(suite_name)
        return bstack11llll11l1_opy_
    @staticmethod
    def bstack11llll111l_opy_(typename):
        if bstack111111l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧข") in typename:
            return bstack111111l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦฃ")
        return bstack111111l_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧค")
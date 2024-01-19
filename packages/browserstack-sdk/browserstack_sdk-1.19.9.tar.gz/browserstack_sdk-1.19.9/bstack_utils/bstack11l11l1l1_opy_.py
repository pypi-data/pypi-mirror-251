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
from browserstack_sdk.bstack111lllll_opy_ import bstack11l11ll11_opy_
from browserstack_sdk.bstack1l111l1l1l_opy_ import RobotHandler
def bstack1l111l11_opy_(framework):
    if framework.lower() == bstack111111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᄭ"):
        return bstack11l11ll11_opy_.version()
    elif framework.lower() == bstack111111l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨᄮ"):
        return RobotHandler.version()
    elif framework.lower() == bstack111111l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪᄯ"):
        import behave
        return behave.__version__
    else:
        return bstack111111l_opy_ (u"ࠫࡺࡴ࡫࡯ࡱࡺࡲࠬᄰ")
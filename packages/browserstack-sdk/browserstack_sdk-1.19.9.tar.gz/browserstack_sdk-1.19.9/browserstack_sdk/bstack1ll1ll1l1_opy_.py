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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1l1ll1ll_opy_ = {}
        bstack1l1l1111ll_opy_ = os.environ.get(bstack111111l_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩ೰"), bstack111111l_opy_ (u"ࠩࠪೱ"))
        if not bstack1l1l1111ll_opy_:
            return bstack1l1ll1ll_opy_
        try:
            bstack1l1l111l11_opy_ = json.loads(bstack1l1l1111ll_opy_)
            if bstack111111l_opy_ (u"ࠥࡳࡸࠨೲ") in bstack1l1l111l11_opy_:
                bstack1l1ll1ll_opy_[bstack111111l_opy_ (u"ࠦࡴࡹࠢೳ")] = bstack1l1l111l11_opy_[bstack111111l_opy_ (u"ࠧࡵࡳࠣ೴")]
            if bstack111111l_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥ೵") in bstack1l1l111l11_opy_ or bstack111111l_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥ೶") in bstack1l1l111l11_opy_:
                bstack1l1ll1ll_opy_[bstack111111l_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦ೷")] = bstack1l1l111l11_opy_.get(bstack111111l_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ೸"), bstack1l1l111l11_opy_.get(bstack111111l_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨ೹")))
            if bstack111111l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧ೺") in bstack1l1l111l11_opy_ or bstack111111l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥ೻") in bstack1l1l111l11_opy_:
                bstack1l1ll1ll_opy_[bstack111111l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦ೼")] = bstack1l1l111l11_opy_.get(bstack111111l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣ೽"), bstack1l1l111l11_opy_.get(bstack111111l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨ೾")))
            if bstack111111l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦ೿") in bstack1l1l111l11_opy_ or bstack111111l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦഀ") in bstack1l1l111l11_opy_:
                bstack1l1ll1ll_opy_[bstack111111l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧഁ")] = bstack1l1l111l11_opy_.get(bstack111111l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢം"), bstack1l1l111l11_opy_.get(bstack111111l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢഃ")))
            if bstack111111l_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࠢഄ") in bstack1l1l111l11_opy_ or bstack111111l_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧഅ") in bstack1l1l111l11_opy_:
                bstack1l1ll1ll_opy_[bstack111111l_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨആ")] = bstack1l1l111l11_opy_.get(bstack111111l_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࠥഇ"), bstack1l1l111l11_opy_.get(bstack111111l_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣഈ")))
            if bstack111111l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢഉ") in bstack1l1l111l11_opy_ or bstack111111l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧഊ") in bstack1l1l111l11_opy_:
                bstack1l1ll1ll_opy_[bstack111111l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨഋ")] = bstack1l1l111l11_opy_.get(bstack111111l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥഌ"), bstack1l1l111l11_opy_.get(bstack111111l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ഍")))
            if bstack111111l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠨഎ") in bstack1l1l111l11_opy_ or bstack111111l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨഏ") in bstack1l1l111l11_opy_:
                bstack1l1ll1ll_opy_[bstack111111l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢഐ")] = bstack1l1l111l11_opy_.get(bstack111111l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ഑"), bstack1l1l111l11_opy_.get(bstack111111l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤഒ")))
            if bstack111111l_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥഓ") in bstack1l1l111l11_opy_:
                bstack1l1ll1ll_opy_[bstack111111l_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦഔ")] = bstack1l1l111l11_opy_[bstack111111l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧക")]
        except Exception as error:
            logger.error(bstack111111l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡦࡺࡡ࠻ࠢࠥഖ") +  str(error))
        return bstack1l1ll1ll_opy_
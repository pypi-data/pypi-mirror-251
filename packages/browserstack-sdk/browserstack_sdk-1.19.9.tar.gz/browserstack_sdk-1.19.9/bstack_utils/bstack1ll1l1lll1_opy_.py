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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack11lll1ll1l_opy_, bstack11ll111l1_opy_, get_host_info, bstack11lll1l111_opy_, bstack11lll11l11_opy_, bstack11l11ll11l_opy_, \
    bstack11l1ll111l_opy_, bstack11l1ll11ll_opy_, bstack1lll111l_opy_, bstack11ll111lll_opy_, bstack1ll111111_opy_, bstack1l11llll11_opy_
from bstack_utils.bstack11111lllll_opy_ import bstack11111lll1l_opy_
from bstack_utils.bstack1l11l1ll1l_opy_ import bstack1l11l1l11l_opy_
bstack1llllllllll_opy_ = [
    bstack111111l_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᑣ"), bstack111111l_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩᑤ"), bstack111111l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᑥ"), bstack111111l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᑦ"),
    bstack111111l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᑧ"), bstack111111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᑨ"), bstack111111l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᑩ")
]
bstack1llllll111l_opy_ = bstack111111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫᑪ")
logger = logging.getLogger(__name__)
class bstack111lll1l_opy_:
    bstack11111lllll_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l11llll11_opy_(class_method=True)
    def launch(cls, bs_config, bstack1lllllllll1_opy_):
        cls.bs_config = bs_config
        if not cls.bstack1llllll11l1_opy_():
            return
        cls.bstack1lllllll111_opy_()
        bstack11lll1ll11_opy_ = bstack11lll1l111_opy_(bs_config)
        bstack11ll1ll11l_opy_ = bstack11lll11l11_opy_(bs_config)
        data = {
            bstack111111l_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬᑫ"): bstack111111l_opy_ (u"࠭ࡪࡴࡱࡱࠫᑬ"),
            bstack111111l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭ᑭ"): bs_config.get(bstack111111l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᑮ"), bstack111111l_opy_ (u"ࠩࠪᑯ")),
            bstack111111l_opy_ (u"ࠪࡲࡦࡳࡥࠨᑰ"): bs_config.get(bstack111111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᑱ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack111111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᑲ"): bs_config.get(bstack111111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᑳ")),
            bstack111111l_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᑴ"): bs_config.get(bstack111111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᑵ"), bstack111111l_opy_ (u"ࠩࠪᑶ")),
            bstack111111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡡࡷ࡭ࡲ࡫ࠧᑷ"): datetime.datetime.now().isoformat(),
            bstack111111l_opy_ (u"ࠫࡹࡧࡧࡴࠩᑸ"): bstack11l11ll11l_opy_(bs_config),
            bstack111111l_opy_ (u"ࠬ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠨᑹ"): get_host_info(),
            bstack111111l_opy_ (u"࠭ࡣࡪࡡ࡬ࡲ࡫ࡵࠧᑺ"): bstack11ll111l1_opy_(),
            bstack111111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡲࡶࡰࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᑻ"): os.environ.get(bstack111111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧᑼ")),
            bstack111111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡴࡨࡶࡺࡴࠧᑽ"): os.environ.get(bstack111111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨᑾ"), False),
            bstack111111l_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡩ࡯࡯ࡶࡵࡳࡱ࠭ᑿ"): bstack11lll1ll1l_opy_(),
            bstack111111l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᒀ"): {
                bstack111111l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭ᒁ"): bstack1lllllllll1_opy_.get(bstack111111l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨᒂ"), bstack111111l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨᒃ")),
                bstack111111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᒄ"): bstack1lllllllll1_opy_.get(bstack111111l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᒅ")),
                bstack111111l_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᒆ"): bstack1lllllllll1_opy_.get(bstack111111l_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪᒇ"))
            }
        }
        config = {
            bstack111111l_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᒈ"): (bstack11lll1ll11_opy_, bstack11ll1ll11l_opy_),
            bstack111111l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᒉ"): cls.default_headers()
        }
        response = bstack1lll111l_opy_(bstack111111l_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᒊ"), cls.request_url(bstack111111l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴࠩᒋ")), data, config)
        if response.status_code != 200:
            os.environ[bstack111111l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩᒌ")] = bstack111111l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᒍ")
            os.environ[bstack111111l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᒎ")] = bstack111111l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᒏ")
            os.environ[bstack111111l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᒐ")] = bstack111111l_opy_ (u"ࠣࡰࡸࡰࡱࠨᒑ")
            os.environ[bstack111111l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪᒒ")] = bstack111111l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᒓ")
            bstack1llllll1lll_opy_ = response.json()
            if bstack1llllll1lll_opy_ and bstack1llllll1lll_opy_[bstack111111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᒔ")]:
                error_message = bstack1llllll1lll_opy_[bstack111111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᒕ")]
                if bstack1llllll1lll_opy_[bstack111111l_opy_ (u"࠭ࡥࡳࡴࡲࡶ࡙ࡿࡰࡦࠩᒖ")] == bstack111111l_opy_ (u"ࠧࡆࡔࡕࡓࡗࡥࡉࡏࡘࡄࡐࡎࡊ࡟ࡄࡔࡈࡈࡊࡔࡔࡊࡃࡏࡗࠬᒗ"):
                    logger.error(error_message)
                elif bstack1llllll1lll_opy_[bstack111111l_opy_ (u"ࠨࡧࡵࡶࡴࡸࡔࡺࡲࡨࠫᒘ")] == bstack111111l_opy_ (u"ࠩࡈࡖࡗࡕࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡆࡈࡒࡎࡋࡄࠨᒙ"):
                    logger.info(error_message)
                elif bstack1llllll1lll_opy_[bstack111111l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡖࡼࡴࡪ࠭ᒚ")] == bstack111111l_opy_ (u"ࠫࡊࡘࡒࡐࡔࡢࡗࡉࡑ࡟ࡅࡇࡓࡖࡊࡉࡁࡕࡇࡇࠫᒛ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack111111l_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡚ࠥࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡪࡦ࡯࡬ࡦࡦࠣࡨࡺ࡫ࠠࡵࡱࠣࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢᒜ"))
            return [None, None, None]
        logger.debug(bstack111111l_opy_ (u"࠭ࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪᒝ"))
        os.environ[bstack111111l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭ᒞ")] = bstack111111l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᒟ")
        bstack1llllll1lll_opy_ = response.json()
        if bstack1llllll1lll_opy_.get(bstack111111l_opy_ (u"ࠩ࡭ࡻࡹ࠭ᒠ")):
            os.environ[bstack111111l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᒡ")] = bstack1llllll1lll_opy_[bstack111111l_opy_ (u"ࠫ࡯ࡽࡴࠨᒢ")]
            os.environ[bstack111111l_opy_ (u"ࠬࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࡢࡊࡔࡘ࡟ࡄࡔࡄࡗࡍࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩᒣ")] = json.dumps({
                bstack111111l_opy_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨᒤ"): bstack11lll1ll11_opy_,
                bstack111111l_opy_ (u"ࠧࡱࡣࡶࡷࡼࡵࡲࡥࠩᒥ"): bstack11ll1ll11l_opy_
            })
        if bstack1llllll1lll_opy_.get(bstack111111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᒦ")):
            os.environ[bstack111111l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᒧ")] = bstack1llllll1lll_opy_[bstack111111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᒨ")]
        if bstack1llllll1lll_opy_.get(bstack111111l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᒩ")):
            os.environ[bstack111111l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ᒪ")] = str(bstack1llllll1lll_opy_[bstack111111l_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᒫ")])
        return [bstack1llllll1lll_opy_[bstack111111l_opy_ (u"ࠧ࡫ࡹࡷࠫᒬ")], bstack1llllll1lll_opy_[bstack111111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᒭ")], bstack1llllll1lll_opy_[bstack111111l_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᒮ")]]
    @classmethod
    @bstack1l11llll11_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack111111l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᒯ")] == bstack111111l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᒰ") or os.environ[bstack111111l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᒱ")] == bstack111111l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᒲ"):
            print(bstack111111l_opy_ (u"ࠧࡆ࡚ࡆࡉࡕ࡚ࡉࡐࡐࠣࡍࡓࠦࡳࡵࡱࡳࡆࡺ࡯࡬ࡥࡗࡳࡷࡹࡸࡥࡢ࡯ࠣࡖࡊࡗࡕࡆࡕࡗࠤ࡙ࡕࠠࡕࡇࡖࡘࠥࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࠥࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨᒳ"))
            return {
                bstack111111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᒴ"): bstack111111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᒵ"),
                bstack111111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᒶ"): bstack111111l_opy_ (u"࡙ࠫࡵ࡫ࡦࡰ࠲ࡦࡺ࡯࡬ࡥࡋࡇࠤ࡮ࡹࠠࡶࡰࡧࡩ࡫࡯࡮ࡦࡦ࠯ࠤࡧࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥࡳࡩࡨࡪࡷࠤ࡭ࡧࡶࡦࠢࡩࡥ࡮ࡲࡥࡥࠩᒷ")
            }
        else:
            cls.bstack11111lllll_opy_.shutdown()
            data = {
                bstack111111l_opy_ (u"ࠬࡹࡴࡰࡲࡢࡸ࡮ࡳࡥࠨᒸ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack111111l_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᒹ"): cls.default_headers()
            }
            bstack11l1l1llll_opy_ = bstack111111l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡹࡵࡰࠨᒺ").format(os.environ[bstack111111l_opy_ (u"ࠣࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠢᒻ")])
            bstack1lllll1ll1l_opy_ = cls.request_url(bstack11l1l1llll_opy_)
            response = bstack1lll111l_opy_(bstack111111l_opy_ (u"ࠩࡓ࡙࡙࠭ᒼ"), bstack1lllll1ll1l_opy_, data, config)
            if not response.ok:
                raise Exception(bstack111111l_opy_ (u"ࠥࡗࡹࡵࡰࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡱࡳࡹࠦ࡯࡬ࠤᒽ"))
    @classmethod
    def bstack1l11l1lll1_opy_(cls):
        if cls.bstack11111lllll_opy_ is None:
            return
        cls.bstack11111lllll_opy_.shutdown()
    @classmethod
    def bstack1ll111l1ll_opy_(cls):
        if cls.on():
            print(
                bstack111111l_opy_ (u"࡛ࠫ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠧᒾ").format(os.environ[bstack111111l_opy_ (u"ࠧࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠦᒿ")]))
    @classmethod
    def bstack1lllllll111_opy_(cls):
        if cls.bstack11111lllll_opy_ is not None:
            return
        cls.bstack11111lllll_opy_ = bstack11111lll1l_opy_(cls.bstack1llllll1l1l_opy_)
        cls.bstack11111lllll_opy_.start()
    @classmethod
    def bstack1l111l11ll_opy_(cls, bstack1l11l1l1ll_opy_, bstack1llllll1111_opy_=bstack111111l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬᓀ")):
        if not cls.on():
            return
        bstack11lllll1_opy_ = bstack1l11l1l1ll_opy_[bstack111111l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᓁ")]
        bstack1llllll1ll1_opy_ = {
            bstack111111l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᓂ"): bstack111111l_opy_ (u"ࠩࡗࡩࡸࡺ࡟ࡔࡶࡤࡶࡹࡥࡕࡱ࡮ࡲࡥࡩ࠭ᓃ"),
            bstack111111l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᓄ"): bstack111111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡡࡈࡲࡩࡥࡕࡱ࡮ࡲࡥࡩ࠭ᓅ"),
            bstack111111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᓆ"): bstack111111l_opy_ (u"࠭ࡔࡦࡵࡷࡣࡘࡱࡩࡱࡲࡨࡨࡤ࡛ࡰ࡭ࡱࡤࡨࠬᓇ"),
            bstack111111l_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᓈ"): bstack111111l_opy_ (u"ࠨࡎࡲ࡫ࡤ࡛ࡰ࡭ࡱࡤࡨࠬᓉ"),
            bstack111111l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᓊ"): bstack111111l_opy_ (u"ࠪࡌࡴࡵ࡫ࡠࡕࡷࡥࡷࡺ࡟ࡖࡲ࡯ࡳࡦࡪࠧᓋ"),
            bstack111111l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᓌ"): bstack111111l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡢࡉࡳࡪ࡟ࡖࡲ࡯ࡳࡦࡪࠧᓍ"),
            bstack111111l_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪᓎ"): bstack111111l_opy_ (u"ࠧࡄࡄࡗࡣ࡚ࡶ࡬ࡰࡣࡧࠫᓏ")
        }.get(bstack11lllll1_opy_)
        if bstack1llllll1111_opy_ == bstack111111l_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧᓐ"):
            cls.bstack1lllllll111_opy_()
            cls.bstack11111lllll_opy_.add(bstack1l11l1l1ll_opy_)
        elif bstack1llllll1111_opy_ == bstack111111l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᓑ"):
            cls.bstack1llllll1l1l_opy_([bstack1l11l1l1ll_opy_], bstack1llllll1111_opy_)
    @classmethod
    @bstack1l11llll11_opy_(class_method=True)
    def bstack1llllll1l1l_opy_(cls, bstack1l11l1l1ll_opy_, bstack1llllll1111_opy_=bstack111111l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩᓒ")):
        config = {
            bstack111111l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᓓ"): cls.default_headers()
        }
        response = bstack1lll111l_opy_(bstack111111l_opy_ (u"ࠬࡖࡏࡔࡖࠪᓔ"), cls.request_url(bstack1llllll1111_opy_), bstack1l11l1l1ll_opy_, config)
        bstack11ll1lll11_opy_ = response.json()
    @classmethod
    @bstack1l11llll11_opy_(class_method=True)
    def bstack1l111ll111_opy_(cls, bstack1l1l11111l_opy_):
        bstack1llllllll1l_opy_ = []
        for log in bstack1l1l11111l_opy_:
            bstack1llllllll11_opy_ = {
                bstack111111l_opy_ (u"࠭࡫ࡪࡰࡧࠫᓕ"): bstack111111l_opy_ (u"ࠧࡕࡇࡖࡘࡤࡒࡏࡈࠩᓖ"),
                bstack111111l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᓗ"): log[bstack111111l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᓘ")],
                bstack111111l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᓙ"): log[bstack111111l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᓚ")],
                bstack111111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡢࡶࡪࡹࡰࡰࡰࡶࡩࠬᓛ"): {},
                bstack111111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᓜ"): log[bstack111111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᓝ")],
            }
            if bstack111111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᓞ") in log:
                bstack1llllllll11_opy_[bstack111111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᓟ")] = log[bstack111111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᓠ")]
            elif bstack111111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᓡ") in log:
                bstack1llllllll11_opy_[bstack111111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᓢ")] = log[bstack111111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᓣ")]
            bstack1llllllll1l_opy_.append(bstack1llllllll11_opy_)
        cls.bstack1l111l11ll_opy_({
            bstack111111l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᓤ"): bstack111111l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᓥ"),
            bstack111111l_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧᓦ"): bstack1llllllll1l_opy_
        })
    @classmethod
    @bstack1l11llll11_opy_(class_method=True)
    def bstack1lllllll11l_opy_(cls, steps):
        bstack1lllll1llll_opy_ = []
        for step in steps:
            bstack1111111111_opy_ = {
                bstack111111l_opy_ (u"ࠪ࡯࡮ࡴࡤࠨᓧ"): bstack111111l_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡘࡊࡖࠧᓨ"),
                bstack111111l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᓩ"): step[bstack111111l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᓪ")],
                bstack111111l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᓫ"): step[bstack111111l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᓬ")],
                bstack111111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᓭ"): step[bstack111111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᓮ")],
                bstack111111l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᓯ"): step[bstack111111l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᓰ")]
            }
            if bstack111111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᓱ") in step:
                bstack1111111111_opy_[bstack111111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᓲ")] = step[bstack111111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᓳ")]
            elif bstack111111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᓴ") in step:
                bstack1111111111_opy_[bstack111111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᓵ")] = step[bstack111111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᓶ")]
            bstack1lllll1llll_opy_.append(bstack1111111111_opy_)
        cls.bstack1l111l11ll_opy_({
            bstack111111l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᓷ"): bstack111111l_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᓸ"),
            bstack111111l_opy_ (u"ࠧ࡭ࡱࡪࡷࠬᓹ"): bstack1lllll1llll_opy_
        })
    @classmethod
    @bstack1l11llll11_opy_(class_method=True)
    def bstack1ll1lllll_opy_(cls, screenshot):
        cls.bstack1l111l11ll_opy_({
            bstack111111l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᓺ"): bstack111111l_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᓻ"),
            bstack111111l_opy_ (u"ࠪࡰࡴ࡭ࡳࠨᓼ"): [{
                bstack111111l_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᓽ"): bstack111111l_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠧᓾ"),
                bstack111111l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᓿ"): datetime.datetime.utcnow().isoformat() + bstack111111l_opy_ (u"࡛ࠧࠩᔀ"),
                bstack111111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᔁ"): screenshot[bstack111111l_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨᔂ")],
                bstack111111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᔃ"): screenshot[bstack111111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᔄ")]
            }]
        }, bstack1llllll1111_opy_=bstack111111l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᔅ"))
    @classmethod
    @bstack1l11llll11_opy_(class_method=True)
    def bstack1llllll1ll_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l111l11ll_opy_({
            bstack111111l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᔆ"): bstack111111l_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫᔇ"),
            bstack111111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪᔈ"): {
                bstack111111l_opy_ (u"ࠤࡸࡹ࡮ࡪࠢᔉ"): cls.current_test_uuid(),
                bstack111111l_opy_ (u"ࠥ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠤᔊ"): cls.bstack1l11l11111_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack111111l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᔋ"), None) is None or os.environ[bstack111111l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᔌ")] == bstack111111l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᔍ"):
            return False
        return True
    @classmethod
    def bstack1llllll11l1_opy_(cls):
        return bstack1ll111111_opy_(cls.bs_config.get(bstack111111l_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᔎ"), False))
    @staticmethod
    def request_url(url):
        return bstack111111l_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧᔏ").format(bstack1llllll111l_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack111111l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᔐ"): bstack111111l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᔑ"),
            bstack111111l_opy_ (u"ࠫ࡝࠳ࡂࡔࡖࡄࡇࡐ࠳ࡔࡆࡕࡗࡓࡕ࡙ࠧᔒ"): bstack111111l_opy_ (u"ࠬࡺࡲࡶࡧࠪᔓ")
        }
        if os.environ.get(bstack111111l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᔔ"), None):
            headers[bstack111111l_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧᔕ")] = bstack111111l_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫᔖ").format(os.environ[bstack111111l_opy_ (u"ࠤࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠥᔗ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack111111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᔘ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack111111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᔙ"), None)
    @staticmethod
    def bstack1l11111l1l_opy_():
        if getattr(threading.current_thread(), bstack111111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᔚ"), None):
            return {
                bstack111111l_opy_ (u"࠭ࡴࡺࡲࡨࠫᔛ"): bstack111111l_opy_ (u"ࠧࡵࡧࡶࡸࠬᔜ"),
                bstack111111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᔝ"): getattr(threading.current_thread(), bstack111111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᔞ"), None)
            }
        if getattr(threading.current_thread(), bstack111111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᔟ"), None):
            return {
                bstack111111l_opy_ (u"ࠫࡹࡿࡰࡦࠩᔠ"): bstack111111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᔡ"),
                bstack111111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᔢ"): getattr(threading.current_thread(), bstack111111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᔣ"), None)
            }
        return None
    @staticmethod
    def bstack1l11l11111_opy_(driver):
        return {
            bstack11l1ll11ll_opy_(): bstack11l1ll111l_opy_(driver)
        }
    @staticmethod
    def bstack1llllll11ll_opy_(exception_info, report):
        return [{bstack111111l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᔤ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11llll111l_opy_(typename):
        if bstack111111l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧᔥ") in typename:
            return bstack111111l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᔦ")
        return bstack111111l_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧᔧ")
    @staticmethod
    def bstack1llllll1l11_opy_(func):
        def wrap(*args, **kwargs):
            if bstack111lll1l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l1111l1ll_opy_(test, hook_name=None):
        bstack1lllllll1ll_opy_ = test.parent
        if hook_name in [bstack111111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪᔨ"), bstack111111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧᔩ"), bstack111111l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ᔪ"), bstack111111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᔫ")]:
            bstack1lllllll1ll_opy_ = test
        scope = []
        while bstack1lllllll1ll_opy_ is not None:
            scope.append(bstack1lllllll1ll_opy_.name)
            bstack1lllllll1ll_opy_ = bstack1lllllll1ll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1lllll1lll1_opy_(hook_type):
        if hook_type == bstack111111l_opy_ (u"ࠤࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠢᔬ"):
            return bstack111111l_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢ࡫ࡳࡴࡱࠢᔭ")
        elif hook_type == bstack111111l_opy_ (u"ࠦࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠣᔮ"):
            return bstack111111l_opy_ (u"࡚ࠧࡥࡢࡴࡧࡳࡼࡴࠠࡩࡱࡲ࡯ࠧᔯ")
    @staticmethod
    def bstack1lllllll1l1_opy_(bstack1lll1lll1_opy_):
        try:
            if not bstack111lll1l_opy_.on():
                return bstack1lll1lll1_opy_
            if os.environ.get(bstack111111l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠦᔰ"), None) == bstack111111l_opy_ (u"ࠢࡵࡴࡸࡩࠧᔱ"):
                tests = os.environ.get(bstack111111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠧᔲ"), None)
                if tests is None or tests == bstack111111l_opy_ (u"ࠤࡱࡹࡱࡲࠢᔳ"):
                    return bstack1lll1lll1_opy_
                bstack1lll1lll1_opy_ = tests.split(bstack111111l_opy_ (u"ࠪ࠰ࠬᔴ"))
                return bstack1lll1lll1_opy_
        except Exception as exc:
            print(bstack111111l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡪࡸࡵ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴ࠽ࠤࠧᔵ"), str(exc))
        return bstack1lll1lll1_opy_
    @classmethod
    def bstack1l11ll11l1_opy_(cls, event: str, bstack1l11l1l1ll_opy_: bstack1l11l1l11l_opy_):
        bstack1l1l111111_opy_ = {
            bstack111111l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᔶ"): event,
            bstack1l11l1l1ll_opy_.bstack1l11l11ll1_opy_(): bstack1l11l1l1ll_opy_.bstack1l111lll1l_opy_(event)
        }
        bstack111lll1l_opy_.bstack1l111l11ll_opy_(bstack1l1l111111_opy_)
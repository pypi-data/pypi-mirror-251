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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack11l1l111l1_opy_, bstack1l11l1ll1_opy_, bstack1l1l1l111_opy_, bstack1ll1llllll_opy_, \
    bstack11l1ll1l1l_opy_
def bstack11lll11l_opy_(bstack11111l1l11_opy_):
    for driver in bstack11111l1l11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack111llll1l_opy_(driver, status, reason=bstack111111l_opy_ (u"ࠩࠪᏱ")):
    bstack1111ll1ll_opy_ = Config.bstack11l11l1ll_opy_()
    if bstack1111ll1ll_opy_.bstack11lllll1ll_opy_():
        return
    bstack11l1lll11_opy_ = bstack11l1lll1l_opy_(bstack111111l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭Ᏺ"), bstack111111l_opy_ (u"ࠫࠬᏳ"), status, reason, bstack111111l_opy_ (u"ࠬ࠭Ᏼ"), bstack111111l_opy_ (u"࠭ࠧᏵ"))
    driver.execute_script(bstack11l1lll11_opy_)
def bstack1ll1l11111_opy_(page, status, reason=bstack111111l_opy_ (u"ࠧࠨ᏶")):
    try:
        if page is None:
            return
        bstack1111ll1ll_opy_ = Config.bstack11l11l1ll_opy_()
        if bstack1111ll1ll_opy_.bstack11lllll1ll_opy_():
            return
        bstack11l1lll11_opy_ = bstack11l1lll1l_opy_(bstack111111l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ᏷"), bstack111111l_opy_ (u"ࠩࠪᏸ"), status, reason, bstack111111l_opy_ (u"ࠪࠫᏹ"), bstack111111l_opy_ (u"ࠫࠬᏺ"))
        page.evaluate(bstack111111l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᏻ"), bstack11l1lll11_opy_)
    except Exception as e:
        print(bstack111111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡽࢀࠦᏼ"), e)
def bstack11l1lll1l_opy_(type, name, status, reason, bstack11lll1lll_opy_, bstack11lll1l1_opy_):
    bstack11l1ll1l1_opy_ = {
        bstack111111l_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧᏽ"): type,
        bstack111111l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ᏾"): {}
    }
    if type == bstack111111l_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ᏿"):
        bstack11l1ll1l1_opy_[bstack111111l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭᐀")][bstack111111l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᐁ")] = bstack11lll1lll_opy_
        bstack11l1ll1l1_opy_[bstack111111l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᐂ")][bstack111111l_opy_ (u"࠭ࡤࡢࡶࡤࠫᐃ")] = json.dumps(str(bstack11lll1l1_opy_))
    if type == bstack111111l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᐄ"):
        bstack11l1ll1l1_opy_[bstack111111l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᐅ")][bstack111111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᐆ")] = name
    if type == bstack111111l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᐇ"):
        bstack11l1ll1l1_opy_[bstack111111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᐈ")][bstack111111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᐉ")] = status
        if status == bstack111111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᐊ") and str(reason) != bstack111111l_opy_ (u"ࠢࠣᐋ"):
            bstack11l1ll1l1_opy_[bstack111111l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᐌ")][bstack111111l_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᐍ")] = json.dumps(str(reason))
    bstack11l11l11_opy_ = bstack111111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨᐎ").format(json.dumps(bstack11l1ll1l1_opy_))
    return bstack11l11l11_opy_
def bstack11ll1lll_opy_(url, config, logger, bstack1ll11111l1_opy_=False):
    hostname = bstack1l11l1ll1_opy_(url)
    is_private = bstack1ll1llllll_opy_(hostname)
    try:
        if is_private or bstack1ll11111l1_opy_:
            file_path = bstack11l1l111l1_opy_(bstack111111l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᐏ"), bstack111111l_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᐐ"), logger)
            if os.environ.get(bstack111111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᐑ")) and eval(
                    os.environ.get(bstack111111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᐒ"))):
                return
            if (bstack111111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᐓ") in config and not config[bstack111111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᐔ")]):
                os.environ[bstack111111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᐕ")] = str(True)
                bstack11111l1ll1_opy_ = {bstack111111l_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ᐖ"): hostname}
                bstack11l1ll1l1l_opy_(bstack111111l_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᐗ"), bstack111111l_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫᐘ"), bstack11111l1ll1_opy_, logger)
    except Exception as e:
        pass
def bstack1l11l11l1_opy_(caps, bstack11111l1l1l_opy_):
    if bstack111111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᐙ") in caps:
        caps[bstack111111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᐚ")][bstack111111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨᐛ")] = True
        if bstack11111l1l1l_opy_:
            caps[bstack111111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᐜ")][bstack111111l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᐝ")] = bstack11111l1l1l_opy_
    else:
        caps[bstack111111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪᐞ")] = True
        if bstack11111l1l1l_opy_:
            caps[bstack111111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᐟ")] = bstack11111l1l1l_opy_
def bstack1111l1l11l_opy_(bstack1l11l11lll_opy_):
    bstack11111l1lll_opy_ = bstack1l1l1l111_opy_(threading.current_thread(), bstack111111l_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫᐠ"), bstack111111l_opy_ (u"ࠨࠩᐡ"))
    if bstack11111l1lll_opy_ == bstack111111l_opy_ (u"ࠩࠪᐢ") or bstack11111l1lll_opy_ == bstack111111l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᐣ"):
        threading.current_thread().testStatus = bstack1l11l11lll_opy_
    else:
        if bstack1l11l11lll_opy_ == bstack111111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᐤ"):
            threading.current_thread().testStatus = bstack1l11l11lll_opy_
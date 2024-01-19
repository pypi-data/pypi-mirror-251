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
import re
from bstack_utils.bstack1l1lll1l1_opy_ import bstack1111l1l11l_opy_
def bstack1111ll111l_opy_(fixture_name):
    if fixture_name.startswith(bstack111111l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᎼ")):
        return bstack111111l_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᎽ")
    elif fixture_name.startswith(bstack111111l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᎾ")):
        return bstack111111l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧᎿ")
    elif fixture_name.startswith(bstack111111l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᏀ")):
        return bstack111111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᏁ")
    elif fixture_name.startswith(bstack111111l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᏂ")):
        return bstack111111l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᏃ")
def bstack1111l1l1l1_opy_(fixture_name):
    return bool(re.match(bstack111111l_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࢂ࡭ࡰࡦࡸࡰࡪ࠯࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᏄ"), fixture_name))
def bstack1111l1l1ll_opy_(fixture_name):
    return bool(re.match(bstack111111l_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᏅ"), fixture_name))
def bstack1111ll11l1_opy_(fixture_name):
    return bool(re.match(bstack111111l_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᏆ"), fixture_name))
def bstack1111l1ll11_opy_(fixture_name):
    if fixture_name.startswith(bstack111111l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᏇ")):
        return bstack111111l_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᏈ"), bstack111111l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᏉ")
    elif fixture_name.startswith(bstack111111l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᏊ")):
        return bstack111111l_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᏋ"), bstack111111l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᏌ")
    elif fixture_name.startswith(bstack111111l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ꮝ")):
        return bstack111111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭Ꮞ"), bstack111111l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᏏ")
    elif fixture_name.startswith(bstack111111l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᏐ")):
        return bstack111111l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᏑ"), bstack111111l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᏒ")
    return None, None
def bstack1111l1lll1_opy_(hook_name):
    if hook_name in [bstack111111l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭Ꮣ"), bstack111111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᏔ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1111ll1l11_opy_(hook_name):
    if hook_name in [bstack111111l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᏕ"), bstack111111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᏖ")]:
        return bstack111111l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᏗ")
    elif hook_name in [bstack111111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᏘ"), bstack111111l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᏙ")]:
        return bstack111111l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᏚ")
    elif hook_name in [bstack111111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᏛ"), bstack111111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᏜ")]:
        return bstack111111l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᏝ")
    elif hook_name in [bstack111111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭Ꮮ"), bstack111111l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭Ꮯ")]:
        return bstack111111l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᏠ")
    return hook_name
def bstack1111l1llll_opy_(node, scenario):
    if hasattr(node, bstack111111l_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᏡ")):
        parts = node.nodeid.rsplit(bstack111111l_opy_ (u"ࠣ࡝ࠥᏢ"))
        params = parts[-1]
        return bstack111111l_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᏣ").format(scenario.name, params)
    return scenario.name
def bstack1111l1ll1l_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack111111l_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᏤ")):
            examples = list(node.callspec.params[bstack111111l_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᏥ")].values())
        return examples
    except:
        return []
def bstack1111ll1111_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1111ll1l1l_opy_(report):
    try:
        status = bstack111111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᏦ")
        if report.passed or (report.failed and hasattr(report, bstack111111l_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᏧ"))):
            status = bstack111111l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᏨ")
        elif report.skipped:
            status = bstack111111l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᏩ")
        bstack1111l1l11l_opy_(status)
    except:
        pass
def bstack111111l1l_opy_(status):
    try:
        bstack1111ll11ll_opy_ = bstack111111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᏪ")
        if status == bstack111111l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᏫ"):
            bstack1111ll11ll_opy_ = bstack111111l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᏬ")
        elif status == bstack111111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭Ꮽ"):
            bstack1111ll11ll_opy_ = bstack111111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᏮ")
        bstack1111l1l11l_opy_(bstack1111ll11ll_opy_)
    except:
        pass
def bstack1111l1l111_opy_(item=None, report=None, summary=None, extra=None):
    return
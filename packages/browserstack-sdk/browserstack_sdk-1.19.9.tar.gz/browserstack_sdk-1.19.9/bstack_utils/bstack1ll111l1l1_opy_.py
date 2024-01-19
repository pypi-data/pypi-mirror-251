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
import requests
import logging
from urllib.parse import urlparse
from datetime import datetime
from bstack_utils.constants import bstack11lll11111_opy_ as bstack11ll1ll1ll_opy_
from bstack_utils.helper import bstack11ll1l1l_opy_, bstack1llll1l11_opy_, bstack11lll1l111_opy_, bstack11lll11l11_opy_, bstack11ll111l1_opy_, get_host_info, bstack11lll1ll1l_opy_, bstack1lll111l_opy_, bstack1l11llll11_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack1l11llll11_opy_(class_method=False)
def _11lll11l1l_opy_(driver, bstack1lll1ll1l_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack111111l_opy_ (u"ࠬࡵࡳࡠࡰࡤࡱࡪ࠭ฅ"): caps.get(bstack111111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬฆ"), None),
        bstack111111l_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫง"): bstack1lll1ll1l_opy_.get(bstack111111l_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫจ"), None),
        bstack111111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨฉ"): caps.get(bstack111111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨช"), None),
        bstack111111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ซ"): caps.get(bstack111111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ฌ"), None)
    }
  except Exception as error:
    logger.debug(bstack111111l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡩࡹࡧࡩ࡭ࡵࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠ࠻ࠢࠪญ") + str(error))
  return response
def bstack1lllll11l_opy_(config):
  return config.get(bstack111111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧฎ"), False) or any([p.get(bstack111111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨฏ"), False) == True for p in config[bstack111111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬฐ")]])
def bstack1111l1lll_opy_(config, bstack111l1l1l_opy_):
  try:
    if not bstack1llll1l11_opy_(config):
      return False
    bstack11lll1l1l1_opy_ = config.get(bstack111111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪฑ"), False)
    bstack11lll11ll1_opy_ = config[bstack111111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧฒ")][bstack111l1l1l_opy_].get(bstack111111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬณ"), None)
    if bstack11lll11ll1_opy_ != None:
      bstack11lll1l1l1_opy_ = bstack11lll11ll1_opy_
    bstack11ll1llll1_opy_ = os.getenv(bstack111111l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫด")) is not None and len(os.getenv(bstack111111l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬต"))) > 0 and os.getenv(bstack111111l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ถ")) != bstack111111l_opy_ (u"ࠩࡱࡹࡱࡲࠧท")
    return bstack11lll1l1l1_opy_ and bstack11ll1llll1_opy_
  except Exception as error:
    logger.debug(bstack111111l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡩࡷ࡯ࡦࡺ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡩࡸࡹࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠ࠻ࠢࠪธ") + str(error))
  return False
def bstack11ll1ll1l_opy_(bstack11ll1ll111_opy_, test_tags):
  bstack11ll1ll111_opy_ = os.getenv(bstack111111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬน"))
  if bstack11ll1ll111_opy_ is None:
    return True
  bstack11ll1ll111_opy_ = json.loads(bstack11ll1ll111_opy_)
  try:
    include_tags = bstack11ll1ll111_opy_[bstack111111l_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪบ")] if bstack111111l_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫป") in bstack11ll1ll111_opy_ and isinstance(bstack11ll1ll111_opy_[bstack111111l_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬผ")], list) else []
    exclude_tags = bstack11ll1ll111_opy_[bstack111111l_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ฝ")] if bstack111111l_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧพ") in bstack11ll1ll111_opy_ and isinstance(bstack11ll1ll111_opy_[bstack111111l_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨฟ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack111111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡹࡥࡱ࡯ࡤࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡣࡱࡲ࡮ࡴࡧ࠯ࠢࡈࡶࡷࡵࡲࠡ࠼ࠣࠦภ") + str(error))
  return False
def bstack1l1l1ll1l1_opy_(config, bstack11ll1lll1l_opy_, bstack11lll1llll_opy_):
  bstack11lll1ll11_opy_ = bstack11lll1l111_opy_(config)
  bstack11ll1ll11l_opy_ = bstack11lll11l11_opy_(config)
  if bstack11lll1ll11_opy_ is None or bstack11ll1ll11l_opy_ is None:
    logger.error(bstack111111l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡳࡷࡱࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭ม"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack111111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧย"), bstack111111l_opy_ (u"ࠧࡼࡿࠪร")))
    data = {
        bstack111111l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ฤ"): config[bstack111111l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧล")],
        bstack111111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ฦ"): config.get(bstack111111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧว"), os.path.basename(os.getcwd())),
        bstack111111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡘ࡮ࡳࡥࠨศ"): bstack11ll1l1l_opy_(),
        bstack111111l_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫษ"): config.get(bstack111111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪส"), bstack111111l_opy_ (u"ࠨࠩห")),
        bstack111111l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩฬ"): {
            bstack111111l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡔࡡ࡮ࡧࠪอ"): bstack11ll1lll1l_opy_,
            bstack111111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧฮ"): bstack11lll1llll_opy_,
            bstack111111l_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩฯ"): __version__
        },
        bstack111111l_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨะ"): settings,
        bstack111111l_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡄࡱࡱࡸࡷࡵ࡬ࠨั"): bstack11lll1ll1l_opy_(),
        bstack111111l_opy_ (u"ࠨࡥ࡬ࡍࡳ࡬࡯ࠨา"): bstack11ll111l1_opy_(),
        bstack111111l_opy_ (u"ࠩ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠫำ"): get_host_info(),
        bstack111111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬิ"): bstack1llll1l11_opy_(config)
    }
    headers = {
        bstack111111l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪี"): bstack111111l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨึ"),
    }
    config = {
        bstack111111l_opy_ (u"࠭ࡡࡶࡶ࡫ࠫื"): (bstack11lll1ll11_opy_, bstack11ll1ll11l_opy_),
        bstack111111l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨุ"): headers
    }
    response = bstack1lll111l_opy_(bstack111111l_opy_ (u"ࠨࡒࡒࡗู࡙࠭"), bstack11ll1ll1ll_opy_ + bstack111111l_opy_ (u"ࠩ࠲ࡸࡪࡹࡴࡠࡴࡸࡲࡸฺ࠭"), data, config)
    bstack11ll1lll11_opy_ = response.json()
    if bstack11ll1lll11_opy_[bstack111111l_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ฻")]:
      parsed = json.loads(os.getenv(bstack111111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ฼"), bstack111111l_opy_ (u"ࠬࢁࡽࠨ฽")))
      parsed[bstack111111l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ฾")] = bstack11ll1lll11_opy_[bstack111111l_opy_ (u"ࠧࡥࡣࡷࡥࠬ฿")][bstack111111l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩเ")]
      os.environ[bstack111111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪแ")] = json.dumps(parsed)
      return bstack11ll1lll11_opy_[bstack111111l_opy_ (u"ࠪࡨࡦࡺࡡࠨโ")][bstack111111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩใ")], bstack11ll1lll11_opy_[bstack111111l_opy_ (u"ࠬࡪࡡࡵࡣࠪไ")][bstack111111l_opy_ (u"࠭ࡩࡥࠩๅ")]
    else:
      logger.error(bstack111111l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠨๆ") + bstack11ll1lll11_opy_[bstack111111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ็")])
      if bstack11ll1lll11_opy_[bstack111111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧ่ࠪ")] == bstack111111l_opy_ (u"ࠪࡍࡳࡼࡡ࡭࡫ࡧࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡵࡧࡳࡴࡧࡧ࠲้ࠬ"):
        for bstack11lll1l1ll_opy_ in bstack11ll1lll11_opy_[bstack111111l_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶ๊ࠫ")]:
          logger.error(bstack11lll1l1ll_opy_[bstack111111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ๋࠭")])
      return None, None
  except Exception as error:
    logger.error(bstack111111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠢ์") +  str(error))
    return None, None
def bstack1ll1l1l1l_opy_():
  if os.getenv(bstack111111l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬํ")) is None:
    return {
        bstack111111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ๎"): bstack111111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ๏"),
        bstack111111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ๐"): bstack111111l_opy_ (u"ࠫࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡮ࡡࡥࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠪ๑")
    }
  data = {bstack111111l_opy_ (u"ࠬ࡫࡮ࡥࡖ࡬ࡱࡪ࠭๒"): bstack11ll1l1l_opy_()}
  headers = {
      bstack111111l_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭๓"): bstack111111l_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࠨ๔") + os.getenv(bstack111111l_opy_ (u"ࠣࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙ࠨ๕")),
      bstack111111l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ๖"): bstack111111l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭๗")
  }
  response = bstack1lll111l_opy_(bstack111111l_opy_ (u"ࠫࡕ࡛ࡔࠨ๘"), bstack11ll1ll1ll_opy_ + bstack111111l_opy_ (u"ࠬ࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴ࠱ࡶࡸࡴࡶࠧ๙"), data, { bstack111111l_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ๚"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack111111l_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲࠥࡳࡡࡳ࡭ࡨࡨࠥࡧࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤࡦࡺࠠࠣ๛") + datetime.utcnow().isoformat() + bstack111111l_opy_ (u"ࠨ࡜ࠪ๜"))
      return {bstack111111l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ๝"): bstack111111l_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ๞"), bstack111111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ๟"): bstack111111l_opy_ (u"ࠬ࠭๠")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack111111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳࠦ࡯ࡧࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴ࠺ࠡࠤ๡") + str(error))
    return {
        bstack111111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ๢"): bstack111111l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ๣"),
        bstack111111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ๤"): str(error)
    }
def bstack1l11l111l_opy_(caps, options):
  try:
    bstack11ll1lllll_opy_ = caps.get(bstack111111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ๥"), {}).get(bstack111111l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ๦"), caps.get(bstack111111l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ๧"), bstack111111l_opy_ (u"࠭ࠧ๨")))
    if bstack11ll1lllll_opy_:
      logger.warn(bstack111111l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡅࡧࡶ࡯ࡹࡵࡰࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦ๩"))
      return False
    browser = caps.get(bstack111111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭๪"), bstack111111l_opy_ (u"ࠩࠪ๫")).lower()
    if browser != bstack111111l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ๬"):
      logger.warn(bstack111111l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢ๭"))
      return False
    browser_version = caps.get(bstack111111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭๮"), caps.get(bstack111111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ๯")))
    if browser_version and browser_version != bstack111111l_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺࠧ๰") and int(browser_version.split(bstack111111l_opy_ (u"ࠨ࠰ࠪ๱"))[0]) <= 94:
      logger.warn(bstack111111l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡬ࡸࡥࡢࡶࡨࡶࠥࡺࡨࡢࡰࠣ࠽࠹࠴ࠢ๲"))
      return False
    if not options is None:
      bstack11ll1ll1l1_opy_ = options.to_capabilities().get(bstack111111l_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ๳"), {})
      if bstack111111l_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨ๴") in bstack11ll1ll1l1_opy_.get(bstack111111l_opy_ (u"ࠬࡧࡲࡨࡵࠪ๵"), []):
        logger.warn(bstack111111l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣ๶"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack111111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡢ࡮࡬ࡨࡦࡺࡥࠡࡣ࠴࠵ࡾࠦࡳࡶࡲࡳࡳࡷࡺࠠ࠻ࠤ๷") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack11lll1111l_opy_ = config.get(bstack111111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ๸"), {})
    bstack11lll1111l_opy_[bstack111111l_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬ๹")] = os.getenv(bstack111111l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ๺"))
    bstack11lll111ll_opy_ = json.loads(os.getenv(bstack111111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ๻"), bstack111111l_opy_ (u"ࠬࢁࡽࠨ๼"))).get(bstack111111l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ๽"))
    caps[bstack111111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ๾")] = True
    if bstack111111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ๿") in caps:
      caps[bstack111111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ຀")][bstack111111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪກ")] = bstack11lll1111l_opy_
      caps[bstack111111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬຂ")][bstack111111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ຃")][bstack111111l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧຄ")] = bstack11lll111ll_opy_
    else:
      caps[bstack111111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭຅")] = bstack11lll1111l_opy_
      caps[bstack111111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧຆ")][bstack111111l_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪງ")] = bstack11lll111ll_opy_
  except Exception as error:
    logger.debug(bstack111111l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠰ࠣࡉࡷࡸ࡯ࡳ࠼ࠣࠦຈ") +  str(error))
def bstack111ll11l_opy_(driver, bstack11lll11lll_opy_):
  try:
    session = driver.session_id
    if session:
      bstack11lll1l11l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11lll1l11l_opy_ = False
      bstack11lll1l11l_opy_ = url.scheme in [bstack111111l_opy_ (u"ࠦ࡭ࡺࡴࡱࠤຉ"), bstack111111l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦຊ")]
      if bstack11lll1l11l_opy_:
        if bstack11lll11lll_opy_:
          logger.info(bstack111111l_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡬࡯ࡳࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡬ࡦࡹࠠࡴࡶࡤࡶࡹ࡫ࡤ࠯ࠢࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡤࡨ࡫࡮ࡴࠠ࡮ࡱࡰࡩࡳࡺࡡࡳ࡫࡯ࡽ࠳ࠨ຋"))
          driver.execute_async_script(bstack111111l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤࡂࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴ࡝ࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡴࡶࠣࡪࡳࠦ࠽ࠡࠪࠬࠤࡂࡄࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡷࡪࡰࡧࡳࡼ࠴ࡡࡥࡦࡈࡺࡪࡴࡴࡍ࡫ࡶࡸࡪࡴࡥࡳࠪࠪࡅ࠶࠷࡙ࡠࡖࡄࡔࡤ࡙ࡔࡂࡔࡗࡉࡉ࠭ࠬࠡࡨࡱ࠶࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡴࡶࠣࡩࠥࡃࠠ࡯ࡧࡺࠤࡈࡻࡳࡵࡱࡰࡉࡻ࡫࡮ࡵࠪࠪࡅ࠶࠷࡙ࡠࡈࡒࡖࡈࡋ࡟ࡔࡖࡄࡖ࡙࠭ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡷࡪࡰࡧࡳࡼ࠴ࡤࡪࡵࡳࡥࡹࡩࡨࡆࡸࡨࡲࡹ࠮ࡥࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡶࡸࠥ࡬࡮࠳ࠢࡀࠤ࠭࠯ࠠ࠾ࡀࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡭ࡳࡪ࡯ࡸ࠰ࡵࡩࡲࡵࡶࡦࡇࡹࡩࡳࡺࡌࡪࡵࡷࡩࡳ࡫ࡲࠩࠩࡄ࠵࠶࡟࡟ࡕࡃࡓࡣࡘ࡚ࡁࡓࡖࡈࡈࠬ࠲ࠠࡧࡰࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠬ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡩࡲ࠭࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢຌ"))
          logger.info(bstack111111l_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢ࡫ࡥࡸࠦࡳࡵࡣࡵࡸࡪࡪ࠮ࠣຍ"))
        else:
          driver.execute_script(bstack111111l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤࡪࠦ࠽ࠡࡰࡨࡻࠥࡉࡵࡴࡶࡲࡱࡊࡼࡥ࡯ࡶࠫࠫࡆ࠷࠱࡚ࡡࡉࡓࡗࡉࡅࡠࡕࡗࡓࡕ࠭ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡭ࡳࡪ࡯ࡸ࠰ࡧ࡭ࡸࡶࡡࡵࡥ࡫ࡉࡻ࡫࡮ࡵࠪࡨ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧຎ"))
      return bstack11lll11lll_opy_
  except Exception as e:
    logger.error(bstack111111l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࡪࡰࡪࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨຏ") + str(e))
    return False
def bstack111l11111_opy_(driver, class_name, name, module_name, path, bstack1lll1ll1l_opy_):
  try:
    bstack11llll1l1l_opy_ = [class_name] if not class_name is None else []
    bstack11lll111l1_opy_ = {
        bstack111111l_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤຐ"): True,
        bstack111111l_opy_ (u"ࠧࡺࡥࡴࡶࡇࡩࡹࡧࡩ࡭ࡵࠥຑ"): {
            bstack111111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦຒ"): name,
            bstack111111l_opy_ (u"ࠢࡵࡧࡶࡸࡗࡻ࡮ࡊࡦࠥຓ"): os.environ.get(bstack111111l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡗࡉࡘ࡚࡟ࡓࡗࡑࡣࡎࡊࠧດ")),
            bstack111111l_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡐࡢࡶ࡫ࠦຕ"): str(path),
            bstack111111l_opy_ (u"ࠥࡷࡨࡵࡰࡦࡎ࡬ࡷࡹࠨຖ"): [module_name, *bstack11llll1l1l_opy_, name],
        },
        bstack111111l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨທ"): _11lll11l1l_opy_(driver, bstack1lll1ll1l_opy_)
    }
    driver.execute_async_script(bstack111111l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡹࡴࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡁࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳ࡜ࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠱࡞࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡮ࡩࡴ࠰ࡵࡩࡸࠦ࠽ࠡࡰࡸࡰࡱࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡩࠤ࠭ࡧࡲࡨࡷࡰࡩࡳࡺࡳ࡜࠲ࡠ࠲ࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠫࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡮ࡴࡤࡰࡹ࠱ࡥࡩࡪࡅࡷࡧࡱࡸࡑ࡯ࡳࡵࡧࡱࡩࡷ࠮ࠧࡂ࠳࠴࡝ࡤ࡚ࡁࡑࡡࡗࡖࡆࡔࡓࡑࡑࡕࡘࡊࡘࠧ࠭ࠢࠫࡩࡻ࡫࡮ࡵࠫࠣࡁࡃࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡮ࡴࡤࡰࡹ࠱ࡸࡦࡶࡔࡳࡣࡱࡷࡵࡵࡲࡵࡧࡵࡈࡦࡺࡡࠡ࠿ࠣࡩࡻ࡫࡮ࡵ࠰ࡧࡩࡹࡧࡩ࡭࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡨࡪࡵ࠱ࡶࡪࡹࠠ࠾ࠢࡺ࡭ࡳࡪ࡯ࡸ࠰ࡷࡥࡵ࡚ࡲࡢࡰࡶࡴࡴࡸࡴࡦࡴࡇࡥࡹࡧ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠭ࡺࡨࡪࡵ࠱ࡶࡪࡹࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࢃࠊࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲࡸࡺࠠࡦࠢࡀࠤࡳ࡫ࡷࠡࡅࡸࡷࡹࡵ࡭ࡆࡸࡨࡲࡹ࠮ࠧࡂ࠳࠴࡝ࡤ࡚ࡅࡔࡖࡢࡉࡓࡊࠧ࠭ࠢࡾࠤࡩ࡫ࡴࡢ࡫࡯࠾ࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳ࡜࠲ࡠࠤࢂ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡭ࡳࡪ࡯ࡸ࠰ࡧ࡭ࡸࡶࡡࡵࡥ࡫ࡉࡻ࡫࡮ࡵࠪࡨ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࡪࡨࠣࠬࠦࡧࡲࡨࡷࡰࡩࡳࡺࡳ࡜࠲ࡠ࠲ࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠫࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠭࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࢀࠎࠥࠦࠠࠡࠤࠥࠦຘ"), bstack11lll111l1_opy_)
    logger.info(bstack111111l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤນ"))
  except Exception as bstack11lll1lll1_opy_:
    logger.error(bstack111111l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡪࡴࡸࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤບ") + str(path) + bstack111111l_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥປ") + str(bstack11lll1lll1_opy_))
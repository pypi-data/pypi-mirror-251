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
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from bstack_utils.constants import *
from bstack_utils.percy import *
from browserstack_sdk.bstack1ll1ll1l1_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1l1l11l111_opy_ import bstack1ll1111l11_opy_
import time
import requests
def bstack1lllll111_opy_():
  global CONFIG
  headers = {
        bstack111111l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack111111l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1ll11ll111_opy_(CONFIG, bstack11lllll1l_opy_)
  try:
    response = requests.get(bstack11lllll1l_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l1lll11l1_opy_ = response.json()[bstack111111l_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1l1lll111_opy_.format(response.json()))
      return bstack1l1lll11l1_opy_
    else:
      logger.debug(bstack1ll11l1l_opy_.format(bstack111111l_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1ll11l1l_opy_.format(e))
def bstack1l111l11l_opy_(hub_url):
  global CONFIG
  url = bstack111111l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack111111l_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack111111l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack111111l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1ll11ll111_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack11lll1ll_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1ll1l11l1l_opy_.format(hub_url, e))
def bstack11111l1l1_opy_():
  try:
    global bstack111111ll1_opy_
    bstack1l1lll11l1_opy_ = bstack1lllll111_opy_()
    bstack1l111ll1_opy_ = []
    results = []
    for bstack1l1ll11ll1_opy_ in bstack1l1lll11l1_opy_:
      bstack1l111ll1_opy_.append(bstack1l111l1l_opy_(target=bstack1l111l11l_opy_,args=(bstack1l1ll11ll1_opy_,)))
    for t in bstack1l111ll1_opy_:
      t.start()
    for t in bstack1l111ll1_opy_:
      results.append(t.join())
    bstack1l1lll11_opy_ = {}
    for item in results:
      hub_url = item[bstack111111l_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack111111l_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1l1lll11_opy_[hub_url] = latency
    bstack1ll111lll1_opy_ = min(bstack1l1lll11_opy_, key= lambda x: bstack1l1lll11_opy_[x])
    bstack111111ll1_opy_ = bstack1ll111lll1_opy_
    logger.debug(bstack1l1l1llll1_opy_.format(bstack1ll111lll1_opy_))
  except Exception as e:
    logger.debug(bstack1l11l11l_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils.config import Config
from bstack_utils.helper import bstack1lll111l_opy_, bstack11111ll1_opy_, bstack1l1l1l111_opy_, bstack1llll1l11_opy_, \
  Notset, bstack1lllll11_opy_, \
  bstack1ll1l111_opy_, bstack1l1l11llll_opy_, bstack1ll11lll1_opy_, bstack11ll111l1_opy_, bstack1lll11111l_opy_, bstack1l1lllll_opy_, \
  bstack1llll1111l_opy_, \
  bstack1lll1l1l_opy_, bstack1l1l1ll11l_opy_, bstack1lll1lll1l_opy_, bstack1ll11lll_opy_, \
  bstack11ll111ll_opy_, bstack11l1lllll_opy_, bstack1ll111111_opy_
from bstack_utils.bstack11l11l1l1_opy_ import bstack1l111l11_opy_
from bstack_utils.bstack11ll11l1l_opy_ import bstack1lll1l111_opy_
from bstack_utils.bstack1l1lll1l1_opy_ import bstack111llll1l_opy_, bstack1ll1l11111_opy_
from bstack_utils.bstack1ll1l1lll1_opy_ import bstack111lll1l_opy_
from bstack_utils.proxy import bstack11ll11111_opy_, bstack1ll11ll111_opy_, bstack1ll11l1l11_opy_, bstack1ll11l11ll_opy_
import bstack_utils.bstack1ll111l1l1_opy_ as bstack1lll111lll_opy_
from browserstack_sdk.bstack111lllll_opy_ import *
from browserstack_sdk.bstack1l1111ll_opy_ import *
from bstack_utils.bstack1llll1ll1_opy_ import bstack111111l1l_opy_
bstack1l1l1l1lll_opy_ = bstack111111l_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭ࢀ")
bstack11l11lll1_opy_ = bstack111111l_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭ࢁ")
from ._version import __version__
bstack1lll1lll11_opy_ = None
CONFIG = {}
bstack1l1l11ll_opy_ = {}
bstack1lll11l1l1_opy_ = {}
bstack1l1l11ll11_opy_ = None
bstack1l11l1lll_opy_ = None
bstack1ll11111ll_opy_ = None
bstack1llll1ll11_opy_ = -1
bstack11l1111l_opy_ = 0
bstack1ll11l11l1_opy_ = bstack111111111_opy_
bstack1l1l1111_opy_ = 1
bstack1lll1l1l11_opy_ = False
bstack1ll11l1111_opy_ = False
bstack1ll1llll11_opy_ = bstack111111l_opy_ (u"ࠨࠩࢂ")
bstack1llllll11_opy_ = bstack111111l_opy_ (u"ࠩࠪࢃ")
bstack11l111l1_opy_ = False
bstack1l1l1l1l_opy_ = True
bstack1111l1l1_opy_ = bstack111111l_opy_ (u"ࠪࠫࢄ")
bstack11l1l11ll_opy_ = []
bstack111111ll1_opy_ = bstack111111l_opy_ (u"ࠫࠬࢅ")
bstack1111111ll_opy_ = False
bstack1l111ll1l_opy_ = None
bstack1l1l1l1l1_opy_ = None
bstack1l1ll1111l_opy_ = None
bstack1lll11111_opy_ = -1
bstack111ll11l1_opy_ = os.path.join(os.path.expanduser(bstack111111l_opy_ (u"ࠬࢄࠧࢆ")), bstack111111l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ࢇ"), bstack111111l_opy_ (u"ࠧ࠯ࡴࡲࡦࡴࡺ࠭ࡳࡧࡳࡳࡷࡺ࠭ࡩࡧ࡯ࡴࡪࡸ࠮࡫ࡵࡲࡲࠬ࢈"))
bstack1ll11ll1l_opy_ = 0
bstack1ll1l11ll_opy_ = []
bstack1l11lll1_opy_ = []
bstack111111ll_opy_ = []
bstack1ll1l11l1_opy_ = []
bstack1lll11ll11_opy_ = bstack111111l_opy_ (u"ࠨࠩࢉ")
bstack1l1ll1lll1_opy_ = bstack111111l_opy_ (u"ࠩࠪࢊ")
bstack1l1lll111l_opy_ = False
bstack1l11lllll_opy_ = False
bstack111l11lll_opy_ = {}
bstack11l11111_opy_ = None
bstack1ll111lll_opy_ = None
bstack111l1ll11_opy_ = None
bstack1l1llll11l_opy_ = None
bstack1ll1lll1_opy_ = None
bstack1l11111l1_opy_ = None
bstack11l1l11l1_opy_ = None
bstack1l1lll11l_opy_ = None
bstack1lll1l11l_opy_ = None
bstack1ll11l1lll_opy_ = None
bstack1llllll1l1_opy_ = None
bstack1l1l11lll_opy_ = None
bstack11llllll_opy_ = None
bstack1ll11l11l_opy_ = None
bstack1l1ll1lll_opy_ = None
bstack11lll11ll_opy_ = None
bstack1ll111llll_opy_ = None
bstack11ll1111_opy_ = None
bstack111llll11_opy_ = None
bstack1l111l1l1_opy_ = None
bstack1lll111ll_opy_ = None
bstack1l1lllllll_opy_ = bstack111111l_opy_ (u"ࠥࠦࢋ")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1ll11l11l1_opy_,
                    format=bstack111111l_opy_ (u"ࠫࡡࡴࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩࢌ"),
                    datefmt=bstack111111l_opy_ (u"ࠬࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧࢍ"),
                    stream=sys.stdout)
bstack1111ll1ll_opy_ = Config.bstack11l11l1ll_opy_()
percy = bstack1lll11lll_opy_()
bstack1ll11l1l1l_opy_ = bstack1ll1111l11_opy_()
def bstack1l1lllll1_opy_():
  global CONFIG
  global bstack1ll11l11l1_opy_
  if bstack111111l_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨࢎ") in CONFIG:
    bstack1ll11l11l1_opy_ = bstack1lll1111l1_opy_[CONFIG[bstack111111l_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ࢏")]]
    logging.getLogger().setLevel(bstack1ll11l11l1_opy_)
def bstack1l1l1ll1_opy_():
  global CONFIG
  global bstack1l1lll111l_opy_
  global bstack1111ll1ll_opy_
  bstack1lll11llll_opy_ = bstack1lll1lll_opy_(CONFIG)
  if (bstack111111l_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ࢐") in bstack1lll11llll_opy_ and str(bstack1lll11llll_opy_[bstack111111l_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ࢑")]).lower() == bstack111111l_opy_ (u"ࠪࡸࡷࡻࡥࠨ࢒")):
    bstack1l1lll111l_opy_ = True
  bstack1111ll1ll_opy_.bstack1l1lll1lll_opy_(bstack1lll11llll_opy_.get(bstack111111l_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࢓"), False))
def bstack1ll1l111ll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack11111ll11_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1ll1l11_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack111111l_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࢔") == args[i].lower() or bstack111111l_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࢕") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1111l1l1_opy_
      bstack1111l1l1_opy_ += bstack111111l_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠬ࢖") + path
      return path
  return None
bstack1llll111l1_opy_ = re.compile(bstack111111l_opy_ (u"ࡳࠤ࠱࠮ࡄࡢࠤࡼࠪ࠱࠮ࡄ࠯ࡽ࠯ࠬࡂࠦࢗ"))
def bstack111l11l1l_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1llll111l1_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack111111l_opy_ (u"ࠤࠧࡿࠧ࢘") + group + bstack111111l_opy_ (u"ࠥࢁ࢙ࠧ"), os.environ.get(group))
  return value
def bstack1lll11l111_opy_():
  bstack1l1lll1ll_opy_ = bstack1l1ll1l11_opy_()
  if bstack1l1lll1ll_opy_ and os.path.exists(os.path.abspath(bstack1l1lll1ll_opy_)):
    fileName = bstack1l1lll1ll_opy_
  if bstack111111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࢚") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack111111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࢛ࠩ")])) and not bstack111111l_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨ࢜") in locals():
    fileName = os.environ[bstack111111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢝")]
  if bstack111111l_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪ࢞") in locals():
    bstack1l1l111_opy_ = os.path.abspath(fileName)
  else:
    bstack1l1l111_opy_ = bstack111111l_opy_ (u"ࠩࠪ࢟")
  bstack1llll11l1l_opy_ = os.getcwd()
  bstack1l1l1111l_opy_ = bstack111111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ࢠ")
  bstack1lll11ll1l_opy_ = bstack111111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨࢡ")
  while (not os.path.exists(bstack1l1l111_opy_)) and bstack1llll11l1l_opy_ != bstack111111l_opy_ (u"ࠧࠨࢢ"):
    bstack1l1l111_opy_ = os.path.join(bstack1llll11l1l_opy_, bstack1l1l1111l_opy_)
    if not os.path.exists(bstack1l1l111_opy_):
      bstack1l1l111_opy_ = os.path.join(bstack1llll11l1l_opy_, bstack1lll11ll1l_opy_)
    if bstack1llll11l1l_opy_ != os.path.dirname(bstack1llll11l1l_opy_):
      bstack1llll11l1l_opy_ = os.path.dirname(bstack1llll11l1l_opy_)
    else:
      bstack1llll11l1l_opy_ = bstack111111l_opy_ (u"ࠨࠢࢣ")
  if not os.path.exists(bstack1l1l111_opy_):
    bstack1l1llll11_opy_(
      bstack1ll1111lll_opy_.format(os.getcwd()))
  try:
    with open(bstack1l1l111_opy_, bstack111111l_opy_ (u"ࠧࡳࠩࢤ")) as stream:
      yaml.add_implicit_resolver(bstack111111l_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤࢥ"), bstack1llll111l1_opy_)
      yaml.add_constructor(bstack111111l_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥࢦ"), bstack111l11l1l_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1l1l111_opy_, bstack111111l_opy_ (u"ࠪࡶࠬࢧ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1l1llll11_opy_(bstack1llll1l11l_opy_.format(str(exc)))
def bstack1lll111l1_opy_(config):
  bstack11l1l111l_opy_ = bstack1l1ll11l11_opy_(config)
  for option in list(bstack11l1l111l_opy_):
    if option.lower() in bstack111l111l1_opy_ and option != bstack111l111l1_opy_[option.lower()]:
      bstack11l1l111l_opy_[bstack111l111l1_opy_[option.lower()]] = bstack11l1l111l_opy_[option]
      del bstack11l1l111l_opy_[option]
  return config
def bstack1l1l11l1l_opy_():
  global bstack1lll11l1l1_opy_
  for key, bstack1l1llll1_opy_ in bstack1ll111ll_opy_.items():
    if isinstance(bstack1l1llll1_opy_, list):
      for var in bstack1l1llll1_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1lll11l1l1_opy_[key] = os.environ[var]
          break
    elif bstack1l1llll1_opy_ in os.environ and os.environ[bstack1l1llll1_opy_] and str(os.environ[bstack1l1llll1_opy_]).strip():
      bstack1lll11l1l1_opy_[key] = os.environ[bstack1l1llll1_opy_]
  if bstack111111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ") in os.environ:
    bstack1lll11l1l1_opy_[bstack111111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢩ")] = {}
    bstack1lll11l1l1_opy_[bstack111111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")][bstack111111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢫ")] = os.environ[bstack111111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪࢬ")]
def bstack1lll111111_opy_():
  global bstack1l1l11ll_opy_
  global bstack1111l1l1_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack111111l_opy_ (u"ࠩ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢭ").lower() == val.lower():
      bstack1l1l11ll_opy_[bstack111111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࢮ")] = {}
      bstack1l1l11ll_opy_[bstack111111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࢯ")][bstack111111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack11ll1l11l_opy_ in bstack1111ll11l_opy_.items():
    if isinstance(bstack11ll1l11l_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack11ll1l11l_opy_:
          if idx < len(sys.argv) and bstack111111l_opy_ (u"࠭࠭࠮ࠩࢱ") + var.lower() == val.lower() and not key in bstack1l1l11ll_opy_:
            bstack1l1l11ll_opy_[key] = sys.argv[idx + 1]
            bstack1111l1l1_opy_ += bstack111111l_opy_ (u"ࠧࠡ࠯࠰ࠫࢲ") + var + bstack111111l_opy_ (u"ࠨࠢࠪࢳ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack111111l_opy_ (u"ࠩ࠰࠱ࠬࢴ") + bstack11ll1l11l_opy_.lower() == val.lower() and not key in bstack1l1l11ll_opy_:
          bstack1l1l11ll_opy_[key] = sys.argv[idx + 1]
          bstack1111l1l1_opy_ += bstack111111l_opy_ (u"ࠪࠤ࠲࠳ࠧࢵ") + bstack11ll1l11l_opy_ + bstack111111l_opy_ (u"ࠫࠥ࠭ࢶ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1ll1l1llll_opy_(config):
  bstack1l1ll111ll_opy_ = config.keys()
  for bstack1lll1l1l1_opy_, bstack11l1l1l1l_opy_ in bstack1l111l1ll_opy_.items():
    if bstack11l1l1l1l_opy_ in bstack1l1ll111ll_opy_:
      config[bstack1lll1l1l1_opy_] = config[bstack11l1l1l1l_opy_]
      del config[bstack11l1l1l1l_opy_]
  for bstack1lll1l1l1_opy_, bstack11l1l1l1l_opy_ in bstack111l1l11_opy_.items():
    if isinstance(bstack11l1l1l1l_opy_, list):
      for bstack1lll1l1ll1_opy_ in bstack11l1l1l1l_opy_:
        if bstack1lll1l1ll1_opy_ in bstack1l1ll111ll_opy_:
          config[bstack1lll1l1l1_opy_] = config[bstack1lll1l1ll1_opy_]
          del config[bstack1lll1l1ll1_opy_]
          break
    elif bstack11l1l1l1l_opy_ in bstack1l1ll111ll_opy_:
      config[bstack1lll1l1l1_opy_] = config[bstack11l1l1l1l_opy_]
      del config[bstack11l1l1l1l_opy_]
  for bstack1lll1l1ll1_opy_ in list(config):
    for bstack1111ll111_opy_ in bstack111lll11_opy_:
      if bstack1lll1l1ll1_opy_.lower() == bstack1111ll111_opy_.lower() and bstack1lll1l1ll1_opy_ != bstack1111ll111_opy_:
        config[bstack1111ll111_opy_] = config[bstack1lll1l1ll1_opy_]
        del config[bstack1lll1l1ll1_opy_]
  bstack1l1l1l11ll_opy_ = []
  if bstack111111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࢷ") in config:
    bstack1l1l1l11ll_opy_ = config[bstack111111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࢸ")]
  for platform in bstack1l1l1l11ll_opy_:
    for bstack1lll1l1ll1_opy_ in list(platform):
      for bstack1111ll111_opy_ in bstack111lll11_opy_:
        if bstack1lll1l1ll1_opy_.lower() == bstack1111ll111_opy_.lower() and bstack1lll1l1ll1_opy_ != bstack1111ll111_opy_:
          platform[bstack1111ll111_opy_] = platform[bstack1lll1l1ll1_opy_]
          del platform[bstack1lll1l1ll1_opy_]
  for bstack1lll1l1l1_opy_, bstack11l1l1l1l_opy_ in bstack111l1l11_opy_.items():
    for platform in bstack1l1l1l11ll_opy_:
      if isinstance(bstack11l1l1l1l_opy_, list):
        for bstack1lll1l1ll1_opy_ in bstack11l1l1l1l_opy_:
          if bstack1lll1l1ll1_opy_ in platform:
            platform[bstack1lll1l1l1_opy_] = platform[bstack1lll1l1ll1_opy_]
            del platform[bstack1lll1l1ll1_opy_]
            break
      elif bstack11l1l1l1l_opy_ in platform:
        platform[bstack1lll1l1l1_opy_] = platform[bstack11l1l1l1l_opy_]
        del platform[bstack11l1l1l1l_opy_]
  for bstack1lll1ll1_opy_ in bstack11ll1l11_opy_:
    if bstack1lll1ll1_opy_ in config:
      if not bstack11ll1l11_opy_[bstack1lll1ll1_opy_] in config:
        config[bstack11ll1l11_opy_[bstack1lll1ll1_opy_]] = {}
      config[bstack11ll1l11_opy_[bstack1lll1ll1_opy_]].update(config[bstack1lll1ll1_opy_])
      del config[bstack1lll1ll1_opy_]
  for platform in bstack1l1l1l11ll_opy_:
    for bstack1lll1ll1_opy_ in bstack11ll1l11_opy_:
      if bstack1lll1ll1_opy_ in list(platform):
        if not bstack11ll1l11_opy_[bstack1lll1ll1_opy_] in platform:
          platform[bstack11ll1l11_opy_[bstack1lll1ll1_opy_]] = {}
        platform[bstack11ll1l11_opy_[bstack1lll1ll1_opy_]].update(platform[bstack1lll1ll1_opy_])
        del platform[bstack1lll1ll1_opy_]
  config = bstack1lll111l1_opy_(config)
  return config
def bstack1111lllll_opy_(config):
  global bstack1llllll11_opy_
  if bstack111111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࢹ") in config and str(config[bstack111111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢺ")]).lower() != bstack111111l_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨࢻ"):
    if not bstack111111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࢼ") in config:
      config[bstack111111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࢽ")] = {}
    if not bstack111111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢾ") in config[bstack111111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢿ")]:
      bstack11ll1l1l_opy_ = datetime.datetime.now()
      bstack1l11lll11_opy_ = bstack11ll1l1l_opy_.strftime(bstack111111l_opy_ (u"ࠧࠦࡦࡢࠩࡧࡥࠥࡉࠧࡐࠫࣀ"))
      hostname = socket.gethostname()
      bstack1llll1lll1_opy_ = bstack111111l_opy_ (u"ࠨࠩࣁ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack111111l_opy_ (u"ࠩࡾࢁࡤࢁࡽࡠࡽࢀࠫࣂ").format(bstack1l11lll11_opy_, hostname, bstack1llll1lll1_opy_)
      config[bstack111111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣃ")][bstack111111l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣄ")] = identifier
    bstack1llllll11_opy_ = config[bstack111111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣅ")][bstack111111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣆ")]
  return config
def bstack1ll1ll11_opy_():
  bstack11l1111l1_opy_ =  bstack11ll111l1_opy_()[bstack111111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷ࠭ࣇ")]
  return bstack11l1111l1_opy_ if bstack11l1111l1_opy_ else -1
def bstack111l1lll1_opy_(bstack11l1111l1_opy_):
  global CONFIG
  if not bstack111111l_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣈ") in CONFIG[bstack111111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣉ")]:
    return
  CONFIG[bstack111111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")] = CONFIG[bstack111111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣋")].replace(
    bstack111111l_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧ࣌"),
    str(bstack11l1111l1_opy_)
  )
def bstack111l11ll1_opy_():
  global CONFIG
  if not bstack111111l_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬ࣍") in CONFIG[bstack111111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣎")]:
    return
  bstack11ll1l1l_opy_ = datetime.datetime.now()
  bstack1l11lll11_opy_ = bstack11ll1l1l_opy_.strftime(bstack111111l_opy_ (u"ࠨࠧࡧ࠱ࠪࡨ࠭ࠦࡊ࠽ࠩࡒ࣏࠭"))
  CONFIG[bstack111111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")] = CONFIG[bstack111111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣑ࠬ")].replace(
    bstack111111l_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿ࣒ࠪ"),
    bstack1l11lll11_opy_
  )
def bstack1lll1ll1ll_opy_():
  global CONFIG
  if bstack111111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ") in CONFIG and not bool(CONFIG[bstack111111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣔ")]):
    del CONFIG[bstack111111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣕ")]
    return
  if not bstack111111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ") in CONFIG:
    CONFIG[bstack111111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣗ")] = bstack111111l_opy_ (u"ࠪࠧࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣘ")
  if bstack111111l_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪࣙ") in CONFIG[bstack111111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣚ")]:
    bstack111l11ll1_opy_()
    os.environ[bstack111111l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪࣛ")] = CONFIG[bstack111111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣜ")]
  if not bstack111111l_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣝ") in CONFIG[bstack111111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣞ")]:
    return
  bstack11l1111l1_opy_ = bstack111111l_opy_ (u"ࠪࠫࣟ")
  bstack1lllll11ll_opy_ = bstack1ll1ll11_opy_()
  if bstack1lllll11ll_opy_ != -1:
    bstack11l1111l1_opy_ = bstack111111l_opy_ (u"ࠫࡈࡏࠠࠨ࣠") + str(bstack1lllll11ll_opy_)
  if bstack11l1111l1_opy_ == bstack111111l_opy_ (u"ࠬ࠭࣡"):
    bstack1ll1lll1l_opy_ = bstack1llll11l_opy_(CONFIG[bstack111111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ࣢")])
    if bstack1ll1lll1l_opy_ != -1:
      bstack11l1111l1_opy_ = str(bstack1ll1lll1l_opy_)
  if bstack11l1111l1_opy_:
    bstack111l1lll1_opy_(bstack11l1111l1_opy_)
    os.environ[bstack111111l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࣣࠫ")] = CONFIG[bstack111111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣤ")]
def bstack11ll11l1_opy_(bstack1l1l1lllll_opy_, bstack1ll1lll1ll_opy_, path):
  bstack1l1l1ll1ll_opy_ = {
    bstack111111l_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣥ"): bstack1ll1lll1ll_opy_
  }
  if os.path.exists(path):
    bstack1l11l111_opy_ = json.load(open(path, bstack111111l_opy_ (u"ࠪࡶࡧࣦ࠭")))
  else:
    bstack1l11l111_opy_ = {}
  bstack1l11l111_opy_[bstack1l1l1lllll_opy_] = bstack1l1l1ll1ll_opy_
  with open(path, bstack111111l_opy_ (u"ࠦࡼ࠱ࠢࣧ")) as outfile:
    json.dump(bstack1l11l111_opy_, outfile)
def bstack1llll11l_opy_(bstack1l1l1lllll_opy_):
  bstack1l1l1lllll_opy_ = str(bstack1l1l1lllll_opy_)
  bstack11l11lll_opy_ = os.path.join(os.path.expanduser(bstack111111l_opy_ (u"ࠬࢄࠧࣨ")), bstack111111l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࣩ࠭"))
  try:
    if not os.path.exists(bstack11l11lll_opy_):
      os.makedirs(bstack11l11lll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack111111l_opy_ (u"ࠧࡿࠩ࣪")), bstack111111l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ࣫"), bstack111111l_opy_ (u"ࠩ࠱ࡦࡺ࡯࡬ࡥ࠯ࡱࡥࡲ࡫࠭ࡤࡣࡦ࡬ࡪ࠴ࡪࡴࡱࡱࠫ࣬"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack111111l_opy_ (u"ࠪࡻ࣭ࠬ")):
        pass
      with open(file_path, bstack111111l_opy_ (u"ࠦࡼ࠱࣮ࠢ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack111111l_opy_ (u"ࠬࡸ࣯ࠧ")) as bstack1lll1ll111_opy_:
      bstack1111ll1l_opy_ = json.load(bstack1lll1ll111_opy_)
    if bstack1l1l1lllll_opy_ in bstack1111ll1l_opy_:
      bstack1l1ll11111_opy_ = bstack1111ll1l_opy_[bstack1l1l1lllll_opy_][bstack111111l_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣰࠪ")]
      bstack1111ll11_opy_ = int(bstack1l1ll11111_opy_) + 1
      bstack11ll11l1_opy_(bstack1l1l1lllll_opy_, bstack1111ll11_opy_, file_path)
      return bstack1111ll11_opy_
    else:
      bstack11ll11l1_opy_(bstack1l1l1lllll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack11lllllll_opy_.format(str(e)))
    return -1
def bstack1l1lllll1l_opy_(config):
  if not config[bstack111111l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࣱࠩ")] or not config[bstack111111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࣲࠫ")]:
    return True
  else:
    return False
def bstack11111l111_opy_(config, index=0):
  global bstack11l111l1_opy_
  bstack1ll1111l_opy_ = {}
  caps = bstack111ll1ll_opy_ + bstack11llll1l_opy_
  if bstack11l111l1_opy_:
    caps += bstack1ll1l11l_opy_
  for key in config:
    if key in caps + [bstack111111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࣳ")]:
      continue
    bstack1ll1111l_opy_[key] = config[key]
  if bstack111111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ") in config:
    for bstack1l1ll1l1ll_opy_ in config[bstack111111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣵ")][index]:
      if bstack1l1ll1l1ll_opy_ in caps + [bstack111111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࣶࠪ"), bstack111111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧࣷ")]:
        continue
      bstack1ll1111l_opy_[bstack1l1ll1l1ll_opy_] = config[bstack111111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣸ")][index][bstack1l1ll1l1ll_opy_]
  bstack1ll1111l_opy_[bstack111111l_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࣹࠪ")] = socket.gethostname()
  if bstack111111l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࣺࠪ") in bstack1ll1111l_opy_:
    del (bstack1ll1111l_opy_[bstack111111l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫࣻ")])
  return bstack1ll1111l_opy_
def bstack1l1l1l111l_opy_(config):
  global bstack11l111l1_opy_
  bstack1ll1ll1l_opy_ = {}
  caps = bstack11llll1l_opy_
  if bstack11l111l1_opy_:
    caps += bstack1ll1l11l_opy_
  for key in caps:
    if key in config:
      bstack1ll1ll1l_opy_[key] = config[key]
  return bstack1ll1ll1l_opy_
def bstack1l111111l_opy_(bstack1ll1111l_opy_, bstack1ll1ll1l_opy_):
  bstack1l11l11ll_opy_ = {}
  for key in bstack1ll1111l_opy_.keys():
    if key in bstack1l111l1ll_opy_:
      bstack1l11l11ll_opy_[bstack1l111l1ll_opy_[key]] = bstack1ll1111l_opy_[key]
    else:
      bstack1l11l11ll_opy_[key] = bstack1ll1111l_opy_[key]
  for key in bstack1ll1ll1l_opy_:
    if key in bstack1l111l1ll_opy_:
      bstack1l11l11ll_opy_[bstack1l111l1ll_opy_[key]] = bstack1ll1ll1l_opy_[key]
    else:
      bstack1l11l11ll_opy_[key] = bstack1ll1ll1l_opy_[key]
  return bstack1l11l11ll_opy_
def bstack1l1ll11l_opy_(config, index=0):
  global bstack11l111l1_opy_
  config = copy.deepcopy(config)
  caps = {}
  bstack1ll1ll1l_opy_ = bstack1l1l1l111l_opy_(config)
  bstack1llllll111_opy_ = bstack11llll1l_opy_
  bstack1llllll111_opy_ += bstack1ll1l1ll1l_opy_
  if bstack11l111l1_opy_:
    bstack1llllll111_opy_ += bstack1ll1l11l_opy_
  if bstack111111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ") in config:
    if bstack111111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪࣽ") in config[bstack111111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࣾ")][index]:
      caps[bstack111111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬࣿ")] = config[bstack111111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫऀ")][index][bstack111111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧँ")]
    if bstack111111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫं") in config[bstack111111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧः")][index]:
      caps[bstack111111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऄ")] = str(config[bstack111111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩअ")][index][bstack111111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨआ")])
    bstack111ll111_opy_ = {}
    for bstack1l1ll1l111_opy_ in bstack1llllll111_opy_:
      if bstack1l1ll1l111_opy_ in config[bstack111111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index]:
        if bstack1l1ll1l111_opy_ == bstack111111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫई"):
          try:
            bstack111ll111_opy_[bstack1l1ll1l111_opy_] = str(config[bstack111111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")][index][bstack1l1ll1l111_opy_] * 1.0)
          except:
            bstack111ll111_opy_[bstack1l1ll1l111_opy_] = str(config[bstack111111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧऊ")][index][bstack1l1ll1l111_opy_])
        else:
          bstack111ll111_opy_[bstack1l1ll1l111_opy_] = config[bstack111111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨऋ")][index][bstack1l1ll1l111_opy_]
        del (config[bstack111111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩऌ")][index][bstack1l1ll1l111_opy_])
    bstack1ll1ll1l_opy_ = update(bstack1ll1ll1l_opy_, bstack111ll111_opy_)
  bstack1ll1111l_opy_ = bstack11111l111_opy_(config, index)
  for bstack1lll1l1ll1_opy_ in bstack11llll1l_opy_ + [bstack111111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬऍ"), bstack111111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩऎ")]:
    if bstack1lll1l1ll1_opy_ in bstack1ll1111l_opy_:
      bstack1ll1ll1l_opy_[bstack1lll1l1ll1_opy_] = bstack1ll1111l_opy_[bstack1lll1l1ll1_opy_]
      del (bstack1ll1111l_opy_[bstack1lll1l1ll1_opy_])
  if bstack1lllll11_opy_(config):
    bstack1ll1111l_opy_[bstack111111l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩए")] = True
    caps.update(bstack1ll1ll1l_opy_)
    caps[bstack111111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫऐ")] = bstack1ll1111l_opy_
  else:
    bstack1ll1111l_opy_[bstack111111l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫऑ")] = False
    caps.update(bstack1l111111l_opy_(bstack1ll1111l_opy_, bstack1ll1ll1l_opy_))
    if bstack111111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪऒ") in caps:
      caps[bstack111111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧओ")] = caps[bstack111111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬऔ")]
      del (caps[bstack111111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭क")])
    if bstack111111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪख") in caps:
      caps[bstack111111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬग")] = caps[bstack111111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬघ")]
      del (caps[bstack111111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ङ")])
  return caps
def bstack1ll1l1111_opy_():
  global bstack111111ll1_opy_
  if bstack11111ll11_opy_() <= version.parse(bstack111111l_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭च")):
    if bstack111111ll1_opy_ != bstack111111l_opy_ (u"ࠧࠨछ"):
      return bstack111111l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤज") + bstack111111ll1_opy_ + bstack111111l_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨझ")
    return bstack1llll1ll1l_opy_
  if bstack111111ll1_opy_ != bstack111111l_opy_ (u"ࠪࠫञ"):
    return bstack111111l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨट") + bstack111111ll1_opy_ + bstack111111l_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨठ")
  return bstack1l1l1l1l11_opy_
def bstack1l1ll11lll_opy_(options):
  return hasattr(options, bstack111111l_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧड"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1llll1l1l_opy_(options, bstack11l11ll1l_opy_):
  for bstack11lllll11_opy_ in bstack11l11ll1l_opy_:
    if bstack11lllll11_opy_ in [bstack111111l_opy_ (u"ࠧࡢࡴࡪࡷࠬढ"), bstack111111l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬण")]:
      continue
    if bstack11lllll11_opy_ in options._experimental_options:
      options._experimental_options[bstack11lllll11_opy_] = update(options._experimental_options[bstack11lllll11_opy_],
                                                         bstack11l11ll1l_opy_[bstack11lllll11_opy_])
    else:
      options.add_experimental_option(bstack11lllll11_opy_, bstack11l11ll1l_opy_[bstack11lllll11_opy_])
  if bstack111111l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧत") in bstack11l11ll1l_opy_:
    for arg in bstack11l11ll1l_opy_[bstack111111l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨथ")]:
      options.add_argument(arg)
    del (bstack11l11ll1l_opy_[bstack111111l_opy_ (u"ࠫࡦࡸࡧࡴࠩद")])
  if bstack111111l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩध") in bstack11l11ll1l_opy_:
    for ext in bstack11l11ll1l_opy_[bstack111111l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪन")]:
      options.add_extension(ext)
    del (bstack11l11ll1l_opy_[bstack111111l_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫऩ")])
def bstack111l1l1ll_opy_(options, bstack1l11l1l11_opy_):
  if bstack111111l_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧप") in bstack1l11l1l11_opy_:
    for bstack1lll1l11ll_opy_ in bstack1l11l1l11_opy_[bstack111111l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨफ")]:
      if bstack1lll1l11ll_opy_ in options._preferences:
        options._preferences[bstack1lll1l11ll_opy_] = update(options._preferences[bstack1lll1l11ll_opy_], bstack1l11l1l11_opy_[bstack111111l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩब")][bstack1lll1l11ll_opy_])
      else:
        options.set_preference(bstack1lll1l11ll_opy_, bstack1l11l1l11_opy_[bstack111111l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪभ")][bstack1lll1l11ll_opy_])
  if bstack111111l_opy_ (u"ࠬࡧࡲࡨࡵࠪम") in bstack1l11l1l11_opy_:
    for arg in bstack1l11l1l11_opy_[bstack111111l_opy_ (u"࠭ࡡࡳࡩࡶࠫय")]:
      options.add_argument(arg)
def bstack11l111111_opy_(options, bstack1l1l1ll11_opy_):
  if bstack111111l_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࠨर") in bstack1l1l1ll11_opy_:
    options.use_webview(bool(bstack1l1l1ll11_opy_[bstack111111l_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࠩऱ")]))
  bstack1llll1l1l_opy_(options, bstack1l1l1ll11_opy_)
def bstack1llll1ll_opy_(options, bstack111l1l111_opy_):
  for bstack1lll1l1lll_opy_ in bstack111l1l111_opy_:
    if bstack1lll1l1lll_opy_ in [bstack111111l_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ल"), bstack111111l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨळ")]:
      continue
    options.set_capability(bstack1lll1l1lll_opy_, bstack111l1l111_opy_[bstack1lll1l1lll_opy_])
  if bstack111111l_opy_ (u"ࠫࡦࡸࡧࡴࠩऴ") in bstack111l1l111_opy_:
    for arg in bstack111l1l111_opy_[bstack111111l_opy_ (u"ࠬࡧࡲࡨࡵࠪव")]:
      options.add_argument(arg)
  if bstack111111l_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪश") in bstack111l1l111_opy_:
    options.bstack1l1l11l11l_opy_(bool(bstack111l1l111_opy_[bstack111111l_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫष")]))
def bstack1ll111ll1l_opy_(options, bstack1l1l111l1l_opy_):
  for bstack1ll1lll11l_opy_ in bstack1l1l111l1l_opy_:
    if bstack1ll1lll11l_opy_ in [bstack111111l_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस"), bstack111111l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧह")]:
      continue
    options._options[bstack1ll1lll11l_opy_] = bstack1l1l111l1l_opy_[bstack1ll1lll11l_opy_]
  if bstack111111l_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऺ") in bstack1l1l111l1l_opy_:
    for bstack11ll1l111_opy_ in bstack1l1l111l1l_opy_[bstack111111l_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऻ")]:
      options.bstack1l1l111ll1_opy_(
        bstack11ll1l111_opy_, bstack1l1l111l1l_opy_[bstack111111l_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ़ࠩ")][bstack11ll1l111_opy_])
  if bstack111111l_opy_ (u"࠭ࡡࡳࡩࡶࠫऽ") in bstack1l1l111l1l_opy_:
    for arg in bstack1l1l111l1l_opy_[bstack111111l_opy_ (u"ࠧࡢࡴࡪࡷࠬा")]:
      options.add_argument(arg)
def bstack11l1llll1_opy_(options, caps):
  if not hasattr(options, bstack111111l_opy_ (u"ࠨࡍࡈ࡝ࠬि")):
    return
  if options.KEY == bstack111111l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧी") and options.KEY in caps:
    bstack1llll1l1l_opy_(options, caps[bstack111111l_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨु")])
  elif options.KEY == bstack111111l_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩू") and options.KEY in caps:
    bstack111l1l1ll_opy_(options, caps[bstack111111l_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪृ")])
  elif options.KEY == bstack111111l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧॄ") and options.KEY in caps:
    bstack1llll1ll_opy_(options, caps[bstack111111l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨॅ")])
  elif options.KEY == bstack111111l_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩॆ") and options.KEY in caps:
    bstack11l111111_opy_(options, caps[bstack111111l_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪे")])
  elif options.KEY == bstack111111l_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩै") and options.KEY in caps:
    bstack1ll111ll1l_opy_(options, caps[bstack111111l_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪॉ")])
def bstack1ll1111ll1_opy_(caps):
  global bstack11l111l1_opy_
  if isinstance(os.environ.get(bstack111111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ॊ")), str):
    bstack11l111l1_opy_ = eval(os.getenv(bstack111111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧो")))
  if bstack11l111l1_opy_:
    if bstack1ll1l111ll_opy_() < version.parse(bstack111111l_opy_ (u"ࠧ࠳࠰࠶࠲࠵࠭ौ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack111111l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ्")
    if bstack111111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॎ") in caps:
      browser = caps[bstack111111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨॏ")]
    elif bstack111111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬॐ") in caps:
      browser = caps[bstack111111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭॑")]
    browser = str(browser).lower()
    if browser == bstack111111l_opy_ (u"࠭ࡩࡱࡪࡲࡲࡪ॒࠭") or browser == bstack111111l_opy_ (u"ࠧࡪࡲࡤࡨࠬ॓"):
      browser = bstack111111l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨ॔")
    if browser == bstack111111l_opy_ (u"ࠩࡶࡥࡲࡹࡵ࡯ࡩࠪॕ"):
      browser = bstack111111l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪॖ")
    if browser not in [bstack111111l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫॗ"), bstack111111l_opy_ (u"ࠬ࡫ࡤࡨࡧࠪक़"), bstack111111l_opy_ (u"࠭ࡩࡦࠩख़"), bstack111111l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧग़"), bstack111111l_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩज़")]:
      return None
    try:
      package = bstack111111l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡼࡿ࠱ࡳࡵࡺࡩࡰࡰࡶࠫड़").format(browser)
      name = bstack111111l_opy_ (u"ࠪࡓࡵࡺࡩࡰࡰࡶࠫढ़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l1ll11lll_opy_(options):
        return None
      for bstack1lll1l1ll1_opy_ in caps.keys():
        options.set_capability(bstack1lll1l1ll1_opy_, caps[bstack1lll1l1ll1_opy_])
      bstack11l1llll1_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l1l1ll111_opy_(options, bstack1l1ll111l1_opy_):
  if not bstack1l1ll11lll_opy_(options):
    return
  for bstack1lll1l1ll1_opy_ in bstack1l1ll111l1_opy_.keys():
    if bstack1lll1l1ll1_opy_ in bstack1ll1l1ll1l_opy_:
      continue
    if bstack1lll1l1ll1_opy_ in options._caps and type(options._caps[bstack1lll1l1ll1_opy_]) in [dict, list]:
      options._caps[bstack1lll1l1ll1_opy_] = update(options._caps[bstack1lll1l1ll1_opy_], bstack1l1ll111l1_opy_[bstack1lll1l1ll1_opy_])
    else:
      options.set_capability(bstack1lll1l1ll1_opy_, bstack1l1ll111l1_opy_[bstack1lll1l1ll1_opy_])
  bstack11l1llll1_opy_(options, bstack1l1ll111l1_opy_)
  if bstack111111l_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪफ़") in options._caps:
    if options._caps[bstack111111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪय़")] and options._caps[bstack111111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॠ")].lower() != bstack111111l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨॡ"):
      del options._caps[bstack111111l_opy_ (u"ࠨ࡯ࡲࡾ࠿ࡪࡥࡣࡷࡪ࡫ࡪࡸࡁࡥࡦࡵࡩࡸࡹࠧॢ")]
def bstack1l1l111ll_opy_(proxy_config):
  if bstack111111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ॣ") in proxy_config:
    proxy_config[bstack111111l_opy_ (u"ࠪࡷࡸࡲࡐࡳࡱࡻࡽࠬ।")] = proxy_config[bstack111111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ॥")]
    del (proxy_config[bstack111111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ०")])
  if bstack111111l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ१") in proxy_config and proxy_config[bstack111111l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ२")].lower() != bstack111111l_opy_ (u"ࠨࡦ࡬ࡶࡪࡩࡴࠨ३"):
    proxy_config[bstack111111l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ४")] = bstack111111l_opy_ (u"ࠪࡱࡦࡴࡵࡢ࡮ࠪ५")
  if bstack111111l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡄࡹࡹࡵࡣࡰࡰࡩ࡭࡬࡛ࡲ࡭ࠩ६") in proxy_config:
    proxy_config[bstack111111l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ७")] = bstack111111l_opy_ (u"࠭ࡰࡢࡥࠪ८")
  return proxy_config
def bstack1l1l11ll1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack111111l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭९") in config:
    return proxy
  config[bstack111111l_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧ॰")] = bstack1l1l111ll_opy_(config[bstack111111l_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨॱ")])
  if proxy == None:
    proxy = Proxy(config[bstack111111l_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩॲ")])
  return proxy
def bstack111lllll1_opy_(self):
  global CONFIG
  global bstack1l1l11lll_opy_
  try:
    proxy = bstack1ll11l1l11_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack111111l_opy_ (u"ࠫ࠳ࡶࡡࡤࠩॳ")):
        proxies = bstack11ll11111_opy_(proxy, bstack1ll1l1111_opy_())
        if len(proxies) > 0:
          protocol, bstack11ll111l_opy_ = proxies.popitem()
          if bstack111111l_opy_ (u"ࠧࡀ࠯࠰ࠤॴ") in bstack11ll111l_opy_:
            return bstack11ll111l_opy_
          else:
            return bstack111111l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢॵ") + bstack11ll111l_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack111111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦॶ").format(str(e)))
  return bstack1l1l11lll_opy_(self)
def bstack1l1111l11_opy_():
  global CONFIG
  return bstack1ll11l11ll_opy_(CONFIG) and bstack1l1lllll_opy_() and bstack11111ll11_opy_() >= version.parse(bstack1l1l11111_opy_)
def bstack1ll11lllll_opy_():
  global CONFIG
  return (bstack111111l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫॷ") in CONFIG or bstack111111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ॸ") in CONFIG) and bstack1llll1111l_opy_()
def bstack1l1ll11l11_opy_(config):
  bstack11l1l111l_opy_ = {}
  if bstack111111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧॹ") in config:
    bstack11l1l111l_opy_ = config[bstack111111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॺ")]
  if bstack111111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫॻ") in config:
    bstack11l1l111l_opy_ = config[bstack111111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬॼ")]
  proxy = bstack1ll11l1l11_opy_(config)
  if proxy:
    if proxy.endswith(bstack111111l_opy_ (u"ࠧ࠯ࡲࡤࡧࠬॽ")) and os.path.isfile(proxy):
      bstack11l1l111l_opy_[bstack111111l_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫॾ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack111111l_opy_ (u"ࠩ࠱ࡴࡦࡩࠧॿ")):
        proxies = bstack1ll11ll111_opy_(config, bstack1ll1l1111_opy_())
        if len(proxies) > 0:
          protocol, bstack11ll111l_opy_ = proxies.popitem()
          if bstack111111l_opy_ (u"ࠥ࠾࠴࠵ࠢঀ") in bstack11ll111l_opy_:
            parsed_url = urlparse(bstack11ll111l_opy_)
          else:
            parsed_url = urlparse(protocol + bstack111111l_opy_ (u"ࠦ࠿࠵࠯ࠣঁ") + bstack11ll111l_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack11l1l111l_opy_[bstack111111l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨং")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack11l1l111l_opy_[bstack111111l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩঃ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack11l1l111l_opy_[bstack111111l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ঄")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack11l1l111l_opy_[bstack111111l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫঅ")] = str(parsed_url.password)
  return bstack11l1l111l_opy_
def bstack1lll1lll_opy_(config):
  if bstack111111l_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧআ") in config:
    return config[bstack111111l_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨই")]
  return {}
def bstack1l11l11l1_opy_(caps):
  global bstack1llllll11_opy_
  if bstack111111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬঈ") in caps:
    caps[bstack111111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭উ")][bstack111111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬঊ")] = True
    if bstack1llllll11_opy_:
      caps[bstack111111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨঋ")][bstack111111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪঌ")] = bstack1llllll11_opy_
  else:
    caps[bstack111111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧ঍")] = True
    if bstack1llllll11_opy_:
      caps[bstack111111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ঎")] = bstack1llllll11_opy_
def bstack1111l111_opy_():
  global CONFIG
  if bstack111111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨএ") in CONFIG and bstack1ll111111_opy_(CONFIG[bstack111111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩঐ")]):
    bstack11l1l111l_opy_ = bstack1l1ll11l11_opy_(CONFIG)
    bstack111l111ll_opy_(CONFIG[bstack111111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ঑")], bstack11l1l111l_opy_)
def bstack111l111ll_opy_(key, bstack11l1l111l_opy_):
  global bstack1lll1lll11_opy_
  logger.info(bstack1ll1l1l11_opy_)
  try:
    bstack1lll1lll11_opy_ = Local()
    bstack1ll1llll_opy_ = {bstack111111l_opy_ (u"ࠧ࡬ࡧࡼࠫ঒"): key}
    bstack1ll1llll_opy_.update(bstack11l1l111l_opy_)
    logger.debug(bstack1lll111l1l_opy_.format(str(bstack1ll1llll_opy_)))
    bstack1lll1lll11_opy_.start(**bstack1ll1llll_opy_)
    if bstack1lll1lll11_opy_.isRunning():
      logger.info(bstack1ll1l1lll_opy_)
  except Exception as e:
    bstack1l1llll11_opy_(bstack1ll11lll1l_opy_.format(str(e)))
def bstack1lll1l11l1_opy_():
  global bstack1lll1lll11_opy_
  if bstack1lll1lll11_opy_.isRunning():
    logger.info(bstack1lll1l11_opy_)
    bstack1lll1lll11_opy_.stop()
  bstack1lll1lll11_opy_ = None
def bstack1llll1lll_opy_(bstack1ll1ll1ll1_opy_=[]):
  global CONFIG
  bstack1ll11l11_opy_ = []
  bstack1lllllllll_opy_ = [bstack111111l_opy_ (u"ࠨࡱࡶࠫও"), bstack111111l_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬঔ"), bstack111111l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧক"), bstack111111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭খ"), bstack111111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪগ"), bstack111111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧঘ")]
  try:
    for err in bstack1ll1ll1ll1_opy_:
      bstack1ll111111l_opy_ = {}
      for k in bstack1lllllllll_opy_:
        val = CONFIG[bstack111111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪঙ")][int(err[bstack111111l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧচ")])].get(k)
        if val:
          bstack1ll111111l_opy_[k] = val
      if(err[bstack111111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨছ")] != bstack111111l_opy_ (u"ࠪࠫজ")):
        bstack1ll111111l_opy_[bstack111111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡵࠪঝ")] = {
          err[bstack111111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪঞ")]: err[bstack111111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬট")]
        }
        bstack1ll11l11_opy_.append(bstack1ll111111l_opy_)
  except Exception as e:
    logger.debug(bstack111111l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡳࡷࡳࡡࡵࡶ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࠺ࠡࠩঠ") + str(e))
  finally:
    return bstack1ll11l11_opy_
def bstack111l111l_opy_(file_name):
  bstack1l1l1l1ll1_opy_ = []
  try:
    bstack1ll1111111_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1ll1111111_opy_):
      with open(bstack1ll1111111_opy_) as f:
        bstack1ll1l1ll_opy_ = json.load(f)
        bstack1l1l1l1ll1_opy_ = bstack1ll1l1ll_opy_
      os.remove(bstack1ll1111111_opy_)
    return bstack1l1l1l1ll1_opy_
  except Exception as e:
    logger.debug(bstack111111l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡤࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣࡰ࡮ࡹࡴ࠻ࠢࠪড") + str(e))
def bstack11lll11l_opy_():
  global bstack1l1lllllll_opy_
  global bstack11l1l11ll_opy_
  global bstack1ll1l11ll_opy_
  global bstack1l11lll1_opy_
  global bstack111111ll_opy_
  global bstack1l1ll1lll1_opy_
  percy.shutdown()
  bstack1llll11lll_opy_ = os.environ.get(bstack111111l_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪঢ"))
  if bstack1llll11lll_opy_ in [bstack111111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩণ"), bstack111111l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪত")]:
    bstack1l1llllll1_opy_()
  if bstack1l1lllllll_opy_:
    logger.warning(bstack1l111lll_opy_.format(str(bstack1l1lllllll_opy_)))
  else:
    try:
      bstack1l11l111_opy_ = bstack1ll1l111_opy_(bstack111111l_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫথ"), logger)
      if bstack1l11l111_opy_.get(bstack111111l_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫদ")) and bstack1l11l111_opy_.get(bstack111111l_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬধ")).get(bstack111111l_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪন")):
        logger.warning(bstack1l111lll_opy_.format(str(bstack1l11l111_opy_[bstack111111l_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ঩")][bstack111111l_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬপ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack11l111l1l_opy_)
  global bstack1lll1lll11_opy_
  if bstack1lll1lll11_opy_:
    bstack1lll1l11l1_opy_()
  try:
    for driver in bstack11l1l11ll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1111lll1l_opy_)
  if bstack1l1ll1lll1_opy_ == bstack111111l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪফ"):
    bstack111111ll_opy_ = bstack111l111l_opy_(bstack111111l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ব"))
  if bstack1l1ll1lll1_opy_ == bstack111111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ভ") and len(bstack1l11lll1_opy_) == 0:
    bstack1l11lll1_opy_ = bstack111l111l_opy_(bstack111111l_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬম"))
    if len(bstack1l11lll1_opy_) == 0:
      bstack1l11lll1_opy_ = bstack111l111l_opy_(bstack111111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧয"))
  bstack111lll1ll_opy_ = bstack111111l_opy_ (u"ࠩࠪর")
  if len(bstack1ll1l11ll_opy_) > 0:
    bstack111lll1ll_opy_ = bstack1llll1lll_opy_(bstack1ll1l11ll_opy_)
  elif len(bstack1l11lll1_opy_) > 0:
    bstack111lll1ll_opy_ = bstack1llll1lll_opy_(bstack1l11lll1_opy_)
  elif len(bstack111111ll_opy_) > 0:
    bstack111lll1ll_opy_ = bstack1llll1lll_opy_(bstack111111ll_opy_)
  elif len(bstack1ll1l11l1_opy_) > 0:
    bstack111lll1ll_opy_ = bstack1llll1lll_opy_(bstack1ll1l11l1_opy_)
  if bool(bstack111lll1ll_opy_):
    bstack111l1111l_opy_(bstack111lll1ll_opy_)
  else:
    bstack111l1111l_opy_()
  bstack1l1l11llll_opy_(bstack1l1111111_opy_, logger)
def bstack1ll11l111_opy_(self, *args):
  logger.error(bstack1ll111l11_opy_)
  bstack11lll11l_opy_()
  sys.exit(1)
def bstack1l1llll11_opy_(err):
  logger.critical(bstack1l1llll1l_opy_.format(str(err)))
  bstack111l1111l_opy_(bstack1l1llll1l_opy_.format(str(err)), True)
  atexit.unregister(bstack11lll11l_opy_)
  bstack1l1llllll1_opy_()
  sys.exit(1)
def bstack1llll1llll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack111l1111l_opy_(message, True)
  atexit.unregister(bstack11lll11l_opy_)
  bstack1l1llllll1_opy_()
  sys.exit(1)
def bstack1lll11l11l_opy_():
  global CONFIG
  global bstack1l1l11ll_opy_
  global bstack1lll11l1l1_opy_
  global bstack1l1l1l1l_opy_
  CONFIG = bstack1lll11l111_opy_()
  bstack1l1l11l1l_opy_()
  bstack1lll111111_opy_()
  CONFIG = bstack1ll1l1llll_opy_(CONFIG)
  update(CONFIG, bstack1lll11l1l1_opy_)
  update(CONFIG, bstack1l1l11ll_opy_)
  CONFIG = bstack1111lllll_opy_(CONFIG)
  bstack1l1l1l1l_opy_ = bstack1llll1l11_opy_(CONFIG)
  bstack1111ll1ll_opy_.bstack1l1ll1l1_opy_(bstack111111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ঱"), bstack1l1l1l1l_opy_)
  if (bstack111111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧল") in CONFIG and bstack111111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ঳") in bstack1l1l11ll_opy_) or (
          bstack111111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ঴") in CONFIG and bstack111111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ঵") not in bstack1lll11l1l1_opy_):
    if os.getenv(bstack111111l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬশ")):
      CONFIG[bstack111111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫষ")] = os.getenv(bstack111111l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧস"))
    else:
      bstack1lll1ll1ll_opy_()
  elif (bstack111111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧহ") not in CONFIG and bstack111111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ঺") in CONFIG) or (
          bstack111111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ঻") in bstack1lll11l1l1_opy_ and bstack111111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧ়ࠪ") not in bstack1l1l11ll_opy_):
    del (CONFIG[bstack111111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪঽ")])
  if bstack1l1lllll1l_opy_(CONFIG):
    bstack1l1llll11_opy_(bstack11llll111_opy_)
  bstack1lll1l111l_opy_()
  bstack1ll11111l_opy_()
  if bstack11l111l1_opy_:
    CONFIG[bstack111111l_opy_ (u"ࠩࡤࡴࡵ࠭া")] = bstack1l1l111lll_opy_(CONFIG)
    logger.info(bstack1l1lll1111_opy_.format(CONFIG[bstack111111l_opy_ (u"ࠪࡥࡵࡶࠧি")]))
def bstack1ll11ll11l_opy_(config, bstack111l11ll_opy_):
  global CONFIG
  global bstack11l111l1_opy_
  CONFIG = config
  bstack11l111l1_opy_ = bstack111l11ll_opy_
def bstack1ll11111l_opy_():
  global CONFIG
  global bstack11l111l1_opy_
  if bstack111111l_opy_ (u"ࠫࡦࡶࡰࠨী") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1llll1llll_opy_(e, bstack1111l11ll_opy_)
    bstack11l111l1_opy_ = True
    bstack1111ll1ll_opy_.bstack1l1ll1l1_opy_(bstack111111l_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫু"), True)
def bstack1l1l111lll_opy_(config):
  bstack11l11llll_opy_ = bstack111111l_opy_ (u"࠭ࠧূ")
  app = config[bstack111111l_opy_ (u"ࠧࡢࡲࡳࠫৃ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1llll1l111_opy_:
      if os.path.exists(app):
        bstack11l11llll_opy_ = bstack1lllllll1l_opy_(config, app)
      elif bstack1lll11ll1_opy_(app):
        bstack11l11llll_opy_ = app
      else:
        bstack1l1llll11_opy_(bstack1ll1llll1_opy_.format(app))
    else:
      if bstack1lll11ll1_opy_(app):
        bstack11l11llll_opy_ = app
      elif os.path.exists(app):
        bstack11l11llll_opy_ = bstack1lllllll1l_opy_(app)
      else:
        bstack1l1llll11_opy_(bstack1ll11ll1ll_opy_)
  else:
    if len(app) > 2:
      bstack1l1llll11_opy_(bstack11ll11ll_opy_)
    elif len(app) == 2:
      if bstack111111l_opy_ (u"ࠨࡲࡤࡸ࡭࠭ৄ") in app and bstack111111l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ৅") in app:
        if os.path.exists(app[bstack111111l_opy_ (u"ࠪࡴࡦࡺࡨࠨ৆")]):
          bstack11l11llll_opy_ = bstack1lllllll1l_opy_(config, app[bstack111111l_opy_ (u"ࠫࡵࡧࡴࡩࠩে")], app[bstack111111l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨৈ")])
        else:
          bstack1l1llll11_opy_(bstack1ll1llll1_opy_.format(app))
      else:
        bstack1l1llll11_opy_(bstack11ll11ll_opy_)
    else:
      for key in app:
        if key in bstack1ll11ll11_opy_:
          if key == bstack111111l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ৉"):
            if os.path.exists(app[key]):
              bstack11l11llll_opy_ = bstack1lllllll1l_opy_(config, app[key])
            else:
              bstack1l1llll11_opy_(bstack1ll1llll1_opy_.format(app))
          else:
            bstack11l11llll_opy_ = app[key]
        else:
          bstack1l1llll11_opy_(bstack1ll1ll111_opy_)
  return bstack11l11llll_opy_
def bstack1lll11ll1_opy_(bstack11l11llll_opy_):
  import re
  bstack1ll1l1ll1_opy_ = re.compile(bstack111111l_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢ৊"))
  bstack111ll111l_opy_ = re.compile(bstack111111l_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰࠯࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧো"))
  if bstack111111l_opy_ (u"ࠩࡥࡷ࠿࠵࠯ࠨৌ") in bstack11l11llll_opy_ or re.fullmatch(bstack1ll1l1ll1_opy_, bstack11l11llll_opy_) or re.fullmatch(bstack111ll111l_opy_, bstack11l11llll_opy_):
    return True
  else:
    return False
def bstack1lllllll1l_opy_(config, path, bstack1lll11l1ll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack111111l_opy_ (u"ࠪࡶࡧ্࠭")).read()).hexdigest()
  bstack1l1l1ll1l_opy_ = bstack1l11l1l1l_opy_(md5_hash)
  bstack11l11llll_opy_ = None
  if bstack1l1l1ll1l_opy_:
    logger.info(bstack1ll1lll11_opy_.format(bstack1l1l1ll1l_opy_, md5_hash))
    return bstack1l1l1ll1l_opy_
  bstack1l11ll111_opy_ = MultipartEncoder(
    fields={
      bstack111111l_opy_ (u"ࠫ࡫࡯࡬ࡦࠩৎ"): (os.path.basename(path), open(os.path.abspath(path), bstack111111l_opy_ (u"ࠬࡸࡢࠨ৏")), bstack111111l_opy_ (u"࠭ࡴࡦࡺࡷ࠳ࡵࡲࡡࡪࡰࠪ৐")),
      bstack111111l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ৑"): bstack1lll11l1ll_opy_
    }
  )
  response = requests.post(bstack1ll1l1111l_opy_, data=bstack1l11ll111_opy_,
                           headers={bstack111111l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ৒"): bstack1l11ll111_opy_.content_type},
                           auth=(config[bstack111111l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ৓")], config[bstack111111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭৔")]))
  try:
    res = json.loads(response.text)
    bstack11l11llll_opy_ = res[bstack111111l_opy_ (u"ࠫࡦࡶࡰࡠࡷࡵࡰࠬ৕")]
    logger.info(bstack1llll11111_opy_.format(bstack11l11llll_opy_))
    bstack11l1ll111_opy_(md5_hash, bstack11l11llll_opy_)
  except ValueError as err:
    bstack1l1llll11_opy_(bstack1l11lll1l_opy_.format(str(err)))
  return bstack11l11llll_opy_
def bstack1lll1l111l_opy_():
  global CONFIG
  global bstack1l1l1111_opy_
  bstack1l1ll1ll_opy_ = 0
  bstack1ll111l1l_opy_ = 1
  if bstack111111l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ৖") in CONFIG:
    bstack1ll111l1l_opy_ = CONFIG[bstack111111l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ৗ")]
  if bstack111111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৘") in CONFIG:
    bstack1l1ll1ll_opy_ = len(CONFIG[bstack111111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ৙")])
  bstack1l1l1111_opy_ = int(bstack1ll111l1l_opy_) * int(bstack1l1ll1ll_opy_)
def bstack1l11l1l1l_opy_(md5_hash):
  bstack11l11l11l_opy_ = os.path.join(os.path.expanduser(bstack111111l_opy_ (u"ࠩࢁࠫ৚")), bstack111111l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ৛"), bstack111111l_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬড়"))
  if os.path.exists(bstack11l11l11l_opy_):
    bstack1111llll_opy_ = json.load(open(bstack11l11l11l_opy_, bstack111111l_opy_ (u"ࠬࡸࡢࠨঢ়")))
    if md5_hash in bstack1111llll_opy_:
      bstack1l11l1ll_opy_ = bstack1111llll_opy_[md5_hash]
      bstack1ll1l111l_opy_ = datetime.datetime.now()
      bstack11l11l1l_opy_ = datetime.datetime.strptime(bstack1l11l1ll_opy_[bstack111111l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ৞")], bstack111111l_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫয়"))
      if (bstack1ll1l111l_opy_ - bstack11l11l1l_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1l11l1ll_opy_[bstack111111l_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ৠ")]):
        return None
      return bstack1l11l1ll_opy_[bstack111111l_opy_ (u"ࠩ࡬ࡨࠬৡ")]
  else:
    return None
def bstack11l1ll111_opy_(md5_hash, bstack11l11llll_opy_):
  bstack11l11lll_opy_ = os.path.join(os.path.expanduser(bstack111111l_opy_ (u"ࠪࢂࠬৢ")), bstack111111l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫৣ"))
  if not os.path.exists(bstack11l11lll_opy_):
    os.makedirs(bstack11l11lll_opy_)
  bstack11l11l11l_opy_ = os.path.join(os.path.expanduser(bstack111111l_opy_ (u"ࠬࢄࠧ৤")), bstack111111l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭৥"), bstack111111l_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ০"))
  bstack1lll111ll1_opy_ = {
    bstack111111l_opy_ (u"ࠨ࡫ࡧࠫ১"): bstack11l11llll_opy_,
    bstack111111l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ২"): datetime.datetime.strftime(datetime.datetime.now(), bstack111111l_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧ৩")),
    bstack111111l_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ৪"): str(__version__)
  }
  if os.path.exists(bstack11l11l11l_opy_):
    bstack1111llll_opy_ = json.load(open(bstack11l11l11l_opy_, bstack111111l_opy_ (u"ࠬࡸࡢࠨ৫")))
  else:
    bstack1111llll_opy_ = {}
  bstack1111llll_opy_[md5_hash] = bstack1lll111ll1_opy_
  with open(bstack11l11l11l_opy_, bstack111111l_opy_ (u"ࠨࡷࠬࠤ৬")) as outfile:
    json.dump(bstack1111llll_opy_, outfile)
def bstack11l11l111_opy_(self):
  return
def bstack11ll11l11_opy_(self):
  return
def bstack11111111l_opy_(self):
  global bstack11llllll_opy_
  bstack11llllll_opy_(self)
def bstack1l1lll1l_opy_():
  global bstack1l1ll1111l_opy_
  bstack1l1ll1111l_opy_ = True
def bstack1lll1ll1l1_opy_(self):
  global bstack1ll1llll11_opy_
  global bstack1l1l11ll11_opy_
  global bstack1ll111lll_opy_
  try:
    if bstack111111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ৭") in bstack1ll1llll11_opy_ and self.session_id != None and bstack1l1l1l111_opy_(threading.current_thread(), bstack111111l_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬ৮"), bstack111111l_opy_ (u"ࠩࠪ৯")) != bstack111111l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫৰ"):
      bstack1l1llllll_opy_ = bstack111111l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫৱ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack111111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ৲")
      if bstack1l1llllll_opy_ == bstack111111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭৳"):
        bstack11ll111ll_opy_(logger)
      if self != None:
        bstack111llll1l_opy_(self, bstack1l1llllll_opy_, bstack111111l_opy_ (u"ࠧ࠭ࠢࠪ৴").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack111111l_opy_ (u"ࠨࠩ৵")
    if bstack111111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ৶") in bstack1ll1llll11_opy_ and getattr(threading.current_thread(), bstack111111l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ৷"), None):
      bstack11l11ll11_opy_.bstack1ll1l1l11l_opy_(self, bstack111l11lll_opy_, logger, wait=True)
  except Exception as e:
    logger.debug(bstack111111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧ৸") + str(e))
  bstack1ll111lll_opy_(self)
  self.session_id = None
def bstack11llll1ll_opy_(self, command_executor=bstack111111l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴࠷࠲࠸࠰࠳࠲࠵࠴࠱࠻࠶࠷࠸࠹ࠨ৹"), *args, **kwargs):
  bstack1l1ll11l1l_opy_ = bstack11l11111_opy_(self, command_executor, *args, **kwargs)
  try:
    logger.debug(bstack111111l_opy_ (u"࠭ࡃࡰ࡯ࡰࡥࡳࡪࠠࡆࡺࡨࡧࡺࡺ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣ࡭ࡸࠦࡦࡢ࡮ࡶࡩࠥ࠳ࠠࡼࡿࠪ৺").format(str(command_executor)))
    logger.debug(bstack111111l_opy_ (u"ࠧࡉࡷࡥࠤ࡚ࡘࡌࠡ࡫ࡶࠤ࠲ࠦࡻࡾࠩ৻").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack111111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫৼ") in command_executor._url:
      bstack1111ll1ll_opy_.bstack1l1ll1l1_opy_(bstack111111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ৽"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack111111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭৾") in command_executor):
    bstack1111ll1ll_opy_.bstack1l1ll1l1_opy_(bstack111111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ৿"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack111lll1l_opy_.bstack1llllll1ll_opy_(self)
  return bstack1l1ll11l1l_opy_
def bstack1l1l11l11_opy_(self, driver_command, *args, **kwargs):
  global bstack1l111l1l1_opy_
  response = bstack1l111l1l1_opy_(self, driver_command, *args, **kwargs)
  try:
    if driver_command == bstack111111l_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩ਀"):
      bstack111lll1l_opy_.bstack1ll1lllll_opy_({
          bstack111111l_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬਁ"): response[bstack111111l_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭ਂ")],
          bstack111111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨਃ"): bstack111lll1l_opy_.current_test_uuid() if bstack111lll1l_opy_.current_test_uuid() else bstack111lll1l_opy_.current_hook_uuid()
      })
  except:
    pass
  return response
def bstack11l1l1l1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1l1l11ll11_opy_
  global bstack1llll1ll11_opy_
  global bstack1ll11111ll_opy_
  global bstack1lll1l1l11_opy_
  global bstack1ll11l1111_opy_
  global bstack1ll1llll11_opy_
  global bstack11l11111_opy_
  global bstack11l1l11ll_opy_
  global bstack1lll11111_opy_
  global bstack111l11lll_opy_
  CONFIG[bstack111111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ਄")] = str(bstack1ll1llll11_opy_) + str(__version__)
  command_executor = bstack1ll1l1111_opy_()
  logger.debug(bstack11lll11l1_opy_.format(command_executor))
  proxy = bstack1l1l11ll1_opy_(CONFIG, proxy)
  bstack111l1l1l_opy_ = 0 if bstack1llll1ll11_opy_ < 0 else bstack1llll1ll11_opy_
  try:
    if bstack1lll1l1l11_opy_ is True:
      bstack111l1l1l_opy_ = int(multiprocessing.current_process().name)
    elif bstack1ll11l1111_opy_ is True:
      bstack111l1l1l_opy_ = int(threading.current_thread().name)
  except:
    bstack111l1l1l_opy_ = 0
  bstack1l1ll111l1_opy_ = bstack1l1ll11l_opy_(CONFIG, bstack111l1l1l_opy_)
  logger.debug(bstack11l1ll11l_opy_.format(str(bstack1l1ll111l1_opy_)))
  if bstack111111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧਅ") in CONFIG and bstack1ll111111_opy_(CONFIG[bstack111111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨਆ")]):
    bstack1l11l11l1_opy_(bstack1l1ll111l1_opy_)
  if desired_capabilities:
    bstack1111l11l1_opy_ = bstack1ll1l1llll_opy_(desired_capabilities)
    bstack1111l11l1_opy_[bstack111111l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬਇ")] = bstack1lllll11_opy_(CONFIG)
    bstack111ll1l1_opy_ = bstack1l1ll11l_opy_(bstack1111l11l1_opy_)
    if bstack111ll1l1_opy_:
      bstack1l1ll111l1_opy_ = update(bstack111ll1l1_opy_, bstack1l1ll111l1_opy_)
    desired_capabilities = None
  if options:
    bstack1l1l1ll111_opy_(options, bstack1l1ll111l1_opy_)
  if not options:
    options = bstack1ll1111ll1_opy_(bstack1l1ll111l1_opy_)
  bstack111l11lll_opy_ = CONFIG.get(bstack111111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਈ"))[bstack111l1l1l_opy_]
  if bstack1lll111lll_opy_.bstack1111l1lll_opy_(CONFIG, bstack111l1l1l_opy_) and bstack1lll111lll_opy_.bstack1l11l111l_opy_(bstack1l1ll111l1_opy_, options):
    threading.current_thread().a11yPlatform = True
    bstack1lll111lll_opy_.set_capabilities(bstack1l1ll111l1_opy_, CONFIG)
  if proxy and bstack11111ll11_opy_() >= version.parse(bstack111111l_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧਉ")):
    options.proxy(proxy)
  if options and bstack11111ll11_opy_() >= version.parse(bstack111111l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧਊ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack11111ll11_opy_() < version.parse(bstack111111l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ਋")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1l1ll111l1_opy_)
  logger.info(bstack1l1l1l11l1_opy_)
  if bstack11111ll11_opy_() >= version.parse(bstack111111l_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪ਌")):
    bstack11l11111_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11111ll11_opy_() >= version.parse(bstack111111l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ਍")):
    bstack11l11111_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11111ll11_opy_() >= version.parse(bstack111111l_opy_ (u"ࠬ࠸࠮࠶࠵࠱࠴ࠬ਎")):
    bstack11l11111_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack11l11111_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack1111l1l1l_opy_ = bstack111111l_opy_ (u"࠭ࠧਏ")
    if bstack11111ll11_opy_() >= version.parse(bstack111111l_opy_ (u"ࠧ࠵࠰࠳࠲࠵ࡨ࠱ࠨਐ")):
      bstack1111l1l1l_opy_ = self.caps.get(bstack111111l_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ਑"))
    else:
      bstack1111l1l1l_opy_ = self.capabilities.get(bstack111111l_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤ਒"))
    if bstack1111l1l1l_opy_:
      bstack1lll1lll1l_opy_(bstack1111l1l1l_opy_)
      if bstack11111ll11_opy_() <= version.parse(bstack111111l_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪਓ")):
        self.command_executor._url = bstack111111l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧਔ") + bstack111111ll1_opy_ + bstack111111l_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤਕ")
      else:
        self.command_executor._url = bstack111111l_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣਖ") + bstack1111l1l1l_opy_ + bstack111111l_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣਗ")
      logger.debug(bstack1l1ll1l1l_opy_.format(bstack1111l1l1l_opy_))
    else:
      logger.debug(bstack111111l1_opy_.format(bstack111111l_opy_ (u"ࠣࡑࡳࡸ࡮ࡳࡡ࡭ࠢࡋࡹࡧࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠤਘ")))
  except Exception as e:
    logger.debug(bstack111111l1_opy_.format(e))
  if bstack111111l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨਙ") in bstack1ll1llll11_opy_:
    bstack11l1lll1_opy_(bstack1llll1ll11_opy_, bstack1lll11111_opy_)
  bstack1l1l11ll11_opy_ = self.session_id
  if bstack111111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪਚ") in bstack1ll1llll11_opy_ or bstack111111l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫਛ") in bstack1ll1llll11_opy_ or bstack111111l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫਜ") in bstack1ll1llll11_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack111lll1l_opy_.bstack1llllll1ll_opy_(self)
  bstack11l1l11ll_opy_.append(self)
  if bstack111111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਝ") in CONFIG and bstack111111l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬਞ") in CONFIG[bstack111111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫਟ")][bstack111l1l1l_opy_]:
    bstack1ll11111ll_opy_ = CONFIG[bstack111111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬਠ")][bstack111l1l1l_opy_][bstack111111l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨਡ")]
  logger.debug(bstack11l1l1lll_opy_.format(bstack1l1l11ll11_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1l1ll111l_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1111111ll_opy_
      if(bstack111111l_opy_ (u"ࠦ࡮ࡴࡤࡦࡺ࠱࡮ࡸࠨਢ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack111111l_opy_ (u"ࠬࢄࠧਣ")), bstack111111l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ਤ"), bstack111111l_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩਥ")), bstack111111l_opy_ (u"ࠨࡹࠪਦ")) as fp:
          fp.write(bstack111111l_opy_ (u"ࠤࠥਧ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack111111l_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧਨ")))):
          with open(args[1], bstack111111l_opy_ (u"ࠫࡷ࠭਩")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack111111l_opy_ (u"ࠬࡧࡳࡺࡰࡦࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦ࡟࡯ࡧࡺࡔࡦ࡭ࡥࠩࡥࡲࡲࡹ࡫ࡸࡵ࠮ࠣࡴࡦ࡭ࡥࠡ࠿ࠣࡺࡴ࡯ࡤࠡ࠲ࠬࠫਪ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l1l1l1lll_opy_)
            lines.insert(1, bstack11l11lll1_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack111111l_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣਫ")), bstack111111l_opy_ (u"ࠧࡸࠩਬ")) as bstack1l1lll1l11_opy_:
              bstack1l1lll1l11_opy_.writelines(lines)
        CONFIG[bstack111111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪਭ")] = str(bstack1ll1llll11_opy_) + str(__version__)
        bstack111l1l1l_opy_ = 0 if bstack1llll1ll11_opy_ < 0 else bstack1llll1ll11_opy_
        try:
          if bstack1lll1l1l11_opy_ is True:
            bstack111l1l1l_opy_ = int(multiprocessing.current_process().name)
          elif bstack1ll11l1111_opy_ is True:
            bstack111l1l1l_opy_ = int(threading.current_thread().name)
        except:
          bstack111l1l1l_opy_ = 0
        CONFIG[bstack111111l_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤਮ")] = False
        CONFIG[bstack111111l_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤਯ")] = True
        bstack1l1ll111l1_opy_ = bstack1l1ll11l_opy_(CONFIG, bstack111l1l1l_opy_)
        logger.debug(bstack11l1ll11l_opy_.format(str(bstack1l1ll111l1_opy_)))
        if CONFIG.get(bstack111111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨਰ")):
          bstack1l11l11l1_opy_(bstack1l1ll111l1_opy_)
        if bstack111111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ਱") in CONFIG and bstack111111l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫਲ") in CONFIG[bstack111111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪਲ਼")][bstack111l1l1l_opy_]:
          bstack1ll11111ll_opy_ = CONFIG[bstack111111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ਴")][bstack111l1l1l_opy_][bstack111111l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧਵ")]
        args.append(os.path.join(os.path.expanduser(bstack111111l_opy_ (u"ࠪࢂࠬਸ਼")), bstack111111l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ਷"), bstack111111l_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧਸ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1l1ll111l1_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack111111l_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣਹ"))
      bstack1111111ll_opy_ = True
      return bstack1l1ll1lll_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1ll11l1ll_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1llll1ll11_opy_
    global bstack1ll11111ll_opy_
    global bstack1lll1l1l11_opy_
    global bstack1ll11l1111_opy_
    global bstack1ll1llll11_opy_
    CONFIG[bstack111111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ਺")] = str(bstack1ll1llll11_opy_) + str(__version__)
    bstack111l1l1l_opy_ = 0 if bstack1llll1ll11_opy_ < 0 else bstack1llll1ll11_opy_
    try:
      if bstack1lll1l1l11_opy_ is True:
        bstack111l1l1l_opy_ = int(multiprocessing.current_process().name)
      elif bstack1ll11l1111_opy_ is True:
        bstack111l1l1l_opy_ = int(threading.current_thread().name)
    except:
      bstack111l1l1l_opy_ = 0
    CONFIG[bstack111111l_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ਻")] = True
    bstack1l1ll111l1_opy_ = bstack1l1ll11l_opy_(CONFIG, bstack111l1l1l_opy_)
    logger.debug(bstack11l1ll11l_opy_.format(str(bstack1l1ll111l1_opy_)))
    if CONFIG.get(bstack111111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ਼࠭")):
      bstack1l11l11l1_opy_(bstack1l1ll111l1_opy_)
    if bstack111111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭਽") in CONFIG and bstack111111l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩਾ") in CONFIG[bstack111111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨਿ")][bstack111l1l1l_opy_]:
      bstack1ll11111ll_opy_ = CONFIG[bstack111111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩੀ")][bstack111l1l1l_opy_][bstack111111l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬੁ")]
    import urllib
    import json
    bstack1lll11ll_opy_ = bstack111111l_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪੂ") + urllib.parse.quote(json.dumps(bstack1l1ll111l1_opy_))
    browser = self.connect(bstack1lll11ll_opy_)
    return browser
except Exception as e:
    pass
def bstack11ll1ll11_opy_():
    global bstack1111111ll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1ll11l1ll_opy_
        bstack1111111ll_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1l1ll111l_opy_
      bstack1111111ll_opy_ = True
    except Exception as e:
      pass
def bstack1llll11l11_opy_(context, bstack11l111ll1_opy_):
  try:
    context.page.evaluate(bstack111111l_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ੃"), bstack111111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧ੄")+ json.dumps(bstack11l111ll1_opy_) + bstack111111l_opy_ (u"ࠦࢂࢃࠢ੅"))
  except Exception as e:
    logger.debug(bstack111111l_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿࠥ੆"), e)
def bstack11l1l1l11_opy_(context, message, level):
  try:
    context.page.evaluate(bstack111111l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢੇ"), bstack111111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬੈ") + json.dumps(message) + bstack111111l_opy_ (u"ࠨ࠮ࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠫ੉") + json.dumps(level) + bstack111111l_opy_ (u"ࠩࢀࢁࠬ੊"))
  except Exception as e:
    logger.debug(bstack111111l_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠣࡿࢂࠨੋ"), e)
def bstack1l1lllll11_opy_(self, url):
  global bstack1ll11l11l_opy_
  try:
    bstack11ll1lll_opy_(url)
  except Exception as err:
    logger.debug(bstack1l1lll1ll1_opy_.format(str(err)))
  try:
    bstack1ll11l11l_opy_(self, url)
  except Exception as e:
    try:
      bstack1ll111ll11_opy_ = str(e)
      if any(err_msg in bstack1ll111ll11_opy_ for err_msg in bstack1llll111ll_opy_):
        bstack11ll1lll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l1lll1ll1_opy_.format(str(err)))
    raise e
def bstack11l11ll1_opy_(self):
  global bstack1l1l1l1l1_opy_
  bstack1l1l1l1l1_opy_ = self
  return
def bstack1lll1ll11_opy_(self):
  global bstack1l111ll1l_opy_
  bstack1l111ll1l_opy_ = self
  return
def bstack111lll11l_opy_(self, test):
  global CONFIG
  global bstack111l1ll11_opy_
  if CONFIG.get(bstack111111l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪੌ"), False):
    test_name = str(test.data)
    bstack1ll1111ll_opy_ = str(test.source)
    bstack1l1l111l_opy_ = os.path.relpath(bstack1ll1111ll_opy_, start=os.getcwd())
    suite_name, bstack1l1l1lll1l_opy_ = os.path.splitext(bstack1l1l111l_opy_)
    bstack1ll1l1l111_opy_ = suite_name + bstack111111l_opy_ (u"ࠧ࠳੍ࠢ") + test_name
    threading.current_thread().percySessionName = bstack1ll1l1l111_opy_
  bstack111l1ll11_opy_(self, test)
def bstack1lll111l11_opy_(self, test):
  global CONFIG
  global bstack1l111ll1l_opy_
  global bstack1l1l1l1l1_opy_
  global bstack1l1l11ll11_opy_
  global bstack1l11l1lll_opy_
  global bstack1ll11111ll_opy_
  global bstack1l1llll11l_opy_
  global bstack1ll1lll1_opy_
  global bstack1l11111l1_opy_
  global bstack1lll111ll_opy_
  global bstack11l1l11ll_opy_
  global bstack111l11lll_opy_
  try:
    if not bstack1l1l11ll11_opy_:
      with open(os.path.join(os.path.expanduser(bstack111111l_opy_ (u"࠭ࡾࠨ੎")), bstack111111l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ੏"), bstack111111l_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ੐"))) as f:
        bstack11l1l1111_opy_ = json.loads(bstack111111l_opy_ (u"ࠤࡾࠦੑ") + f.read().strip() + bstack111111l_opy_ (u"ࠪࠦࡽࠨ࠺ࠡࠤࡼࠦࠬ੒") + bstack111111l_opy_ (u"ࠦࢂࠨ੓"))
        bstack1l1l11ll11_opy_ = bstack11l1l1111_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack11l1l11ll_opy_:
    for driver in bstack11l1l11ll_opy_:
      if bstack1l1l11ll11_opy_ == driver.session_id:
        if test:
          bstack1ll1l1l111_opy_ = str(test.data)
          if CONFIG.get(bstack111111l_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ੔"), False):
            if CONFIG.get(bstack111111l_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩ੕"), bstack111111l_opy_ (u"ࠢࡢࡷࡷࡳࠧ੖")) == bstack111111l_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥ੗"):
              bstack111ll1lll_opy_ = bstack1l1l1l111_opy_(threading.current_thread(), bstack111111l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ੘"), None)
              bstack1ll1ll111l_opy_(driver, bstack111ll1lll_opy_)
          if bstack1l1l1l111_opy_(threading.current_thread(), bstack111111l_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧਖ਼"), None) and bstack1l1l1l111_opy_(threading.current_thread(), bstack111111l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪਗ਼"), None):
            logger.info(bstack111111l_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠤࠧਜ਼"))
            bstack1lll111lll_opy_.bstack111l11111_opy_(driver, class_name=test.parent.name, name=test.name, module_name=None, path=test.source, bstack1lll1ll1l_opy_=bstack111l11lll_opy_)
        if not bstack1l1lll111l_opy_ and bstack1ll1l1l111_opy_:
          bstack11l1ll1l1_opy_ = {
            bstack111111l_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ੜ"): bstack111111l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ੝"),
            bstack111111l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫਫ਼"): {
              bstack111111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ੟"): bstack1ll1l1l111_opy_
            }
          }
          bstack11l11l11_opy_ = bstack111111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ੠").format(json.dumps(bstack11l1ll1l1_opy_))
          driver.execute_script(bstack11l11l11_opy_)
        if bstack1l11l1lll_opy_:
          bstack1ll111l1_opy_ = {
            bstack111111l_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫ੡"): bstack111111l_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧ੢"),
            bstack111111l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ੣"): {
              bstack111111l_opy_ (u"ࠧࡥࡣࡷࡥࠬ੤"): bstack1ll1l1l111_opy_ + bstack111111l_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪ੥"),
              bstack111111l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ੦"): bstack111111l_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨ੧")
            }
          }
          if bstack1l11l1lll_opy_.status == bstack111111l_opy_ (u"ࠫࡕࡇࡓࡔࠩ੨"):
            bstack1l1111ll1_opy_ = bstack111111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ੩").format(json.dumps(bstack1ll111l1_opy_))
            driver.execute_script(bstack1l1111ll1_opy_)
            bstack111llll1l_opy_(driver, bstack111111l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭੪"))
          elif bstack1l11l1lll_opy_.status == bstack111111l_opy_ (u"ࠧࡇࡃࡌࡐࠬ੫"):
            reason = bstack111111l_opy_ (u"ࠣࠤ੬")
            bstack1111111l_opy_ = bstack1ll1l1l111_opy_ + bstack111111l_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠪ੭")
            if bstack1l11l1lll_opy_.message:
              reason = str(bstack1l11l1lll_opy_.message)
              bstack1111111l_opy_ = bstack1111111l_opy_ + bstack111111l_opy_ (u"ࠪࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࠪ੮") + reason
            bstack1ll111l1_opy_[bstack111111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ੯")] = {
              bstack111111l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫੰ"): bstack111111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬੱ"),
              bstack111111l_opy_ (u"ࠧࡥࡣࡷࡥࠬੲ"): bstack1111111l_opy_
            }
            bstack1l1111ll1_opy_ = bstack111111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ੳ").format(json.dumps(bstack1ll111l1_opy_))
            driver.execute_script(bstack1l1111ll1_opy_)
            bstack111llll1l_opy_(driver, bstack111111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩੴ"), reason)
            bstack11l1lllll_opy_(reason, str(bstack1l11l1lll_opy_), str(bstack1llll1ll11_opy_), logger)
  elif bstack1l1l11ll11_opy_:
    try:
      data = {}
      bstack1ll1l1l111_opy_ = None
      if test:
        bstack1ll1l1l111_opy_ = str(test.data)
      if not bstack1l1lll111l_opy_ and bstack1ll1l1l111_opy_:
        data[bstack111111l_opy_ (u"ࠪࡲࡦࡳࡥࠨੵ")] = bstack1ll1l1l111_opy_
      if bstack1l11l1lll_opy_:
        if bstack1l11l1lll_opy_.status == bstack111111l_opy_ (u"ࠫࡕࡇࡓࡔࠩ੶"):
          data[bstack111111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ੷")] = bstack111111l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭੸")
        elif bstack1l11l1lll_opy_.status == bstack111111l_opy_ (u"ࠧࡇࡃࡌࡐࠬ੹"):
          data[bstack111111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ੺")] = bstack111111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ੻")
          if bstack1l11l1lll_opy_.message:
            data[bstack111111l_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ੼")] = str(bstack1l11l1lll_opy_.message)
      user = CONFIG[bstack111111l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭੽")]
      key = CONFIG[bstack111111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ੾")]
      url = bstack111111l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠲ࡿࢂ࠴ࡪࡴࡱࡱࠫ੿").format(user, key, bstack1l1l11ll11_opy_)
      headers = {
        bstack111111l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭઀"): bstack111111l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫઁ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1ll11ll1l1_opy_.format(str(e)))
  if bstack1l111ll1l_opy_:
    bstack1ll1lll1_opy_(bstack1l111ll1l_opy_)
  if bstack1l1l1l1l1_opy_:
    bstack1l11111l1_opy_(bstack1l1l1l1l1_opy_)
  if bstack1l1ll1111l_opy_:
    bstack1lll111ll_opy_()
  bstack1l1llll11l_opy_(self, test)
def bstack111llllll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11l1l11l1_opy_
  global CONFIG
  global bstack11l1l11ll_opy_
  global bstack1l1l11ll11_opy_
  bstack11111111_opy_ = None
  try:
    if bstack1l1l1l111_opy_(threading.current_thread(), bstack111111l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨં"), None):
      try:
        if not bstack1l1l11ll11_opy_:
          with open(os.path.join(os.path.expanduser(bstack111111l_opy_ (u"ࠪࢂࠬઃ")), bstack111111l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ઄"), bstack111111l_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧઅ"))) as f:
            bstack11l1l1111_opy_ = json.loads(bstack111111l_opy_ (u"ࠨࡻࠣઆ") + f.read().strip() + bstack111111l_opy_ (u"ࠧࠣࡺࠥ࠾ࠥࠨࡹࠣࠩઇ") + bstack111111l_opy_ (u"ࠣࡿࠥઈ"))
            bstack1l1l11ll11_opy_ = bstack11l1l1111_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack11l1l11ll_opy_:
        for driver in bstack11l1l11ll_opy_:
          if bstack1l1l11ll11_opy_ == driver.session_id:
            bstack11111111_opy_ = driver
    bstack1llll111_opy_ = bstack1lll111lll_opy_.bstack11ll1ll1l_opy_(CONFIG, test.tags)
    if bstack11111111_opy_:
      threading.current_thread().isA11yTest = bstack1lll111lll_opy_.bstack111ll11l_opy_(bstack11111111_opy_, bstack1llll111_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1llll111_opy_
  except:
    pass
  bstack11l1l11l1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l11l1lll_opy_
  bstack1l11l1lll_opy_ = self._test
def bstack11ll11lll_opy_():
  global bstack111ll11l1_opy_
  try:
    if os.path.exists(bstack111ll11l1_opy_):
      os.remove(bstack111ll11l1_opy_)
  except Exception as e:
    logger.debug(bstack111111l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬઉ") + str(e))
def bstack1l1l11ll1l_opy_():
  global bstack111ll11l1_opy_
  bstack1l11l111_opy_ = {}
  try:
    if not os.path.isfile(bstack111ll11l1_opy_):
      with open(bstack111ll11l1_opy_, bstack111111l_opy_ (u"ࠪࡻࠬઊ")):
        pass
      with open(bstack111ll11l1_opy_, bstack111111l_opy_ (u"ࠦࡼ࠱ࠢઋ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack111ll11l1_opy_):
      bstack1l11l111_opy_ = json.load(open(bstack111ll11l1_opy_, bstack111111l_opy_ (u"ࠬࡸࡢࠨઌ")))
  except Exception as e:
    logger.debug(bstack111111l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨઍ") + str(e))
  finally:
    return bstack1l11l111_opy_
def bstack11l1lll1_opy_(platform_index, item_index):
  global bstack111ll11l1_opy_
  try:
    bstack1l11l111_opy_ = bstack1l1l11ll1l_opy_()
    bstack1l11l111_opy_[item_index] = platform_index
    with open(bstack111ll11l1_opy_, bstack111111l_opy_ (u"ࠢࡸ࠭ࠥ઎")) as outfile:
      json.dump(bstack1l11l111_opy_, outfile)
  except Exception as e:
    logger.debug(bstack111111l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡻࡷ࡯ࡴࡪࡰࡪࠤࡹࡵࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭એ") + str(e))
def bstack111ll11ll_opy_(bstack1111lll11_opy_):
  global CONFIG
  bstack1l11111ll_opy_ = bstack111111l_opy_ (u"ࠩࠪઐ")
  if not bstack111111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ઑ") in CONFIG:
    logger.info(bstack111111l_opy_ (u"ࠫࡓࡵࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠣࡴࡦࡹࡳࡦࡦࠣࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡴࡨࡴࡴࡸࡴࠡࡨࡲࡶࠥࡘ࡯ࡣࡱࡷࠤࡷࡻ࡮ࠨ઒"))
  try:
    platform = CONFIG[bstack111111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨઓ")][bstack1111lll11_opy_]
    if bstack111111l_opy_ (u"࠭࡯ࡴࠩઔ") in platform:
      bstack1l11111ll_opy_ += str(platform[bstack111111l_opy_ (u"ࠧࡰࡵࠪક")]) + bstack111111l_opy_ (u"ࠨ࠮ࠣࠫખ")
    if bstack111111l_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬગ") in platform:
      bstack1l11111ll_opy_ += str(platform[bstack111111l_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ઘ")]) + bstack111111l_opy_ (u"ࠫ࠱ࠦࠧઙ")
    if bstack111111l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩચ") in platform:
      bstack1l11111ll_opy_ += str(platform[bstack111111l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪછ")]) + bstack111111l_opy_ (u"ࠧ࠭ࠢࠪજ")
    if bstack111111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪઝ") in platform:
      bstack1l11111ll_opy_ += str(platform[bstack111111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫઞ")]) + bstack111111l_opy_ (u"ࠪ࠰ࠥ࠭ટ")
    if bstack111111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩઠ") in platform:
      bstack1l11111ll_opy_ += str(platform[bstack111111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪડ")]) + bstack111111l_opy_ (u"࠭ࠬࠡࠩઢ")
    if bstack111111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨણ") in platform:
      bstack1l11111ll_opy_ += str(platform[bstack111111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩત")]) + bstack111111l_opy_ (u"ࠩ࠯ࠤࠬથ")
  except Exception as e:
    logger.debug(bstack111111l_opy_ (u"ࠪࡗࡴࡳࡥࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡶࡸࡷ࡯࡮ࡨࠢࡩࡳࡷࠦࡲࡦࡲࡲࡶࡹࠦࡧࡦࡰࡨࡶࡦࡺࡩࡰࡰࠪદ") + str(e))
  finally:
    if bstack1l11111ll_opy_[len(bstack1l11111ll_opy_) - 2:] == bstack111111l_opy_ (u"ࠫ࠱ࠦࠧધ"):
      bstack1l11111ll_opy_ = bstack1l11111ll_opy_[:-2]
    return bstack1l11111ll_opy_
def bstack111lll111_opy_(path, bstack1l11111ll_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1lllll1l11_opy_ = ET.parse(path)
    bstack1l1l1l1111_opy_ = bstack1lllll1l11_opy_.getroot()
    bstack1l1l111l1_opy_ = None
    for suite in bstack1l1l1l1111_opy_.iter(bstack111111l_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫન")):
      if bstack111111l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭઩") in suite.attrib:
        suite.attrib[bstack111111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬપ")] += bstack111111l_opy_ (u"ࠨࠢࠪફ") + bstack1l11111ll_opy_
        bstack1l1l111l1_opy_ = suite
    bstack111111l11_opy_ = None
    for robot in bstack1l1l1l1111_opy_.iter(bstack111111l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨબ")):
      bstack111111l11_opy_ = robot
    bstack1ll1ll1l1l_opy_ = len(bstack111111l11_opy_.findall(bstack111111l_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩભ")))
    if bstack1ll1ll1l1l_opy_ == 1:
      bstack111111l11_opy_.remove(bstack111111l11_opy_.findall(bstack111111l_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪમ"))[0])
      bstack1l1ll1ll11_opy_ = ET.Element(bstack111111l_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫય"), attrib={bstack111111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫર"): bstack111111l_opy_ (u"ࠧࡔࡷ࡬ࡸࡪࡹࠧ઱"), bstack111111l_opy_ (u"ࠨ࡫ࡧࠫલ"): bstack111111l_opy_ (u"ࠩࡶ࠴ࠬળ")})
      bstack111111l11_opy_.insert(1, bstack1l1ll1ll11_opy_)
      bstack111l1l11l_opy_ = None
      for suite in bstack111111l11_opy_.iter(bstack111111l_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩ઴")):
        bstack111l1l11l_opy_ = suite
      bstack111l1l11l_opy_.append(bstack1l1l111l1_opy_)
      bstack1ll11llll_opy_ = None
      for status in bstack1l1l111l1_opy_.iter(bstack111111l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫવ")):
        bstack1ll11llll_opy_ = status
      bstack111l1l11l_opy_.append(bstack1ll11llll_opy_)
    bstack1lllll1l11_opy_.write(path)
  except Exception as e:
    logger.debug(bstack111111l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠪશ") + str(e))
def bstack1l1l1llll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack11ll1111_opy_
  global CONFIG
  if bstack111111l_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡶࡡࡵࡪࠥષ") in options:
    del options[bstack111111l_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦસ")]
  bstack1l1l1ll1ll_opy_ = bstack1l1l11ll1l_opy_()
  for bstack1l1l1lll_opy_ in bstack1l1l1ll1ll_opy_.keys():
    path = os.path.join(os.getcwd(), bstack111111l_opy_ (u"ࠨࡲࡤࡦࡴࡺ࡟ࡳࡧࡶࡹࡱࡺࡳࠨહ"), str(bstack1l1l1lll_opy_), bstack111111l_opy_ (u"ࠩࡲࡹࡹࡶࡵࡵ࠰ࡻࡱࡱ࠭઺"))
    bstack111lll111_opy_(path, bstack111ll11ll_opy_(bstack1l1l1ll1ll_opy_[bstack1l1l1lll_opy_]))
  bstack11ll11lll_opy_()
  return bstack11ll1111_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1111lll1_opy_(self, ff_profile_dir):
  global bstack1l1lll11l_opy_
  if not ff_profile_dir:
    return None
  return bstack1l1lll11l_opy_(self, ff_profile_dir)
def bstack111111lll_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1llllll11_opy_
  bstack1llll11l1_opy_ = []
  if bstack111111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭઻") in CONFIG:
    bstack1llll11l1_opy_ = CONFIG[bstack111111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹ઼ࠧ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack111111l_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨઽ")],
      pabot_args[bstack111111l_opy_ (u"ࠨࡶࡦࡴࡥࡳࡸ࡫ࠢા")],
      argfile,
      pabot_args.get(bstack111111l_opy_ (u"ࠢࡩ࡫ࡹࡩࠧિ")),
      pabot_args[bstack111111l_opy_ (u"ࠣࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠦી")],
      platform[0],
      bstack1llllll11_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack111111l_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡪ࡮ࡲࡥࡴࠤુ")] or [(bstack111111l_opy_ (u"ࠥࠦૂ"), None)]
    for platform in enumerate(bstack1llll11l1_opy_)
  ]
def bstack11llll11_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack111l1llll_opy_=bstack111111l_opy_ (u"ࠫࠬૃ")):
  global bstack1ll11l1lll_opy_
  self.platform_index = platform_index
  self.bstack111l11l1_opy_ = bstack111l1llll_opy_
  bstack1ll11l1lll_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1ll11l111l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1llllll1l1_opy_
  global bstack1111l1l1_opy_
  if not bstack111111l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧૄ") in item.options:
    item.options[bstack111111l_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨૅ")] = []
  for v in item.options[bstack111111l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ૆")]:
    if bstack111111l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞ࠧે") in v:
      item.options[bstack111111l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫૈ")].remove(v)
    if bstack111111l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕࠪૉ") in v:
      item.options[bstack111111l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭૊")].remove(v)
  item.options[bstack111111l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧો")].insert(0, bstack111111l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜࠿ࢁࡽࠨૌ").format(item.platform_index))
  item.options[bstack111111l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦ્ࠩ")].insert(0, bstack111111l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ࠿ࢁࡽࠨ૎").format(item.bstack111l11l1_opy_))
  if bstack1111l1l1_opy_:
    item.options[bstack111111l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ૏")].insert(0, bstack111111l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕ࠽ࡿࢂ࠭ૐ").format(bstack1111l1l1_opy_))
  return bstack1llllll1l1_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack111ll1111_opy_(command, item_index):
  if bstack1111ll1ll_opy_.get_property(bstack111111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ૑")):
    os.environ[bstack111111l_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭૒")] = json.dumps(CONFIG[bstack111111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ૓")][item_index % bstack11l1111l_opy_])
  global bstack1111l1l1_opy_
  if bstack1111l1l1_opy_:
    command[0] = command[0].replace(bstack111111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭૔"), bstack111111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠬ૕") + str(
      item_index) + bstack111111l_opy_ (u"ࠩࠣࠫ૖") + bstack1111l1l1_opy_, 1)
  else:
    command[0] = command[0].replace(bstack111111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ૗"),
                                    bstack111111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡷࡩࡱࠠࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠡ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠠࠨ૘") + str(item_index), 1)
def bstack1l1lll1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1lll1l11l_opy_
  bstack111ll1111_opy_(command, item_index)
  return bstack1lll1l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1ll11lll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1lll1l11l_opy_
  bstack111ll1111_opy_(command, item_index)
  return bstack1lll1l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1llll11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1lll1l11l_opy_
  bstack111ll1111_opy_(command, item_index)
  return bstack1lll1l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack11lll111l_opy_(self, runner, quiet=False, capture=True):
  global bstack1l111ll11_opy_
  bstack11lll1l1l_opy_ = bstack1l111ll11_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack111111l_opy_ (u"ࠬ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࡠࡣࡵࡶࠬ૙")):
      runner.exception_arr = []
    if not hasattr(runner, bstack111111l_opy_ (u"࠭ࡥࡹࡥࡢࡸࡷࡧࡣࡦࡤࡤࡧࡰࡥࡡࡳࡴࠪ૚")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack11lll1l1l_opy_
def bstack1ll1ll1ll_opy_(self, name, context, *args):
  os.environ[bstack111111l_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨ૛")] = json.dumps(CONFIG[bstack111111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ૜")][int(threading.current_thread()._name) % bstack11l1111l_opy_])
  global bstack1ll1lllll1_opy_
  if name == bstack111111l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠪ૝"):
    bstack1ll1lllll1_opy_(self, name, context, *args)
    try:
      if not bstack1l1lll111l_opy_:
        bstack11111111_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1l11lll1_opy_(bstack111111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ૞")) else context.browser
        bstack11l111ll1_opy_ = str(self.feature.name)
        bstack1llll11l11_opy_(context, bstack11l111ll1_opy_)
        bstack11111111_opy_.execute_script(bstack111111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ૟") + json.dumps(bstack11l111ll1_opy_) + bstack111111l_opy_ (u"ࠬࢃࡽࠨૠ"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack111111l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ૡ").format(str(e)))
  elif name == bstack111111l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩૢ"):
    bstack1ll1lllll1_opy_(self, name, context, *args)
    try:
      if not hasattr(self, bstack111111l_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪૣ")):
        self.driver_before_scenario = True
      if (not bstack1l1lll111l_opy_):
        scenario_name = args[0].name
        feature_name = bstack11l111ll1_opy_ = str(self.feature.name)
        bstack11l111ll1_opy_ = feature_name + bstack111111l_opy_ (u"ࠩࠣ࠱ࠥ࠭૤") + scenario_name
        bstack11111111_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1l11lll1_opy_(bstack111111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ૥")) else context.browser
        if self.driver_before_scenario:
          bstack1llll11l11_opy_(context, bstack11l111ll1_opy_)
          bstack11111111_opy_.execute_script(bstack111111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ૦") + json.dumps(bstack11l111ll1_opy_) + bstack111111l_opy_ (u"ࠬࢃࡽࠨ૧"))
    except Exception as e:
      logger.debug(bstack111111l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧ૨").format(str(e)))
  elif name == bstack111111l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ૩"):
    try:
      bstack111l1ll1l_opy_ = args[0].status.name
      bstack11111111_opy_ = threading.current_thread().bstackSessionDriver if bstack111111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ૪") in threading.current_thread().__dict__.keys() else context.browser
      if str(bstack111l1ll1l_opy_).lower() == bstack111111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ૫"):
        bstack11l1l11l_opy_ = bstack111111l_opy_ (u"ࠪࠫ૬")
        bstack11ll1llll_opy_ = bstack111111l_opy_ (u"ࠫࠬ૭")
        bstack1l111lll1_opy_ = bstack111111l_opy_ (u"ࠬ࠭૮")
        try:
          import traceback
          bstack11l1l11l_opy_ = self.exception.__class__.__name__
          bstack1111l11l_opy_ = traceback.format_tb(self.exc_traceback)
          bstack11ll1llll_opy_ = bstack111111l_opy_ (u"࠭ࠠࠨ૯").join(bstack1111l11l_opy_)
          bstack1l111lll1_opy_ = bstack1111l11l_opy_[-1]
        except Exception as e:
          logger.debug(bstack1lll1111ll_opy_.format(str(e)))
        bstack11l1l11l_opy_ += bstack1l111lll1_opy_
        bstack11l1l1l11_opy_(context, json.dumps(str(args[0].name) + bstack111111l_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨ૰") + str(bstack11ll1llll_opy_)),
                            bstack111111l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ૱"))
        if self.driver_before_scenario:
          bstack1ll1l11111_opy_(getattr(context, bstack111111l_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ૲"), None), bstack111111l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ૳"), bstack11l1l11l_opy_)
          bstack11111111_opy_.execute_script(bstack111111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ૴") + json.dumps(str(args[0].name) + bstack111111l_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ૵") + str(bstack11ll1llll_opy_)) + bstack111111l_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭૶"))
        if self.driver_before_scenario:
          bstack111llll1l_opy_(bstack11111111_opy_, bstack111111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ૷"), bstack111111l_opy_ (u"ࠣࡕࡦࡩࡳࡧࡲࡪࡱࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧ૸") + str(bstack11l1l11l_opy_))
      else:
        bstack11l1l1l11_opy_(context, bstack111111l_opy_ (u"ࠤࡓࡥࡸࡹࡥࡥࠣࠥૹ"), bstack111111l_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣૺ"))
        if self.driver_before_scenario:
          bstack1ll1l11111_opy_(getattr(context, bstack111111l_opy_ (u"ࠫࡵࡧࡧࡦࠩૻ"), None), bstack111111l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧૼ"))
        bstack11111111_opy_.execute_script(bstack111111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ૽") + json.dumps(str(args[0].name) + bstack111111l_opy_ (u"ࠢࠡ࠯ࠣࡔࡦࡹࡳࡦࡦࠤࠦ૾")) + bstack111111l_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧ૿"))
        if self.driver_before_scenario:
          bstack111llll1l_opy_(bstack11111111_opy_, bstack111111l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ଀"))
    except Exception as e:
      logger.debug(bstack111111l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬଁ").format(str(e)))
  elif name == bstack111111l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫଂ"):
    try:
      bstack11111111_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1l11lll1_opy_(bstack111111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫଃ")) else context.browser
      if context.failed is True:
        bstack111l1l1l1_opy_ = []
        bstack11111ll1l_opy_ = []
        bstack11l1l111_opy_ = []
        bstack1lll11lll1_opy_ = bstack111111l_opy_ (u"࠭ࠧ଄")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack111l1l1l1_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1111l11l_opy_ = traceback.format_tb(exc_tb)
            bstack1ll1l1l1ll_opy_ = bstack111111l_opy_ (u"ࠧࠡࠩଅ").join(bstack1111l11l_opy_)
            bstack11111ll1l_opy_.append(bstack1ll1l1l1ll_opy_)
            bstack11l1l111_opy_.append(bstack1111l11l_opy_[-1])
        except Exception as e:
          logger.debug(bstack1lll1111ll_opy_.format(str(e)))
        bstack11l1l11l_opy_ = bstack111111l_opy_ (u"ࠨࠩଆ")
        for i in range(len(bstack111l1l1l1_opy_)):
          bstack11l1l11l_opy_ += bstack111l1l1l1_opy_[i] + bstack11l1l111_opy_[i] + bstack111111l_opy_ (u"ࠩ࡟ࡲࠬଇ")
        bstack1lll11lll1_opy_ = bstack111111l_opy_ (u"ࠪࠤࠬଈ").join(bstack11111ll1l_opy_)
        if not self.driver_before_scenario:
          bstack11l1l1l11_opy_(context, bstack1lll11lll1_opy_, bstack111111l_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥଉ"))
          bstack1ll1l11111_opy_(getattr(context, bstack111111l_opy_ (u"ࠬࡶࡡࡨࡧࠪଊ"), None), bstack111111l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨଋ"), bstack11l1l11l_opy_)
          bstack11111111_opy_.execute_script(bstack111111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬଌ") + json.dumps(bstack1lll11lll1_opy_) + bstack111111l_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨ଍"))
          bstack111llll1l_opy_(bstack11111111_opy_, bstack111111l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ଎"), bstack111111l_opy_ (u"ࠥࡗࡴࡳࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡢ࡮ࠣଏ") + str(bstack11l1l11l_opy_))
          bstack1l1l1l11l_opy_ = bstack1ll11lll_opy_(bstack1lll11lll1_opy_, self.feature.name, logger)
          if (bstack1l1l1l11l_opy_ != None):
            bstack1ll1l11l1_opy_.append(bstack1l1l1l11l_opy_)
      else:
        if not self.driver_before_scenario:
          bstack11l1l1l11_opy_(context, bstack111111l_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩ࠿ࠦࠢଐ") + str(self.feature.name) + bstack111111l_opy_ (u"ࠧࠦࡰࡢࡵࡶࡩࡩࠧࠢ଑"), bstack111111l_opy_ (u"ࠨࡩ࡯ࡨࡲࠦ଒"))
          bstack1ll1l11111_opy_(getattr(context, bstack111111l_opy_ (u"ࠧࡱࡣࡪࡩࠬଓ"), None), bstack111111l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣଔ"))
          bstack11111111_opy_.execute_script(bstack111111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧକ") + json.dumps(bstack111111l_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨଖ") + str(self.feature.name) + bstack111111l_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨଗ")) + bstack111111l_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫଘ"))
          bstack111llll1l_opy_(bstack11111111_opy_, bstack111111l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ଙ"))
          bstack1l1l1l11l_opy_ = bstack1ll11lll_opy_(bstack1lll11lll1_opy_, self.feature.name, logger)
          if (bstack1l1l1l11l_opy_ != None):
            bstack1ll1l11l1_opy_.append(bstack1l1l1l11l_opy_)
    except Exception as e:
      logger.debug(bstack111111l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩଚ").format(str(e)))
  else:
    bstack1ll1lllll1_opy_(self, name, context, *args)
  if name in [bstack111111l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨଛ"), bstack111111l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪଜ")]:
    bstack1ll1lllll1_opy_(self, name, context, *args)
    if (name == bstack111111l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫଝ") and self.driver_before_scenario) or (
            name == bstack111111l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫଞ") and not self.driver_before_scenario):
      try:
        bstack11111111_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1l11lll1_opy_(bstack111111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫଟ")) else context.browser
        bstack11111111_opy_.quit()
      except Exception:
        pass
def bstack111ll1l11_opy_(config, startdir):
  return bstack111111l_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࠲ࢀࠦଠ").format(bstack111111l_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨଡ"))
notset = Notset()
def bstack1l1ll1ll1l_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack11lll11ll_opy_
  if str(name).lower() == bstack111111l_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨଢ"):
    return bstack111111l_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣଣ")
  else:
    return bstack11lll11ll_opy_(self, name, default, skip)
def bstack11111l11_opy_(item, when):
  global bstack1ll111llll_opy_
  try:
    bstack1ll111llll_opy_(item, when)
  except Exception as e:
    pass
def bstack1lllll1ll1_opy_():
  return
def bstack11l1lll1l_opy_(type, name, status, reason, bstack11lll1lll_opy_, bstack11lll1l1_opy_):
  bstack11l1ll1l1_opy_ = {
    bstack111111l_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪତ"): type,
    bstack111111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧଥ"): {}
  }
  if type == bstack111111l_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧଦ"):
    bstack11l1ll1l1_opy_[bstack111111l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩଧ")][bstack111111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ନ")] = bstack11lll1lll_opy_
    bstack11l1ll1l1_opy_[bstack111111l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ଩")][bstack111111l_opy_ (u"ࠩࡧࡥࡹࡧࠧପ")] = json.dumps(str(bstack11lll1l1_opy_))
  if type == bstack111111l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫଫ"):
    bstack11l1ll1l1_opy_[bstack111111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧବ")][bstack111111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪଭ")] = name
  if type == bstack111111l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩମ"):
    bstack11l1ll1l1_opy_[bstack111111l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪଯ")][bstack111111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨର")] = status
    if status == bstack111111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ଱"):
      bstack11l1ll1l1_opy_[bstack111111l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ଲ")][bstack111111l_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫଳ")] = json.dumps(str(reason))
  bstack11l11l11_opy_ = bstack111111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ଴").format(json.dumps(bstack11l1ll1l1_opy_))
  return bstack11l11l11_opy_
def bstack1l1ll11ll_opy_(driver_command, response):
    if driver_command == bstack111111l_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪଵ"):
        bstack111lll1l_opy_.bstack1ll1lllll_opy_({
            bstack111111l_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ଶ"): response[bstack111111l_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧଷ")],
            bstack111111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩସ"): bstack111lll1l_opy_.current_test_uuid()
        })
def bstack1lllll1ll_opy_(item, call, rep):
  global bstack111llll11_opy_
  global bstack11l1l11ll_opy_
  global bstack1l1lll111l_opy_
  name = bstack111111l_opy_ (u"ࠪࠫହ")
  try:
    if rep.when == bstack111111l_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ଺"):
      bstack1l1l11ll11_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1l1lll111l_opy_:
          name = str(rep.nodeid)
          bstack11l1lll11_opy_ = bstack11l1lll1l_opy_(bstack111111l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭଻"), name, bstack111111l_opy_ (u"଼࠭ࠧ"), bstack111111l_opy_ (u"ࠧࠨଽ"), bstack111111l_opy_ (u"ࠨࠩା"), bstack111111l_opy_ (u"ࠩࠪି"))
          threading.current_thread().bstack1lllll1l1l_opy_ = name
          for driver in bstack11l1l11ll_opy_:
            if bstack1l1l11ll11_opy_ == driver.session_id:
              driver.execute_script(bstack11l1lll11_opy_)
      except Exception as e:
        logger.debug(bstack111111l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪୀ").format(str(e)))
      try:
        bstack111111l1l_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack111111l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬୁ"):
          status = bstack111111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬୂ") if rep.outcome.lower() == bstack111111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ୃ") else bstack111111l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧୄ")
          reason = bstack111111l_opy_ (u"ࠨࠩ୅")
          if status == bstack111111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ୆"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack111111l_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨେ") if status == bstack111111l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫୈ") else bstack111111l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ୉")
          data = name + bstack111111l_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨ୊") if status == bstack111111l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧୋ") else name + bstack111111l_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠣࠣࠫୌ") + reason
          bstack11ll1lll1_opy_ = bstack11l1lll1l_opy_(bstack111111l_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨ୍ࠫ"), bstack111111l_opy_ (u"ࠪࠫ୎"), bstack111111l_opy_ (u"ࠫࠬ୏"), bstack111111l_opy_ (u"ࠬ࠭୐"), level, data)
          for driver in bstack11l1l11ll_opy_:
            if bstack1l1l11ll11_opy_ == driver.session_id:
              driver.execute_script(bstack11ll1lll1_opy_)
      except Exception as e:
        logger.debug(bstack111111l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡴࡴࡴࡦࡺࡷࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪ୑").format(str(e)))
  except Exception as e:
    logger.debug(bstack111111l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡷࡹࡧࡴࡦࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽࢀࠫ୒").format(str(e)))
  bstack111llll11_opy_(item, call, rep)
def bstack1ll1ll111l_opy_(driver, bstack1ll1ll11l_opy_):
  PercySDK.screenshot(driver, bstack1ll1ll11l_opy_)
def bstack1ll1lll111_opy_(driver):
  if bstack1ll11l1l1l_opy_.bstack11111lll_opy_() is True or bstack1ll11l1l1l_opy_.capturing() is True:
    return
  bstack1ll11l1l1l_opy_.bstack1111l111l_opy_()
  while not bstack1ll11l1l1l_opy_.bstack11111lll_opy_():
    bstack11lll1l11_opy_ = bstack1ll11l1l1l_opy_.bstack1lllllll11_opy_()
    bstack1ll1ll111l_opy_(driver, bstack11lll1l11_opy_)
  bstack1ll11l1l1l_opy_.bstack1l1ll1l1l1_opy_()
def bstack1111llll1_opy_(sequence, driver_command, response = None):
    try:
      if sequence != bstack111111l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨ୓"):
        return
      if not CONFIG.get(bstack111111l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ୔"), False):
        return
      bstack11lll1l11_opy_ = bstack1l1l1l111_opy_(threading.current_thread(), bstack111111l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭୕"), None)
      for command in bstack1l1111lll_opy_:
        if command == driver_command:
          for driver in bstack11l1l11ll_opy_:
            bstack1ll1lll111_opy_(driver)
      bstack1l1llll111_opy_ = CONFIG.get(bstack111111l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧୖ"), bstack111111l_opy_ (u"ࠧࡧࡵࡵࡱࠥୗ"))
      if driver_command in bstack1lll1111_opy_[bstack1l1llll111_opy_]:
        bstack1ll11l1l1l_opy_.bstack1l11ll1l_opy_(bstack11lll1l11_opy_, driver_command)
    except Exception as e:
      pass
def bstack1ll1111l1_opy_(framework_name):
  global bstack1ll1llll11_opy_
  global bstack1111111ll_opy_
  global bstack1l11lllll_opy_
  bstack1ll1llll11_opy_ = framework_name
  logger.info(bstack1111ll1l1_opy_.format(bstack1ll1llll11_opy_.split(bstack111111l_opy_ (u"࠭࠭ࠨ୘"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1l1l1l1l_opy_:
      Service.start = bstack11l11l111_opy_
      Service.stop = bstack11ll11l11_opy_
      webdriver.Remote.get = bstack1l1lllll11_opy_
      WebDriver.close = bstack11111111l_opy_
      WebDriver.quit = bstack1lll1ll1l1_opy_
      webdriver.Remote.__init__ = bstack11l1l1l1_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.bstack1ll1l1l1l1_opy_ = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.bstack1ll1l1ll11_opy_ = getAccessibilityResultsSummary
    if not bstack1l1l1l1l_opy_ and bstack111lll1l_opy_.on():
      webdriver.Remote.__init__ = bstack11llll1ll_opy_
    if bstack111111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭୙") in str(framework_name).lower() and bstack111lll1l_opy_.on():
      WebDriver.execute = bstack1l1l11l11_opy_
    bstack1111111ll_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1l1l1l1l_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1l1lll1l_opy_
  except Exception as e:
    pass
  bstack11ll1ll11_opy_()
  if not bstack1111111ll_opy_:
    bstack1llll1llll_opy_(bstack111111l_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥ୚"), bstack1lllll111l_opy_)
  if bstack1l1111l11_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack111lllll1_opy_
    except Exception as e:
      logger.error(bstack1ll1llll1l_opy_.format(str(e)))
  if bstack1ll11lllll_opy_():
    bstack1lll1l1l_opy_(CONFIG, logger)
  if (bstack111111l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ୛") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if CONFIG.get(bstack111111l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩଡ଼"), False):
          bstack1lll1l111_opy_(bstack1111llll1_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1111lll1_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1lll1ll11_opy_
      except Exception as e:
        logger.warn(bstack1ll1ll11ll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack11l11ll1_opy_
      except Exception as e:
        logger.debug(bstack1l111111_opy_ + str(e))
    except Exception as e:
      bstack1llll1llll_opy_(e, bstack1ll1ll11ll_opy_)
    Output.start_test = bstack111lll11l_opy_
    Output.end_test = bstack1lll111l11_opy_
    TestStatus.__init__ = bstack111llllll_opy_
    QueueItem.__init__ = bstack11llll11_opy_
    pabot._create_items = bstack111111lll_opy_
    try:
      from pabot import __version__ as bstack1lllll11l1_opy_
      if version.parse(bstack1lllll11l1_opy_) >= version.parse(bstack111111l_opy_ (u"ࠫ࠷࠴࠱࠶࠰࠳ࠫଢ଼")):
        pabot._run = bstack1llll11ll_opy_
      elif version.parse(bstack1lllll11l1_opy_) >= version.parse(bstack111111l_opy_ (u"ࠬ࠸࠮࠲࠵࠱࠴ࠬ୞")):
        pabot._run = bstack1ll11lll11_opy_
      else:
        pabot._run = bstack1l1lll1l1l_opy_
    except Exception as e:
      pabot._run = bstack1l1lll1l1l_opy_
    pabot._create_command_for_execution = bstack1ll11l111l_opy_
    pabot._report_results = bstack1l1l1llll_opy_
  if bstack111111l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ୟ") in str(framework_name).lower():
    if not bstack1l1l1l1l_opy_:
      return
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1llll1llll_opy_(e, bstack11l1ll1l_opy_)
    Runner.run_hook = bstack1ll1ll1ll_opy_
    Step.run = bstack11lll111l_opy_
  if bstack111111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧୠ") in str(framework_name).lower():
    if not bstack1l1l1l1l_opy_:
      return
    try:
      if CONFIG.get(bstack111111l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧୡ"), False):
          bstack1lll1l111_opy_(bstack1111llll1_opy_)
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack111ll1l11_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1lllll1ll1_opy_
      Config.getoption = bstack1l1ll1ll1l_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1lllll1ll_opy_
    except Exception as e:
      pass
def bstack11ll1111l_opy_():
  global CONFIG
  if bstack111111l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩୢ") in CONFIG and int(CONFIG[bstack111111l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪୣ")]) > 1:
    logger.warn(bstack11l1llll_opy_)
def bstack1l1l11l1ll_opy_(arg, bstack11llll11l_opy_, bstack1l1l1l1ll1_opy_=None):
  global CONFIG
  global bstack111111ll1_opy_
  global bstack11l111l1_opy_
  global bstack1l1l1l1l_opy_
  global bstack1111ll1ll_opy_
  bstack1llll11lll_opy_ = bstack111111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ୤")
  if bstack11llll11l_opy_ and isinstance(bstack11llll11l_opy_, str):
    bstack11llll11l_opy_ = eval(bstack11llll11l_opy_)
  CONFIG = bstack11llll11l_opy_[bstack111111l_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬ୥")]
  bstack111111ll1_opy_ = bstack11llll11l_opy_[bstack111111l_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧ୦")]
  bstack11l111l1_opy_ = bstack11llll11l_opy_[bstack111111l_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ୧")]
  bstack1l1l1l1l_opy_ = bstack11llll11l_opy_[bstack111111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ୨")]
  bstack1111ll1ll_opy_.bstack1l1ll1l1_opy_(bstack111111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ୩"), bstack1l1l1l1l_opy_)
  os.environ[bstack111111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ୪")] = bstack1llll11lll_opy_
  os.environ[bstack111111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪ୫")] = json.dumps(CONFIG)
  os.environ[bstack111111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬ୬")] = bstack111111ll1_opy_
  os.environ[bstack111111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ୭")] = str(bstack11l111l1_opy_)
  os.environ[bstack111111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭୮")] = str(True)
  if bstack1ll11lll1_opy_(arg, [bstack111111l_opy_ (u"ࠨ࠯ࡱࠫ୯"), bstack111111l_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ୰")]) != -1:
    os.environ[bstack111111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫୱ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1ll1ll1lll_opy_)
    return
  bstack11111l1l_opy_()
  global bstack1l1l1111_opy_
  global bstack1llll1ll11_opy_
  global bstack1llllll11_opy_
  global bstack1111l1l1_opy_
  global bstack1l11lll1_opy_
  global bstack1l11lllll_opy_
  global bstack1lll1l1l11_opy_
  arg.append(bstack111111l_opy_ (u"ࠦ࠲࡝ࠢ୲"))
  arg.append(bstack111111l_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩ࠿ࡓ࡯ࡥࡷ࡯ࡩࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡩ࡮ࡲࡲࡶࡹ࡫ࡤ࠻ࡲࡼࡸࡪࡹࡴ࠯ࡒࡼࡸࡪࡹࡴࡘࡣࡵࡲ࡮ࡴࡧࠣ୳"))
  arg.append(bstack111111l_opy_ (u"ࠨ࠭ࡘࠤ୴"))
  arg.append(bstack111111l_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡕࡪࡨࠤ࡭ࡵ࡯࡬࡫ࡰࡴࡱࠨ୵"))
  global bstack11l11111_opy_
  global bstack1ll111lll_opy_
  global bstack11l1l11l1_opy_
  global bstack1l1lll11l_opy_
  global bstack1ll11l1lll_opy_
  global bstack1llllll1l1_opy_
  global bstack11llllll_opy_
  global bstack1ll11l11l_opy_
  global bstack1l1l11lll_opy_
  global bstack11lll11ll_opy_
  global bstack1ll111llll_opy_
  global bstack111llll11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11l11111_opy_ = webdriver.Remote.__init__
    bstack1ll111lll_opy_ = WebDriver.quit
    bstack11llllll_opy_ = WebDriver.close
    bstack1ll11l11l_opy_ = WebDriver.get
  except Exception as e:
    pass
  if bstack1ll11l11ll_opy_(CONFIG) and bstack1l1lllll_opy_():
    if bstack11111ll11_opy_() < version.parse(bstack1l1l11111_opy_):
      logger.error(bstack11l1ll1ll_opy_.format(bstack11111ll11_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1l11lll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1ll1llll1l_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack11lll11ll_opy_ = Config.getoption
    from _pytest import runner
    bstack1ll111llll_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1111l1111_opy_)
  try:
    from pytest_bdd import reporting
    bstack111llll11_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack111111l_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩ୶"))
  bstack1llllll11_opy_ = CONFIG.get(bstack111111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭୷"), {}).get(bstack111111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ୸"))
  bstack1lll1l1l11_opy_ = True
  bstack1ll1111l1_opy_(bstack1lll11l1l_opy_)
  os.environ[bstack111111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬ୹")] = CONFIG[bstack111111l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ୺")]
  os.environ[bstack111111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩ୻")] = CONFIG[bstack111111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ୼")]
  os.environ[bstack111111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ୽")] = bstack1l1l1l1l_opy_.__str__()
  from _pytest.config import main as bstack1l1ll11l1_opy_
  bstack1l1ll11l1_opy_(arg)
  if bstack111111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭୾") in multiprocessing.current_process().__dict__.keys():
    for bstack1l1l1l11_opy_ in multiprocessing.current_process().bstack_error_list:
      bstack1l1l1l1ll1_opy_.append(bstack1l1l1l11_opy_)
def bstack1l11ll1l1_opy_(arg):
  bstack1ll1111l1_opy_(bstack1lll1l1l1l_opy_)
  os.environ[bstack111111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ୿")] = str(bstack11l111l1_opy_)
  from behave.__main__ import main as bstack1ll11llll1_opy_
  bstack1ll11llll1_opy_(arg)
def bstack111llll1_opy_():
  logger.info(bstack1ll1ll1111_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack111111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ஀"), help=bstack111111l_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡰࡰࡩ࡭࡬࠭஁"))
  parser.add_argument(bstack111111l_opy_ (u"࠭࠭ࡶࠩஂ"), bstack111111l_opy_ (u"ࠧ࠮࠯ࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫஃ"), help=bstack111111l_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠧ஄"))
  parser.add_argument(bstack111111l_opy_ (u"ࠩ࠰࡯ࠬஅ"), bstack111111l_opy_ (u"ࠪ࠱࠲ࡱࡥࡺࠩஆ"), help=bstack111111l_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡣࡦࡧࡪࡹࡳࠡ࡭ࡨࡽࠬஇ"))
  parser.add_argument(bstack111111l_opy_ (u"ࠬ࠳ࡦࠨஈ"), bstack111111l_opy_ (u"࠭࠭࠮ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫஉ"), help=bstack111111l_opy_ (u"࡚ࠧࡱࡸࡶࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ஊ"))
  bstack1l1llll1l1_opy_ = parser.parse_args()
  try:
    bstack1lllllll1_opy_ = bstack111111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡨࡧࡱࡩࡷ࡯ࡣ࠯ࡻࡰࡰ࠳ࡹࡡ࡮ࡲ࡯ࡩࠬ஋")
    if bstack1l1llll1l1_opy_.framework and bstack1l1llll1l1_opy_.framework not in (bstack111111l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ஌"), bstack111111l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫ஍")):
      bstack1lllllll1_opy_ = bstack111111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪஎ")
    bstack1ll111ll1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lllllll1_opy_)
    bstack11ll1ll1_opy_ = open(bstack1ll111ll1_opy_, bstack111111l_opy_ (u"ࠬࡸࠧஏ"))
    bstack111ll1ll1_opy_ = bstack11ll1ll1_opy_.read()
    bstack11ll1ll1_opy_.close()
    if bstack1l1llll1l1_opy_.username:
      bstack111ll1ll1_opy_ = bstack111ll1ll1_opy_.replace(bstack111111l_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ஐ"), bstack1l1llll1l1_opy_.username)
    if bstack1l1llll1l1_opy_.key:
      bstack111ll1ll1_opy_ = bstack111ll1ll1_opy_.replace(bstack111111l_opy_ (u"࡚ࠧࡑࡘࡖࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩ஑"), bstack1l1llll1l1_opy_.key)
    if bstack1l1llll1l1_opy_.framework:
      bstack111ll1ll1_opy_ = bstack111ll1ll1_opy_.replace(bstack111111l_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩஒ"), bstack1l1llll1l1_opy_.framework)
    file_name = bstack111111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬஓ")
    file_path = os.path.abspath(file_name)
    bstack1ll11l1ll1_opy_ = open(file_path, bstack111111l_opy_ (u"ࠪࡻࠬஔ"))
    bstack1ll11l1ll1_opy_.write(bstack111ll1ll1_opy_)
    bstack1ll11l1ll1_opy_.close()
    logger.info(bstack1lll1l1ll_opy_)
    try:
      os.environ[bstack111111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭க")] = bstack1l1llll1l1_opy_.framework if bstack1l1llll1l1_opy_.framework != None else bstack111111l_opy_ (u"ࠧࠨ஖")
      config = yaml.safe_load(bstack111ll1ll1_opy_)
      config[bstack111111l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭஗")] = bstack111111l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡴࡧࡷࡹࡵ࠭஘")
      bstack1l1ll111_opy_(bstack1l11l1111_opy_, config)
    except Exception as e:
      logger.debug(bstack111l1ll1_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1ll1l11ll1_opy_.format(str(e)))
def bstack1l1ll111_opy_(bstack11lllll1_opy_, config, bstack1lll1llll_opy_={}):
  global bstack1l1l1l1l_opy_
  global bstack1l1ll1lll1_opy_
  if not config:
    return
  bstack1l11llll_opy_ = bstack1llll111l_opy_ if not bstack1l1l1l1l_opy_ else (
    bstack11l111l11_opy_ if bstack111111l_opy_ (u"ࠨࡣࡳࡴࠬங") in config else bstack1lllll1111_opy_)
  data = {
    bstack111111l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫச"): config[bstack111111l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ஛")],
    bstack111111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧஜ"): config[bstack111111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ஝")],
    bstack111111l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪஞ"): bstack11lllll1_opy_,
    bstack111111l_opy_ (u"ࠧࡥࡧࡷࡩࡨࡺࡥࡥࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫட"): os.environ.get(bstack111111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪ஠"), bstack1l1ll1lll1_opy_),
    bstack111111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ஡"): bstack1lll11ll11_opy_,
    bstack111111l_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰࠬ஢"): bstack1l1l1ll11l_opy_(),
    bstack111111l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧண"): {
      bstack111111l_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪத"): str(config[bstack111111l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭஥")]) if bstack111111l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ஦") in config else bstack111111l_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ஧"),
      bstack111111l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨ࡚ࡪࡸࡳࡪࡱࡱࠫந"): sys.version,
      bstack111111l_opy_ (u"ࠪࡶࡪ࡬ࡥࡳࡴࡨࡶࠬன"): bstack11lll111_opy_(os.getenv(bstack111111l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࠨப"), bstack111111l_opy_ (u"ࠧࠨ஫"))),
      bstack111111l_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨ஬"): bstack111111l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ஭"),
      bstack111111l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩம"): bstack1l11llll_opy_,
      bstack111111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬய"): config[bstack111111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ர")] if config[bstack111111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧற")] else bstack111111l_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨல"),
      bstack111111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨள"): str(config[bstack111111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩழ")]) if bstack111111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪவ") in config else bstack111111l_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥஶ"),
      bstack111111l_opy_ (u"ࠪࡳࡸ࠭ஷ"): sys.platform,
      bstack111111l_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ஸ"): socket.gethostname()
    }
  }
  update(data[bstack111111l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨஹ")], bstack1lll1llll_opy_)
  try:
    response = bstack1lll111l_opy_(bstack111111l_opy_ (u"࠭ࡐࡐࡕࡗࠫ஺"), bstack11111ll1_opy_(bstack1l11l1l1_opy_), data, {
      bstack111111l_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ஻"): (config[bstack111111l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ஼")], config[bstack111111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ஽")])
    })
    if response:
      logger.debug(bstack1ll1lll1l1_opy_.format(bstack11lllll1_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1llll1l1_opy_.format(str(e)))
def bstack11lll111_opy_(framework):
  return bstack111111l_opy_ (u"ࠥࡿࢂ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢா").format(str(framework), __version__) if framework else bstack111111l_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࡾࢁࠧி").format(
    __version__)
def bstack11111l1l_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack1lll11l11l_opy_()
    logger.debug(bstack11111l1ll_opy_.format(str(CONFIG)))
    bstack1l1lllll1_opy_()
    bstack1l1l1ll1_opy_()
  except Exception as e:
    logger.error(bstack111111l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࠤீ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1l1111l1l_opy_
  atexit.register(bstack11lll11l_opy_)
  signal.signal(signal.SIGINT, bstack1ll11l111_opy_)
  signal.signal(signal.SIGTERM, bstack1ll11l111_opy_)
def bstack1l1111l1l_opy_(exctype, value, traceback):
  global bstack11l1l11ll_opy_
  try:
    for driver in bstack11l1l11ll_opy_:
      bstack111llll1l_opy_(driver, bstack111111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ு"), bstack111111l_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥூ") + str(value))
  except Exception:
    pass
  bstack111l1111l_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack111l1111l_opy_(message=bstack111111l_opy_ (u"ࠨࠩ௃"), bstack1lll1ll11l_opy_ = False):
  global CONFIG
  bstack1l1l1lll1_opy_ = bstack111111l_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡇࡻࡧࡪࡶࡴࡪࡱࡱࠫ௄") if bstack1lll1ll11l_opy_ else bstack111111l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ௅")
  try:
    if message:
      bstack1lll1llll_opy_ = {
        bstack1l1l1lll1_opy_ : str(message)
      }
      bstack1l1ll111_opy_(bstack1l1111l1_opy_, CONFIG, bstack1lll1llll_opy_)
    else:
      bstack1l1ll111_opy_(bstack1l1111l1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1lll1111l_opy_.format(str(e)))
def bstack1l1ll1111_opy_(bstack11ll1l1l1_opy_, size):
  bstack11ll1l1ll_opy_ = []
  while len(bstack11ll1l1l1_opy_) > size:
    bstack111l1lll_opy_ = bstack11ll1l1l1_opy_[:size]
    bstack11ll1l1ll_opy_.append(bstack111l1lll_opy_)
    bstack11ll1l1l1_opy_ = bstack11ll1l1l1_opy_[size:]
  bstack11ll1l1ll_opy_.append(bstack11ll1l1l1_opy_)
  return bstack11ll1l1ll_opy_
def bstack11111lll1_opy_(args):
  if bstack111111l_opy_ (u"ࠫ࠲ࡳࠧெ") in args and bstack111111l_opy_ (u"ࠬࡶࡤࡣࠩே") in args:
    return True
  return False
def run_on_browserstack(bstack1lllll1l1_opy_=None, bstack1l1l1l1ll1_opy_=None, bstack1ll111l11l_opy_=False):
  global CONFIG
  global bstack111111ll1_opy_
  global bstack11l111l1_opy_
  global bstack1l1ll1lll1_opy_
  bstack1llll11lll_opy_ = bstack111111l_opy_ (u"࠭ࠧை")
  bstack1l1l11llll_opy_(bstack1l1111111_opy_, logger)
  if bstack1lllll1l1_opy_ and isinstance(bstack1lllll1l1_opy_, str):
    bstack1lllll1l1_opy_ = eval(bstack1lllll1l1_opy_)
  if bstack1lllll1l1_opy_:
    CONFIG = bstack1lllll1l1_opy_[bstack111111l_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧ௉")]
    bstack111111ll1_opy_ = bstack1lllll1l1_opy_[bstack111111l_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩொ")]
    bstack11l111l1_opy_ = bstack1lllll1l1_opy_[bstack111111l_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫோ")]
    bstack1111ll1ll_opy_.bstack1l1ll1l1_opy_(bstack111111l_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬௌ"), bstack11l111l1_opy_)
    bstack1llll11lll_opy_ = bstack111111l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ்ࠫ")
  if not bstack1ll111l11l_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1ll1ll1lll_opy_)
      return
    if sys.argv[1] == bstack111111l_opy_ (u"ࠬ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ௎") or sys.argv[1] == bstack111111l_opy_ (u"࠭࠭ࡷࠩ௏"):
      logger.info(bstack111111l_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡐࡺࡶ࡫ࡳࡳࠦࡓࡅࡍࠣࡺࢀࢃࠧௐ").format(__version__))
      return
    if sys.argv[1] == bstack111111l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ௑"):
      bstack111llll1_opy_()
      return
  args = sys.argv
  bstack11111l1l_opy_()
  global bstack1l1l1111_opy_
  global bstack11l1111l_opy_
  global bstack1lll1l1l11_opy_
  global bstack1ll11l1111_opy_
  global bstack1llll1ll11_opy_
  global bstack1llllll11_opy_
  global bstack1111l1l1_opy_
  global bstack1ll1l11ll_opy_
  global bstack1l11lll1_opy_
  global bstack1l11lllll_opy_
  global bstack1ll11ll1l_opy_
  bstack11l1111l_opy_ = len(CONFIG[bstack111111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௒")])
  if not bstack1llll11lll_opy_:
    if args[1] == bstack111111l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ௓") or args[1] == bstack111111l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬ௔"):
      bstack1llll11lll_opy_ = bstack111111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ௕")
      args = args[2:]
    elif args[1] == bstack111111l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ௖"):
      bstack1llll11lll_opy_ = bstack111111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ௗ")
      args = args[2:]
    elif args[1] == bstack111111l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ௘"):
      bstack1llll11lll_opy_ = bstack111111l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ௙")
      args = args[2:]
    elif args[1] == bstack111111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ௚"):
      bstack1llll11lll_opy_ = bstack111111l_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ௛")
      args = args[2:]
    elif args[1] == bstack111111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ௜"):
      bstack1llll11lll_opy_ = bstack111111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭௝")
      args = args[2:]
    elif args[1] == bstack111111l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ௞"):
      bstack1llll11lll_opy_ = bstack111111l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ௟")
      args = args[2:]
    else:
      if not bstack111111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ௠") in CONFIG or str(CONFIG[bstack111111l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭௡")]).lower() in [bstack111111l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ௢"), bstack111111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭௣")]:
        bstack1llll11lll_opy_ = bstack111111l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭௤")
        args = args[1:]
      elif str(CONFIG[bstack111111l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ௥")]).lower() == bstack111111l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ௦"):
        bstack1llll11lll_opy_ = bstack111111l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ௧")
        args = args[1:]
      elif str(CONFIG[bstack111111l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭௨")]).lower() == bstack111111l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ௩"):
        bstack1llll11lll_opy_ = bstack111111l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ௪")
        args = args[1:]
      elif str(CONFIG[bstack111111l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ௫")]).lower() == bstack111111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ௬"):
        bstack1llll11lll_opy_ = bstack111111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ௭")
        args = args[1:]
      elif str(CONFIG[bstack111111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ௮")]).lower() == bstack111111l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ௯"):
        bstack1llll11lll_opy_ = bstack111111l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ௰")
        args = args[1:]
      else:
        os.environ[bstack111111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ௱")] = bstack1llll11lll_opy_
        bstack1l1llll11_opy_(bstack1lll1lllll_opy_)
  os.environ[bstack111111l_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧ௲")] = bstack1llll11lll_opy_
  bstack1l1ll1lll1_opy_ = bstack1llll11lll_opy_
  global bstack1l1ll1lll_opy_
  if bstack1lllll1l1_opy_:
    try:
      os.environ[bstack111111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ௳")] = bstack1llll11lll_opy_
      bstack1l1ll111_opy_(bstack111l1111_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1lll1111l_opy_.format(str(e)))
  global bstack11l11111_opy_
  global bstack1ll111lll_opy_
  global bstack111l1ll11_opy_
  global bstack1l1llll11l_opy_
  global bstack1l11111l1_opy_
  global bstack1ll1lll1_opy_
  global bstack11l1l11l1_opy_
  global bstack1l1lll11l_opy_
  global bstack1lll1l11l_opy_
  global bstack1ll11l1lll_opy_
  global bstack1llllll1l1_opy_
  global bstack11llllll_opy_
  global bstack1ll1lllll1_opy_
  global bstack1l111ll11_opy_
  global bstack1ll11l11l_opy_
  global bstack1l1l11lll_opy_
  global bstack11lll11ll_opy_
  global bstack1ll111llll_opy_
  global bstack11ll1111_opy_
  global bstack111llll11_opy_
  global bstack1l111l1l1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11l11111_opy_ = webdriver.Remote.__init__
    bstack1ll111lll_opy_ = WebDriver.quit
    bstack11llllll_opy_ = WebDriver.close
    bstack1ll11l11l_opy_ = WebDriver.get
    bstack1l111l1l1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1ll1lll_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    global bstack1lll111ll_opy_
    from QWeb.keywords import browser
    bstack1lll111ll_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1ll11l11ll_opy_(CONFIG) and bstack1l1lllll_opy_():
    if bstack11111ll11_opy_() < version.parse(bstack1l1l11111_opy_):
      logger.error(bstack11l1ll1ll_opy_.format(bstack11111ll11_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1l11lll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1ll1llll1l_opy_.format(str(e)))
  if bstack1llll11lll_opy_ != bstack111111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ௴") or (bstack1llll11lll_opy_ == bstack111111l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ௵") and not bstack1lllll1l1_opy_):
    bstack11111l1l1_opy_()
  if (bstack1llll11lll_opy_ in [bstack111111l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ௶"), bstack111111l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ௷"), bstack111111l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭௸")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1111lll1_opy_
        bstack1ll1lll1_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1ll1ll11ll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1l11111l1_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1l111111_opy_ + str(e))
    except Exception as e:
      bstack1llll1llll_opy_(e, bstack1ll1ll11ll_opy_)
    if bstack1llll11lll_opy_ != bstack111111l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ௹"):
      bstack11ll11lll_opy_()
    bstack111l1ll11_opy_ = Output.start_test
    bstack1l1llll11l_opy_ = Output.end_test
    bstack11l1l11l1_opy_ = TestStatus.__init__
    bstack1lll1l11l_opy_ = pabot._run
    bstack1ll11l1lll_opy_ = QueueItem.__init__
    bstack1llllll1l1_opy_ = pabot._create_command_for_execution
    bstack11ll1111_opy_ = pabot._report_results
  if bstack1llll11lll_opy_ == bstack111111l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ௺"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1llll1llll_opy_(e, bstack11l1ll1l_opy_)
    bstack1ll1lllll1_opy_ = Runner.run_hook
    bstack1l111ll11_opy_ = Step.run
  if bstack1llll11lll_opy_ == bstack111111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ௻"):
    try:
      from _pytest.config import Config
      bstack11lll11ll_opy_ = Config.getoption
      from _pytest import runner
      bstack1ll111llll_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1111l1111_opy_)
    try:
      from pytest_bdd import reporting
      bstack111llll11_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack111111l_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪ௼"))
  if bstack1llll11lll_opy_ in bstack1l1ll1llll_opy_:
    try:
      framework_name = bstack111111l_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩ௽") if bstack1llll11lll_opy_ in [bstack111111l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ௾"), bstack111111l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ௿"), bstack111111l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧఀ")] else bstack1llllllll_opy_(bstack1llll11lll_opy_)
      bstack111lll1l_opy_.launch(CONFIG, {
        bstack111111l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨఁ"): bstack111111l_opy_ (u"ࠨࡽ࠳ࢁ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧం").format(framework_name) if bstack1llll11lll_opy_ == bstack111111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩః") and bstack1lll11111l_opy_() else framework_name,
        bstack111111l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧఄ"): bstack1l111l11_opy_(framework_name),
        bstack111111l_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩఅ"): __version__
      })
    except Exception as e:
      logger.debug(bstack11llllll1_opy_.format(bstack111111l_opy_ (u"ࠬࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬఆ"), str(e)))
  if bstack1llll11lll_opy_ in bstack1l1ll1l11l_opy_:
    try:
      framework_name = bstack111111l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬఇ") if bstack1llll11lll_opy_ in [bstack111111l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ఈ"), bstack111111l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧఉ")] else bstack1llll11lll_opy_
      if bstack1l1l1l1l_opy_ and bstack111111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩఊ") in CONFIG and CONFIG[bstack111111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪఋ")] == True:
        if bstack111111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫఌ") in CONFIG:
          os.environ[bstack111111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭఍")] = os.getenv(bstack111111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧఎ"), json.dumps(CONFIG[bstack111111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧఏ")]))
          CONFIG[bstack111111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨఐ")].pop(bstack111111l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ఑"), None)
          CONFIG[bstack111111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪఒ")].pop(bstack111111l_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩఓ"), None)
        bstack1ll11111_opy_, bstack1l11llll1_opy_ = bstack1lll111lll_opy_.bstack1l1l1ll1l1_opy_(CONFIG, bstack1llll11lll_opy_, bstack1l111l11_opy_(framework_name))
        if not bstack1ll11111_opy_ is None:
          os.environ[bstack111111l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪఔ")] = bstack1ll11111_opy_
          os.environ[bstack111111l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡕࡇࡖࡘࡤࡘࡕࡏࡡࡌࡈࠬక")] = str(bstack1l11llll1_opy_)
    except Exception as e:
      logger.debug(bstack11llllll1_opy_.format(bstack111111l_opy_ (u"ࠧࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧఖ"), str(e)))
  if bstack1llll11lll_opy_ == bstack111111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨగ"):
    bstack1lll1l1l11_opy_ = True
    if bstack1lllll1l1_opy_ and bstack1ll111l11l_opy_:
      bstack1llllll11_opy_ = CONFIG.get(bstack111111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ఘ"), {}).get(bstack111111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬఙ"))
      bstack1ll1111l1_opy_(bstack1llllllll1_opy_)
    elif bstack1lllll1l1_opy_:
      bstack1llllll11_opy_ = CONFIG.get(bstack111111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨచ"), {}).get(bstack111111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧఛ"))
      global bstack11l1l11ll_opy_
      try:
        if bstack11111lll1_opy_(bstack1lllll1l1_opy_[bstack111111l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩజ")]) and multiprocessing.current_process().name == bstack111111l_opy_ (u"ࠧ࠱ࠩఝ"):
          bstack1lllll1l1_opy_[bstack111111l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫఞ")].remove(bstack111111l_opy_ (u"ࠩ࠰ࡱࠬట"))
          bstack1lllll1l1_opy_[bstack111111l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఠ")].remove(bstack111111l_opy_ (u"ࠫࡵࡪࡢࠨడ"))
          bstack1lllll1l1_opy_[bstack111111l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨఢ")] = bstack1lllll1l1_opy_[bstack111111l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩణ")][0]
          with open(bstack1lllll1l1_opy_[bstack111111l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪత")], bstack111111l_opy_ (u"ࠨࡴࠪథ")) as f:
            bstack1lllll1lll_opy_ = f.read()
          bstack11111llll_opy_ = bstack111111l_opy_ (u"ࠤࠥࠦ࡫ࡸ࡯࡮ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡧ࡯ࠥ࡯࡭ࡱࡱࡵࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥ࠼ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩ࠭ࢁࡽࠪ࠽ࠣࡪࡷࡵ࡭ࠡࡲࡧࡦࠥ࡯࡭ࡱࡱࡵࡸࠥࡖࡤࡣ࠽ࠣࡳ࡬ࡥࡤࡣࠢࡀࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࡸࡥࡢ࡭࠾ࠎࡩ࡫ࡦࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠬࡸ࡫࡬ࡧ࠮ࠣࡥࡷ࡭ࠬࠡࡶࡨࡱࡵࡵࡲࡢࡴࡼࠤࡂࠦ࠰ࠪ࠼ࠍࠤࠥࡺࡲࡺ࠼ࠍࠤࠥࠦࠠࡢࡴࡪࠤࡂࠦࡳࡵࡴࠫ࡭ࡳࡺࠨࡢࡴࡪ࠭࠰࠷࠰ࠪࠌࠣࠤࡪࡾࡣࡦࡲࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡢࡵࠣࡩ࠿ࠐࠠࠡࠢࠣࡴࡦࡹࡳࠋࠢࠣࡳ࡬ࡥࡤࡣࠪࡶࡩࡱ࡬ࠬࡢࡴࡪ࠰ࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠩࠋࡒࡧࡦ࠳ࡪ࡯ࡠࡤࠣࡁࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠋࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࡖࡤࡣࠪࠬ࠲ࡸ࡫ࡴࡠࡶࡵࡥࡨ࡫ࠨࠪ࡞ࡱࠦࠧࠨద").format(str(bstack1lllll1l1_opy_))
          bstack1l1l1l1l1l_opy_ = bstack11111llll_opy_ + bstack1lllll1lll_opy_
          bstack1l1l1l1ll_opy_ = bstack1lllll1l1_opy_[bstack111111l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ధ")] + bstack111111l_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡺࡥ࡮ࡲ࠱ࡴࡾ࠭న")
          with open(bstack1l1l1l1ll_opy_, bstack111111l_opy_ (u"ࠬࡽࠧ఩")):
            pass
          with open(bstack1l1l1l1ll_opy_, bstack111111l_opy_ (u"ࠨࡷࠬࠤప")) as f:
            f.write(bstack1l1l1l1l1l_opy_)
          import subprocess
          bstack1ll1111l1l_opy_ = subprocess.run([bstack111111l_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢఫ"), bstack1l1l1l1ll_opy_])
          if os.path.exists(bstack1l1l1l1ll_opy_):
            os.unlink(bstack1l1l1l1ll_opy_)
          os._exit(bstack1ll1111l1l_opy_.returncode)
        else:
          if bstack11111lll1_opy_(bstack1lllll1l1_opy_[bstack111111l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫబ")]):
            bstack1lllll1l1_opy_[bstack111111l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬభ")].remove(bstack111111l_opy_ (u"ࠪ࠱ࡲ࠭మ"))
            bstack1lllll1l1_opy_[bstack111111l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧయ")].remove(bstack111111l_opy_ (u"ࠬࡶࡤࡣࠩర"))
            bstack1lllll1l1_opy_[bstack111111l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩఱ")] = bstack1lllll1l1_opy_[bstack111111l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪల")][0]
          bstack1ll1111l1_opy_(bstack1llllllll1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1lllll1l1_opy_[bstack111111l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫళ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack111111l_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫఴ")] = bstack111111l_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬవ")
          mod_globals[bstack111111l_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭శ")] = os.path.abspath(bstack1lllll1l1_opy_[bstack111111l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨష")])
          exec(open(bstack1lllll1l1_opy_[bstack111111l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩస")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack111111l_opy_ (u"ࠧࡄࡣࡸ࡫࡭ࡺࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠧహ").format(str(e)))
          for driver in bstack11l1l11ll_opy_:
            bstack1l1l1l1ll1_opy_.append({
              bstack111111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭఺"): bstack1lllll1l1_opy_[bstack111111l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ఻")],
              bstack111111l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳ఼ࠩ"): str(e),
              bstack111111l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪఽ"): multiprocessing.current_process().name
            })
            bstack111llll1l_opy_(driver, bstack111111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬా"), bstack111111l_opy_ (u"ࠨࡓࡦࡵࡶ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤి") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack11l1l11ll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack11l111l1_opy_, CONFIG, logger)
      bstack1111l111_opy_()
      bstack11ll1111l_opy_()
      bstack11llll11l_opy_ = {
        bstack111111l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪీ"): args[0],
        bstack111111l_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨు"): CONFIG,
        bstack111111l_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪూ"): bstack111111ll1_opy_,
        bstack111111l_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬృ"): bstack11l111l1_opy_
      }
      percy.bstack11ll11ll1_opy_()
      if bstack111111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧౄ") in CONFIG:
        bstack1l1l11l1l1_opy_ = []
        manager = multiprocessing.Manager()
        bstack1lll11l11_opy_ = manager.list()
        if bstack11111lll1_opy_(args):
          for index, platform in enumerate(CONFIG[bstack111111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ౅")]):
            if index == 0:
              bstack11llll11l_opy_[bstack111111l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩె")] = args
            bstack1l1l11l1l1_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack11llll11l_opy_, bstack1lll11l11_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack111111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪే")]):
            bstack1l1l11l1l1_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack11llll11l_opy_, bstack1lll11l11_opy_)))
        for t in bstack1l1l11l1l1_opy_:
          t.start()
        for t in bstack1l1l11l1l1_opy_:
          t.join()
        bstack1ll1l11ll_opy_ = list(bstack1lll11l11_opy_)
      else:
        if bstack11111lll1_opy_(args):
          bstack11llll11l_opy_[bstack111111l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫై")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack11llll11l_opy_,))
          test.start()
          test.join()
        else:
          bstack1ll1111l1_opy_(bstack1llllllll1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack111111l_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫ౉")] = bstack111111l_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬొ")
          mod_globals[bstack111111l_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭ో")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1llll11lll_opy_ == bstack111111l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫౌ") or bstack1llll11lll_opy_ == bstack111111l_opy_ (u"࠭ࡲࡰࡤࡲࡸ్ࠬ"):
    percy.init(bstack11l111l1_opy_, CONFIG, logger)
    percy.bstack11ll11ll1_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1llll1llll_opy_(e, bstack1ll1ll11ll_opy_)
    bstack1111l111_opy_()
    bstack1ll1111l1_opy_(bstack11llll1l1_opy_)
    if bstack111111l_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ౎") in args:
      i = args.index(bstack111111l_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭౏"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1l1l1111_opy_))
    args.insert(0, str(bstack111111l_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ౐")))
    if bstack111lll1l_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack11l111lll_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1l11ll1ll_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack111111l_opy_ (u"ࠥࡖࡔࡈࡏࡕࡡࡒࡔ࡙ࡏࡏࡏࡕࠥ౑"),
        ).parse_args(bstack11l111lll_opy_)
        args.insert(args.index(bstack1l11ll1ll_opy_[0]), str(bstack111111l_opy_ (u"ࠫ࠲࠳࡬ࡪࡵࡷࡩࡳ࡫ࡲࠨ౒")))
        args.insert(args.index(bstack1l11ll1ll_opy_[0]), str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡸ࡯ࡣࡱࡷࡣࡱ࡯ࡳࡵࡧࡱࡩࡷ࠴ࡰࡺࠩ౓"))))
        if bstack1ll111111_opy_(os.environ.get(bstack111111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫ౔"))) and str(os.environ.get(bstack111111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖౕࠫ"), bstack111111l_opy_ (u"ࠨࡰࡸࡰࡱౖ࠭"))) != bstack111111l_opy_ (u"ࠩࡱࡹࡱࡲࠧ౗"):
          for bstack1llll11ll1_opy_ in bstack1l11ll1ll_opy_:
            args.remove(bstack1llll11ll1_opy_)
          bstack111lll1l1_opy_ = os.environ.get(bstack111111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠧౘ")).split(bstack111111l_opy_ (u"ࠫ࠱࠭ౙ"))
          for bstack1l11111l_opy_ in bstack111lll1l1_opy_:
            args.append(bstack1l11111l_opy_)
      except Exception as e:
        logger.error(bstack111111l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡥࡹࡺࡡࡤࡪ࡬ࡲ࡬ࠦ࡬ࡪࡵࡷࡩࡳ࡫ࡲࠡࡨࡲࡶࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࠦࡅࡳࡴࡲࡶࠥ࠳ࠠࠣౚ").format(e))
    pabot.main(args)
  elif bstack1llll11lll_opy_ == bstack111111l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ౛"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1llll1llll_opy_(e, bstack1ll1ll11ll_opy_)
    for a in args:
      if bstack111111l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭౜") in a:
        bstack1llll1ll11_opy_ = int(a.split(bstack111111l_opy_ (u"ࠨ࠼ࠪౝ"))[1])
      if bstack111111l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭౞") in a:
        bstack1llllll11_opy_ = str(a.split(bstack111111l_opy_ (u"ࠪ࠾ࠬ౟"))[1])
      if bstack111111l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖࠫౠ") in a:
        bstack1111l1l1_opy_ = str(a.split(bstack111111l_opy_ (u"ࠬࡀࠧౡ"))[1])
    bstack1111l1ll_opy_ = None
    if bstack111111l_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬౢ") in args:
      i = args.index(bstack111111l_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭ౣ"))
      args.pop(i)
      bstack1111l1ll_opy_ = args.pop(i)
    if bstack1111l1ll_opy_ is not None:
      global bstack1lll11111_opy_
      bstack1lll11111_opy_ = bstack1111l1ll_opy_
    bstack1ll1111l1_opy_(bstack11llll1l1_opy_)
    run_cli(args)
    if bstack111111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬ౤") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1l1l11_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l1l1l1ll1_opy_.append(bstack1l1l1l11_opy_)
  elif bstack1llll11lll_opy_ == bstack111111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ౥"):
    percy.init(bstack11l111l1_opy_, CONFIG, logger)
    percy.bstack11ll11ll1_opy_()
    bstack11lll1111_opy_ = bstack11l11ll11_opy_(args, logger, CONFIG, bstack1l1l1l1l_opy_)
    bstack11lll1111_opy_.bstack11111l11l_opy_()
    bstack1111l111_opy_()
    bstack1ll11l1111_opy_ = True
    bstack1l11lllll_opy_ = bstack11lll1111_opy_.bstack1ll1ll11l1_opy_()
    bstack11lll1111_opy_.bstack11llll11l_opy_(bstack1l1lll111l_opy_)
    bstack1l11lll1_opy_ = bstack11lll1111_opy_.bstack1llll1l1l1_opy_(bstack1l1l11l1ll_opy_, {
      bstack111111l_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫ౦"): bstack111111ll1_opy_,
      bstack111111l_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭౧"): bstack11l111l1_opy_,
      bstack111111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ౨"): bstack1l1l1l1l_opy_
    })
    bstack1ll11ll1l_opy_ = 1 if len(bstack1l11lll1_opy_) > 0 else 0
  elif bstack1llll11lll_opy_ == bstack111111l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭౩"):
    try:
      from behave.__main__ import main as bstack1ll11llll1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1llll1llll_opy_(e, bstack11l1ll1l_opy_)
    bstack1111l111_opy_()
    bstack1ll11l1111_opy_ = True
    bstack1ll1l1l1_opy_ = 1
    if bstack111111l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ౪") in CONFIG:
      bstack1ll1l1l1_opy_ = CONFIG[bstack111111l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ౫")]
    bstack1ll1l11lll_opy_ = int(bstack1ll1l1l1_opy_) * int(len(CONFIG[bstack111111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౬")]))
    config = Configuration(args)
    bstack1ll1ll1l11_opy_ = config.paths
    if len(bstack1ll1ll1l11_opy_) == 0:
      import glob
      pattern = bstack111111l_opy_ (u"ࠪ࠮࠯࠵ࠪ࠯ࡨࡨࡥࡹࡻࡲࡦࠩ౭")
      bstack1ll1l11l11_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1ll1l11l11_opy_)
      config = Configuration(args)
      bstack1ll1ll1l11_opy_ = config.paths
    bstack1lll1lll1_opy_ = [os.path.normpath(item) for item in bstack1ll1ll1l11_opy_]
    bstack111ll1l1l_opy_ = [os.path.normpath(item) for item in args]
    bstack1llll1111_opy_ = [item for item in bstack111ll1l1l_opy_ if item not in bstack1lll1lll1_opy_]
    import platform as pf
    if pf.system().lower() == bstack111111l_opy_ (u"ࠫࡼ࡯࡮ࡥࡱࡺࡷࠬ౮"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1lll1lll1_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1ll111l111_opy_)))
                    for bstack1ll111l111_opy_ in bstack1lll1lll1_opy_]
    bstack11l111ll_opy_ = []
    for spec in bstack1lll1lll1_opy_:
      bstack1l1llll1ll_opy_ = []
      bstack1l1llll1ll_opy_ += bstack1llll1111_opy_
      bstack1l1llll1ll_opy_.append(spec)
      bstack11l111ll_opy_.append(bstack1l1llll1ll_opy_)
    execution_items = []
    for bstack1l1llll1ll_opy_ in bstack11l111ll_opy_:
      for index, _ in enumerate(CONFIG[bstack111111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ౯")]):
        item = {}
        item[bstack111111l_opy_ (u"࠭ࡡࡳࡩࠪ౰")] = bstack111111l_opy_ (u"ࠧࠡࠩ౱").join(bstack1l1llll1ll_opy_)
        item[bstack111111l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ౲")] = index
        execution_items.append(item)
    bstack11l1111ll_opy_ = bstack1l1ll1111_opy_(execution_items, bstack1ll1l11lll_opy_)
    for execution_item in bstack11l1111ll_opy_:
      bstack1l1l11l1l1_opy_ = []
      for item in execution_item:
        bstack1l1l11l1l1_opy_.append(bstack1l111l1l_opy_(name=str(item[bstack111111l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ౳")]),
                                             target=bstack1l11ll1l1_opy_,
                                             args=(item[bstack111111l_opy_ (u"ࠪࡥࡷ࡭ࠧ౴")],)))
      for t in bstack1l1l11l1l1_opy_:
        t.start()
      for t in bstack1l1l11l1l1_opy_:
        t.join()
  else:
    bstack1l1llll11_opy_(bstack1lll1lllll_opy_)
  if not bstack1lllll1l1_opy_:
    bstack1l1llllll1_opy_()
def browserstack_initialize(bstack1ll1l111l1_opy_=None):
  run_on_browserstack(bstack1ll1l111l1_opy_, None, True)
def bstack1l1llllll1_opy_():
  global CONFIG
  global bstack1l1ll1lll1_opy_
  global bstack1ll11ll1l_opy_
  bstack111lll1l_opy_.stop()
  bstack111lll1l_opy_.bstack1ll111l1ll_opy_()
  if bstack1lll111lll_opy_.bstack1lllll11l_opy_(CONFIG):
    bstack1lll111lll_opy_.bstack1ll1l1l1l_opy_()
  [bstack1l1l1lll11_opy_, bstack111l11l11_opy_] = bstack1llllll1l_opy_()
  if bstack1l1l1lll11_opy_ is not None and bstack1ll1ll11_opy_() != -1:
    sessions = bstack1ll11ll1_opy_(bstack1l1l1lll11_opy_)
    bstack1lll1l1111_opy_(sessions, bstack111l11l11_opy_)
  if bstack1l1ll1lll1_opy_ == bstack111111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ౵") and bstack1ll11ll1l_opy_ != 0:
    sys.exit(bstack1ll11ll1l_opy_)
def bstack1llllllll_opy_(bstack1lll1llll1_opy_):
  if bstack1lll1llll1_opy_:
    return bstack1lll1llll1_opy_.capitalize()
  else:
    return bstack111111l_opy_ (u"ࠬ࠭౶")
def bstack1111111l1_opy_(bstack11lll1ll1_opy_):
  if bstack111111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ౷") in bstack11lll1ll1_opy_ and bstack11lll1ll1_opy_[bstack111111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ౸")] != bstack111111l_opy_ (u"ࠨࠩ౹"):
    return bstack11lll1ll1_opy_[bstack111111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ౺")]
  else:
    bstack1ll1l1l111_opy_ = bstack111111l_opy_ (u"ࠥࠦ౻")
    if bstack111111l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ౼") in bstack11lll1ll1_opy_ and bstack11lll1ll1_opy_[bstack111111l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ౽")] != None:
      bstack1ll1l1l111_opy_ += bstack11lll1ll1_opy_[bstack111111l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭౾")] + bstack111111l_opy_ (u"ࠢ࠭ࠢࠥ౿")
      if bstack11lll1ll1_opy_[bstack111111l_opy_ (u"ࠨࡱࡶࠫಀ")] == bstack111111l_opy_ (u"ࠤ࡬ࡳࡸࠨಁ"):
        bstack1ll1l1l111_opy_ += bstack111111l_opy_ (u"ࠥ࡭ࡔ࡙ࠠࠣಂ")
      bstack1ll1l1l111_opy_ += (bstack11lll1ll1_opy_[bstack111111l_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨಃ")] or bstack111111l_opy_ (u"ࠬ࠭಄"))
      return bstack1ll1l1l111_opy_
    else:
      bstack1ll1l1l111_opy_ += bstack1llllllll_opy_(bstack11lll1ll1_opy_[bstack111111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧಅ")]) + bstack111111l_opy_ (u"ࠢࠡࠤಆ") + (
              bstack11lll1ll1_opy_[bstack111111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪಇ")] or bstack111111l_opy_ (u"ࠩࠪಈ")) + bstack111111l_opy_ (u"ࠥ࠰ࠥࠨಉ")
      if bstack11lll1ll1_opy_[bstack111111l_opy_ (u"ࠫࡴࡹࠧಊ")] == bstack111111l_opy_ (u"ࠧ࡝ࡩ࡯ࡦࡲࡻࡸࠨಋ"):
        bstack1ll1l1l111_opy_ += bstack111111l_opy_ (u"ࠨࡗࡪࡰࠣࠦಌ")
      bstack1ll1l1l111_opy_ += bstack11lll1ll1_opy_[bstack111111l_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫ಍")] or bstack111111l_opy_ (u"ࠨࠩಎ")
      return bstack1ll1l1l111_opy_
def bstack1llll1l1ll_opy_(bstack1l1lll11ll_opy_):
  if bstack1l1lll11ll_opy_ == bstack111111l_opy_ (u"ࠤࡧࡳࡳ࡫ࠢಏ"):
    return bstack111111l_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿࡭ࡲࡦࡧࡱ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧ࡭ࡲࡦࡧࡱࠦࡃࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ಐ")
  elif bstack1l1lll11ll_opy_ == bstack111111l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ಑"):
    return bstack111111l_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡳࡧࡧ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡸࡥࡥࠤࡁࡊࡦ࡯࡬ࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨಒ")
  elif bstack1l1lll11ll_opy_ == bstack111111l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨಓ"):
    return bstack111111l_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡪࡶࡪ࡫࡮࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡪࡶࡪ࡫࡮ࠣࡀࡓࡥࡸࡹࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧಔ")
  elif bstack1l1lll11ll_opy_ == bstack111111l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢಕ"):
    return bstack111111l_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡷ࡫ࡤ࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡵࡩࡩࠨ࠾ࡆࡴࡵࡳࡷࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫಖ")
  elif bstack1l1lll11ll_opy_ == bstack111111l_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦಗ"):
    return bstack111111l_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࠣࡦࡧࡤ࠷࠷࠼࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࠥࡨࡩࡦ࠹࠲࠷ࠤࡁࡘ࡮ࡳࡥࡰࡷࡷࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩಘ")
  elif bstack1l1lll11ll_opy_ == bstack111111l_opy_ (u"ࠧࡸࡵ࡯ࡰ࡬ࡲ࡬ࠨಙ"):
    return bstack111111l_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࡔࡸࡲࡳ࡯࡮ࡨ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧಚ")
  else:
    return bstack111111l_opy_ (u"ࠧ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡦࡱࡧࡣ࡬࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡦࡱࡧࡣ࡬ࠤࡁࠫಛ") + bstack1llllllll_opy_(
      bstack1l1lll11ll_opy_) + bstack111111l_opy_ (u"ࠨ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧಜ")
def bstack1l111llll_opy_(session):
  return bstack111111l_opy_ (u"ࠩ࠿ࡸࡷࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡲࡰࡹࠥࡂࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠦࡳࡦࡵࡶ࡭ࡴࡴ࠭࡯ࡣࡰࡩࠧࡄ࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࡽࢀࠦࠥࡺࡡࡳࡩࡨࡸࡂࠨ࡟ࡣ࡮ࡤࡲࡰࠨ࠾ࡼࡿ࠿࠳ࡦࡄ࠼࠰ࡶࡧࡂࢀࢃࡻࡾ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀ࠴ࡺࡲ࠿ࠩಝ").format(
    session[bstack111111l_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧಞ")], bstack1111111l1_opy_(session), bstack1llll1l1ll_opy_(session[bstack111111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡹࡧࡴࡶࡵࠪಟ")]),
    bstack1llll1l1ll_opy_(session[bstack111111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬಠ")]),
    bstack1llllllll_opy_(session[bstack111111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧಡ")] or session[bstack111111l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧಢ")] or bstack111111l_opy_ (u"ࠨࠩಣ")) + bstack111111l_opy_ (u"ࠤࠣࠦತ") + (session[bstack111111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬಥ")] or bstack111111l_opy_ (u"ࠫࠬದ")),
    session[bstack111111l_opy_ (u"ࠬࡵࡳࠨಧ")] + bstack111111l_opy_ (u"ࠨࠠࠣನ") + session[bstack111111l_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫ಩")], session[bstack111111l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪಪ")] or bstack111111l_opy_ (u"ࠩࠪಫ"),
    session[bstack111111l_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺࠧಬ")] if session[bstack111111l_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨಭ")] else bstack111111l_opy_ (u"ࠬ࠭ಮ"))
def bstack1lll1l1111_opy_(sessions, bstack111l11l11_opy_):
  try:
    bstack11l11111l_opy_ = bstack111111l_opy_ (u"ࠨࠢಯ")
    if not os.path.exists(bstack11l1ll11_opy_):
      os.mkdir(bstack11l1ll11_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111111l_opy_ (u"ࠧࡢࡵࡶࡩࡹࡹ࠯ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰࠬರ")), bstack111111l_opy_ (u"ࠨࡴࠪಱ")) as f:
      bstack11l11111l_opy_ = f.read()
    bstack11l11111l_opy_ = bstack11l11111l_opy_.replace(bstack111111l_opy_ (u"ࠩࡾࠩࡗࡋࡓࡖࡎࡗࡗࡤࡉࡏࡖࡐࡗࠩࢂ࠭ಲ"), str(len(sessions)))
    bstack11l11111l_opy_ = bstack11l11111l_opy_.replace(bstack111111l_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠦࡿࠪಳ"), bstack111l11l11_opy_)
    bstack11l11111l_opy_ = bstack11l11111l_opy_.replace(bstack111111l_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤࡔࡁࡎࡇࠨࢁࠬ಴"),
                                              sessions[0].get(bstack111111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡳࡧ࡭ࡦࠩವ")) if sessions[0] else bstack111111l_opy_ (u"࠭ࠧಶ"))
    with open(os.path.join(bstack11l1ll11_opy_, bstack111111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫಷ")), bstack111111l_opy_ (u"ࠨࡹࠪಸ")) as stream:
      stream.write(bstack11l11111l_opy_.split(bstack111111l_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭ಹ"))[0])
      for session in sessions:
        stream.write(bstack1l111llll_opy_(session))
      stream.write(bstack11l11111l_opy_.split(bstack111111l_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧ಺"))[1])
    logger.info(bstack111111l_opy_ (u"ࠫࡌ࡫࡮ࡦࡴࡤࡸࡪࡪࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡢࡶ࡫࡯ࡨࠥࡧࡲࡵ࡫ࡩࡥࡨࡺࡳࠡࡣࡷࠤࢀࢃࠧ಻").format(bstack11l1ll11_opy_));
  except Exception as e:
    logger.debug(bstack1llllll11l_opy_.format(str(e)))
def bstack1ll11ll1_opy_(bstack1l1l1lll11_opy_):
  global CONFIG
  try:
    host = bstack111111l_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨ಼") if bstack111111l_opy_ (u"࠭ࡡࡱࡲࠪಽ") in CONFIG else bstack111111l_opy_ (u"ࠧࡢࡲ࡬ࠫಾ")
    user = CONFIG[bstack111111l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪಿ")]
    key = CONFIG[bstack111111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬೀ")]
    bstack1l11ll11l_opy_ = bstack111111l_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩು") if bstack111111l_opy_ (u"ࠫࡦࡶࡰࠨೂ") in CONFIG else bstack111111l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧೃ")
    url = bstack111111l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠴ࡪࡴࡱࡱࠫೄ").format(user, key, host, bstack1l11ll11l_opy_,
                                                                                bstack1l1l1lll11_opy_)
    headers = {
      bstack111111l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭೅"): bstack111111l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫೆ"),
    }
    proxies = bstack1ll11ll111_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack111111l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠧೇ")], response.json()))
  except Exception as e:
    logger.debug(bstack1111l1l11_opy_.format(str(e)))
def bstack1llllll1l_opy_():
  global CONFIG
  global bstack1lll11ll11_opy_
  try:
    if bstack111111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ೈ") in CONFIG:
      host = bstack111111l_opy_ (u"ࠫࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪࠧ೉") if bstack111111l_opy_ (u"ࠬࡧࡰࡱࠩೊ") in CONFIG else bstack111111l_opy_ (u"࠭ࡡࡱ࡫ࠪೋ")
      user = CONFIG[bstack111111l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩೌ")]
      key = CONFIG[bstack111111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼ್ࠫ")]
      bstack1l11ll11l_opy_ = bstack111111l_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ೎") if bstack111111l_opy_ (u"ࠪࡥࡵࡶࠧ೏") in CONFIG else bstack111111l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭೐")
      url = bstack111111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࢁࡽ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠮࡫ࡵࡲࡲࠬ೑").format(user, key, host, bstack1l11ll11l_opy_)
      headers = {
        bstack111111l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬ೒"): bstack111111l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ೓"),
      }
      if bstack111111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ೔") in CONFIG:
        params = {bstack111111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧೕ"): CONFIG[bstack111111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ೖ")], bstack111111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ೗"): CONFIG[bstack111111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ೘")]}
      else:
        params = {bstack111111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ೙"): CONFIG[bstack111111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ೚")]}
      proxies = bstack1ll11ll111_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack11l1l1ll_opy_ = response.json()[0][bstack111111l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡨࡵࡪ࡮ࡧࠫ೛")]
        if bstack11l1l1ll_opy_:
          bstack111l11l11_opy_ = bstack11l1l1ll_opy_[bstack111111l_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭೜")].split(bstack111111l_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥ࠰ࡦࡺ࡯࡬ࡥࠩೝ"))[0] + bstack111111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡶ࠳ࠬೞ") + bstack11l1l1ll_opy_[
            bstack111111l_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ೟")]
          logger.info(bstack11l1l1ll1_opy_.format(bstack111l11l11_opy_))
          bstack1lll11ll11_opy_ = bstack11l1l1ll_opy_[bstack111111l_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩೠ")]
          bstack1l1ll1ll1_opy_ = CONFIG[bstack111111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪೡ")]
          if bstack111111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪೢ") in CONFIG:
            bstack1l1ll1ll1_opy_ += bstack111111l_opy_ (u"ࠩࠣࠫೣ") + CONFIG[bstack111111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ೤")]
          if bstack1l1ll1ll1_opy_ != bstack11l1l1ll_opy_[bstack111111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ೥")]:
            logger.debug(bstack1111l1ll1_opy_.format(bstack11l1l1ll_opy_[bstack111111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ೦")], bstack1l1ll1ll1_opy_))
          return [bstack11l1l1ll_opy_[bstack111111l_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ೧")], bstack111l11l11_opy_]
    else:
      logger.warn(bstack1l1l11l1_opy_)
  except Exception as e:
    logger.debug(bstack1l11ll11_opy_.format(str(e)))
  return [None, None]
def bstack11ll1lll_opy_(url, bstack1ll11111l1_opy_=False):
  global CONFIG
  global bstack1l1lllllll_opy_
  if not bstack1l1lllllll_opy_:
    hostname = bstack1l11l1ll1_opy_(url)
    is_private = bstack1ll1llllll_opy_(hostname)
    if (bstack111111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ೨") in CONFIG and not bstack1ll111111_opy_(CONFIG[bstack111111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ೩")])) and (is_private or bstack1ll11111l1_opy_):
      bstack1l1lllllll_opy_ = hostname
def bstack1l11l1ll1_opy_(url):
  return urlparse(url).hostname
def bstack1ll1llllll_opy_(hostname):
  for bstack1lll11l1_opy_ in bstack1ll11l1l1_opy_:
    regex = re.compile(bstack1lll11l1_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1l1l11lll1_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1llll1ll11_opy_
  if not bstack1lll111lll_opy_.bstack1111l1lll_opy_(CONFIG, bstack1llll1ll11_opy_):
    logger.warning(bstack111111l_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶ࠲ࠧ೪"))
    return {}
  try:
    results = driver.execute_script(bstack111111l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡷࡹࡷࡴࠠ࡯ࡧࡺࠤࡕࡸ࡯࡮࡫ࡶࡩ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࠩࡴࡨࡷࡴࡲࡶࡦ࠮ࠣࡶࡪࡰࡥࡤࡶࠬࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡹࡸࡹࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤࡪࡼࡥ࡯ࡶࠣࡁࠥࡴࡥࡸࠢࡆࡹࡸࡺ࡯࡮ࡇࡹࡩࡳࡺࠨࠨࡃ࠴࠵࡞ࡥࡔࡂࡒࡢࡋࡊ࡚࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࠨࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡶࡸࠥ࡬࡮ࠡ࠿ࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࠮ࡥࡷࡧࡱࡸ࠮ࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡳࡧࡰࡳࡻ࡫ࡅࡷࡧࡱࡸࡑ࡯ࡳࡵࡧࡱࡩࡷ࠮ࠧࡂ࠳࠴࡝ࡤࡘࡅࡔࡗࡏࡘࡘࡥࡒࡆࡕࡓࡓࡓ࡙ࡅࠨ࠮ࠣࡪࡳ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡶࡳࡱࡼࡥࠩࡧࡹࡩࡳࡺ࠮ࡥࡧࡷࡥ࡮ࡲ࠮ࡥࡣࡷࡥ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡢࡦࡧࡉࡻ࡫࡮ࡵࡎ࡬ࡷࡹ࡫࡮ࡦࡴࠫࠫࡆ࠷࠱࡚ࡡࡕࡉࡘ࡛ࡌࡕࡕࡢࡖࡊ࡙ࡐࡐࡐࡖࡉࠬ࠲ࠠࡧࡰࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡥ࡫ࡶࡴࡦࡺࡣࡩࡇࡹࡩࡳࡺࠨࡦࡸࡨࡲࡹ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠡࡥࡤࡸࡨ࡮ࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡪࡦࡥࡷࠬ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠊࠡࠢࠣࠤࠥࠦࠠࠡࡿࠬ࠿ࠏࠦࠠࠡࠢࠥࠦࠧ೫"))
    return results
  except Exception:
    logger.error(bstack111111l_opy_ (u"ࠦࡓࡵࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡹࡨࡶࡪࠦࡦࡰࡷࡱࡨ࠳ࠨ೬"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1llll1ll11_opy_
  if not bstack1lll111lll_opy_.bstack1111l1lll_opy_(CONFIG, bstack1llll1ll11_opy_):
    logger.warning(bstack111111l_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡴࡷࡰࡱࡦࡸࡹ࠯ࠤ೭"))
    return {}
  try:
    bstack1l111l111_opy_ = driver.execute_script(bstack111111l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡺࡵࡳࡰࠣࡲࡪࡽࠠࡑࡴࡲࡱ࡮ࡹࡥࠩࡨࡸࡲࡨࡺࡩࡰࡰࠣࠬࡷ࡫ࡳࡰ࡮ࡹࡩ࠱ࠦࡲࡦ࡬ࡨࡧࡹ࠯ࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡴࡼࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲࡸࡺࠠࡦࡸࡨࡲࡹࠦ࠽ࠡࡰࡨࡻࠥࡉࡵࡴࡶࡲࡱࡊࡼࡥ࡯ࡶࠫࠫࡆ࠷࠱࡚ࡡࡗࡅࡕࡥࡇࡆࡖࡢࡖࡊ࡙ࡕࡍࡖࡖࡣࡘ࡛ࡍࡎࡃࡕ࡝ࠬ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡩࡲࠥࡃࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࠫࡩࡻ࡫࡮ࡵࠫࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡷ࡫࡭ࡰࡸࡨࡉࡻ࡫࡮ࡵࡎ࡬ࡷࡹ࡫࡮ࡦࡴࠫࠫࡆ࠷࠱࡚ࡡࡕࡉࡘ࡛ࡌࡕࡕࡢࡗ࡚ࡓࡍࡂࡔ࡜ࡣࡗࡋࡓࡑࡑࡑࡗࡊ࠭ࠬࠡࡨࡱ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡴࡱ࡯ࡺࡪ࠮ࡥࡷࡧࡱࡸ࠳ࡪࡥࡵࡣ࡬ࡰ࠳ࡹࡵ࡮࡯ࡤࡶࡾ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡣࡧࡨࡊࡼࡥ࡯ࡶࡏ࡭ࡸࡺࡥ࡯ࡧࡵࠬࠬࡇ࠱࠲࡛ࡢࡖࡊ࡙ࡕࡍࡖࡖࡣࡘ࡛ࡍࡎࡃࡕ࡝ࡤࡘࡅࡔࡒࡒࡒࡘࡋࠧ࠭ࠢࡩࡲ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡭ࡳࡪ࡯ࡸ࠰ࡧ࡭ࡸࡶࡡࡵࡥ࡫ࡉࡻ࡫࡮ࡵࠪࡨࡺࡪࡴࡴࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠣࡧࡦࡺࡣࡩࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦ࡬ࡨࡧࡹ࠮ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠌࠣࠤࠥࠦࠠࠡࠢࠣࢁ࠮ࡁࠊࠡࠢࠣࠤࠧࠨࠢ೮"))
    return bstack1l111l111_opy_
  except Exception:
    logger.error(bstack111111l_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡺࡳ࡭ࡢࡴࡼࠤࡼࡧࡳࠡࡨࡲࡹࡳࡪ࠮ࠣ೯"))
    return {}
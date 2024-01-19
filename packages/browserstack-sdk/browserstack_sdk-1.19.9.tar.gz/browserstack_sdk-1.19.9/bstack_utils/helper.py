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
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import bstack11ll11l1l1_opy_, bstack1ll11l1l1_opy_, bstack1llll1ll1l_opy_, bstack1l1l1l1l11_opy_
from bstack_utils.messages import bstack11lllllll_opy_, bstack1ll1llll1l_opy_
from bstack_utils.proxy import bstack1ll11ll111_opy_, bstack1ll11l1l11_opy_
bstack1111ll1ll_opy_ = Config.bstack11l11l1ll_opy_()
def bstack11lll1l111_opy_(config):
    return config[bstack111111l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᄱ")]
def bstack11lll11l11_opy_(config):
    return config[bstack111111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᄲ")]
def bstack1llll1111l_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l1lll11l_opy_(obj):
    values = []
    bstack11ll1111ll_opy_ = re.compile(bstack111111l_opy_ (u"ࡲࠣࡠࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࡜ࡥ࠭ࠧࠦᄳ"), re.I)
    for key in obj.keys():
        if bstack11ll1111ll_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l11ll11l_opy_(config):
    tags = []
    tags.extend(bstack11l1lll11l_opy_(os.environ))
    tags.extend(bstack11l1lll11l_opy_(config))
    return tags
def bstack11l11ll1ll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l1l11l11_opy_(bstack11l1l1l1ll_opy_):
    if not bstack11l1l1l1ll_opy_:
        return bstack111111l_opy_ (u"ࠨࠩᄴ")
    return bstack111111l_opy_ (u"ࠤࡾࢁࠥ࠮ࡻࡾࠫࠥᄵ").format(bstack11l1l1l1ll_opy_.name, bstack11l1l1l1ll_opy_.email)
def bstack11lll1ll1l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l1ll1l11_opy_ = repo.common_dir
        info = {
            bstack111111l_opy_ (u"ࠥࡷ࡭ࡧࠢᄶ"): repo.head.commit.hexsha,
            bstack111111l_opy_ (u"ࠦࡸ࡮࡯ࡳࡶࡢࡷ࡭ࡧࠢᄷ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack111111l_opy_ (u"ࠧࡨࡲࡢࡰࡦ࡬ࠧᄸ"): repo.active_branch.name,
            bstack111111l_opy_ (u"ࠨࡴࡢࡩࠥᄹ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack111111l_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࠥᄺ"): bstack11l1l11l11_opy_(repo.head.commit.committer),
            bstack111111l_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡵࡧࡵࡣࡩࡧࡴࡦࠤᄻ"): repo.head.commit.committed_datetime.isoformat(),
            bstack111111l_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࠤᄼ"): bstack11l1l11l11_opy_(repo.head.commit.author),
            bstack111111l_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡢࡨࡦࡺࡥࠣᄽ"): repo.head.commit.authored_datetime.isoformat(),
            bstack111111l_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧᄾ"): repo.head.commit.message,
            bstack111111l_opy_ (u"ࠧࡸ࡯ࡰࡶࠥᄿ"): repo.git.rev_parse(bstack111111l_opy_ (u"ࠨ࠭࠮ࡵ࡫ࡳࡼ࠳ࡴࡰࡲ࡯ࡩࡻ࡫࡬ࠣᅀ")),
            bstack111111l_opy_ (u"ࠢࡤࡱࡰࡱࡴࡴ࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣᅁ"): bstack11l1ll1l11_opy_,
            bstack111111l_opy_ (u"ࠣࡹࡲࡶࡰࡺࡲࡦࡧࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦᅂ"): subprocess.check_output([bstack111111l_opy_ (u"ࠤࡪ࡭ࡹࠨᅃ"), bstack111111l_opy_ (u"ࠥࡶࡪࡼ࠭ࡱࡣࡵࡷࡪࠨᅄ"), bstack111111l_opy_ (u"ࠦ࠲࠳ࡧࡪࡶ࠰ࡧࡴࡳ࡭ࡰࡰ࠰ࡨ࡮ࡸࠢᅅ")]).strip().decode(
                bstack111111l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᅆ")),
            bstack111111l_opy_ (u"ࠨ࡬ࡢࡵࡷࡣࡹࡧࡧࠣᅇ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack111111l_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡳࡠࡵ࡬ࡲࡨ࡫࡟࡭ࡣࡶࡸࡤࡺࡡࡨࠤᅈ"): repo.git.rev_list(
                bstack111111l_opy_ (u"ࠣࡽࢀ࠲࠳ࢁࡽࠣᅉ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l1llll11_opy_ = []
        for remote in remotes:
            bstack11l1l1ll1l_opy_ = {
                bstack111111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᅊ"): remote.name,
                bstack111111l_opy_ (u"ࠥࡹࡷࡲࠢᅋ"): remote.url,
            }
            bstack11l1llll11_opy_.append(bstack11l1l1ll1l_opy_)
        return {
            bstack111111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᅌ"): bstack111111l_opy_ (u"ࠧ࡭ࡩࡵࠤᅍ"),
            **info,
            bstack111111l_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡹࠢᅎ"): bstack11l1llll11_opy_
        }
    except Exception as err:
        print(bstack111111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡰࡲࡸࡰࡦࡺࡩ࡯ࡩࠣࡋ࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᅏ").format(err))
        return {}
def bstack11ll111l1_opy_():
    env = os.environ
    if (bstack111111l_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨᅐ") in env and len(env[bstack111111l_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠢᅑ")]) > 0) or (
            bstack111111l_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤᅒ") in env and len(env[bstack111111l_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥᅓ")]) > 0):
        return {
            bstack111111l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᅔ"): bstack111111l_opy_ (u"ࠨࡊࡦࡰ࡮࡭ࡳࡹࠢᅕ"),
            bstack111111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᅖ"): env.get(bstack111111l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᅗ")),
            bstack111111l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᅘ"): env.get(bstack111111l_opy_ (u"ࠥࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᅙ")),
            bstack111111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᅚ"): env.get(bstack111111l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᅛ"))
        }
    if env.get(bstack111111l_opy_ (u"ࠨࡃࡊࠤᅜ")) == bstack111111l_opy_ (u"ࠢࡵࡴࡸࡩࠧᅝ") and bstack1ll111111_opy_(env.get(bstack111111l_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡄࡋࠥᅞ"))):
        return {
            bstack111111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᅟ"): bstack111111l_opy_ (u"ࠥࡇ࡮ࡸࡣ࡭ࡧࡆࡍࠧᅠ"),
            bstack111111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᅡ"): env.get(bstack111111l_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᅢ")),
            bstack111111l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᅣ"): env.get(bstack111111l_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡋࡑࡅࠦᅤ")),
            bstack111111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᅥ"): env.get(bstack111111l_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࠧᅦ"))
        }
    if env.get(bstack111111l_opy_ (u"ࠥࡇࡎࠨᅧ")) == bstack111111l_opy_ (u"ࠦࡹࡸࡵࡦࠤᅨ") and bstack1ll111111_opy_(env.get(bstack111111l_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࠧᅩ"))):
        return {
            bstack111111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᅪ"): bstack111111l_opy_ (u"ࠢࡕࡴࡤࡺ࡮ࡹࠠࡄࡋࠥᅫ"),
            bstack111111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᅬ"): env.get(bstack111111l_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠ࡙ࡈࡆࡤ࡛ࡒࡍࠤᅭ")),
            bstack111111l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᅮ"): env.get(bstack111111l_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᅯ")),
            bstack111111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᅰ"): env.get(bstack111111l_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᅱ"))
        }
    if env.get(bstack111111l_opy_ (u"ࠢࡄࡋࠥᅲ")) == bstack111111l_opy_ (u"ࠣࡶࡵࡹࡪࠨᅳ") and env.get(bstack111111l_opy_ (u"ࠤࡆࡍࡤࡔࡁࡎࡇࠥᅴ")) == bstack111111l_opy_ (u"ࠥࡧࡴࡪࡥࡴࡪ࡬ࡴࠧᅵ"):
        return {
            bstack111111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᅶ"): bstack111111l_opy_ (u"ࠧࡉ࡯ࡥࡧࡶ࡬࡮ࡶࠢᅷ"),
            bstack111111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᅸ"): None,
            bstack111111l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᅹ"): None,
            bstack111111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᅺ"): None
        }
    if env.get(bstack111111l_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡒࡂࡐࡆࡌࠧᅻ")) and env.get(bstack111111l_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨᅼ")):
        return {
            bstack111111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᅽ"): bstack111111l_opy_ (u"ࠧࡈࡩࡵࡤࡸࡧࡰ࡫ࡴࠣᅾ"),
            bstack111111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᅿ"): env.get(bstack111111l_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡋࡎ࡚࡟ࡉࡖࡗࡔࡤࡕࡒࡊࡉࡌࡒࠧᆀ")),
            bstack111111l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᆁ"): None,
            bstack111111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᆂ"): env.get(bstack111111l_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᆃ"))
        }
    if env.get(bstack111111l_opy_ (u"ࠦࡈࡏࠢᆄ")) == bstack111111l_opy_ (u"ࠧࡺࡲࡶࡧࠥᆅ") and bstack1ll111111_opy_(env.get(bstack111111l_opy_ (u"ࠨࡄࡓࡑࡑࡉࠧᆆ"))):
        return {
            bstack111111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᆇ"): bstack111111l_opy_ (u"ࠣࡆࡵࡳࡳ࡫ࠢᆈ"),
            bstack111111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᆉ"): env.get(bstack111111l_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡎࡌࡒࡐࠨᆊ")),
            bstack111111l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᆋ"): None,
            bstack111111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᆌ"): env.get(bstack111111l_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᆍ"))
        }
    if env.get(bstack111111l_opy_ (u"ࠢࡄࡋࠥᆎ")) == bstack111111l_opy_ (u"ࠣࡶࡵࡹࡪࠨᆏ") and bstack1ll111111_opy_(env.get(bstack111111l_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࠧᆐ"))):
        return {
            bstack111111l_opy_ (u"ࠥࡲࡦࡳࡥࠣᆑ"): bstack111111l_opy_ (u"ࠦࡘ࡫࡭ࡢࡲ࡫ࡳࡷ࡫ࠢᆒ"),
            bstack111111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᆓ"): env.get(bstack111111l_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡒࡖࡌࡇࡎࡊ࡜ࡄࡘࡎࡕࡎࡠࡗࡕࡐࠧᆔ")),
            bstack111111l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᆕ"): env.get(bstack111111l_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᆖ")),
            bstack111111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᆗ"): env.get(bstack111111l_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡍࡉࠨᆘ"))
        }
    if env.get(bstack111111l_opy_ (u"ࠦࡈࡏࠢᆙ")) == bstack111111l_opy_ (u"ࠧࡺࡲࡶࡧࠥᆚ") and bstack1ll111111_opy_(env.get(bstack111111l_opy_ (u"ࠨࡇࡊࡖࡏࡅࡇࡥࡃࡊࠤᆛ"))):
        return {
            bstack111111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᆜ"): bstack111111l_opy_ (u"ࠣࡉ࡬ࡸࡑࡧࡢࠣᆝ"),
            bstack111111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᆞ"): env.get(bstack111111l_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢ࡙ࡗࡒࠢᆟ")),
            bstack111111l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᆠ"): env.get(bstack111111l_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᆡ")),
            bstack111111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᆢ"): env.get(bstack111111l_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡊࡆࠥᆣ"))
        }
    if env.get(bstack111111l_opy_ (u"ࠣࡅࡌࠦᆤ")) == bstack111111l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᆥ") and bstack1ll111111_opy_(env.get(bstack111111l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࠨᆦ"))):
        return {
            bstack111111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᆧ"): bstack111111l_opy_ (u"ࠧࡈࡵࡪ࡮ࡧ࡯࡮ࡺࡥࠣᆨ"),
            bstack111111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᆩ"): env.get(bstack111111l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᆪ")),
            bstack111111l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᆫ"): env.get(bstack111111l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡒࡁࡃࡇࡏࠦᆬ")) or env.get(bstack111111l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨᆭ")),
            bstack111111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᆮ"): env.get(bstack111111l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᆯ"))
        }
    if bstack1ll111111_opy_(env.get(bstack111111l_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣᆰ"))):
        return {
            bstack111111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᆱ"): bstack111111l_opy_ (u"ࠣࡘ࡬ࡷࡺࡧ࡬ࠡࡕࡷࡹࡩ࡯࡯ࠡࡖࡨࡥࡲࠦࡓࡦࡴࡹ࡭ࡨ࡫ࡳࠣᆲ"),
            bstack111111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᆳ"): bstack111111l_opy_ (u"ࠥࡿࢂࢁࡽࠣᆴ").format(env.get(bstack111111l_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧᆵ")), env.get(bstack111111l_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࡌࡈࠬᆶ"))),
            bstack111111l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᆷ"): env.get(bstack111111l_opy_ (u"ࠢࡔ࡛ࡖࡘࡊࡓ࡟ࡅࡇࡉࡍࡓࡏࡔࡊࡑࡑࡍࡉࠨᆸ")),
            bstack111111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᆹ"): env.get(bstack111111l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤᆺ"))
        }
    if bstack1ll111111_opy_(env.get(bstack111111l_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࠧᆻ"))):
        return {
            bstack111111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᆼ"): bstack111111l_opy_ (u"ࠧࡇࡰࡱࡸࡨࡽࡴࡸࠢᆽ"),
            bstack111111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᆾ"): bstack111111l_opy_ (u"ࠢࡼࡿ࠲ࡴࡷࡵࡪࡦࡥࡷ࠳ࢀࢃ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠨᆿ").format(env.get(bstack111111l_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢ࡙ࡗࡒࠧᇀ")), env.get(bstack111111l_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡆࡉࡃࡐࡗࡑࡘࡤࡔࡁࡎࡇࠪᇁ")), env.get(bstack111111l_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡓࡍࡗࡊࠫᇂ")), env.get(bstack111111l_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨᇃ"))),
            bstack111111l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᇄ"): env.get(bstack111111l_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᇅ")),
            bstack111111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᇆ"): env.get(bstack111111l_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᇇ"))
        }
    if env.get(bstack111111l_opy_ (u"ࠤࡄ࡞࡚ࡘࡅࡠࡊࡗࡘࡕࡥࡕࡔࡇࡕࡣࡆࡍࡅࡏࡖࠥᇈ")) and env.get(bstack111111l_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧᇉ")):
        return {
            bstack111111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᇊ"): bstack111111l_opy_ (u"ࠧࡇࡺࡶࡴࡨࠤࡈࡏࠢᇋ"),
            bstack111111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᇌ"): bstack111111l_opy_ (u"ࠢࡼࡿࡾࢁ࠴ࡥࡢࡶ࡫࡯ࡨ࠴ࡸࡥࡴࡷ࡯ࡸࡸࡅࡢࡶ࡫࡯ࡨࡎࡪ࠽ࡼࡿࠥᇍ").format(env.get(bstack111111l_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫᇎ")), env.get(bstack111111l_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࠧᇏ")), env.get(bstack111111l_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠪᇐ"))),
            bstack111111l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᇑ"): env.get(bstack111111l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᇒ")),
            bstack111111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᇓ"): env.get(bstack111111l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᇔ"))
        }
    if any([env.get(bstack111111l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᇕ")), env.get(bstack111111l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡘࡅࡔࡑࡏ࡚ࡊࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣᇖ")), env.get(bstack111111l_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢᇗ"))]):
        return {
            bstack111111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᇘ"): bstack111111l_opy_ (u"ࠧࡇࡗࡔࠢࡆࡳࡩ࡫ࡂࡶ࡫࡯ࡨࠧᇙ"),
            bstack111111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᇚ"): env.get(bstack111111l_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡔ࡚ࡈࡌࡊࡅࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᇛ")),
            bstack111111l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᇜ"): env.get(bstack111111l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᇝ")),
            bstack111111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᇞ"): env.get(bstack111111l_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᇟ"))
        }
    if env.get(bstack111111l_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥᇠ")):
        return {
            bstack111111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᇡ"): bstack111111l_opy_ (u"ࠢࡃࡣࡰࡦࡴࡵࠢᇢ"),
            bstack111111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᇣ"): env.get(bstack111111l_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡓࡧࡶࡹࡱࡺࡳࡖࡴ࡯ࠦᇤ")),
            bstack111111l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᇥ"): env.get(bstack111111l_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡸ࡮࡯ࡳࡶࡍࡳࡧࡔࡡ࡮ࡧࠥᇦ")),
            bstack111111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᇧ"): env.get(bstack111111l_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦᇨ"))
        }
    if env.get(bstack111111l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࠣᇩ")) or env.get(bstack111111l_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥᇪ")):
        return {
            bstack111111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᇫ"): bstack111111l_opy_ (u"࡛ࠥࡪࡸࡣ࡬ࡧࡵࠦᇬ"),
            bstack111111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᇭ"): env.get(bstack111111l_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᇮ")),
            bstack111111l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᇯ"): bstack111111l_opy_ (u"ࠢࡎࡣ࡬ࡲࠥࡖࡩࡱࡧ࡯࡭ࡳ࡫ࠢᇰ") if env.get(bstack111111l_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥᇱ")) else None,
            bstack111111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᇲ"): env.get(bstack111111l_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡌࡏࡔࡠࡅࡒࡑࡒࡏࡔࠣᇳ"))
        }
    if any([env.get(bstack111111l_opy_ (u"ࠦࡌࡉࡐࡠࡒࡕࡓࡏࡋࡃࡕࠤᇴ")), env.get(bstack111111l_opy_ (u"ࠧࡍࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨᇵ")), env.get(bstack111111l_opy_ (u"ࠨࡇࡐࡑࡊࡐࡊࡥࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨᇶ"))]):
        return {
            bstack111111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᇷ"): bstack111111l_opy_ (u"ࠣࡉࡲࡳ࡬ࡲࡥࠡࡅ࡯ࡳࡺࡪࠢᇸ"),
            bstack111111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᇹ"): None,
            bstack111111l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᇺ"): env.get(bstack111111l_opy_ (u"ࠦࡕࡘࡏࡋࡇࡆࡘࡤࡏࡄࠣᇻ")),
            bstack111111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᇼ"): env.get(bstack111111l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣᇽ"))
        }
    if env.get(bstack111111l_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࠥᇾ")):
        return {
            bstack111111l_opy_ (u"ࠣࡰࡤࡱࡪࠨᇿ"): bstack111111l_opy_ (u"ࠤࡖ࡬࡮ࡶࡰࡢࡤ࡯ࡩࠧሀ"),
            bstack111111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨሁ"): env.get(bstack111111l_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥሂ")),
            bstack111111l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢሃ"): bstack111111l_opy_ (u"ࠨࡊࡰࡤࠣࠧࢀࢃࠢሄ").format(env.get(bstack111111l_opy_ (u"ࠧࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠪህ"))) if env.get(bstack111111l_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠦሆ")) else None,
            bstack111111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣሇ"): env.get(bstack111111l_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧለ"))
        }
    if bstack1ll111111_opy_(env.get(bstack111111l_opy_ (u"ࠦࡓࡋࡔࡍࡋࡉ࡝ࠧሉ"))):
        return {
            bstack111111l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥሊ"): bstack111111l_opy_ (u"ࠨࡎࡦࡶ࡯࡭࡫ࡿࠢላ"),
            bstack111111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥሌ"): env.get(bstack111111l_opy_ (u"ࠣࡆࡈࡔࡑࡕ࡙ࡠࡗࡕࡐࠧል")),
            bstack111111l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦሎ"): env.get(bstack111111l_opy_ (u"ࠥࡗࡎ࡚ࡅࡠࡐࡄࡑࡊࠨሏ")),
            bstack111111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥሐ"): env.get(bstack111111l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢሑ"))
        }
    if bstack1ll111111_opy_(env.get(bstack111111l_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡁࡄࡖࡌࡓࡓ࡙ࠢሒ"))):
        return {
            bstack111111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧሓ"): bstack111111l_opy_ (u"ࠣࡉ࡬ࡸࡍࡻࡢࠡࡃࡦࡸ࡮ࡵ࡮ࡴࠤሔ"),
            bstack111111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧሕ"): bstack111111l_opy_ (u"ࠥࡿࢂ࠵ࡻࡾ࠱ࡤࡧࡹ࡯࡯࡯ࡵ࠲ࡶࡺࡴࡳ࠰ࡽࢀࠦሖ").format(env.get(bstack111111l_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡘࡋࡒࡗࡇࡕࡣ࡚ࡘࡌࠨሗ")), env.get(bstack111111l_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡅࡑࡑࡖࡍ࡙ࡕࡒ࡚ࠩመ")), env.get(bstack111111l_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉ࠭ሙ"))),
            bstack111111l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤሚ"): env.get(bstack111111l_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠ࡙ࡒࡖࡐࡌࡌࡐ࡙ࠥማ")),
            bstack111111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣሜ"): env.get(bstack111111l_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠥም"))
        }
    if env.get(bstack111111l_opy_ (u"ࠦࡈࡏࠢሞ")) == bstack111111l_opy_ (u"ࠧࡺࡲࡶࡧࠥሟ") and env.get(bstack111111l_opy_ (u"ࠨࡖࡆࡔࡆࡉࡑࠨሠ")) == bstack111111l_opy_ (u"ࠢ࠲ࠤሡ"):
        return {
            bstack111111l_opy_ (u"ࠣࡰࡤࡱࡪࠨሢ"): bstack111111l_opy_ (u"ࠤ࡙ࡩࡷࡩࡥ࡭ࠤሣ"),
            bstack111111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨሤ"): bstack111111l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࢀࢃࠢሥ").format(env.get(bstack111111l_opy_ (u"ࠬ࡜ࡅࡓࡅࡈࡐࡤ࡛ࡒࡍࠩሦ"))),
            bstack111111l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣሧ"): None,
            bstack111111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨረ"): None,
        }
    if env.get(bstack111111l_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢ࡚ࡊࡘࡓࡊࡑࡑࠦሩ")):
        return {
            bstack111111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢሪ"): bstack111111l_opy_ (u"ࠥࡘࡪࡧ࡭ࡤ࡫ࡷࡽࠧራ"),
            bstack111111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢሬ"): None,
            bstack111111l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢር"): env.get(bstack111111l_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡒࡕࡓࡏࡋࡃࡕࡡࡑࡅࡒࡋࠢሮ")),
            bstack111111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨሯ"): env.get(bstack111111l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢሰ"))
        }
    if any([env.get(bstack111111l_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࠧሱ")), env.get(bstack111111l_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡓࡎࠥሲ")), env.get(bstack111111l_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠤሳ")), env.get(bstack111111l_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡖࡈࡅࡒࠨሴ"))]):
        return {
            bstack111111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦስ"): bstack111111l_opy_ (u"ࠢࡄࡱࡱࡧࡴࡻࡲࡴࡧࠥሶ"),
            bstack111111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦሷ"): None,
            bstack111111l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦሸ"): env.get(bstack111111l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦሹ")) or None,
            bstack111111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥሺ"): env.get(bstack111111l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢሻ"), 0)
        }
    if env.get(bstack111111l_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦሼ")):
        return {
            bstack111111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧሽ"): bstack111111l_opy_ (u"ࠣࡉࡲࡇࡉࠨሾ"),
            bstack111111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧሿ"): None,
            bstack111111l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧቀ"): env.get(bstack111111l_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤቁ")),
            bstack111111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦቂ"): env.get(bstack111111l_opy_ (u"ࠨࡇࡐࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡈࡕࡕࡏࡖࡈࡖࠧቃ"))
        }
    if env.get(bstack111111l_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧቄ")):
        return {
            bstack111111l_opy_ (u"ࠣࡰࡤࡱࡪࠨቅ"): bstack111111l_opy_ (u"ࠤࡆࡳࡩ࡫ࡆࡳࡧࡶ࡬ࠧቆ"),
            bstack111111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨቇ"): env.get(bstack111111l_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥቈ")),
            bstack111111l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ቉"): env.get(bstack111111l_opy_ (u"ࠨࡃࡇࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤቊ")),
            bstack111111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨቋ"): env.get(bstack111111l_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨቌ"))
        }
    return {bstack111111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣቍ"): None}
def get_host_info():
    return {
        bstack111111l_opy_ (u"ࠥ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠧ቎"): platform.node(),
        bstack111111l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨ቏"): platform.system(),
        bstack111111l_opy_ (u"ࠧࡺࡹࡱࡧࠥቐ"): platform.machine(),
        bstack111111l_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢቑ"): platform.version(),
        bstack111111l_opy_ (u"ࠢࡢࡴࡦ࡬ࠧቒ"): platform.architecture()[0]
    }
def bstack1l1lllll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l1ll11ll_opy_():
    if bstack1111ll1ll_opy_.get_property(bstack111111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩቓ")):
        return bstack111111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨቔ")
    return bstack111111l_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠩቕ")
def bstack11l1ll111l_opy_(driver):
    info = {
        bstack111111l_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪቖ"): driver.capabilities,
        bstack111111l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠩ቗"): driver.session_id,
        bstack111111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧቘ"): driver.capabilities.get(bstack111111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ቙"), None),
        bstack111111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪቚ"): driver.capabilities.get(bstack111111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪቛ"), None),
        bstack111111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࠬቜ"): driver.capabilities.get(bstack111111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪቝ"), None),
    }
    if bstack11l1ll11ll_opy_() == bstack111111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ቞"):
        info[bstack111111l_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧ቟")] = bstack111111l_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭በ") if bstack111l11ll_opy_() else bstack111111l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪቡ")
    return info
def bstack111l11ll_opy_():
    if bstack1111ll1ll_opy_.get_property(bstack111111l_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨቢ")):
        return True
    if bstack1ll111111_opy_(os.environ.get(bstack111111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫባ"), None)):
        return True
    return False
def bstack1lll111l_opy_(bstack11l11lll1l_opy_, url, data, config):
    headers = config.get(bstack111111l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬቤ"), None)
    proxies = bstack1ll11ll111_opy_(config, url)
    auth = config.get(bstack111111l_opy_ (u"ࠬࡧࡵࡵࡪࠪብ"), None)
    response = requests.request(
            bstack11l11lll1l_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l1ll1111_opy_(bstack11ll1l1l1_opy_, size):
    bstack11ll1l1ll_opy_ = []
    while len(bstack11ll1l1l1_opy_) > size:
        bstack111l1lll_opy_ = bstack11ll1l1l1_opy_[:size]
        bstack11ll1l1ll_opy_.append(bstack111l1lll_opy_)
        bstack11ll1l1l1_opy_ = bstack11ll1l1l1_opy_[size:]
    bstack11ll1l1ll_opy_.append(bstack11ll1l1l1_opy_)
    return bstack11ll1l1ll_opy_
def bstack11ll111lll_opy_(message, bstack11l1lll111_opy_=False):
    os.write(1, bytes(message, bstack111111l_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬቦ")))
    os.write(1, bytes(bstack111111l_opy_ (u"ࠧ࡝ࡰࠪቧ"), bstack111111l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧቨ")))
    if bstack11l1lll111_opy_:
        with open(bstack111111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯ࡲ࠵࠶ࡿ࠭ࠨቩ") + os.environ[bstack111111l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩቪ")] + bstack111111l_opy_ (u"ࠫ࠳ࡲ࡯ࡨࠩቫ"), bstack111111l_opy_ (u"ࠬࡧࠧቬ")) as f:
            f.write(message + bstack111111l_opy_ (u"࠭࡜࡯ࠩቭ"))
def bstack11l1ll1ll1_opy_():
    return os.environ[bstack111111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪቮ")].lower() == bstack111111l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ቯ")
def bstack11111ll1_opy_(bstack11l1l1llll_opy_):
    return bstack111111l_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨተ").format(bstack11ll11l1l1_opy_, bstack11l1l1llll_opy_)
def bstack11ll1l1l_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack111111l_opy_ (u"ࠪ࡞ࠬቱ")
def bstack11ll11l111_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack111111l_opy_ (u"ࠫ࡟࠭ቲ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack111111l_opy_ (u"ࠬࡠࠧታ")))).total_seconds() * 1000
def bstack11ll11111l_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack111111l_opy_ (u"࡚࠭ࠨቴ")
def bstack11l1lllll1_opy_(bstack11l1ll11l1_opy_):
    date_format = bstack111111l_opy_ (u"࡛ࠧࠦࠨࡱࠪࡪࠠࠦࡊ࠽ࠩࡒࡀࠥࡔ࠰ࠨࡪࠬት")
    bstack11l1l1111l_opy_ = datetime.datetime.strptime(bstack11l1ll11l1_opy_, date_format)
    return bstack11l1l1111l_opy_.isoformat() + bstack111111l_opy_ (u"ࠨ࡜ࠪቶ")
def bstack11l1ll1lll_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack111111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩቷ")
    else:
        return bstack111111l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪቸ")
def bstack1ll111111_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack111111l_opy_ (u"ࠫࡹࡸࡵࡦࠩቹ")
def bstack11l11llll1_opy_(val):
    return val.__str__().lower() == bstack111111l_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫቺ")
def bstack1l11llll11_opy_(bstack11l1l1l1l1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l1l1l1l1_opy_ as e:
                print(bstack111111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨቻ").format(func.__name__, bstack11l1l1l1l1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l1lll1ll_opy_(bstack11l1l1lll1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l1l1lll1_opy_(cls, *args, **kwargs)
            except bstack11l1l1l1l1_opy_ as e:
                print(bstack111111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢቼ").format(bstack11l1l1lll1_opy_.__name__, bstack11l1l1l1l1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l1lll1ll_opy_
    else:
        return decorator
def bstack1llll1l11_opy_(bstack1l11111111_opy_):
    if bstack111111l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬች") in bstack1l11111111_opy_ and bstack11l11llll1_opy_(bstack1l11111111_opy_[bstack111111l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ቾ")]):
        return False
    if bstack111111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬቿ") in bstack1l11111111_opy_ and bstack11l11llll1_opy_(bstack1l11111111_opy_[bstack111111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ኀ")]):
        return False
    return True
def bstack1lll11111l_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1ll1l1111_opy_(hub_url):
    if bstack11111ll11_opy_() <= version.parse(bstack111111l_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬኁ")):
        if hub_url != bstack111111l_opy_ (u"࠭ࠧኂ"):
            return bstack111111l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣኃ") + hub_url + bstack111111l_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧኄ")
        return bstack1llll1ll1l_opy_
    if hub_url != bstack111111l_opy_ (u"ࠩࠪኅ"):
        return bstack111111l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧኆ") + hub_url + bstack111111l_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧኇ")
    return bstack1l1l1l1l11_opy_
def bstack11l11lll11_opy_():
    return isinstance(os.getenv(bstack111111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫኈ")), str)
def bstack1l11l1ll1_opy_(url):
    return urlparse(url).hostname
def bstack1ll1llllll_opy_(hostname):
    for bstack1lll11l1_opy_ in bstack1ll11l1l1_opy_:
        regex = re.compile(bstack1lll11l1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1l111l1_opy_(bstack11l1l1l11l_opy_, file_name, logger):
    bstack11l11lll_opy_ = os.path.join(os.path.expanduser(bstack111111l_opy_ (u"࠭ࡾࠨ኉")), bstack11l1l1l11l_opy_)
    try:
        if not os.path.exists(bstack11l11lll_opy_):
            os.makedirs(bstack11l11lll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack111111l_opy_ (u"ࠧࡿࠩኊ")), bstack11l1l1l11l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack111111l_opy_ (u"ࠨࡹࠪኋ")):
                pass
            with open(file_path, bstack111111l_opy_ (u"ࠤࡺ࠯ࠧኌ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack11lllllll_opy_.format(str(e)))
def bstack11l1ll1l1l_opy_(file_name, key, value, logger):
    file_path = bstack11l1l111l1_opy_(bstack111111l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪኍ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l11l111_opy_ = json.load(open(file_path, bstack111111l_opy_ (u"ࠫࡷࡨࠧ኎")))
        else:
            bstack1l11l111_opy_ = {}
        bstack1l11l111_opy_[key] = value
        with open(file_path, bstack111111l_opy_ (u"ࠧࡽࠫࠣ኏")) as outfile:
            json.dump(bstack1l11l111_opy_, outfile)
def bstack1ll1l111_opy_(file_name, logger):
    file_path = bstack11l1l111l1_opy_(bstack111111l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ነ"), file_name, logger)
    bstack1l11l111_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack111111l_opy_ (u"ࠧࡳࠩኑ")) as bstack1lll1ll111_opy_:
            bstack1l11l111_opy_ = json.load(bstack1lll1ll111_opy_)
    return bstack1l11l111_opy_
def bstack1l1l11llll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack111111l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬኒ") + file_path + bstack111111l_opy_ (u"ࠩࠣࠫና") + str(e))
def bstack11111ll11_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack111111l_opy_ (u"ࠥࡀࡓࡕࡔࡔࡇࡗࡂࠧኔ")
def bstack1lllll11_opy_(config):
    if bstack111111l_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪን") in config:
        del (config[bstack111111l_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫኖ")])
        return False
    if bstack11111ll11_opy_() < version.parse(bstack111111l_opy_ (u"࠭࠳࠯࠶࠱࠴ࠬኗ")):
        return False
    if bstack11111ll11_opy_() >= version.parse(bstack111111l_opy_ (u"ࠧ࠵࠰࠴࠲࠺࠭ኘ")):
        return True
    if bstack111111l_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨኙ") in config and config[bstack111111l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩኚ")] is False:
        return False
    else:
        return True
def bstack1ll11lll1_opy_(args_list, bstack11ll111l11_opy_):
    index = -1
    for value in bstack11ll111l11_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l111l111l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l111l111l_opy_ = bstack1l111l111l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack111111l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪኛ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack111111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫኜ"), exception=exception)
    def bstack11llll111l_opy_(self):
        if self.result != bstack111111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬኝ"):
            return None
        if bstack111111l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤኞ") in self.exception_type:
            return bstack111111l_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣኟ")
        return bstack111111l_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤአ")
    def bstack11l1l111ll_opy_(self):
        if self.result != bstack111111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩኡ"):
            return None
        if self.bstack1l111l111l_opy_:
            return self.bstack1l111l111l_opy_
        return bstack11l1llllll_opy_(self.exception)
def bstack11l1llllll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l1ll1111_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1l1l1l111_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1lll1l1l_opy_(config, logger):
    try:
        import playwright
        bstack11ll111111_opy_ = playwright.__file__
        bstack11l1lll1l1_opy_ = os.path.split(bstack11ll111111_opy_)
        bstack11l1l1l111_opy_ = bstack11l1lll1l1_opy_[0] + bstack111111l_opy_ (u"ࠪ࠳ࡩࡸࡩࡷࡧࡵ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠴ࡲࡩࡣ࠱ࡦࡰ࡮࠵ࡣ࡭࡫࠱࡮ࡸ࠭ኢ")
        os.environ[bstack111111l_opy_ (u"ࠫࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠧኣ")] = bstack1ll11l1l11_opy_(config)
        with open(bstack11l1l1l111_opy_, bstack111111l_opy_ (u"ࠬࡸࠧኤ")) as f:
            bstack1lllll1lll_opy_ = f.read()
            bstack11l1l1ll11_opy_ = bstack111111l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬእ")
            bstack11l1l11111_opy_ = bstack1lllll1lll_opy_.find(bstack11l1l1ll11_opy_)
            if bstack11l1l11111_opy_ == -1:
              process = subprocess.Popen(bstack111111l_opy_ (u"ࠢ࡯ࡲࡰࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠦኦ"), shell=True, cwd=bstack11l1lll1l1_opy_[0])
              process.wait()
              bstack11l11l1lll_opy_ = bstack111111l_opy_ (u"ࠨࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࠨ࠻ࠨኧ")
              bstack11l1l11ll1_opy_ = bstack111111l_opy_ (u"ࠤࠥࠦࠥࡢࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࡠࠧࡁࠠࡤࡱࡱࡷࡹࠦࡻࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠤࢂࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩࠬ࠿ࠥ࡯ࡦࠡࠪࡳࡶࡴࡩࡥࡴࡵ࠱ࡩࡳࡼ࠮ࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠬࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠨࠪ࠽ࠣࠦࠧࠨከ")
              bstack11l11ll111_opy_ = bstack1lllll1lll_opy_.replace(bstack11l11l1lll_opy_, bstack11l1l11ll1_opy_)
              with open(bstack11l1l1l111_opy_, bstack111111l_opy_ (u"ࠪࡻࠬኩ")) as f:
                f.write(bstack11l11ll111_opy_)
    except Exception as e:
        logger.error(bstack1ll1llll1l_opy_.format(str(e)))
def bstack1l1l1ll11l_opy_():
  try:
    bstack11l11lllll_opy_ = os.path.join(tempfile.gettempdir(), bstack111111l_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫኪ"))
    bstack11l11l1ll1_opy_ = []
    if os.path.exists(bstack11l11lllll_opy_):
      with open(bstack11l11lllll_opy_) as f:
        bstack11l11l1ll1_opy_ = json.load(f)
      os.remove(bstack11l11lllll_opy_)
    return bstack11l11l1ll1_opy_
  except:
    pass
  return []
def bstack1lll1lll1l_opy_(bstack1111l1l1l_opy_):
  try:
    bstack11l11l1ll1_opy_ = []
    bstack11l11lllll_opy_ = os.path.join(tempfile.gettempdir(), bstack111111l_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲ࠮࡫ࡵࡲࡲࠬካ"))
    if os.path.exists(bstack11l11lllll_opy_):
      with open(bstack11l11lllll_opy_) as f:
        bstack11l11l1ll1_opy_ = json.load(f)
    bstack11l11l1ll1_opy_.append(bstack1111l1l1l_opy_)
    with open(bstack11l11lllll_opy_, bstack111111l_opy_ (u"࠭ࡷࠨኬ")) as f:
        json.dump(bstack11l11l1ll1_opy_, f)
  except:
    pass
def bstack11ll111ll_opy_(logger, bstack11l11ll1l1_opy_ = False):
  try:
    test_name = os.environ.get(bstack111111l_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪክ"), bstack111111l_opy_ (u"ࠨࠩኮ"))
    if test_name == bstack111111l_opy_ (u"ࠩࠪኯ"):
        test_name = threading.current_thread().__dict__.get(bstack111111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡅࡨࡩࡥࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠩኰ"), bstack111111l_opy_ (u"ࠫࠬ኱"))
    bstack11l1llll1l_opy_ = bstack111111l_opy_ (u"ࠬ࠲ࠠࠨኲ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l11ll1l1_opy_:
        bstack111l1l1l_opy_ = os.environ.get(bstack111111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ኳ"), bstack111111l_opy_ (u"ࠧ࠱ࠩኴ"))
        bstack1l1l1l11l_opy_ = {bstack111111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ኵ"): test_name, bstack111111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ኶"): bstack11l1llll1l_opy_, bstack111111l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ኷"): bstack111l1l1l_opy_}
        bstack11l1l11lll_opy_ = []
        bstack11ll1111l1_opy_ = os.path.join(tempfile.gettempdir(), bstack111111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪኸ"))
        if os.path.exists(bstack11ll1111l1_opy_):
            with open(bstack11ll1111l1_opy_) as f:
                bstack11l1l11lll_opy_ = json.load(f)
        bstack11l1l11lll_opy_.append(bstack1l1l1l11l_opy_)
        with open(bstack11ll1111l1_opy_, bstack111111l_opy_ (u"ࠬࡽࠧኹ")) as f:
            json.dump(bstack11l1l11lll_opy_, f)
    else:
        bstack1l1l1l11l_opy_ = {bstack111111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫኺ"): test_name, bstack111111l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ኻ"): bstack11l1llll1l_opy_, bstack111111l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧኼ"): str(multiprocessing.current_process().name)}
        if bstack111111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭ኽ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l1l1l11l_opy_)
  except Exception as e:
      logger.warn(bstack111111l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡶࡹࡵࡧࡶࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢኾ").format(e))
def bstack11l1lllll_opy_(error_message, test_name, index, logger):
  try:
    bstack11ll111l1l_opy_ = []
    bstack1l1l1l11l_opy_ = {bstack111111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ኿"): test_name, bstack111111l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫዀ"): error_message, bstack111111l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ዁"): index}
    bstack11l1l11l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack111111l_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨዂ"))
    if os.path.exists(bstack11l1l11l1l_opy_):
        with open(bstack11l1l11l1l_opy_) as f:
            bstack11ll111l1l_opy_ = json.load(f)
    bstack11ll111l1l_opy_.append(bstack1l1l1l11l_opy_)
    with open(bstack11l1l11l1l_opy_, bstack111111l_opy_ (u"ࠨࡹࠪዃ")) as f:
        json.dump(bstack11ll111l1l_opy_, f)
  except Exception as e:
    logger.warn(bstack111111l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡷࡵࡢࡰࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧዄ").format(e))
def bstack1ll11lll_opy_(bstack1lll11lll1_opy_, name, logger):
  try:
    bstack1l1l1l11l_opy_ = {bstack111111l_opy_ (u"ࠪࡲࡦࡳࡥࠨዅ"): name, bstack111111l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ዆"): bstack1lll11lll1_opy_, bstack111111l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ዇"): str(threading.current_thread()._name)}
    return bstack1l1l1l11l_opy_
  except Exception as e:
    logger.warn(bstack111111l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡤࡨ࡬ࡦࡼࡥࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥወ").format(e))
  return
def bstack11ll111ll1_opy_():
    return platform.system() == bstack111111l_opy_ (u"ࠧࡘ࡫ࡱࡨࡴࡽࡳࠨዉ")
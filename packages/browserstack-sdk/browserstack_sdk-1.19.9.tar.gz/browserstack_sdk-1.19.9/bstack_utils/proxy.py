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
from urllib.parse import urlparse
from bstack_utils.messages import bstack11l1111l1l_opy_
def bstack1111ll1lll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1111lll111_opy_(bstack1111lll11l_opy_, bstack1111ll1ll1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1111lll11l_opy_):
        with open(bstack1111lll11l_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1111ll1lll_opy_(bstack1111lll11l_opy_):
        pac = get_pac(url=bstack1111lll11l_opy_)
    else:
        raise Exception(bstack111111l_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪ᎗").format(bstack1111lll11l_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack111111l_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧ᎘"), 80))
        bstack1111lll1ll_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1111lll1ll_opy_ = bstack111111l_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭᎙")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1111ll1ll1_opy_, bstack1111lll1ll_opy_)
    return proxy_url
def bstack1ll11l11ll_opy_(config):
    return bstack111111l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ᎚") in config or bstack111111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ᎛") in config
def bstack1ll11l1l11_opy_(config):
    if not bstack1ll11l11ll_opy_(config):
        return
    if config.get(bstack111111l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ᎜")):
        return config.get(bstack111111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ᎝"))
    if config.get(bstack111111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ᎞")):
        return config.get(bstack111111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ᎟"))
def bstack1ll11ll111_opy_(config, bstack1111ll1ll1_opy_):
    proxy = bstack1ll11l1l11_opy_(config)
    proxies = {}
    if config.get(bstack111111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᎠ")) or config.get(bstack111111l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᎡ")):
        if proxy.endswith(bstack111111l_opy_ (u"ࠧ࠯ࡲࡤࡧࠬᎢ")):
            proxies = bstack11ll11111_opy_(proxy, bstack1111ll1ll1_opy_)
        else:
            proxies = {
                bstack111111l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᎣ"): proxy
            }
    return proxies
def bstack11ll11111_opy_(bstack1111lll11l_opy_, bstack1111ll1ll1_opy_):
    proxies = {}
    global bstack1111llll11_opy_
    if bstack111111l_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬᎤ") in globals():
        return bstack1111llll11_opy_
    try:
        proxy = bstack1111lll111_opy_(bstack1111lll11l_opy_, bstack1111ll1ll1_opy_)
        if bstack111111l_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥᎥ") in proxy:
            proxies = {}
        elif bstack111111l_opy_ (u"ࠦࡍ࡚ࡔࡑࠤᎦ") in proxy or bstack111111l_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦᎧ") in proxy or bstack111111l_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧᎨ") in proxy:
            bstack1111lll1l1_opy_ = proxy.split(bstack111111l_opy_ (u"ࠢࠡࠤᎩ"))
            if bstack111111l_opy_ (u"ࠣ࠼࠲࠳ࠧᎪ") in bstack111111l_opy_ (u"ࠤࠥᎫ").join(bstack1111lll1l1_opy_[1:]):
                proxies = {
                    bstack111111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᎬ"): bstack111111l_opy_ (u"ࠦࠧᎭ").join(bstack1111lll1l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack111111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᎮ"): str(bstack1111lll1l1_opy_[0]).lower() + bstack111111l_opy_ (u"ࠨ࠺࠰࠱ࠥᎯ") + bstack111111l_opy_ (u"ࠢࠣᎰ").join(bstack1111lll1l1_opy_[1:])
                }
        elif bstack111111l_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢᎱ") in proxy:
            bstack1111lll1l1_opy_ = proxy.split(bstack111111l_opy_ (u"ࠤࠣࠦᎲ"))
            if bstack111111l_opy_ (u"ࠥ࠾࠴࠵ࠢᎳ") in bstack111111l_opy_ (u"ࠦࠧᎴ").join(bstack1111lll1l1_opy_[1:]):
                proxies = {
                    bstack111111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᎵ"): bstack111111l_opy_ (u"ࠨࠢᎶ").join(bstack1111lll1l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack111111l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭Ꮇ"): bstack111111l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᎸ") + bstack111111l_opy_ (u"ࠤࠥᎹ").join(bstack1111lll1l1_opy_[1:])
                }
        else:
            proxies = {
                bstack111111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᎺ"): proxy
            }
    except Exception as e:
        print(bstack111111l_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣᎻ"), bstack11l1111l1l_opy_.format(bstack1111lll11l_opy_, str(e)))
    bstack1111llll11_opy_ = proxies
    return proxies
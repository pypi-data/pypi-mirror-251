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
from uuid import uuid4
from bstack_utils.helper import bstack11ll1l1l_opy_, bstack11ll11l111_opy_
from bstack_utils.bstack1llll1ll1_opy_ import bstack1111l1ll1l_opy_
class bstack1l11l1l11l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack1l111l1l11_opy_=None, framework=None, tags=[], scope=[], bstack11111l11ll_opy_=None, bstack11111l1111_opy_=True, bstack1111111ll1_opy_=None, bstack11lllll1_opy_=None, result=None, duration=None, bstack1l1111l11l_opy_=None, meta={}):
        self.bstack1l1111l11l_opy_ = bstack1l1111l11l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack11111l1111_opy_:
            self.uuid = uuid4().__str__()
        self.bstack1l111l1l11_opy_ = bstack1l111l1l11_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack11111l11ll_opy_ = bstack11111l11ll_opy_
        self.bstack1111111ll1_opy_ = bstack1111111ll1_opy_
        self.bstack11lllll1_opy_ = bstack11lllll1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack1l11l111l1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1111111l11_opy_(self):
        bstack1111111l1l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack111111l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᐥ"): bstack1111111l1l_opy_,
            bstack111111l_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᐦ"): bstack1111111l1l_opy_,
            bstack111111l_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬᐧ"): bstack1111111l1l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack111111l_opy_ (u"ࠣࡗࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡷࡰࡩࡳࡺ࠺ࠡࠤᐨ") + key)
            setattr(self, key, val)
    def bstack111111llll_opy_(self):
        return {
            bstack111111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᐩ"): self.name,
            bstack111111l_opy_ (u"ࠪࡦࡴࡪࡹࠨᐪ"): {
                bstack111111l_opy_ (u"ࠫࡱࡧ࡮ࡨࠩᐫ"): bstack111111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᐬ"),
                bstack111111l_opy_ (u"࠭ࡣࡰࡦࡨࠫᐭ"): self.code
            },
            bstack111111l_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᐮ"): self.scope,
            bstack111111l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᐯ"): self.tags,
            bstack111111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᐰ"): self.framework,
            bstack111111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᐱ"): self.bstack1l111l1l11_opy_
        }
    def bstack111111ll1l_opy_(self):
        return {
         bstack111111l_opy_ (u"ࠫࡲ࡫ࡴࡢࠩᐲ"): self.meta
        }
    def bstack11111111l1_opy_(self):
        return {
            bstack111111l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨᐳ"): {
                bstack111111l_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪᐴ"): self.bstack11111l11ll_opy_
            }
        }
    def bstack11111l11l1_opy_(self, bstack111111111l_opy_, details):
        step = next(filter(lambda st: st[bstack111111l_opy_ (u"ࠧࡪࡦࠪᐵ")] == bstack111111111l_opy_, self.meta[bstack111111l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᐶ")]), None)
        step.update(details)
    def bstack11111l111l_opy_(self, bstack111111111l_opy_):
        step = next(filter(lambda st: st[bstack111111l_opy_ (u"ࠩ࡬ࡨࠬᐷ")] == bstack111111111l_opy_, self.meta[bstack111111l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᐸ")]), None)
        step.update({
            bstack111111l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᐹ"): bstack11ll1l1l_opy_()
        })
    def bstack1l111ll1l1_opy_(self, bstack111111111l_opy_, result, duration=None):
        bstack1111111ll1_opy_ = bstack11ll1l1l_opy_()
        if bstack111111111l_opy_ is not None and self.meta.get(bstack111111l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᐺ")):
            step = next(filter(lambda st: st[bstack111111l_opy_ (u"࠭ࡩࡥࠩᐻ")] == bstack111111111l_opy_, self.meta[bstack111111l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᐼ")]), None)
            step.update({
                bstack111111l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᐽ"): bstack1111111ll1_opy_,
                bstack111111l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᐾ"): duration if duration else bstack11ll11l111_opy_(step[bstack111111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᐿ")], bstack1111111ll1_opy_),
                bstack111111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᑀ"): result.result,
                bstack111111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᑁ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack111111ll11_opy_):
        if self.meta.get(bstack111111l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᑂ")):
            self.meta[bstack111111l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᑃ")].append(bstack111111ll11_opy_)
        else:
            self.meta[bstack111111l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᑄ")] = [ bstack111111ll11_opy_ ]
    def bstack111111l1ll_opy_(self):
        return {
            bstack111111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᑅ"): self.bstack1l11l111l1_opy_(),
            **self.bstack111111llll_opy_(),
            **self.bstack1111111l11_opy_(),
            **self.bstack111111ll1l_opy_()
        }
    def bstack111111l1l1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack111111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᑆ"): self.bstack1111111ll1_opy_,
            bstack111111l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᑇ"): self.duration,
            bstack111111l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᑈ"): self.result.result
        }
        if data[bstack111111l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᑉ")] == bstack111111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᑊ"):
            data[bstack111111l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᑋ")] = self.result.bstack11llll111l_opy_()
            data[bstack111111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᑌ")] = [{bstack111111l_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᑍ"): self.result.bstack11l1l111ll_opy_()}]
        return data
    def bstack111111lll1_opy_(self):
        return {
            bstack111111l_opy_ (u"ࠫࡺࡻࡩࡥࠩᑎ"): self.bstack1l11l111l1_opy_(),
            **self.bstack111111llll_opy_(),
            **self.bstack1111111l11_opy_(),
            **self.bstack111111l1l1_opy_(),
            **self.bstack111111ll1l_opy_()
        }
    def bstack1l111lll1l_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack111111l_opy_ (u"࡙ࠬࡴࡢࡴࡷࡩࡩ࠭ᑏ") in event:
            return self.bstack111111l1ll_opy_()
        elif bstack111111l_opy_ (u"࠭ࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᑐ") in event:
            return self.bstack111111lll1_opy_()
    def bstack1l11l11ll1_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1111111ll1_opy_ = time if time else bstack11ll1l1l_opy_()
        self.duration = duration if duration else bstack11ll11l111_opy_(self.bstack1l111l1l11_opy_, self.bstack1111111ll1_opy_)
        if result:
            self.result = result
class bstack1l11l1llll_opy_(bstack1l11l1l11l_opy_):
    def __init__(self, hooks=[], bstack1l11ll11ll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack1l11ll11ll_opy_ = bstack1l11ll11ll_opy_
        super().__init__(*args, **kwargs, bstack11lllll1_opy_=bstack111111l_opy_ (u"ࠧࡵࡧࡶࡸࠬᑑ"))
    @classmethod
    def bstack111111l111_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack111111l_opy_ (u"ࠨ࡫ࡧࠫᑒ"): id(step),
                bstack111111l_opy_ (u"ࠩࡷࡩࡽࡺࠧᑓ"): step.name,
                bstack111111l_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫᑔ"): step.keyword,
            })
        return bstack1l11l1llll_opy_(
            **kwargs,
            meta={
                bstack111111l_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬᑕ"): {
                    bstack111111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᑖ"): feature.name,
                    bstack111111l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫᑗ"): feature.filename,
                    bstack111111l_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᑘ"): feature.description
                },
                bstack111111l_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪᑙ"): {
                    bstack111111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᑚ"): scenario.name
                },
                bstack111111l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᑛ"): steps,
                bstack111111l_opy_ (u"ࠫࡪࡾࡡ࡮ࡲ࡯ࡩࡸ࠭ᑜ"): bstack1111l1ll1l_opy_(test)
            }
        )
    def bstack11111111ll_opy_(self):
        return {
            bstack111111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᑝ"): self.hooks
        }
    def bstack1111111lll_opy_(self):
        if self.bstack1l11ll11ll_opy_:
            return {
                bstack111111l_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᑞ"): self.bstack1l11ll11ll_opy_
            }
        return {}
    def bstack111111lll1_opy_(self):
        return {
            **super().bstack111111lll1_opy_(),
            **self.bstack11111111ll_opy_()
        }
    def bstack111111l1ll_opy_(self):
        return {
            **super().bstack111111l1ll_opy_(),
            **self.bstack1111111lll_opy_()
        }
    def bstack1l11l11ll1_opy_(self):
        return bstack111111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᑟ")
class bstack1l11111lll_opy_(bstack1l11l1l11l_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack11lllll1_opy_=bstack111111l_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᑠ"))
    def bstack1l11lll111_opy_(self):
        return self.hook_type
    def bstack111111l11l_opy_(self):
        return {
            bstack111111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᑡ"): self.hook_type
        }
    def bstack111111lll1_opy_(self):
        return {
            **super().bstack111111lll1_opy_(),
            **self.bstack111111l11l_opy_()
        }
    def bstack111111l1ll_opy_(self):
        return {
            **super().bstack111111l1ll_opy_(),
            **self.bstack111111l11l_opy_()
        }
    def bstack1l11l11ll1_opy_(self):
        return bstack111111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࠬᑢ")
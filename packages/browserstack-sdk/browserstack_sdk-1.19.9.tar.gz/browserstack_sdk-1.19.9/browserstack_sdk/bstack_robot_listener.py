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
import datetime
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1l111l1l1l_opy_ import RobotHandler
from bstack_utils.capture import bstack1l11l11l1l_opy_
from bstack_utils.bstack1l11l1ll1l_opy_ import bstack1l11l1l11l_opy_, bstack1l11111lll_opy_, bstack1l11l1llll_opy_
from bstack_utils.bstack1ll1l1lll1_opy_ import bstack111lll1l_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1l1l1l111_opy_, bstack11ll1l1l_opy_, Result, \
    bstack1l11llll11_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack111111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩഗ"): [],
        bstack111111l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬഘ"): [],
        bstack111111l_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫങ"): []
    }
    bstack1l1111l1l1_opy_ = []
    bstack1l11ll1111_opy_ = []
    @staticmethod
    def bstack1l111llll1_opy_(log):
        if not (log[bstack111111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩച")] and log[bstack111111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪഛ")].strip()):
            return
        active = bstack111lll1l_opy_.bstack1l11111l1l_opy_()
        log = {
            bstack111111l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩജ"): log[bstack111111l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪഝ")],
            bstack111111l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨഞ"): datetime.datetime.utcnow().isoformat() + bstack111111l_opy_ (u"࡚࠭ࠨട"),
            bstack111111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨഠ"): log[bstack111111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩഡ")],
        }
        if active:
            if active[bstack111111l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧഢ")] == bstack111111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨണ"):
                log[bstack111111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫത")] = active[bstack111111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬഥ")]
            elif active[bstack111111l_opy_ (u"࠭ࡴࡺࡲࡨࠫദ")] == bstack111111l_opy_ (u"ࠧࡵࡧࡶࡸࠬധ"):
                log[bstack111111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨന")] = active[bstack111111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩഩ")]
        bstack111lll1l_opy_.bstack1l111ll111_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._1l111111l1_opy_ = None
        self._1l1111l111_opy_ = None
        self._1l11111ll1_opy_ = OrderedDict()
        self.bstack1l111l1111_opy_ = bstack1l11l11l1l_opy_(self.bstack1l111llll1_opy_)
    @bstack1l11llll11_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1l11l111ll_opy_()
        if not self._1l11111ll1_opy_.get(attrs.get(bstack111111l_opy_ (u"ࠪ࡭ࡩ࠭പ")), None):
            self._1l11111ll1_opy_[attrs.get(bstack111111l_opy_ (u"ࠫ࡮ࡪࠧഫ"))] = {}
        bstack1l11ll1l11_opy_ = bstack1l11l1llll_opy_(
                bstack1l1111l11l_opy_=attrs.get(bstack111111l_opy_ (u"ࠬ࡯ࡤࠨബ")),
                name=name,
                bstack1l111l1l11_opy_=bstack11ll1l1l_opy_(),
                file_path=os.path.relpath(attrs[bstack111111l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ഭ")], start=os.getcwd()) if attrs.get(bstack111111l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧമ")) != bstack111111l_opy_ (u"ࠨࠩയ") else bstack111111l_opy_ (u"ࠩࠪര"),
                framework=bstack111111l_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩറ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack111111l_opy_ (u"ࠫ࡮ࡪࠧല"), None)
        self._1l11111ll1_opy_[attrs.get(bstack111111l_opy_ (u"ࠬ࡯ࡤࠨള"))][bstack111111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩഴ")] = bstack1l11ll1l11_opy_
    @bstack1l11llll11_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1l111l1lll_opy_()
        self._1l11llllll_opy_(messages)
        for bstack1l1l1111l1_opy_ in self.bstack1l1111l1l1_opy_:
            bstack1l1l1111l1_opy_[bstack111111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩവ")][bstack111111l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧശ")].extend(self.store[bstack111111l_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨഷ")])
            bstack111lll1l_opy_.bstack1l111l11ll_opy_(bstack1l1l1111l1_opy_)
        self.bstack1l1111l1l1_opy_ = []
        self.store[bstack111111l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩസ")] = []
    @bstack1l11llll11_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1l111l1111_opy_.start()
        if not self._1l11111ll1_opy_.get(attrs.get(bstack111111l_opy_ (u"ࠫ࡮ࡪࠧഹ")), None):
            self._1l11111ll1_opy_[attrs.get(bstack111111l_opy_ (u"ࠬ࡯ࡤࠨഺ"))] = {}
        driver = bstack1l1l1l111_opy_(threading.current_thread(), bstack111111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶ഻ࠬ"), None)
        bstack1l11l1ll1l_opy_ = bstack1l11l1llll_opy_(
            bstack1l1111l11l_opy_=attrs.get(bstack111111l_opy_ (u"ࠧࡪࡦ഼ࠪ")),
            name=name,
            bstack1l111l1l11_opy_=bstack11ll1l1l_opy_(),
            file_path=os.path.relpath(attrs[bstack111111l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨഽ")], start=os.getcwd()),
            scope=RobotHandler.bstack1l1111l1ll_opy_(attrs.get(bstack111111l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩാ"), None)),
            framework=bstack111111l_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩി"),
            tags=attrs[bstack111111l_opy_ (u"ࠫࡹࡧࡧࡴࠩീ")],
            hooks=self.store[bstack111111l_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫു")],
            bstack1l11ll11ll_opy_=bstack111lll1l_opy_.bstack1l11l11111_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack111111l_opy_ (u"ࠨࡻࡾࠢ࡟ࡲࠥࢁࡽࠣൂ").format(bstack111111l_opy_ (u"ࠢࠡࠤൃ").join(attrs[bstack111111l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ൄ")]), name) if attrs[bstack111111l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ൅")] else name
        )
        self._1l11111ll1_opy_[attrs.get(bstack111111l_opy_ (u"ࠪ࡭ࡩ࠭െ"))][bstack111111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧേ")] = bstack1l11l1ll1l_opy_
        threading.current_thread().current_test_uuid = bstack1l11l1ll1l_opy_.bstack1l11l111l1_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack111111l_opy_ (u"ࠬ࡯ࡤࠨൈ"), None)
        self.bstack1l11ll11l1_opy_(bstack111111l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ൉"), bstack1l11l1ll1l_opy_)
    @bstack1l11llll11_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1l111l1111_opy_.reset()
        bstack1l11l11lll_opy_ = bstack1l11lllll1_opy_.get(attrs.get(bstack111111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧൊ")), bstack111111l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩോ"))
        self._1l11111ll1_opy_[attrs.get(bstack111111l_opy_ (u"ࠩ࡬ࡨࠬൌ"))][bstack111111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ്࠭")].stop(time=bstack11ll1l1l_opy_(), duration=int(attrs.get(bstack111111l_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩൎ"), bstack111111l_opy_ (u"ࠬ࠶ࠧ൏"))), result=Result(result=bstack1l11l11lll_opy_, exception=attrs.get(bstack111111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ൐")), bstack1l111l111l_opy_=[attrs.get(bstack111111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ൑"))]))
        self.bstack1l11ll11l1_opy_(bstack111111l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ൒"), self._1l11111ll1_opy_[attrs.get(bstack111111l_opy_ (u"ࠩ࡬ࡨࠬ൓"))][bstack111111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ൔ")], True)
        self.store[bstack111111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨൕ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack1l11llll11_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1l11l111ll_opy_()
        current_test_id = bstack1l1l1l111_opy_(threading.current_thread(), bstack111111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧൖ"), None)
        bstack1l111l1ll1_opy_ = current_test_id if bstack1l1l1l111_opy_(threading.current_thread(), bstack111111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨൗ"), None) else bstack1l1l1l111_opy_(threading.current_thread(), bstack111111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪ൘"), None)
        if attrs.get(bstack111111l_opy_ (u"ࠨࡶࡼࡴࡪ࠭൙"), bstack111111l_opy_ (u"ࠩࠪ൚")).lower() in [bstack111111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ൛"), bstack111111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭൜")]:
            hook_type = bstack1l111111ll_opy_(attrs.get(bstack111111l_opy_ (u"ࠬࡺࡹࡱࡧࠪ൝")), bstack1l1l1l111_opy_(threading.current_thread(), bstack111111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ൞"), None))
            hook_name = bstack111111l_opy_ (u"ࠧࡼࡿࠪൟ").format(attrs.get(bstack111111l_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨൠ"), bstack111111l_opy_ (u"ࠩࠪൡ")))
            if hook_type in [bstack111111l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧൢ"), bstack111111l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧൣ")]:
                hook_name = bstack111111l_opy_ (u"ࠬࡡࡻࡾ࡟ࠣࡿࢂ࠭൤").format(bstack1l111lllll_opy_.get(hook_type), attrs.get(bstack111111l_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭൥"), bstack111111l_opy_ (u"ࠧࠨ൦")))
            bstack1l1111llll_opy_ = bstack1l11111lll_opy_(
                bstack1l1111l11l_opy_=bstack1l111l1ll1_opy_ + bstack111111l_opy_ (u"ࠨ࠯ࠪ൧") + attrs.get(bstack111111l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ൨"), bstack111111l_opy_ (u"ࠪࠫ൩")).lower(),
                name=hook_name,
                bstack1l111l1l11_opy_=bstack11ll1l1l_opy_(),
                file_path=os.path.relpath(attrs.get(bstack111111l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ൪")), start=os.getcwd()),
                framework=bstack111111l_opy_ (u"ࠬࡘ࡯ࡣࡱࡷࠫ൫"),
                tags=attrs[bstack111111l_opy_ (u"࠭ࡴࡢࡩࡶࠫ൬")],
                scope=RobotHandler.bstack1l1111l1ll_opy_(attrs.get(bstack111111l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ൭"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1l1111llll_opy_.bstack1l11l111l1_opy_()
            threading.current_thread().current_hook_id = bstack1l111l1ll1_opy_ + bstack111111l_opy_ (u"ࠨ࠯ࠪ൮") + attrs.get(bstack111111l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ൯"), bstack111111l_opy_ (u"ࠪࠫ൰")).lower()
            self.store[bstack111111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ൱")] = [bstack1l1111llll_opy_.bstack1l11l111l1_opy_()]
            if bstack1l1l1l111_opy_(threading.current_thread(), bstack111111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ൲"), None):
                self.store[bstack111111l_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ൳")].append(bstack1l1111llll_opy_.bstack1l11l111l1_opy_())
            else:
                self.store[bstack111111l_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭൴")].append(bstack1l1111llll_opy_.bstack1l11l111l1_opy_())
            if bstack1l111l1ll1_opy_:
                self._1l11111ll1_opy_[bstack1l111l1ll1_opy_ + bstack111111l_opy_ (u"ࠨ࠯ࠪ൵") + attrs.get(bstack111111l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ൶"), bstack111111l_opy_ (u"ࠪࠫ൷")).lower()] = { bstack111111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ൸"): bstack1l1111llll_opy_ }
            bstack111lll1l_opy_.bstack1l11ll11l1_opy_(bstack111111l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭൹"), bstack1l1111llll_opy_)
        else:
            bstack1l11ll1l1l_opy_ = {
                bstack111111l_opy_ (u"࠭ࡩࡥࠩൺ"): uuid4().__str__(),
                bstack111111l_opy_ (u"ࠧࡵࡧࡻࡸࠬൻ"): bstack111111l_opy_ (u"ࠨࡽࢀࠤࢀࢃࠧർ").format(attrs.get(bstack111111l_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩൽ")), attrs.get(bstack111111l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨൾ"), bstack111111l_opy_ (u"ࠫࠬൿ"))) if attrs.get(bstack111111l_opy_ (u"ࠬࡧࡲࡨࡵࠪ඀"), []) else attrs.get(bstack111111l_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ඁ")),
                bstack111111l_opy_ (u"ࠧࡴࡶࡨࡴࡤࡧࡲࡨࡷࡰࡩࡳࡺࠧං"): attrs.get(bstack111111l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ඃ"), []),
                bstack111111l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭඄"): bstack11ll1l1l_opy_(),
                bstack111111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪඅ"): bstack111111l_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬආ"),
                bstack111111l_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪඇ"): attrs.get(bstack111111l_opy_ (u"࠭ࡤࡰࡥࠪඈ"), bstack111111l_opy_ (u"ࠧࠨඉ"))
            }
            if attrs.get(bstack111111l_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩඊ"), bstack111111l_opy_ (u"ࠩࠪඋ")) != bstack111111l_opy_ (u"ࠪࠫඌ"):
                bstack1l11ll1l1l_opy_[bstack111111l_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬඍ")] = attrs.get(bstack111111l_opy_ (u"ࠬࡲࡩࡣࡰࡤࡱࡪ࠭ඎ"))
            if not self.bstack1l11ll1111_opy_:
                self._1l11111ll1_opy_[self._1l11l1l1l1_opy_()][bstack111111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩඏ")].add_step(bstack1l11ll1l1l_opy_)
                threading.current_thread().current_step_uuid = bstack1l11ll1l1l_opy_[bstack111111l_opy_ (u"ࠧࡪࡦࠪඐ")]
            self.bstack1l11ll1111_opy_.append(bstack1l11ll1l1l_opy_)
    @bstack1l11llll11_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1l111l1lll_opy_()
        self._1l11llllll_opy_(messages)
        current_test_id = bstack1l1l1l111_opy_(threading.current_thread(), bstack111111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪඑ"), None)
        bstack1l111l1ll1_opy_ = current_test_id if current_test_id else bstack1l1l1l111_opy_(threading.current_thread(), bstack111111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨࠬඒ"), None)
        bstack1l1111lll1_opy_ = bstack1l11lllll1_opy_.get(attrs.get(bstack111111l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪඓ")), bstack111111l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬඔ"))
        bstack1l11lll11l_opy_ = attrs.get(bstack111111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ඕ"))
        if bstack1l1111lll1_opy_ != bstack111111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧඖ") and not attrs.get(bstack111111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ඗")) and self._1l111111l1_opy_:
            bstack1l11lll11l_opy_ = self._1l111111l1_opy_
        bstack1l111ll1ll_opy_ = Result(result=bstack1l1111lll1_opy_, exception=bstack1l11lll11l_opy_, bstack1l111l111l_opy_=[bstack1l11lll11l_opy_])
        if attrs.get(bstack111111l_opy_ (u"ࠨࡶࡼࡴࡪ࠭඘"), bstack111111l_opy_ (u"ࠩࠪ඙")).lower() in [bstack111111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩක"), bstack111111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ඛ")]:
            bstack1l111l1ll1_opy_ = current_test_id if current_test_id else bstack1l1l1l111_opy_(threading.current_thread(), bstack111111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨග"), None)
            if bstack1l111l1ll1_opy_:
                bstack1l11l11l11_opy_ = bstack1l111l1ll1_opy_ + bstack111111l_opy_ (u"ࠨ࠭ࠣඝ") + attrs.get(bstack111111l_opy_ (u"ࠧࡵࡻࡳࡩࠬඞ"), bstack111111l_opy_ (u"ࠨࠩඟ")).lower()
                self._1l11111ll1_opy_[bstack1l11l11l11_opy_][bstack111111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬච")].stop(time=bstack11ll1l1l_opy_(), duration=int(attrs.get(bstack111111l_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨඡ"), bstack111111l_opy_ (u"ࠫ࠵࠭ජ"))), result=bstack1l111ll1ll_opy_)
                bstack111lll1l_opy_.bstack1l11ll11l1_opy_(bstack111111l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧඣ"), self._1l11111ll1_opy_[bstack1l11l11l11_opy_][bstack111111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩඤ")])
        else:
            bstack1l111l1ll1_opy_ = current_test_id if current_test_id else bstack1l1l1l111_opy_(threading.current_thread(), bstack111111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡩࡥࠩඥ"), None)
            if bstack1l111l1ll1_opy_ and len(self.bstack1l11ll1111_opy_) == 1:
                current_step_uuid = bstack1l1l1l111_opy_(threading.current_thread(), bstack111111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡸࡪࡶ࡟ࡶࡷ࡬ࡨࠬඦ"), None)
                self._1l11111ll1_opy_[bstack1l111l1ll1_opy_][bstack111111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬට")].bstack1l111ll1l1_opy_(current_step_uuid, duration=int(attrs.get(bstack111111l_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨඨ"), bstack111111l_opy_ (u"ࠫ࠵࠭ඩ"))), result=bstack1l111ll1ll_opy_)
            else:
                self.bstack1l111ll11l_opy_(attrs)
            self.bstack1l11ll1111_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack111111l_opy_ (u"ࠬ࡮ࡴ࡮࡮ࠪඪ"), bstack111111l_opy_ (u"࠭࡮ࡰࠩණ")) == bstack111111l_opy_ (u"ࠧࡺࡧࡶࠫඬ"):
                return
            self.messages.push(message)
            bstack1l1l11111l_opy_ = []
            if bstack111lll1l_opy_.bstack1l11111l1l_opy_():
                bstack1l1l11111l_opy_.append({
                    bstack111111l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫත"): bstack11ll1l1l_opy_(),
                    bstack111111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪථ"): message.get(bstack111111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫද")),
                    bstack111111l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪධ"): message.get(bstack111111l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫන")),
                    **bstack111lll1l_opy_.bstack1l11111l1l_opy_()
                })
                if len(bstack1l1l11111l_opy_) > 0:
                    bstack111lll1l_opy_.bstack1l111ll111_opy_(bstack1l1l11111l_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack111lll1l_opy_.bstack1l11l1lll1_opy_()
    def bstack1l111ll11l_opy_(self, bstack1l11ll111l_opy_):
        if not bstack111lll1l_opy_.bstack1l11111l1l_opy_():
            return
        kwname = bstack111111l_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬ඲").format(bstack1l11ll111l_opy_.get(bstack111111l_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧඳ")), bstack1l11ll111l_opy_.get(bstack111111l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ප"), bstack111111l_opy_ (u"ࠩࠪඵ"))) if bstack1l11ll111l_opy_.get(bstack111111l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨබ"), []) else bstack1l11ll111l_opy_.get(bstack111111l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫභ"))
        error_message = bstack111111l_opy_ (u"ࠧࡱࡷ࡯ࡣࡰࡩ࠿ࠦ࡜ࠣࡽ࠳ࢁࡡࠨࠠࡽࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡠࠧࢁ࠱ࡾ࡞ࠥࠤࢁࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡠࠧࢁ࠲ࡾ࡞ࠥࠦම").format(kwname, bstack1l11ll111l_opy_.get(bstack111111l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ඹ")), str(bstack1l11ll111l_opy_.get(bstack111111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨය"))))
        bstack1l11l1l111_opy_ = bstack111111l_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠢර").format(kwname, bstack1l11ll111l_opy_.get(bstack111111l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ඼")))
        bstack1l111l11l1_opy_ = error_message if bstack1l11ll111l_opy_.get(bstack111111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫල")) else bstack1l11l1l111_opy_
        bstack1l11lll1ll_opy_ = {
            bstack111111l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ඾"): self.bstack1l11ll1111_opy_[-1].get(bstack111111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ඿"), bstack11ll1l1l_opy_()),
            bstack111111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧව"): bstack1l111l11l1_opy_,
            bstack111111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ශ"): bstack111111l_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧෂ") if bstack1l11ll111l_opy_.get(bstack111111l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩස")) == bstack111111l_opy_ (u"ࠪࡊࡆࡏࡌࠨහ") else bstack111111l_opy_ (u"ࠫࡎࡔࡆࡐࠩළ"),
            **bstack111lll1l_opy_.bstack1l11111l1l_opy_()
        }
        bstack111lll1l_opy_.bstack1l111ll111_opy_([bstack1l11lll1ll_opy_])
    def _1l11l1l1l1_opy_(self):
        for bstack1l1111l11l_opy_ in reversed(self._1l11111ll1_opy_):
            bstack1l11l1ll11_opy_ = bstack1l1111l11l_opy_
            data = self._1l11111ll1_opy_[bstack1l1111l11l_opy_][bstack111111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨෆ")]
            if isinstance(data, bstack1l11111lll_opy_):
                if not bstack111111l_opy_ (u"࠭ࡅࡂࡅࡋࠫ෇") in data.bstack1l11lll111_opy_():
                    return bstack1l11l1ll11_opy_
            else:
                return bstack1l11l1ll11_opy_
    def _1l11llllll_opy_(self, messages):
        try:
            bstack1l11lll1l1_opy_ = BuiltIn().get_variable_value(bstack111111l_opy_ (u"ࠢࠥࡽࡏࡓࡌࠦࡌࡆࡘࡈࡐࢂࠨ෈")) in (bstack1l111lll11_opy_.DEBUG, bstack1l111lll11_opy_.TRACE)
            for message, bstack1l11l1111l_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack111111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ෉"))
                level = message.get(bstack111111l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ්"))
                if level == bstack1l111lll11_opy_.FAIL:
                    self._1l111111l1_opy_ = name or self._1l111111l1_opy_
                    self._1l1111l111_opy_ = bstack1l11l1111l_opy_.get(bstack111111l_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦ෋")) if bstack1l11lll1l1_opy_ and bstack1l11l1111l_opy_ else self._1l1111l111_opy_
        except:
            pass
    @classmethod
    def bstack1l11ll11l1_opy_(self, event: str, bstack1l11l1l1ll_opy_: bstack1l11l1l11l_opy_, bstack1l1111ll11_opy_=False):
        if event == bstack111111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭෌"):
            bstack1l11l1l1ll_opy_.set(hooks=self.store[bstack111111l_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ෍")])
        if event == bstack111111l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧ෎"):
            event = bstack111111l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩා")
        if bstack1l1111ll11_opy_:
            bstack1l1l111111_opy_ = {
                bstack111111l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬැ"): event,
                bstack1l11l1l1ll_opy_.bstack1l11l11ll1_opy_(): bstack1l11l1l1ll_opy_.bstack1l111lll1l_opy_(event)
            }
            self.bstack1l1111l1l1_opy_.append(bstack1l1l111111_opy_)
        else:
            bstack111lll1l_opy_.bstack1l11ll11l1_opy_(event, bstack1l11l1l1ll_opy_)
class Messages:
    def __init__(self):
        self._1l11llll1l_opy_ = []
    def bstack1l11l111ll_opy_(self):
        self._1l11llll1l_opy_.append([])
    def bstack1l111l1lll_opy_(self):
        return self._1l11llll1l_opy_.pop() if self._1l11llll1l_opy_ else list()
    def push(self, message):
        self._1l11llll1l_opy_[-1].append(message) if self._1l11llll1l_opy_ else self._1l11llll1l_opy_.append([message])
class bstack1l111lll11_opy_:
    FAIL = bstack111111l_opy_ (u"ࠩࡉࡅࡎࡒࠧෑ")
    ERROR = bstack111111l_opy_ (u"ࠪࡉࡗࡘࡏࡓࠩි")
    WARNING = bstack111111l_opy_ (u"ࠫ࡜ࡇࡒࡏࠩී")
    bstack1l11111l11_opy_ = bstack111111l_opy_ (u"ࠬࡏࡎࡇࡑࠪු")
    DEBUG = bstack111111l_opy_ (u"࠭ࡄࡆࡄࡘࡋࠬ෕")
    TRACE = bstack111111l_opy_ (u"ࠧࡕࡔࡄࡇࡊ࠭ූ")
    bstack1l11ll1ll1_opy_ = [FAIL, ERROR]
def bstack1l11ll1lll_opy_(bstack1l1111ll1l_opy_):
    if not bstack1l1111ll1l_opy_:
        return None
    if bstack1l1111ll1l_opy_.get(bstack111111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ෗"), None):
        return getattr(bstack1l1111ll1l_opy_[bstack111111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬෘ")], bstack111111l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨෙ"), None)
    return bstack1l1111ll1l_opy_.get(bstack111111l_opy_ (u"ࠫࡺࡻࡩࡥࠩේ"), None)
def bstack1l111111ll_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack111111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫෛ"), bstack111111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨො")]:
        return
    if hook_type.lower() == bstack111111l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ෝ"):
        if current_test_uuid is None:
            return bstack111111l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬෞ")
        else:
            return bstack111111l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧෟ")
    elif hook_type.lower() == bstack111111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ෠"):
        if current_test_uuid is None:
            return bstack111111l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ෡")
        else:
            return bstack111111l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩ෢")
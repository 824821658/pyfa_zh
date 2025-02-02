# noinspection PyPackageRequirements
import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.contextMenu import ContextMenuSingle
from service.fit import Fit
from service.settings import ContextMenuSettings


class AmmoToDmgPattern(ContextMenuSingle):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, callingWindow, srcContext, mainItem):
        if not self.settings.get('ammoPattern'):
            return False

        if srcContext not in ("marketItemGroup", "marketItemMisc") or self.mainFrame.getActiveFit() is None:
            return False

        if mainItem is None:
            return False

        for attr in ("emDamage", "thermalDamage", "explosiveDamage", "kineticDamage"):
            if mainItem.getAttribute(attr) is not None:
                return True

        return False

    def getText(self, callingWindow, itmContext, mainItem):
        return "将 {} 设为武器伤害类型".format(itmContext if itmContext is not None else "Item")

    def activate(self, callingWindow, fullContext, mainItem, i):
        fitID = self.mainFrame.getActiveFit()
        Fit.getInstance().setAsPattern(fitID, mainItem)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))

    def getBitmap(self, callingWindow, context, mainItem):
        return None


AmmoToDmgPattern.register()

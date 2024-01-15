
from pyldplayer._internal._interfaces.ldconsoleInstanceI import LDConsoleInstanceI
import pygetwindow as gw
import pyldplayer._utils.misc as misc 
import numpy as np
import typing
from pyldplayer._utils.misc import find_word_coordinates, multiToggle

class LDWndI:
    def __init__(self, instance : LDConsoleInstanceI):
        self._instance = instance
        self.__cachedWnd : gw.Window = None
        
    @property        
    def isAvailable(self):
        return self._instance.isrunning()
    
    def _getWnd(self):
        if self.__cachedWnd and misc.is_window_valid(self.__cachedWnd):
            return self.__cachedWnd
        
        self.__cachedWnd = None
        
        if not self.isAvailable:
            return None
        
        for w in gw.getAllWindows():
            w : gw.Window
            if w._hWnd == self._instance.top_window_handle:
                self.__cachedWnd = w
                return w

    @property
    def windowRect(self):
        """
        Return the rectangle representing the position and size of the window.

        :return: A tuple containing the left, top, width, and height values of the window rectangle.
        :rtype: tuple[int, int, int, int]
        """
        wnd = self._activateWnd()
        
        return (
            wnd.left, 
            wnd.top, 
            wnd.width, 
            wnd.height
        )
        
    def screenshot(
        self,
        format : typing.Literal["img", "np"] = "np"
    ):
        wnd = self._activateWnd()
        region = self.windowRect

        res, mnumber = misc.screenshot(wnd, region)

        match format:
            case "img":
                return res, mnumber
            case "np":
                return np.array(res), mnumber
    
    def _activateWnd(self):
        wnd = self._getWnd()
        if wnd is None:
            raise RuntimeError("Window Not Found")
        
        try:
            wnd.activate()    
        except gw.PyGetWindowException:
            pass
            
        return wnd
    
    @multiToggle
    def _ocr(self, text : str, languages = ["en"]):
        ss, mnumber = self.screenshot()
        found = find_word_coordinates(ss, text, languages)
        
        if len(found) == 0:
            raise ValueError("cannot locate text: %s" % text)
        
        if mnumber == 1:
            return found
      
        newRet = []
        
        for f in found:
            newRet.append(
               (
                   f[0] + self.windowRect[0],
                   f[1] + self.windowRect[1],
                   f[2],
                   f[3]
               ) 
            )
    
        
        return newRet
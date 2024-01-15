from pyldplayer._internal._interfaces.ldWndI import LDWndI
import pyautogui as pg
import typing

class LDInstanceWndCtrl(LDWndI):
    
    def clickAt(
        self,
        x : float,
        y : float, 
        method : typing.Callable = pg.click
    ):
        rect = self.windowRect
        x = rect[0] + x
        y = rect[1] + y 
        method(x, y)
        
    def clickImg(
        self,
        img : str,
        method : typing.Callable = pg.click,
        imgConfidence : float = 0.8
    ):
        rect = self.windowRect
        res  = pg.locateOnScreen(img, region=rect, grayscale=True, confidence=imgConfidence)
        if res is None:
            raise ValueError("cannot locate image: %s" % img)
        center = pg.center(res)
        x, y = center

        method(x, y)
        
    def hasImg(
        self,
        img : str,
        imgConfidence : float = 0.8
    ):
        rect = self.windowRect
        res  = pg.locateOnScreen(img, region=rect, grayscale=True, confidence=imgConfidence)
        return res
    
    def waitTillImg(
        self,
        img : str,
        imgConfidence : float = 0.8,
        interval : float = 1,
        timeout : float = 10,
        method : typing.Callable = pg.click
    ):
        while True:
            res = self.hasImg(img, imgConfidence)
            if res:
                if method:
                    return method(*res)
                return res
            
            pg.sleep(interval)
            if timeout > 0:
                timeout -= interval
            else:
                break    
        
    def waitForLaunch(
        self,
        max : int = 20,
        min : int = 0
    ):
        if not self._instance.isrunning():
            self._instance.launch()
        
        while True:
            if self.isAvailable and min <= 0:
                return
        
            if max > 0:
                max -= 1
            else:
                break
            
            min -= 1
            
            pg.sleep(1)
            
            
    
    def clickAtText(
        self,
        text : str,
        languages = ["en"],
        method : typing.Callable = pg.click
    ):
        
        res = self._ocr(text, languages, multi=False)
        point = pg.center(res)
    
    
        method(*point)
        
    def waitTillText(
        self,
        text : str,
        languages = ["en"],
        interval : float = 1,
        timeout : float = 10,
        method : typing.Callable = pg.click
    ):
        while True:
            res = self._ocr(text, languages, multi=False)
            if res:
                if method:
                    return method(*res)
                return res
            
            pg.sleep(interval)
            if timeout > 0:
                timeout -= interval
            else:
                break
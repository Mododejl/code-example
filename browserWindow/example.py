from adisp import process
from helpers import dependency
from skeletons.gui.game_control import IBrowserController

class BrowserWindow(object):

    browserCtrl = dependency.descriptor(IBrowserController) 
    
    @process
    def browser(self, url, title, browserSize): 
        yield self.browserCtrl.load(url=url, title=title, browserSize=browserSize, showActionBtn=True, showCloseBtn=True, showWaiting=True)

browserWindow = BrowserWindow()

browserWindow.browser('https://ekspoint-mods.ru/', 'ekspoint-mods.ru', [900, 600])

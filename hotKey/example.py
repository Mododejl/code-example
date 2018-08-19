import Keys
import BigWorld
import game
from game import convertKeyEvent
from gui.app_loader import g_appLoader
        
class HotKeys(object):
        
    def event(self, repeat, down, isDown, isRepeat):
        return not repeat if isRepeat else down if isDown else None
        
    def hotKey(self, event, parse, isDown=True, isRepeat=False):
        result = []
        event = convertKeyEvent(event)
        for key in [x.strip().upper() for x in parse.strip().upper().split(' AND ')]:
            try:
                result.append(getattr(Keys, key if key.startswith('KEY_') else 'KEY_' + key))
            except:
                pass
                
        if len(result) == 1:
            return event[1] == result[0] and self.event(event[3], event[0], isDown, isRepeat)
        return event[1] == result[1] and BigWorld.isKeyDown(result[0]) and self.event(event[3], event[0], isDown, isRepeat) if len(result) == 2 else False    
          
    def getLobby(self):
        return g_appLoader.getDefLobbyApp() 
        
    def getBattle(self):
        return g_appLoader.getDefBattleApp() 


hotKeys = HotKeys() 

def new_handleKeyEvent(event):
    if hotKeys.getLobby(): 
        if hotKeys.hotKey(event, 'LALT and 1'):
            print 'Hangar'
    if hotKeys.getBattle(): 
        if hotKeys.hotKey(event, 'LALT and 1'):
            print 'Battle'
    old_handleKeyEvent(event)


old_handleKeyEvent = game.handleKeyEvent
game.handleKeyEvent = new_handleKeyEvent

import BigWorld
from gui.app_loader import g_appLoader
from gui.Scaleform.framework import ViewTypes

def battleMessage(self, text='', colour='Green', panel='Player'):
    """
    panel = 'Player', 'Vehicle', 'VehicleError'
    colour = 'Red', 'Purple', 'Green', 'Gold', 'Yellow', 'Self'
    """
    battle = g_appLoader.getDefBattleApp()
    battle_page = battle.containerManager.getContainer(ViewTypes.VIEW).getView()
    if battle and battle_page is not None:
        getattr(battle_page.components['battle%sMessages' % panel], 'as_show%sMessageS' % colour, None)(None, text)
    else:
        BigWorld.callback(0.5, partial(battleMessage, text, colour, panel))
        
battleMessage('text', 'Green', 'Player')
battleMessage('text', 'Green', 'Vehicle')
battleMessage('text', 'Green', 'VehicleError')

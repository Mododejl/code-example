from helpers import dependency
from skeletons.gui.shared import IItemsCache
from skeletons.gameplay import IGameplayLogic
from skeletons.gui.goodies import IGoodiesCache
from skeletons.gui.shared.utils import IHangarSpace
from skeletons.gui.lobby_context import ILobbyContext
from skeletons.connection_mgr import IConnectionManager
from skeletons.gui.game_control import IBrowserController
from skeletons.gui.battle_session import IBattleSessionProvider
from skeletons.account_helpers.settings_core import ISettingsCore
from skeletons.account_helpers.settings_core import ISettingsCache

class Skeletons(object):
    
    itemsCache = dependency.descriptor(IItemsCache)
    gameplay = dependency.descriptor(IGameplayLogic)
    hangarSpace = dependency.descriptor(IHangarSpace)
    goodiesCache = dependency.descriptor(IGoodiesCache)
    settingsCore = dependency.descriptor(ISettingsCore)
    lobbyContext = dependency.descriptor(ILobbyContext)
    settingsCache = dependency.descriptor(ISettingsCache)
    browserCtrl = dependency.descriptor(IBrowserController) 
    connectionManager = dependency.descriptor(IConnectionManager)
    sessionProvider = dependency.descriptor(IBattleSessionProvider)

skeletons = Skeletons()

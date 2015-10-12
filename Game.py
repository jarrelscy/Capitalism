import requests
requests.packages.urllib3.disable_warnings()
from firebase import firebase
from Action import *
firebase = firebase.FirebaseApplication('https://capitalism.firebaseio.com', None)

        
class Game:
    def __init__(self, gameID, playerName):
        game = firebase.get('/', gameID)
        if game == None:
            game = {}
            game['Actions'] = []
            game['Players'] = [playerName]
            firebase.put('/', gameID, game)
        self.game = game
        self.gameID = gameID
        self.player = playerName
        self.isLocked = False
    def getCurrentLock(self):
        return firebase.get('/'+self.gameID, 'lock')
    def lock(self):
        lock = self.getCurrentLock()
        if lock == None:
            self.game = firebase.get('/', self.gameID)
            firebase.put('/'+self.gameID+'/', 'lock', self.player)
            self.isLocked = True
            # TODO add consistency check, make sure previous game state is consistent with current           
            return True
        raise Exception('Could not lock - in use by:' + lock)
    def addPlayer(self, player):
        if not self.isLocked:
            raise Exception('Must be locked first')
        if 'Players' not in self.game:
            self.game['Players'] = []
        self.game['Players'].append(player)
    def addAction(self, action):
        # TODO ensure actions are correct actions, e.g. in turn etc.
        if not self.isLocked:
            raise Exception('Must be locked first')        
        if 'Actions' not in self.game:
            self.game['Actions'] = []
        action['player'] = self.player
        self.game['Actions'].append(action)        
    def flush(self):
        if not self.isLocked: #check local lock
            raise Exception('Must be locked first')
        lock = self.getCurrentLock() # check that no one else has inadvertently locked it after us
        if lock == self.player: 
            firebase.put('/', self.gameID, self.game)
            firebase.put('/'+self.gameID+'/', 'lock', None)
            self.isLocked = False
        else:
            raise Exception('Not locked to current player - in use by:' + lock)
    def read(self):
        '''
        note that this does not update the local representation of game as it may not be consistent
        '''
        return firebase.get('/', self.gameID)
        

            
if __name__ == '__main__':
    g = Game('Game1', 'jarrel')
    g.lock()
    g.addAction(Action(action='buy', target='marketing'))
    g.addAction(Action(action='buy', target='marketing'))
    g.addAction(Action(action='buy', target='marketing'))
    g.addAction(Action(action='buy', target='marketing'))
    g.addAction(Action(action='buy', target='libel'))
    g.addAction(Action(action='buy', target='libel'))
    g.addAction(Action(action='buy', target='libel'))    
    g.flush()   
    
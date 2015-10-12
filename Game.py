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
        
    def getCurrentLock(self):
        return firebase.get('/'+self.gameID, 'lock')
    def lock(self):
        lock = self.getCurrentLock()
        if lock == None:
            self.game = firebase.get('/', self.gameID)
            firebase.put('/'+self.gameID+'/', 'lock', self.player)
            # TODO add consistency check, make sure previous game state is consistent with current           
            return True
        raise Exception('Could not lock - in use by:' + lock)
    def addPlayer(self, player):
        if 'Players' not in self.game:
            self.game['Players'] = []
        self.game['Players'].append(player)
    def addAction(self, action):
        if 'Actions' not in self.game:
            self.game['Actions'] = []
        action['player'] = self.player
        self.game['Actions'].append(action)
    def flush(self):
        lock = self.getCurrentLock()
        if lock == self.player:
            firebase.put('/', self.gameID, self.game)
            firebase.put('/'+self.gameID+'/', 'lock', None)
        else:
            raise Exception('Not locked to current player - in use by:' + lock)
    

            
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
    
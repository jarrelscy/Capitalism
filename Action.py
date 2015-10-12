class Action(dict):
    def __init__(self, action, player=None, target=None):
        self['action'] = action
        self['player'] = player
        if target != None:
            self['target'] = target
    
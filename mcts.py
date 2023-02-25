class TreeNode:
    def __init__(self,player, state, parent=None):
        self.player = player
        self.state = state
        self.childrens = {}
        self.baagh_win = 0
        self.goat_win = 0
        self.parent = parent
 
    
    
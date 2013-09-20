class Device():
    """ Instance that serves items(requests)"""
    def __init__(self):
        self.state = False
        self.free_time = 0
        self.end_time = 0

    def __repr__(self):
            return repr((self.state, self.free_time, self.end_time))

class Item():
    """ Instance that serves by device """
    def __init__(self, prc_time):
        self.processing_time = prc_time
        self.enter_stack_time = 0

    def __repr__(self):
                return repr((self.processing_time, self.enter_stack_time))

class Game:
    
    status = {
        0: 'Standing-by',
        1: 'Game started',
        2: 'Escape-pod reached',
        3: 'Escaped'

    }
    progress = 0

    def __init__(self):
        pass

    def next_stage(self) -> None:
        self.progress += 1

    def reset(self) -> None:
        self.progress = 0

    def __str__(self) -> str:
        return self.status[self.progress]
        
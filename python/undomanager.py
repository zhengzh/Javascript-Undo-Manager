class UndoManager:
    def __init__(self):
        self.commands = []
        self.index = -1
        self.limit = 2
        self.isExecuting = False
        self.callback = None
    
    def execute(self, command, action):
        if not command or not callable(command[action]):
            return self
        
        self.isExecuting = True
        
        command[action]()

        self.isExecuting = False
        return self
    
    def add(self, command):
        if self.isExecuting:
            return self
        
        # if we are here after having called undo,
        # invalidate items higher on the stack
        del self.commands[self.index + 1 : -1]

        self.commands.append(command)

        # if limit is set, remove items from the start

        if self.limit and len(self.commands) > self.limit:
            del self.commands[0:-self.limit]
        
        self.index = len(self.commands) - 1

        if self.callback:
            self.callback()
        
        return self
    
    def undo(self):
        if self.index < 0:
            return self

        command = self.commands[self.index]
        
        self.execute(command, "undo")

        self.index -= 1

        if self.callback:
            self.callback()
        
        return self

    def redo(self):
        if self.index + 1 > len(self.commands):
            return self

        command = self.commands[self.index+1]
        
        self.execute(command, "redo")

        self.index += 1

        if self.callback:
            self.callback()

    def clear(self):
        self.commands = []
        self.index = -1
        
    
def test():
    undoManager = UndoManager()
    
    people = {}
    def addPerson(id, name):
        people[id] = name
    
    def removePerson(id):
        del people[id]

    def createPerson(id, name):
        addPerson(id, name)

        undoManager.add({
            "undo": lambda : removePerson(id),
            "redo": lambda : addPerson(id, name)
        })

    createPerson(101, "John")
    createPerson(102, "Mary")
    createPerson(103, "Zhang")
    createPerson(104, "Chen")
    createPerson(105, "Lu")
    print(people)

    undoManager.undo()
    print(people)
    
    undoManager.undo()
    print(people)

    undoManager.clear()

    undoManager.undo()
    print(people)

    createPerson(106, "Qi")

    undoManager.undo()
    print(people)

    undoManager.redo()
    print(people)

if __name__ == '__main__':
    test()
      

        
        
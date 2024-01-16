class SuperList(list):
    def __init__(self, userlist):
        super().__init__(userlist)
        self.userlist = userlist

    def super_append(self, appenders):
        for appender in range(len(appenders)): self.userlist.append(appenders[appender])
        self.extend(appenders)

    def super_insert(self, enteredlist, startingnum):
        num = startingnum
        for element in enteredlist:
            self.userlist.insert(num, element)
            num += 1
        self.clear()
        self.extend(self.userlist)
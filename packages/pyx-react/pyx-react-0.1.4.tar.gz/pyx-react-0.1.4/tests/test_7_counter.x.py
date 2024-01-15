import pyx

import pyx

class Counter:
    def __init__(self):
        self.count = 0

    async def increment(self, event):
        k = await event.altKey
        if k:
            self.count -= 1
        else:
            self.count += 1

    def __render__(self, user):
        return (
            pyx.createElement("div", {"onClick": self.increment}, 
                pyx.createElement("p", {}, "Count: ", self.count), 
                pyx.createElement("button", {"onClick": self.increment}, "Increment"))
        )

app = pyx.App(Counter())

app.run()


import pyx


import pyx
from PIL import Image

class TestApp(pyx.App):
    def __render__(self, user):
        img = Image.open('test.png')
        return (
            pyx.createElement("div", {"src": img}, 
                pyx.createElement("img", {"src": img}, ))
        )

app = TestApp()
app.run()


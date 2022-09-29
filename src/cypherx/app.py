"""
To secure what you send!
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from .CypherX import RSA
import ast
import random

class CypherX(toga.App):
    
    def starter(self):
        self.GenerateButton.enabled = False
        self.SavePrivateButton.enabled = False
        #self.CopyPublicButton.enabled = False
        self.ReadButton.enabled = False
        self.LoadPrivateButton.enabled = False
        self.TextBox.enabled = False
        self.Public_textinput.enabled = False
        self.Private_textinput.enabled = False
        self.EncryptButton.enabled = False
        self.DecryptButton.enabled = False
        self.progressbar.start()
        
    def stoper(self):
        self.progressbar.stop()
        self.GenerateButton.enabled = True
        self.SavePrivateButton.enabled = True
        #self.CopyPublicButton.enabled = True
        self.ReadButton.enabled = True
        self.LoadPrivateButton.enabled = True
        self.TextBox.enabled = True
        self.Public_textinput.enabled = True
        self.Private_textinput.enabled = True
        self.EncryptButton.enabled = True
        self.DecryptButton.enabled = True

    async def GenerateKey(self, widget) -> None:
        self.starter()

        await self.rsa.MakeKey()
        self.Public_textinput.value = str(self.rsa.PublicKey)
        self.Private_textinput.value = str(self.rsa.PrivateKey)

        self.stoper()

    async def SavePrivateKey(self, widget):
        pass
    
    async def ReadKeys(self, widget):
        self.starter()

        try:
            self.rsa.PublicKey = ast.literal_eval(self.Public_textinput.value)
            self.rsa.PrivateKey = ast.literal_eval(
                self.Private_textinput.value)

            if type(self.rsa.PublicKey) is not list or type(self.rsa.PrivateKey) is not list:
                self.rsa.PublicKey = None
                self.rsa.PrivateKey = None

            elif (len(self.rsa.PublicKey) != 2) or (len(self.rsa.PrivateKey) != 2):
                self.rsa.PublicKey = None
                self.rsa.PrivateKey = None
            elif (type(self.rsa.PublicKey[0]) is not int) or (type(self.rsa.PublicKey[1]) is not int):
                self.rsa.PublicKey = None
                self.rsa.PrivateKey = None
            elif (type(self.rsa.PrivateKey[0]) is not int) or (type(self.rsa.PrivateKey[1]) is not int):
                self.rsa.PublicKey = None
                self.rsa.PrivateKey = None
        except:
            self.rsa.PublicKey = None
            self.rsa.PrivateKey = None

        self.stoper()

    async def LoadPrivateKey(self, widget):
        pass

    async def Encrypt(self, widget):

        if self.rsa.PublicKey == None:
            return

        self.starter()

        message = 0
        for x in self.TextBox.value:
            message <<= 8
            message += ord(x)

        newmessage = ''
        while message > 0:
            tmp = random.randrange(
                0, 1 << (self.rsa.size // 2)) << (self.rsa.size // 2)
            tmp |= message & ((1 << (self.rsa.size // 2)) - 1)
            tmp = await self.rsa.Crypto(self.rsa.PublicKey, tmp)
            newmessage = '{num:0{width}x}'.format(
                num=tmp, width=((self.rsa.size >> 2) + 2)) + newmessage
            message >>= (self.rsa.size//2)

        self.TextBox.value = newmessage

        self.stoper()

    async def Decrypt(self, widget):

        if self.rsa.PrivateKey == None:
            return

        self.starter()

        message = 0
        it = 0
        tmp = ''
        for x in self.TextBox.value:
            if it == (self.rsa.size // 4) + 2:
                try:
                    z = int(tmp, 16)
                except:
                    z = 0
                tmp = await self.rsa.Crypto(self.rsa.PrivateKey, z)
                tmp &= (1 << (self.rsa.size // 2)) - 1
                message <<= (self.rsa.size // 2)
                message += tmp
                it = 0
                tmp = ''

            tmp += x
            it += 1

        if it > 0:
            try:
                z = int(tmp, 16)
            except:
                z = 0
            tmp = await self.rsa.Crypto(self.rsa.PrivateKey, z)
            tmp &= (1 << (self.rsa.size // 2)) - 1
            message <<= (self.rsa.size // 2)
            message += tmp

        newmessage = ''

        while message > 0:
            newmessage += chr(message & 0xFF)
            message >>= 8

        self.TextBox.value = newmessage[::-1]

        self.stoper()

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """

        self.rsa = RSA(1024)

        main_box = toga.Box(style=Pack(direction=COLUMN))

        Public_label = toga.Label(
            'Public Key:\t',
            style=Pack(padding=(0, 5))
        )
        self.Public_textinput = toga.TextInput(style=Pack(flex=1))
        '''self.CopyPublicButton = toga.Button(
            'Copy Public Key!',
            on_press=self.CopyPublicKey,
            style=Pack(padding=2),
        )'''

        Public_box = toga.Box(style=Pack(direction=ROW, padding=5))
        Public_box.add(Public_label)
        Public_box.add(self.Public_textinput)
        #Public_box.add(self.CopyPublicButton)
        
        Private_label = toga.Label(
            'Private Key:\t',
            style=Pack(padding=(0, 5))
        )
        self.Private_textinput = toga.TextInput(style=Pack(flex=1))
        '''self.CopyPrivateButton = toga.Button(
            'Copy Private Key!',
            on_press=self.CopyPrivateKey,
            style=Pack(padding=2),
        )'''
        
        Private_box = toga.Box(style=Pack(direction=ROW, padding=5))
        Private_box.add(Private_label)
        Private_box.add(self.Private_textinput)
        #Private_box.add(self.CopyPrivateButton)
        
        self.GenerateButton = toga.Button(
            'Generate Key!',
            on_press=self.GenerateKey,
            style=Pack(padding=5),
        )

        self.SavePrivateButton = toga.Button(
            'Save Private Key!',
            on_press=self.SavePrivateKey,
            style=Pack(padding=5),
        )

        self.ReadButton = toga.Button(
            'Read Keys!',
            on_press=self.ReadKeys,
            style=Pack(padding=5),
        )

        self.LoadPrivateButton = toga.Button(
            'Load Private Key!',
            on_press=self.LoadPrivateKey,
            style=Pack(padding=5),
        )

        self.TextBox = toga.MultilineTextInput(
            style=Pack(padding=5),
        )
        self.TextBox.MIN_HEIGHT = 500

        self.EncryptButton = toga.Button(
            'Code!',
            on_press=self.Encrypt,
            style=Pack(padding=5),
        )

        self.DecryptButton = toga.Button(
            'Decode!',
            on_press=self.Decrypt,
            style=Pack(padding=5),
        )

        self.progressbar = toga.ProgressBar(
            max=None,
            value=20,
        )

        main_box.add(self.progressbar)
        main_box.add(Public_box)
        main_box.add(Private_box)
        main_box.add(self.GenerateButton)
        # main_box.add(self.SavePrivateButton)
        main_box.add(self.ReadButton)
        # main_box.add(self.LoadPrivateButton)
        main_box.add(self.TextBox)
        main_box.add(self.EncryptButton)
        main_box.add(self.DecryptButton)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return CypherX()

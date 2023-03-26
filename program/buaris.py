import os
import asyncio
from dotenv import load_dotenv
import sys
import pygame
import time
from mtranslate import translate
from langdetect import detect
from buaris_dict import language_map
from PyQt5.QtCore import (QSize, Qt, ) 
from PyQt5.QtGui import (QImage, QPalette, QBrush, QIcon,QFont )
from discord import Intents
from discord.ext import commands
import qasync
from PyQt5.QtWidgets import (QApplication,QHBoxLayout,QLabel,QLineEdit,QTextEdit,QVBoxLayout,QWidget,QPushButton )
import PyQt5.QtCore as QtCore
intents = Intents.all()
from discord import Intents
from discord.ext import commands

class Buaris(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle("Buaris")
        self.setGeometry(50, 50, 1800, 900)
        oImage = QImage("white.png")
        sImage = oImage.scaled(QSize(1800, 900))                   # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))                        
        self.setPalette(palette)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setMinimumSize(1800, 900)

        # Initialize the Discord bot
        self.bot = commands.Bot(command_prefix="!", intents=intents)

        # Create the message input, post button, and message display
        self.message_input = QLineEdit()
        self.post_button = QPushButton(
            "Post", clicked=lambda: asyncio.create_task(self.post_message()))
        self.message_display = QTextEdit()
        self.message_input.returnPressed.connect(self.post_button.animateClick)

        # Set the font and colors of the message input
        self.message_input.setFont(QFont("Arial", 12))
        self.message_input.setStyleSheet(
            'QLineEdit {'
            '   border: 2px solid #007bff;'
            '   border-radius: 5px;'
            '   padding: 5px;'
            '   color: #000;'
            '   background-color: #ccc;'
            '}'
        )

        # Set the font and colors of the post button
        self.post_button.setFont(QFont("Arial", 12))
        self.post_button.setStyleSheet(
            "QPushButton {"
            "   border: none;"
            "   border-radius: 5px;"
            "   padding: 8px 15px;"
            "   background-color: #007bff;"
            "   color: #fff;"
            "}"
            "QPushButton:hover {"
            "   background-color: #0069d9;"
            "}"
        )

        # Set the font and colors of the message display
        self.message_display.setFont(QFont("Arial", 15))
        self.message_display.setStyleSheet(
            "QTextEdit {"
            "   border: 2px solid #007bff;"
            "   border-radius: 5px;"
            "   padding: 5px;"
            "   color: #333;"
            "   background-color: #fff;"
            "}"
        )

        # Create the layout and add the widgets
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("What's on your mind?"), alignment=Qt.AlignCenter)
        layout.addWidget(self.message_input)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.post_button)
        self.message_display.setStyleSheet(
            "QTextEdit {"
            "   border: 2px solid #666;"
            "   border-radius: 5px;"
            "   padding: 5px;"
            "   color: #333;"
            "   background-color: #ccc;"
            "}"
        )
        self.message_display.setReadOnly(True)
        layout.addLayout(button_layout)
        layout.addWidget(QLabel("chat logs:"), alignment=Qt.AlignCenter)
        pygame.mixer.pre_init(48000, -16, 1, 1024)
        dark_button = QPushButton("Dark mode")
        dark_button.setStyleSheet("QPushButton {background-color: #00008b; color: #fff} QPushButton:hover {background-color: #0069d9;} QPushButton:pressed {background-color:#004085;}")
        light_button = QPushButton("Light mode")
        light_button.setStyleSheet("QPushButton {background-color: #007bff; color: #fff} QPushButton:hover {background-color: #0069d9;} QPushButton:pressed {background-color:#004085;}")
        dark_button.clicked.connect(lambda:app.setStyleSheet("QWidget {background-color: #333;} QLabel {color: #fff}"))
        light_button.clicked.connect(lambda:app.setStyleSheet("QWidget {background-color: #fff;} QLabel {color: #000}"))
        layout.addWidget(light_button, alignment=Qt.AlignRight)
        layout.addWidget(dark_button, alignment=Qt.AlignRight)
        pygame.init()
        self.sound = pygame.mixer.Sound("beep.mp3")
        layout.addWidget(self.message_display)

    # Register the on_message event listener
        @self.bot.event
        async def on_message(message):
                if message.author == self.bot.user:
                    return
                if message.channel.id == 1084464995011657809:
                    self.message_display.append("<font color = blue>"+message.author.name +": "+ translate(message.content) +"</font>")
                    self.sound.play()
                

    async def post_message(self):
        message = self.message_input.text()
        self.message_display.append(message)
        self.message_input.setText("")

        # Send the message to Discord via the bot
        channel_id = 1084464995011657809  # Replace with the ID of the channel you want to post messages to
        channel = self.bot.get_channel(channel_id)
        await channel.send(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set the background color of the application
    app.setStyleSheet(
        "QWidget {" "   background-color: #f8f9fa;" "}" "QLabel {" "   color: #333;" "}"
    )

    # Initialize the Discord bot
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    buaris_app = Buaris()
    loop = qasync.QSelectorEventLoop(app)
    asyncio.set_event_loop(loop)

    async def main():
        asyncio.create_task(buaris_app.bot.start(TOKEN))
        while True:
             buaris_app.show()
             await asyncio.sleep(5)
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()

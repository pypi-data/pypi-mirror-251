from oscarbot.menu import Menu, Button
from oscarbot.response import TGResponse


def start(user, message):
    menu = Menu([
        Button("Начнем", callback="/diagnostic/"),
    ])
    return TGResponse(
        message="Привет! Мы здесь, чтобы продиагностировать твой бизнес. Начнем?",
        menu=menu
    )


def first_question(user, message):
    menu = Menu([
        Button("Да", callback="/diagnostic/"),
    ])
    return TGResponse(
        message="Привет! Мы здесь, чтобы продиагностировать твой бизнес. Начнем?",
        menu=menu
    )

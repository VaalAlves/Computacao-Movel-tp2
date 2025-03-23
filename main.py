
import flet as ft

from trello_app import TrelloApp

if __name__ == "__main__":
 
    def main(page: ft.Page):
 
        page.title = "(Not) Trello"
        page.padding = 0
        page.bgcolor = ft.Colors.GREY_400
        app = TrelloApp(page)
        page.add(app)
        page.update()
 
    ft.app(main)
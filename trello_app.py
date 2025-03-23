
import flet as ft
 
class TrelloApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.appbar_items = [
            ft.PopupMenuItem(text = "Login"),
            ft.PopupMenuItem(),
            ft.PopupMenuItem(text = "Settings")
        ]
        self.appbar = ft.AppBar(
            leading = ft.Icon(ft.Icons.MOOD),
            leading_width = 100,
            title = ft.Text("(Not) Trello",size = 32, text_align = "start"),
            center_title = False,
            toolbar_height = 75,
            bgcolor = ft.Colors.PURPLE_900,
            actions = [
                ft.Container(
                    content = ft.PopupMenuButton(
                        items = self.appbar_items
                    ),
                    margin = ft.margin.only(left = 50, right = 25)
                )
            ],
        )
        self.page.appbar = self.appbar
        self.page.update()
import flet as ft

from app_layout import AppLayout
from board import Board
from user import User
from data_store import DataStore
from memory_store import InMemoryStore
from theme_manager import ThemeManager

class TrelloApp(AppLayout):
    def __init__(self, page: ft.Page, store: DataStore):
        self.page: ft.Page = page
        self.store: DataStore = store
        self.user: User | None = None
        self.page.on_route_change = self.route_change
        self.boards = self.store.get_boards()
        
        self.current_theme = "light"
        self.theme_colors = ThemeManager.get_theme_colors(self.current_theme)
        
        self.login_profile_button = ft.PopupMenuItem(text = "Log in", on_click = self.login)
        self.theme_toggle_button = ft.PopupMenuItem(
            text = "Switch to Dark Mode", 
            on_click = self.toggle_theme
        )
        
        self.appbar_items = [
            self.login_profile_button,
            ft.PopupMenuItem(),
            self.theme_toggle_button,
            ft.PopupMenuItem(),
            ft.PopupMenuItem(text = "Settings"),
        ]
        
        self.appbar = ft.AppBar(
            leading = ft.Icon(ft.Icons.GRID_GOLDENRATIO_ROUNDED),
            leading_width = 100,
            title = ft.Text(
                f"(Not) Trello",
                font_family = "Helvetica",
                size = 32,
                text_align = ft.TextAlign.START,
                color = self.theme_colors["text"],
            ),
            center_title = False,
            toolbar_height = 75,
            bgcolor = self.theme_colors["appbar"],
            actions = [
                ft.Container(
                    content = ft.PopupMenuButton(items = self.appbar_items),
                    margin = ft.margin.only(left = 50, right = 25),
                )
            ],
        )
        self.page.appbar = self.appbar
        
        self.page.bgcolor = self.theme_colors["background"]
        self.page.update()
        
        super().__init__(
            self,
            self.page,
            self.store,
            tight = True,
            expand = True,
            vertical_alignment = ft.CrossAxisAlignment.START,
        )
    
    def toggle_theme(self, e=None):
        if self.user:
            self.current_theme = self.user.toggle_theme()
        else:
            self.current_theme = "dark" if self.current_theme == "light" else "light"
        
        self.theme_colors = ThemeManager.get_theme_colors(self.current_theme)
        
        self.theme_toggle_button.text = "Switch to Light Mode" if self.current_theme == "dark" else "Switch to Dark Mode"
        
        self.apply_theme()
        
        self.page.update()
    
    def apply_theme(self):
        self.page.bgcolor = self.theme_colors["background"]
        
        self.appbar.bgcolor = self.theme_colors["appbar"]
        self.appbar.title.color = self.theme_colors["text"]
        
        if hasattr(self, "sidebar"):
            self.sidebar.bgcolor = self.theme_colors["sidebar"]
            self.sidebar.top_nav_rail.bgcolor = self.theme_colors["sidebar"]
            self.sidebar.bottom_nav_rail.bgcolor = self.theme_colors["sidebar"]
            
            for dest in self.sidebar.top_nav_rail.destinations:
                if hasattr(dest, "label_content") and isinstance(dest.label_content, ft.Text):
                    dest.label_content.color = self.theme_colors["sidebar_text"]
            
            for dest in self.sidebar.bottom_nav_rail.destinations:
                if hasattr(dest, "label_content") and isinstance(dest.label_content, ft.Text):
                    dest.label_content.color = self.theme_colors["sidebar_text"]
        
        if hasattr(self, "active_view") and self.active_view:
            if isinstance(self.active_view, Board):
                self.active_view.board_lists.bgcolor = self.theme_colors["background"]
                
                for control in self.active_view.board_content.controls:
                    if isinstance(control, BoardList):
                        if hasattr(control, "header"):
                            for header_control in control.header.controls:
                                if isinstance(header_control, ft.Text):
                                    header_control.color = self.theme_colors["list_title"]
                            
                        for item_container in control.items.controls:
                            if len(item_container.controls) > 1:
                                item = item_container.controls[1]
                                if hasattr(item, "checkbox"):
                                    item.checkbox.label_style = ft.TextStyle(
                                        color=self.theme_colors["item_text"]
                                    )
            elif self.active_view == self.all_boards_view:
                self.all_boards_view.bgcolor = self.theme_colors["background"]
                
                for control in self.all_boards_view.controls:
                    if isinstance(control, ft.Row) and len(control.controls) > 0:
                        for row_control in control.controls:
                            if isinstance(row_control, ft.Container) and hasattr(row_control, "content"):
                                if isinstance(row_control.content, ft.Text):
                                    row_control.content.color = self.theme_colors["board_text"]
    
    def login(self, e):
        def close_dlg(e):
            if user_name.value == "" or password.value == "":
                user_name.error_text = "Please enter an username"
                password.error_text = "Please enter a password"
                self.page.update()
                return
            else:
                user = User(user_name.value, password.value)
                if user not in self.store.get_users():
                    self.store.add_user(user)
                self.user = user
                self.page.client_storage.set("current_user", user_name.value)
                
                self.current_theme = self.user.get_theme()
                self.theme_colors = ThemeManager.get_theme_colors(self.current_theme)
                self.theme_toggle_button.text = "Switch to Light Mode" if self.current_theme == "dark" else "Switch to Dark Mode"
                self.apply_theme()

            self.page.close(dialog)
            self.appbar_items[0] = ft.PopupMenuItem(
                text = f"{self.page.client_storage.get('current_user')}'s Profile"
            )
            self.page.update()

        user_name = ft.TextField(label = "User name")
        password = ft.TextField(label = "Password", password=True)
        dialog = ft.AlertDialog(
            title = ft.Text("Please enter your login credentials"),
            content = ft.Column(
                [
                    user_name,
                    password,
                    ft.ElevatedButton(text = "Login", on_click = close_dlg),
                ],
                tight = True,
            ),
            on_dismiss = lambda e: print("Modal dialog dismissed!"),
        )
        self.page.open(dialog)

    def route_change(self, e):
        troute = ft.TemplateRoute(self.page.route)
        if troute.match("/"):
            self.page.go("/boards")
        elif troute.match("/board/:id"):
            if int(troute.id) > len(self.store.get_boards()):
                self.page.go("/")
                return
            self.set_board_view(int(troute.id))
        elif troute.match("/boards"):
            self.set_all_boards_view()
        elif troute.match("/members"):
            self.set_members_view()
        self.page.update()

    def add_board(self, e):
        def close_dlg(e):
            if (hasattr(e.control, "text") and not e.control.text == "Cancel") or (
                type(e.control) is ft.TextField and e.control.value != ""
            ):
                self.create_new_board(dialog_text.value)
            self.page.close(dialog)
            self.page.update()

        def textfield_change(e):
            if dialog_text.value == "":
                create_button.disabled = True
            else:
                create_button.disabled = False
            self.page.update()

        dialog_text = ft.TextField(
            label = "New Board Name", on_submit=close_dlg, on_change=textfield_change
        )
        create_button = ft.ElevatedButton(
            text = "Create", bgcolor = ft.Colors.PURPLE_400, on_click=close_dlg, disabled=True
        )
        dialog = ft.AlertDialog(
            title = ft.Text("Name your new board"),
            content = ft.Column(
                [
                    dialog_text,
                    ft.Row(
                        [
                            ft.ElevatedButton(text = "Cancel", on_click = close_dlg),
                            create_button,
                        ],
                        alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                tight = True,
            ),
            on_dismiss = lambda e: print("Modal dialog dismissed!"),
        )
        self.page.open(dialog)
        dialog.open = True
        self.page.update()
        dialog_text.focus()

    def create_new_board(self, board_name):
        new_board = Board(self, self.store, board_name, self.page)
        self.store.add_board(new_board)
        self.hydrate_all_boards_view()

    def delete_board(self, e):
        self.store.remove_board(e.control.data)
        self.set_all_boards_view()


def main(page: ft.Page):

    page.title = "(Not) Trello"
    page.padding = 0
    page.theme = ft.Theme(font_family = "Verdana")
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme.page_transitions.windows = "cupertino"
    page.fonts = {"Helvetica": "Helvetica.ttf"}
    page.bgcolor = ft.Colors.GREY_200
    app = TrelloApp(page, InMemoryStore())
    page.add(app)
    page.update()
    app.initialize()


print("flet version: ", ft.version.version)
print("flet path: ", ft.__file__)
ft.app(target = main, assets_dir = "../assets")

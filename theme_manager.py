import flet as ft

class ThemeManager:
    """Manages theme colors for the application"""
    
    @staticmethod
    def get_theme_colors(theme="light"):
        """Get color scheme based on theme"""
        if theme == "dark":
            return {
                "background": ft.colors.GREY_900,
                "card_background": ft.colors.GREY_800,
                "sidebar": ft.colors.GREY_800,
                "appbar": ft.colors.PURPLE_900,
                "text": ft.colors.WHITE,
                "secondary_text": ft.colors.GREY_300,
                "button": ft.colors.PURPLE_700,
                "border": ft.colors.GREY_700,
                "hover": ft.colors.GREY_700,
                "board_text": ft.colors.WHITE,
                "sidebar_text": ft.colors.WHITE,
                "list_title": ft.colors.WHITE,
                "item_text": ft.colors.WHITE,
            }
        else:
            return {
                "background": ft.colors.GREY_200,
                "card_background": ft.colors.WHITE,
                "sidebar": ft.colors.GREY,
                "appbar": ft.colors.PURPLE_400,
                "text": ft.colors.BLACK,
                "secondary_text": ft.colors.GREY_800,
                "button": ft.colors.PURPLE_400,
                "border": ft.colors.BLACK12,
                "hover": ft.colors.GREY_400,
                "board_text": ft.colors.BLACK,
                "sidebar_text": ft.colors.BLACK,
                "list_title": ft.colors.BLACK,
                "item_text": ft.colors.BLACK,
            }
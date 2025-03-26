from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board_list import BoardList
import itertools
import flet as ft
from data_store import DataStore


class Item(ft.Container):
    id_counter = itertools.count()

    def __init__(self, list: "BoardList", store: DataStore, item_text: str):
        self.item_id = next(Item.id_counter)
        self.store: DataStore = store
        self.list = list
        self.item_text = item_text
        
        self.checkbox = ft.Checkbox(label=f"{self.item_text}", width=200)
        
        self.popup_menu = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(
                    content=ft.Text(
                        value="Edit",
                        theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    on_click=self.edit_item,
                ),
                ft.PopupMenuItem(),
                ft.PopupMenuItem(
                    content=ft.Text(
                        value="Delete",
                        theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    on_click=self.delete_item,
                ),
            ],
        )
        
        self.card_item = ft.Card(
            content=ft.Row(
                [
                    ft.Container(
                        content=self.checkbox,
                        border_radius=ft.border_radius.all(5),
                        expand=True,
                    ),
                    ft.Container(
                        content=self.popup_menu,
                        padding=ft.padding.only(right=5),
                    )
                ],
                width=200,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            elevation=1,
            data=self.list,
        )
        
        self.edit_field = ft.Row(
            [
                ft.TextField(
                    value=self.item_text,
                    width=150,
                    height=40,
                    content_padding=ft.padding.only(left=10, bottom=10),
                ),
                ft.TextButton(text="Save", on_click=self.save_item_text),
            ]
        )
        
        self.view = ft.Draggable(
            group="items",
            content=ft.DragTarget(
                group="items",
                content=self.card_item,
                on_accept=self.drag_accept,
                on_leave=self.drag_leave,
                on_will_accept=self.drag_will_accept,
            ),
            data=self,
        )
        super().__init__(content=self.view)

    def edit_item(self, e):
        self.card_item.content.controls[0].content = self.edit_field
        self.card_item.content.controls[1].visible = False
        self.update()

    def save_item_text(self, e):
        self.item_text = self.edit_field.controls[0].value
        self.checkbox.label = self.item_text
        self.card_item.content.controls[0].content = self.checkbox
        self.card_item.content.controls[1].visible = True
        self.update()

    def delete_item(self, e):
        self.list.remove_item(self)

    def drag_accept(self, e):
        src = self.page.get_control(e.src_id)

        if src.content.content == e.control.content:
            self.card_item.elevation = 1
            self.list.set_indicator_opacity(self, 0.0)
            e.control.update()
            return

        if src.data.list == self.list:
            self.list.add_item(chosen_control=src.data, swap_control=self)
            self.card_item.elevation = 1
            e.control.update()
            return

        self.list.add_item(src.data.item_text, swap_control=self)
        src.data.list.remove_item(src.data)
        self.list.set_indicator_opacity(self, 0.0)
        self.card_item.elevation = 1
        self.page.update()

    def drag_will_accept(self, e):
        if e.data == "true":
            self.list.set_indicator_opacity(self, 1.0)
        self.card_item.elevation = 20 if e.data == "true" else 1
        self.page.update()

    def drag_leave(self, e):
        self.list.set_indicator_opacity(self, 0.0)
        self.card_item.elevation = 1
        self.page.update()

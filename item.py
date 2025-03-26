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
        self.tags = []
        self.priority = "normal"
        
        self.checkbox = ft.Checkbox(label=f"{self.item_text}", width=200)
        
        self.priority_indicator = ft.Container(
            width=10,
            height=10,
            border_radius=ft.border_radius.all(5),
            bgcolor=self.get_priority_color(),
            margin=ft.margin.only(right=5)
        )
        
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
                        value="Set Priority",
                        theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    on_click=self.change_priority,
                ),
                ft.PopupMenuItem(),
                ft.PopupMenuItem(
                    content=ft.Text(
                        value="Add Tag",
                        theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    on_click=self.add_tag,
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
                        content=ft.Row(
                            [
                                self.priority_indicator,
                                self.checkbox
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
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
        
    def add_tag(self, e):
        def close_dlg(e):
            if (hasattr(e.control, "text") and not e.control.text == "Cancel") or (
                type(e.control) is ft.TextField and e.control.value != ""
            ):
                tag = tag_text.value.strip()
                if tag and tag not in self.tags:
                    self.tags.append(tag)
                    self.update_tag_display()
            self.page.close(dialog)
            
        def textfield_change(e):
            if tag_text.value.strip() == "":
                add_button.disabled = True
            else:
                add_button.disabled = False
            self.page.update()
            
        tag_text = ft.TextField(
            label="Tag Name", 
            on_submit=close_dlg, 
            on_change=textfield_change
        )
        
        add_button = ft.ElevatedButton(
            text="Add", 
            bgcolor=ft.Colors.PURPLE_400, 
            on_click=close_dlg, 
            disabled=True
        )
        
        dialog = ft.AlertDialog(
            title=ft.Text("Add a tag"),
            content=ft.Column(
                [
                    tag_text,
                    ft.Row(
                        [
                            ft.ElevatedButton(text="Cancel", on_click=close_dlg),
                            add_button,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                tight=True,
            ),
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        
        self.page.open(dialog)
        tag_text.focus()
        
    def update_tag_display(self):
        if self.tags:
            tags_text = ", ".join(self.tags)
            self.checkbox.label = f"{self.item_text} [Tags: {tags_text}]"
        else:
            self.checkbox.label = self.item_text
        self.update()

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

    def get_priority_color(self):
        if self.priority == "high":
            return ft.colors.RED_500
        elif self.priority == "low":
            return ft.colors.GREEN_500
        else:
            return ft.colors.GREY_400
    
    def change_priority(self, e):
        if self.priority == "normal":
            self.priority = "high"
        elif self.priority == "high":
            self.priority = "low"
        else:
            self.priority = "normal"
        
        self.priority_indicator.bgcolor = self.get_priority_color()
        self.update()
import flet as ft
import time
import threading
from playsound import *

def app(page: ft.Page):
    page.title = "Timer App"
    page.window.width = 600
    page.window.height = 400
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = "dark"
    
    starting_time = 0
    timer_thread = None
    remaining_time = 0
    killed = False
    completed = False
    
    main_text = ft.Text(value="Timer App",size=30)
    alert_text = ft.Text(value="Please enter a valid value ...", color="red", visible=False)
    time_area = ft.TextField(label="Seconds", hint_text="Enter seconds", text_align="right")
    
    def timer_function():
        nonlocal remaining_time, killed, completed
        try:
            while remaining_time > 0:
                main_text.value = f"{remaining_time} seconds left!"
                remaining_time -= 1
                page.update()
                for i in range(30):
                    if killed:
                        break
                    time.sleep(0.05)
                if killed:
                    break
            
            if not killed:
                main_text.value = "Timer Finished"
                main_text.color = ft.Colors.GREEN
                page.update()
                completed = True
                while not killed:
                    pass
                main_text.value="Timer App"
                main_text.color = ft.Colors.WHITE
                controls_row.visible = False
                timeset_row.visible = True
                time_area.value = None
                completed = False
                page.update()
            else:
                killed = False
                main_text.value="Timer App"
                main_text.color = ft.Colors.WHITE
                controls_row.visible = False
                timeset_row.visible = True
                time_area.value = None
                page.update()
        except:
            alert_text.visible = True
            page.update()
    
    def reset(e):
        nonlocal remaining_time
        if not completed:
            remaining_time = starting_time
        else:
            start_timer(e)
            main_text.color = ft.Colors.WHITE
            page.update()
        
    def start_timer(e):
        nonlocal remaining_time, timer_thread, starting_time
        try:
            remaining_time = int(time_area.value)
            starting_time = int(time_area.value)
            timeset_row.visible = False
            controls_row.visible = True
            alert_text.visible = False
            page.update()
            timer_thread = threading.Thread(target=timer_function, daemon=True)
            timer_thread.start()
            
        except:
            alert_text.visible = True
            page.update()
    
    def exit(e):
        nonlocal killed
        killed = True
    
    timeset_row = ft.Row([
        time_area,
        ft.IconButton(icon=ft.Icons.START, bgcolor=ft.Colors.BLUE, icon_color=ft.Colors.WHITE, on_click=start_timer, hover_color=ft.Colors.BLUE_300)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        visible=True
    )
    
    controls_row = ft.Row([
        ft.FilledButton(text="reset", expand=0, width=100, on_click=reset),
        ft.FilledButton(text="exit", expand=0, width=100, on_click=exit)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        visible=False
    )
    
    page.add(
        ft.Icon(name=ft.Icons.TIMER_OUTLINED,size=100),
        main_text,
        timeset_row,
        controls_row,
        alert_text
    )

ft.app(app)
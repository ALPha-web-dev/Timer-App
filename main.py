import flet as ft
import asyncio

async def app(page: ft.Page):
    page.title = "Timer App"
    page.window.width = 600
    page.window.height = 400
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = "dark"
    
    starting_time = 0
    timer_task = None
    
    main_text = ft.Text(value="Timer App", size=30)
    alert_text = ft.Text(value="Lütfen geçerli bir değer girin...", color="red", visible=False)
    time_area = ft.TextField(label="Saniye", hint_text="Saniye girin", text_align="right")
    
    async def timer_function():
        nonlocal timer_task
        try:
            remaining_time = starting_time
            while remaining_time > 0:
                main_text.value = f"{remaining_time} saniye kaldı!"
                remaining_time -= 1
                page.update()
                await asyncio.sleep(1)
            
            main_text.value = "Sayaç Bitti"
            main_text.color = ft.Colors.GREEN
            page.update()
            
            controls_row.visible = False
            timeset_row.visible = True
            time_area.value = None
            page.update()

        except asyncio.CancelledError:
            pass
        
    async def start_timer(e):
        nonlocal starting_time, timer_task
        try:
            input_value = int(time_area.value)
            if input_value <= 0:
                alert_text.value = "Lütfen pozitif bir değer girin."
                alert_text.visible = True
                page.update()
                return
            
            starting_time = input_value
            
            if timer_task and not timer_task.done():
                timer_task.cancel()
            
            timeset_row.visible = False
            controls_row.visible = True
            alert_text.visible = False
            
            page.update()
            
            timer_task = asyncio.create_task(timer_function())
        except (ValueError, TypeError):
            alert_text.value = "Lütfen geçerli bir sayı girin."
            alert_text.visible = True
            page.update()
    
    async def reset(e):
        nonlocal starting_time, timer_task
        if timer_task and not timer_task.done():
            timer_task.cancel()
        
        main_text.value = f"{starting_time} saniye kaldı!"
        main_text.color = ft.Colors.WHITE
        page.update()

        timer_task = asyncio.create_task(timer_function())

    async def exit_app(e):
        nonlocal timer_task
        if timer_task and not timer_task.done():
            timer_task.cancel()
        
        main_text.value = "Sayaç Uygulaması"
        main_text.color = ft.Colors.WHITE
        controls_row.visible = False
        timeset_row.visible = True
        time_area.value = None
        alert_text.visible = False
        page.update()
    
    timeset_row = ft.Row([
        time_area,
        ft.IconButton(icon=ft.Icons.START, bgcolor=ft.Colors.BLUE, icon_color=ft.Colors.WHITE, on_click=start_timer, hover_color=ft.Colors.BLUE_300)
    ], alignment=ft.MainAxisAlignment.CENTER)
    
    controls_row = ft.Row([
        ft.FilledButton(text="sıfırla", expand=0, width=100, on_click=reset),
        ft.FilledButton(text="çıkış", expand=0, width=100, on_click=exit_app)
    ], alignment=ft.MainAxisAlignment.CENTER, visible=False)
    
    page.add(
        ft.Icon(name=ft.Icons.TIMER_OUTLINED, size=100),
        main_text,
        timeset_row,
        controls_row,
        alert_text
    )

ft.app(target=app)

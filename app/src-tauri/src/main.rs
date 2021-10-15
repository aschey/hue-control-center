#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use std::sync::Mutex;

use lazy_static::lazy_static;
use tauri::{
    AppHandle, CustomMenuItem, Event, Manager, PhysicalPosition, Position, SystemTray,
    SystemTrayEvent, SystemTrayMenu, SystemTrayMenuItem, Wry,
};
lazy_static! {
    static ref POS: Mutex<PhysicalPosition::<i32>> =
        Mutex::new(PhysicalPosition::<i32> { x: 0, y: 0 });
}

fn hide_window(app: &AppHandle<Wry>) {
    let window = app.get_window("main").unwrap();
    let mut pos = POS.lock().unwrap();
    *pos = window.inner_position().unwrap();

    window.hide().unwrap();
}

fn show_window(app: &AppHandle<Wry>) {
    let window = app.get_window("main").unwrap();
    let pos = POS.lock().unwrap();
    window.set_position(Position::Physical(*pos)).unwrap();
    window.unminimize().unwrap();
    window.set_focus().unwrap();
    window.show().unwrap();
}

fn main() {
    let quit = CustomMenuItem::new("quit".to_string(), "Quit");
    let hide = CustomMenuItem::new("hide".to_string(), "Hide");
    let show = CustomMenuItem::new("show".to_string(), "Show");
    let tray_menu = SystemTrayMenu::new()
        .add_item(quit)
        .add_native_item(SystemTrayMenuItem::Separator)
        .add_item(hide)
        .add_native_item(SystemTrayMenuItem::Separator)
        .add_item(show);
    let tray = SystemTray::new().with_menu(tray_menu);

    let app = tauri::Builder::default()
        .system_tray(tray)
        .on_system_tray_event(|app, event| match event {
            SystemTrayEvent::LeftClick { .. } => {
                let window = app.get_window("main").unwrap();
                let size = window.inner_size().unwrap();
                if window.is_visible().unwrap() && size.height > 0 && size.width > 0 {
                    hide_window(app);
                } else {
                    show_window(app);
                }
            }
            SystemTrayEvent::MenuItemClick { id, .. } => match id.as_str() {
                "quit" => {
                    let window = app.get_window("main").unwrap();
                    window.close().unwrap();
                }
                "hide" => {
                    hide_window(app);
                }
                "show" => {
                    show_window(app);
                }
                _ => {}
            },
            _ => {}
        })
        .plugin(tauri_plugin_window_state::WindowState::default())
        .build(tauri::generate_context!())
        .expect("error while running tauri application");

    app.run(|app_handle, e| match e {
        Event::CloseRequested { label, api, .. } => {
            let app_handle = app_handle.clone();
            let window = app_handle.get_window(&label).unwrap();
            api.prevent_close();
            std::thread::spawn(move || {
                let mut pos = POS.lock().unwrap();
                *pos = window.inner_position().unwrap();
                window.hide().unwrap();
            });
        }
        _ => {}
    });
}

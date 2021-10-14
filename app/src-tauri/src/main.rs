#![cfg_attr(
  all(not(debug_assertions), target_os = "windows"),
  windows_subsystem = "windows"
)]

use std::sync::Mutex;

use lazy_static::lazy_static;
use tauri::{
  CustomMenuItem, Event, Manager, PhysicalPosition, Position, SystemTray, SystemTrayEvent,
  SystemTrayMenu, SystemTrayMenuItem, WindowBuilder,
};
lazy_static! {
  static ref POS: Mutex<PhysicalPosition::<i32>> =
    Mutex::new(PhysicalPosition::<i32> { x: 0, y: 0 });
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
        let mut pos = POS.lock().unwrap();
        if window.is_visible().unwrap() {
          *pos = window.inner_position().unwrap();

          window.hide().unwrap();
        } else {
          window.set_position(Position::Physical(*pos));
          window.show().unwrap();
        }
      }
      SystemTrayEvent::MenuItemClick { id, .. } => match id.as_str() {
        "quit" => {
          std::process::exit(0);
        }
        "hide" => {
          let window = app.get_window("main").unwrap();
          let mut pos = POS.lock().unwrap();
          *pos = window.inner_position().unwrap();

          window.hide().unwrap();
        }
        "show" => {
          let window = app.get_window("main").unwrap();
          let pos = POS.lock().unwrap();
          window.set_position(Position::Physical(*pos));
          window.show().unwrap();
        }
        _ => {}
      },
      _ => {}
    })
    .setup(|app| {
      app.create_window(
        "main".to_string(),
        Default::default(),
        |win_attrs, webview_attrs| (win_attrs, webview_attrs),
      );
      Ok(())
    })
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
        window.hide();
      });
    }
    _ => {}
  });
}

use macroquad::prelude::*;
use std::fs::{File, OpenOptions};
use std::io::{BufRead, BufReader, Write};
use std::path::PathBuf;

#[macroquad::main("Editor de Texto con Imágenes")]
async fn main() {
    // --- Determinar directorio base ---
    let base_dir: PathBuf = std::env::current_dir().unwrap();

    // --- Rutas de imágenes ---
    let img1_path = base_dir.join("imagenes").join("img1.png");
    let img2_path = base_dir.join("imagenes").join("img2.png");

    // --- Cargar texturas ---
    let img_fixed = match load_texture(img1_path.to_str().unwrap()).await {
        Ok(tex) => tex,
        Err(_) => {
            println!("No se pudo cargar img1.png, usar rectángulo rojo");
            Texture2D::empty()
        }
    };

    let img_movable = match load_texture(img2_path.to_str().unwrap()).await {
        Ok(tex) => tex,
        Err(_) => {
            println!("No se pudo cargar img2.png, usar rectángulo azul");
            Texture2D::empty()
        }
    };

    // --- Estado de la imagen movible ---
    let mut movable_pos = vec2(300.0, 200.0);
    let mut movable_scale = 1.0;
    let mut dragging = false;
    let mut drag_offset = vec2(0.0, 0.0);
    let mut resizing = false;
    let mut start_scale = 1.0;
    let mut start_mouse_x = 0.0;

    // --- Texto editable ---
    let filename = "contenido.txt";
    let mut lines: Vec<String> = if let Ok(file) = File::open(filename) {
        BufReader::new(file).lines().filter_map(Result::ok).collect()
    } else {
        vec!["".to_string()]
    };
    let mut cursor_row = 0;
    let mut cursor_col = 0;

    loop {
        clear_background(DARKGRAY);

        // --- Dibujar imagen fija ---
        if img_fixed.width() > 0.0 {
            draw_texture(&img_fixed, 50.0, 100.0, WHITE);
        } else {
            draw_rectangle(50.0, 100.0, 100.0, 100.0, RED);
        }

        // --- Dibujar imagen movible ---
        let img_w = if img_movable.width() > 0.0 { img_movable.width() * movable_scale } else { 100.0 * movable_scale };
        let img_h = if img_movable.height() > 0.0 { img_movable.height() * movable_scale } else { 100.0 * movable_scale };

        if img_movable.width() > 0.0 {
            draw_texture(&img_movable, movable_pos.x, movable_pos.y, WHITE);
        } else {
            draw_rectangle(movable_pos.x, movable_pos.y, img_w, img_h, BLUE);
        }

        // --- Mover y redimensionar imagen movible ---
        let mouse = mouse_position();

        // Iniciar arrastre
        if !dragging && is_mouse_button_down(MouseButton::Left) &&
           mouse.0 >= movable_pos.x && mouse.0 <= movable_pos.x + img_w &&
           mouse.1 >= movable_pos.y && mouse.1 <= movable_pos.y + img_h
        {
            dragging = true;
            drag_offset = vec2(mouse.0 - movable_pos.x, mouse.1 - movable_pos.y);
        }

        // Iniciar redimensionado
        if !resizing && is_mouse_button_down(MouseButton::Right) &&
           mouse.0 >= movable_pos.x && mouse.0 <= movable_pos.x + img_w &&
           mouse.1 >= movable_pos.y && mouse.1 <= movable_pos.y + img_h
        {
            resizing = true;
            start_scale = movable_scale;
            start_mouse_x = mouse.0;
        }

        // Aplicar movimiento o escala
        if dragging && is_mouse_button_down(MouseButton::Left) {
            movable_pos = vec2(mouse.0 - drag_offset.x, mouse.1 - drag_offset.y);
        } else if dragging {
            dragging = false;
        }

        if resizing && is_mouse_button_down(MouseButton::Right) {
            let delta = (mouse.0 - start_mouse_x) / 100.0;
            movable_scale = (start_scale + delta).max(0.1);
        } else if resizing {
            resizing = false;
        }

        // --- Dibujar texto ---
        let mut y = 10.0;
        for (i, line) in lines.iter().enumerate() {
            draw_text(line, 10.0, y, 24.0, WHITE);

            // Cursor
            if i == cursor_row {
                let cursor_x = 10.0 + measure_text(&line[..cursor_col.min(line.len())], None, 24, 1.0).width;
                draw_line(cursor_x, y - 20.0, cursor_x, y + 4.0, 2.0, YELLOW);
            }

            y += 30.0;
        }

        // --- Teclado: insertar caracteres ---
        if let Some(ch) = get_char_pressed() {
            lines[cursor_row].insert(cursor_col, ch);
            cursor_col += 1;
        }

        // Backspace
        if is_key_pressed(KeyCode::Backspace) {
            if cursor_col > 0 {
                lines[cursor_row].remove(cursor_col - 1);
                cursor_col -= 1;
            } else if cursor_row > 0 {
                let removed = lines.remove(cursor_row);
                cursor_row -= 1;
                cursor_col = lines[cursor_row].len();
                lines[cursor_row].push_str(&removed);
            }
        }

        // Enter
        if is_key_pressed(KeyCode::Enter) {
            let new_line = lines[cursor_row].split_off(cursor_col);
            lines.insert(cursor_row + 1, new_line);
            cursor_row += 1;
            cursor_col = 0;
        }

        // Flechas
        if is_key_pressed(KeyCode::Up) && cursor_row > 0 {
            cursor_row -= 1;
            cursor_col = cursor_col.min(lines[cursor_row].len());
        }
        if is_key_pressed(KeyCode::Down) && cursor_row < lines.len() - 1 {
            cursor_row += 1;
            cursor_col = cursor_col.min(lines[cursor_row].len());
        }
        if is_key_pressed(KeyCode::Left) && cursor_col > 0 {
            cursor_col -= 1;
        }
        if is_key_pressed(KeyCode::Right) && cursor_col < lines[cursor_row].len() {
            cursor_col += 1;
        }

        // Guardar con Ctrl+S
        if is_key_pressed(KeyCode::S) && (is_key_down(KeyCode::LeftControl) || is_key_down(KeyCode::RightControl)) {
            if let Ok(mut file) = OpenOptions::new().write(true).create(true).truncate(true).open(filename) {
                for line in &lines {
                    writeln!(file, "{}", line).unwrap();
                }
            }
            println!("Guardado en {}", filename);
        }

        next_frame().await;
    }
}

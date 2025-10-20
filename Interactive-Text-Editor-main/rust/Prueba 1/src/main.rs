use macroquad::prelude::*;
use std::fs::{File, OpenOptions};
use std::io::{BufRead, BufReader, Write};

#[macroquad::main("Editor de Texto con Archivo")]
async fn main() {
    let filename = "contenido.txt";

    // --- Cargar archivo ---
    let mut lines: Vec<String> = if let Ok(file) = File::open(filename) {
        BufReader::new(file).lines().filter_map(Result::ok).collect()
    } else {
        vec!["".to_string()] // archivo no existe, línea vacía
    };

    let mut cursor_row = 0;
    let mut cursor_col = 0;

    loop {
        clear_background(DARKGRAY);

        // --- Dibujar texto ---
        let mut y = 10.0;
        for (i, line) in lines.iter().enumerate() {
            draw_text(line, 10.0, y, 24.0, WHITE);

            // Dibujar cursor
            if i == cursor_row {
                let cursor_x = 10.0
                    + measure_text(&line[..cursor_col.min(line.len())], None, 24, 1.0).width;
                draw_line(cursor_x, y - 20.0, cursor_x, y + 4.0, 2.0, YELLOW);
            }

            y += 30.0;
        }

        // --- Teclado: inserción de caracteres ---
        if let Some(ch) = get_char_pressed() {
            let line = &mut lines[cursor_row];
            line.insert(cursor_col, ch);
            cursor_col += 1;
        }

        // --- Backspace ---
        if is_key_pressed(KeyCode::Backspace) {
    if cursor_col > 0 {
        // Borrar dentro de la línea
        lines[cursor_row].remove(cursor_col - 1);
        cursor_col -= 1;
    } else if cursor_row > 0 {
        // Fusionar línea actual con la anterior
        let removed_line = lines.remove(cursor_row);  // elimina la línea actual
        cursor_row -= 1;
        cursor_col = lines[cursor_row].len();
        lines[cursor_row].push_str(&removed_line); // concatenar
    }
}


        // --- Enter ---
        if is_key_pressed(KeyCode::Enter) {
            let line = &mut lines[cursor_row];
            let new_line = line.split_off(cursor_col);
            lines.insert(cursor_row + 1, new_line);
            cursor_row += 1;
            cursor_col = 0;
        }

        // --- Flechas ---
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

        // --- Guardar con Ctrl+S ---
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

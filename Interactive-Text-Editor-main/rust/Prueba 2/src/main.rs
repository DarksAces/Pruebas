use macroquad::prelude::*;
use std::fs::{File, OpenOptions};
use std::io::{BufRead, BufReader, Write};
use std::time::{Duration, Instant};

#[macroquad::main("Editor de Texto con Archivo")]
async fn main() {
    let filename = "contenido.txt";

    // --- Leer archivo por primera vez ---
    let mut lines: Vec<String> = if let Ok(file) = File::open(filename) {
        BufReader::new(file).lines().filter_map(Result::ok).collect()
    } else {
        vec!["".to_string()]
    };

    let mut cursor_row = 0;
    let mut cursor_col = 0;

    // Para live reload
    let mut last_reload = Instant::now();
    let reload_interval = Duration::from_millis(500);

    loop {
        clear_background(DARKGRAY);

        // --- Live reload del archivo cada 0.5s ---
        if last_reload.elapsed() > reload_interval {
            if let Ok(file) = File::open(filename) {
                let new_lines: Vec<String> = BufReader::new(file).lines().filter_map(Result::ok).collect();
                if new_lines != lines {
                    lines = new_lines;
                    cursor_row = cursor_row.min(lines.len() - 1);
                    cursor_col = cursor_col.min(lines[cursor_row].len());
                }
            }
            last_reload = Instant::now();
        }

        // --- Dibujar texto ---
        let mut y = 10.0;
        for (i, line) in lines.iter().enumerate() {
            draw_text(line, 10.0, y, 24.0, WHITE);
            if i == cursor_row {
                let cursor_x = 10.0
                    + measure_text(&line[..cursor_col.min(line.len())], None, 24, 1.0).width;
                draw_line(cursor_x, y - 20.0, cursor_x, y + 4.0, 2.0, YELLOW);
            }
            y += 30.0;
        }

        // --- Teclado para editar ---
        if let Some(ch) = get_char_pressed() {
            lines[cursor_row].insert(cursor_col, ch);
            cursor_col += 1;
        }

        if is_key_pressed(KeyCode::Backspace) {
            if cursor_col > 0 {
                lines[cursor_row].remove(cursor_col - 1);
                cursor_col -= 1;
            } else if cursor_row > 0 {
                let removed_line = lines.remove(cursor_row);
                cursor_row -= 1;
                cursor_col = lines[cursor_row].len();
                lines[cursor_row].push_str(&removed_line);
            }
        }

        if is_key_pressed(KeyCode::Enter) {
            let line = &mut lines[cursor_row];
            let new_line = line.split_off(cursor_col);
            lines.insert(cursor_row + 1, new_line);
            cursor_row += 1;
            cursor_col = 0;
        }

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

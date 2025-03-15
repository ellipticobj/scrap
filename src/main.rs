use crossterm::{
    event::{self, DisableMouseCapture, EnableMouseCapture, Event as CEvent, KeyCode},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
};
use std::{error::Error, io::stdout, io::Write};
use tui::{
    backend::{Backend, CrosstermBackend},
    Terminal,
    widgets::{Block, Borders, Paragraph},
    layout::{Constraint, Direction, Layout},
    style::{Style, Color},
    text::{Span, Spans},
};

enum Mode {
    Normal,
    Insert,
    Command
}

struct App {
    mode: Mode,
    commandbuff: String,
    textbuff: String
}

impl App {
    fn new() -> App {
        App {
            mode: Mode::Normal,
            textbuff: String::new(),
            commandbuff: String::new(),
        }
    }
}

fn main() -> Result<(), Box<dyn Error>> {

}
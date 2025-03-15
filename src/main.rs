use crossterm::{
    terminal::{self, EnterAlternateScreen, LeaveAlternateScreen, Clear, ClearType},
    ExecutableCommand,
    event::{self, Event, KeyCode},
};
use std::io::{self, Write};
use std::time::Duration;


fn main() -> crossterm::Result<()> {
    let mut stdout = io::stdout();
    let mut running = true;

    stdout.execute(EnterAlternateScreen)?;
    terminal::enable_raw_mode()?;

    while running {
        stdout.execute(Clear(ClearType::All))?;
        println!("press q to exit");

        if event::poll(Duration::from_millis(100))? {
            if let Event::Key(event) = event::read()? {
                match event.code {
                    KeyCode::Char('q') => running = false,
                    KeyCode::Char(c) => {
                        println!("pressed {}", c);
                    }
                    _ => {}
                }
            }
        }
    }

    terminal::disable_raw_mode()?;
    stdout.execute(LeaveAlternateScreen)?;
    Ok(())
}

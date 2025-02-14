# scrap
this is a super simple vim-like notetaking app i made for myself  
built with cython

## installation
clone this repo 
```bash
git clone https://github.com/yourusername/scrappad.git
```
then install dependencies:
```bash
pip install -r requirements.txt
```
then install the app:
```bash
pip install .
```
note that on some systems (like macos) you might have to use `pip3` instead of `pip`.

## features
super basic vim keybinds:  
`:w` --- save  
`:q` --- quit (`:q!` to force quit)  
`:wq` -- write and quit  
`i` ---- insert mode  
  
default folder for notes is at ~/.config/scrappad  

## building
edit setup.py to whatever  
run `pip install .` to build this project.

## screenshots
![screenshot](assets/screenshot.png)

## roadmap
- [ ] logging  
- [ ] make program run faster  
- [ ] add support for markdown  
- [ ] add support for exporting notes  
- [ ] autosave?  
- [ ] argparse?

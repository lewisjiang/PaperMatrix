# PaperMatrix

A PyQt GUI for paper reading notes management and comparison. 

## Overview  

PaperMatrix organizes paper notes by domains, and it is easy for human to compare same domains of several papers. The entry-domain viewing model makes it a matrix of notes.

This is a work during the self-quarantine in February 2019 because of the COVID-19. Were to publish on the extraordinary Feb 29th, but delayed till Mar 8th. >_<

## Prerequisite

Python 3.5+

PyQt 5.9+

## How to use

Just run `python3 papermatrix.py` in the terminal (or equivalent w/ different configurations on different OS)

## Main Functionalities

### v0.1

#### Record paper notes by domains

#### Put notes together for domain by domain comparison

#### Filter notes by domain and search notes by regex

#### Change individual note in one place and sync in all Comparators

#### Compact entry view or expand notes of interest for details 

#### Customizable & saveable domain order and hide/show status

#### One click save / load default database

## License

## Todo list

- [ ] open source license w.r.t. Qt
- [ ] a better way to generate unique paper id.
- [ ] font size for accurate collapse/expand entries in viewers
- [ ] reset default view mode (when dragging columns, adjusting width went too far)
- [ ] move entries up and down in Comparator's `proxyView`, and save the order in db.
- [ ] article attribute: reading progress (see `ReadingProgess` class in article.py).
- [ ] warning message window for reassurance. 
- [ ] **markdown & mathjax support.**
- [ ] load / save database via GUI filesystem
- [ ] standard data i/o api, e.g. JSON, from pasted bibtex, etc. (too lazy & just using pickle for now :p)
- [ ] tidy up menu bar & status bar & tool bar (not having one though)
- [ ] installer & icon for win/Linux
- [ ] aesthetics, icon, itemDelegates
- [ ] ...




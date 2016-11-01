## git

```
git config --global user.email "mattjw@mattjw.net"
git config --global user.name "Matt J Williams"
```


## homebrew
TODO


## vim
See: `.vimrc`.


## tmux



## python

Built-in Python:
```
/System/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7
Python 2.7.10 (default, Oct 23 2015, 19:19:21) 
[GCC 4.2.1 Compatible Apple LLVM 7.0.0 (clang-700.0.59.5)] on darwin
```

Python Software Foundation release (https://www.python.org/downloads/mac-osx/):
```
/Library/Frameworks/Python.framework/Versions/2.7/bin/python
Python 2.7.12 (v2.7.12:d33e0cf91556, Jun 26 2016, 12:10:39) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
```

pip bundled with PSF release:
```
which pip
/Library/Frameworks/Python.framework/Versions/2.7/bin/pip
```

If pip not included by default:
```
curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
python get-pip.py --user
```

**Warning:** Avoid spaces in file paths.

Then generic pipeline...

```
pip install --user virtualenv
# or:  ~/Library/Python/2.7/bin/pip  install --user virtualenv
```

```
virtualenv venv
# or: python ~/Library/Python/2.7/lib/python/site-packages/virtualenv.py venv
```

```
source venv/bin/activate
which pip python
```

```
pip install requests publicsuffix2 urllib3 flask beautifulsoup4 scrapy
pip install sh functools32 python-dateutil pytz unicodecsv
pip install scipy numpy pandas jupyter
pip install matplotlib
pip install nltk scikit-learn pyclust
pip install patsy statsmodels gensim
pip install networkx python-igraph powerlaw
pip install pymongo couchdb
pip install shapely fiona geopy pysal rtree
```

Cartopy (http://louistiao.me/posts/installing-cartopy-on-mac-osx-1011/)...
```
brew install geos
brew install proj
pip install pyproj cartopy
```


## OS X apps

```
Android SDK
Android Studio
Alfred 2 (*)
Base (sqlite explorer) (*)
Caffeine (anti-sleep)
Chicken of the VNC (VNC client)
Cyberduck (file transfer client)
DropBox
DaisyDisk (*)
Eclipse Juno
Eclipse Scala IDE
EverNote
Gephi 0.8
Gephi 0.9
Gimp
git
Graphviz
HDFView
homebrew
Handbrake (video conversion)
Inkscape
iStat Menus (*)
Java JDK
Kaleidoscope (GUI diff) (*)
Karabiner
Keynote (*)
MacDown (Markdown editor; not Mou)
MacTex (2016; comes with LaTeXiT)
Moom (window manager) (*)
Mousepose (not OmniDazzle) (*)
Name Mangler (*)
Octave
python-igraph
Skim
OpenOffice
Postgres
PostGIS
Postbox (*)
QGIS
R
RStudio
Sip (colour picker)
Spotify
Sublime Text 3
Synergy
TextMate 2
TotalSpaces2 (screen manager) (*)
Transmission (BitTorrent client)
Trim Enabler
VirtualBox
Weka (data mining suite)
Xcode
Zotero
```

`(*)` indicates software that there is no free option for this software. Under this definition, freemium (e.g., Dropbox) is considered 'free', whereas anything only offers a finite trial period is 'not free'.

## OS X Config

* Add standard user account to sudoers. `sudo visudo`.
* Screen hotspots. `Mission Control -> Hot Corners`. Top right: Display to Sleep. Bottom right: Desktop.
* Better Trackpad. Lookup = Off. Secondary Click = Two-Fingers. Tap to Click = Off. Silent Clicking = True. Force Click & Haptic Feedback = Off.
* No annoying text substitutions. Open TextEdit. Preferences. Options: disable Correct Spelling Automatically; disable Smart Quotes, Smart Dashes, Text Replacement
* Desktop icons. Show View Optons... Icon Size = 32x32; Grid Spacing = ???; Text Size = 10; Sort By = Snap to Grid
* Finder...
  * Open directory. Right click. Show view options... Always open in list view; Browse in list view; Show columns = Kind; Sort By = Kind. Use as Defaults.
  * Finder show all files. `defaults write com.apple.finder AppleShowAllFiles YES`
  * Finder Preferences: New Finder windows show: `<user>`
* Increase display DPI. Sys Pref -> Display -> Scaled -> third from left.
* Add more desktops. Three-finger gesture zoom-out. `+` button.

## Other config

* Dropbox manual copy.
  * Install Dropbox. Sign-in.
  * On "Would you like to sync everything?". Disable WiFi / prevent syncing. Click 'Sync Everything'.
  * Close app. Copy files to `~/Dropbox2`. `cp -paR /Volumes/some/other/place/Dropbox ~/Dropbox2`.
  * Delete Dropbox metadata files so they'll be re-created. (`.dropbox` and `.dropbox.cache`.) Delete `~/Dropbox`, replace it with `~/Dropbox2`.
  * Re-open app. Resume syncing.

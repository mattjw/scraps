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
python get-pip --user
```

**Warning:** Avoid spaces in file paths.

Then generic pipeline...

```
pip install --user virtualenv
```

```
python ~/Library/Python/2.7/lib/python/site-packages/virtualenv.py venv
virtualenv venv
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

* DropBox.
* Nylas. Mail client.
* MOOM. Window manager.
* TotalSpaces2. Screen manager
* Alfred. Spotlight replacement.
* MacDown. Markdown editor.
* iStat Menus.
* Caffeine. Anti-sleep.
* Base. sqlite database explorer.
* Spotify.
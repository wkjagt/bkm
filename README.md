# BKM : Command line bookmark manager

BKM is a small project of the "scratching my own itch type". I spend a lot of time in my terminal. Every time I needed to open a page in my  browser, I felt like I needed to be able to do this from the command line by typing a bookmark name. Now I can.

**Tip** : The bookmarks are stored in a file `.bkm` in your home folder. If you put this file in your DropBox folder and symlink to it, you'll have your bookmarks synced on all your computers. Another advantage of this is that your bookmarks will be versioned by DropBox so you can go restore bookmarks if you accidentally remove them.

## Installation

```
git clone git@github.com:wkjagt/bkm.git
cd bkm
pip install .
```

If you don't have pip installed, [here's](http://pip.readthedocs.org/en/latest/installing.html) the instructions.

## Usage

### Add a bookmark

Adds a bookmark **my_github** for **https://github.com/wkjagt**

```
bkm add my_github https://github.com/wkjagt
```

### Open a bookmark


Open the **my_github** bookmark in a browser.

```
bkm open my_github
```

You can also open multiple bookmarks by providing multiple bookmark names

```
bkm open my_github google
```

If you don't provide any bookmark name, you'll get a list of all your bookmarks from which you can select.

```
bkm
```

### Show a bookmark

Show the url for the **my_github** bookmark

```
bkm show my_github
```

### List bookmarks

List all bookmarks

```
bkm list
```

### Remove a bookmark

Remove the the **my_github** bookmark

```
bkm remove my_github
```

### Change a bookmark

Change the **my_github** bookmark to **https://www.github.com/wkjagt**

```
bkm change my_github https://www.github.com/wkjagt
```



## TODO
- Support autocomplete with [argcomplete](https://pypi.python.org/pypi/argcomplete)
- Search
- Have a config for which browser to use
- Be able to type `bkm my_github` instead of `bkm open my_github`

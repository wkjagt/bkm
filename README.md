# BKM : Command line bookmark manager

BKM is a small project of the "scratching my own itch type". I spend a lot of time in my terminal. Every time I needed to open a page in my  browser, I felt like I needed to be able to do this from the command line. Now I can.

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


Open the **my_github** bookmark in a browser

```
bkm open my_github
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

### Select from list

Without any arguments, `bkm` gives you the list of bookmarks. Select which one to open.

```
bkm
```


## TODO
- Support autocomplete with [argcomplete](https://pypi.python.org/pypi/argcomplete)
- Run `bkm` without command, and select bookmark with arrow keys
- Search
- Have a config for which browser to use

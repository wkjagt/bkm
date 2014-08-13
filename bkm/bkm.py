#!/usr/bin/env python
import click, webbrowser, ConfigParser, os

CONFIG_FILE = os.path.join(os.path.expanduser("~"), '.bkm')

class Output(object):

    def error(self, msg):
        """Output an error message in red

        :param msg: the error message to output
        """
        click.echo(click.style(msg, bg='red', fg='white'))
        exit()

    def success(self, msg):
        """Output a success message in green

        :param msg: the success message to output
        """
        click.echo(click.style(msg, fg='green'))

    def info(self, msg):
        """Output an informational message in yellow

        :param msg: the informational message to output
        """
        click.echo(click.style(msg, fg='yellow'))

    def as_columns(self, rows):
        widths = [max(map(len, col)) for col in zip(*rows)]
        for row in rows:
            self.info("  ".join((val.ljust(width) for val, width in zip(row, widths))))


class Bookmarks(ConfigParser.ConfigParser):
    """A collection of bookmarks stored in a configuration file.
    The file storage may not be the responsibility of this class
    but for such a small project I'm not going to bother taking
    it out for now.

    :param config_file_path: the path to the configuration file
    :param config_file: an actual file handle to the configuration file
    :param output: an object that outputs information to the user
    """
    def __init__(self, config_file_path, config_file, output, *args, **kwargs):
        ConfigParser.ConfigParser.__init__(self, *args, **kwargs)
        self.config_file = config_file
        self.read(config_file_path)
        self.output = output
        if not self.has_section('bookmarks'):
            self.add_section('bookmarks')

    def get_bookmark_url(self, bookmark):
        """Get the url of a bookmark.

        :param bookmark: The name of the bookmark
        """
        return self.get('bookmarks', bookmark)

    def check_bookmark_exists(self, bookmark):
        """Assert that a bookmark exists in the bookmarks collection.

        :param bookmark: The name of the bookmark
        """
        if not self.has_option('bookmarks', bookmark):
            self.output.error('Bookmark "{0}" doesn\'t exist'.format(bookmark))

    def check_bookmark_doesnt_exist(self, bookmark):
        """Assert that a bookmark doesn't exist in the bookmarks collection.

        :param bookmark: The name of the bookmark
        """
        if self.has_option('bookmarks', bookmark):
            self.output.error('Bookmark "{0}" exist'.format(bookmark))

    def get_bookmarks(self):
        """Get all bookmarks from the bookmarks collection.
        """
        return self.options('bookmarks')

    def save_bookmark(self, bookmark, url):
        """Save a bookmark to the bookmarks collection.

        :param bookmark: The name of the bookmark
        :param url: The url of the bookmark
        """
        self.set('bookmarks', bookmark, url)
        self.write_config_file()

    def delete_bookmark(self, bookmark):
        """Delete a bookmark from the bookmarks collection.

        :param bookmark: The name of the bookmark
        """
        self.remove_option('bookmarks', bookmark)
        self.write_config_file()

    def write_config_file(self):
        """Write the current state of the bookmarks to file.
        """
        self.write(self.config_file)


class BKM(object):
    """The BKM application that manages bookmarks from the command line.

    :param bookmarks: The collection of bookmarks to manage
    :param output: an object that outputs information to the user
    """
    def __init__(self, bookmarks, output):
        self.bookmarks = bookmarks
        self.output = output

    def open(self, bookmarks):
        """Open one or more bookmarks from the bookmark collection or show an
        error if at least one of the bookmarks doesn't exist. If no bookmark
        names are provided, this shows a numbered list of all existing bookmarks
        and a prompt to let the user select one.

        :param bookmarks: the names of the bookmarks to open.
        """
        if len(bookmarks) > 0:
            for bookmark in bookmarks:
                self.bookmarks.check_bookmark_exists(bookmark)
            for bookmark in bookmarks:
                self._open_bookmark(bookmark)
        else:
            self._select_from_list()

    def add(self, bookmark, url):
        """Save a new bookmark to the bookmark collection or show an
        error if a bookmark with the provided name already exists.

        :param bookmark: the name of the bookmark to add.
        :param url: the url of the bookmark to add.
        """
        self.bookmarks.check_bookmark_doesnt_exist(bookmark)
        self.bookmarks.save_bookmark(bookmark, url)
        self.output.success('"{0}" added for "{1}"'.format(bookmark, url))

    def _select_from_list(self):
        """ Show a numbered list of all existing bookmarks and a prompt to
        let the user select one.
        """
        self._list_bookmarks()
        idx = click.prompt('Enter the number of the bookmark to open', type=int)
        try:
            bookmark = self.bookmarks.options('bookmarks')[idx-1]
            self._open_bookmark(bookmark)
        except Exception, e:
            self.output.error('{0} is not a valid option'.format(idx))

    def _list_bookmarks(self):
        """ Show a numbered list of all existing bookmarks.
        """
        rows = []
        for i, bookmark in enumerate(self.bookmarks.get_bookmarks()):
            rows.append([str(i+1), bookmark, self.bookmarks.get('bookmarks', bookmark)])

        self.output.as_columns(rows)

    def _open_bookmark(self, bookmark):
        """Open a bookmark in a web browser, of show an error message of the bookmark
        doesn't exist.

        :param bookmark: The name of the bookmark to open.
        """
        try:
            webbrowser.open(self.bookmarks.get_bookmark_url(bookmark), new=2)
        except ConfigParser.NoOptionError:
            self.output.error('No bookmark named "{0}"'.format(bookmark))

    def show(self, bookmark):
        """Show a saved bookmark.

        :param bookmark: The name of the bookmark to show.
        """
        self.bookmarks.check_bookmark_exists(bookmark)
        self.output.info('Bookmark "{0}" : "{1}"'.format(bookmark, self.bookmarks.get_bookmark_url(bookmark)))

    def list(self):
        """Show a numbered list of bookmarks.
        """
        self._list_bookmarks()

    def change(self, bookmark, url):
        """Change the url of an existing bookmark or show an error if the bookmark
        doesn't exist.

        :param bookmark: the name of the bookmark to change
        """
        self.bookmarks.check_bookmark_exists(bookmark)
        self.bookmarks.save_bookmark(bookmark, url)
        self.output.success('"{0}" changed to "{1}"'.format(bookmark, url))

    def remove(self, bookmark):
        """Remove a bookmark from the save bookmarks

        :param bookmark: the name of the bookmark to remove
        """
        self.bookmarks.check_bookmark_exists(bookmark)
        self.bookmarks.delete_bookmark(bookmark)
        self.output.success('Bookmark "{0}" deleted'.format(bookmark))

@click.group()
@click.pass_context
@click.option('--config_file', type=click.File('w+'), default=CONFIG_FILE)
def cli(ctx, config_file):
    output = Output()
    bookmarks = Bookmarks(CONFIG_FILE, config_file, output)
    bkm = BKM(bookmarks, output)
    ctx.obj = {'bkm' : bkm}

@cli.command()
@click.pass_context
@click.argument('bookmarks', nargs=-1)
def open(ctx, *args, **kwargs):
    getattr(ctx.obj['bkm'], ctx.command.name)(*args, **kwargs)

@cli.command()
@click.pass_context
@click.argument('bookmark', nargs=1)
@click.argument('url', nargs=1)
def add(ctx, *args, **kwargs):
    getattr(ctx.obj['bkm'], ctx.command.name)(*args, **kwargs)

@cli.command()
@click.pass_context
@click.argument('bookmark', nargs=1)
def show(ctx, *args, **kwargs):
    getattr(ctx.obj['bkm'], ctx.command.name)(*args, **kwargs)

@cli.command()
@click.pass_context
def list(ctx, *args, **kwargs):
    getattr(ctx.obj['bkm'], ctx.command.name)(*args, **kwargs)

@cli.command()
@click.pass_context
@click.argument('bookmark', nargs=1)
@click.argument('url', nargs=1)
def change(ctx, *args, **kwargs):
    getattr(ctx.obj['bkm'], ctx.command.name)(*args, **kwargs)

@cli.command()
@click.pass_context
@click.argument('bookmark', nargs=1)
def remove(ctx, *args, **kwargs):
    getattr(ctx.obj['bkm'], ctx.command.name)(*args, **kwargs)

if __name__ == '__main__':
    cli()
#!/usr/bin/env python
import click, webbrowser, ConfigParser, os

CONFIG_FILE = os.path.join(os.path.expanduser("~"), '.bkm')

class Output(object):

    def error(self, msg):
        click.echo(click.style(msg, bg='red', fg='white'))
        exit()

    def success(self, msg):
        click.echo(click.style(msg, fg='green'))

    def info(self, msg):
        click.echo(click.style(msg, fg='yellow'))

    def as_columns(self, rows):
        widths = [max(map(len, col)) for col in zip(*rows)]
        for row in rows:
            self.info("  ".join((val.ljust(width) for val, width in zip(row, widths))))


class Config(ConfigParser.ConfigParser, Output):

    def __init__(self, config_file_path, config_file, *args, **kwargs):
        ConfigParser.ConfigParser.__init__(self, *args, **kwargs)
        self.config_file = config_file
        self.read(config_file_path)
        if not self.has_section('bookmarks'):
            self.add_section('bookmarks')

    def assert_bookmark_exists(self, bookmark):
        if not self.has_option('bookmarks', bookmark):
            self.error('Bookmark "{0}" doesn\'t exist'.format(bookmark))

    def get_bookmark_url(self, bookmark):
        return self.get('bookmarks', bookmark)

    def check_bookmark_exists(self, bookmark):
        if not self.has_option('bookmarks', bookmark):
            self.error('Bookmark "{0}" doesn\'t exist'.format(bookmark))

    def check_bookmark_doesnt_exist(self, bookmark):
        if self.has_option('bookmarks', bookmark):
            self.error('Bookmark "{0}" exist'.format(bookmark))

    def get_bookmarks(self):
        return self.options('bookmarks')

    def save_bookmark(self, bookmark, url):
        self.set('bookmarks', bookmark, url)
        self.write_config_file()

    def delete_bookmark(self, bookmark):
        self.remove_option('bookmarks', bookmark)
        self.write_config_file()

    def write_config_file(self):
        self.write(self.config_file)


class BKM(Output):

    def __init__(self, config):
        self.config = config

    def open(self, bookmarks):
        if len(bookmarks) > 0:
            for bookmark in bookmarks:
                self.config.check_bookmark_exists(bookmark)
            for bookmark in bookmarks:
                self.open_bookmark(bookmark)
        else:
            self.select_from_list()

    def add(self, bookmark, url):

        self.config.check_bookmark_doesnt_exist(bookmark)
        self.config.save_bookmark(bookmark, url)
        self.success('"{0}" added for "{1}"'.format(bookmark, url))

    def select_from_list(self):
        self.list_bookmarks()
        idx = click.prompt('Enter the number of the bookmark to open', type=int)
        try:
            bookmark = self.config.options('bookmarks')[idx-1]
            self.open_bookmark(bookmark)
        except Exception, e:
            print e
            self.error('{0} is not a valid option'.format(idx))

    def list_bookmarks(self):
        rows = []
        for i, bookmark in enumerate(self.config.get_bookmarks()):
            rows.append([str(i+1), bookmark, self.config.get('bookmarks', bookmark)])

        self.as_columns(rows)

    def open_bookmark(self, bookmark):
        try:
            webbrowser.open(self.config.get_bookmark_url(bookmark), new=2)
        except ConfigParser.NoOptionError:
            self.error('No bookmark named "{0}"'.format(bookmark))

    def show(self, bookmark):
        self.config.check_bookmark_exists(bookmark)
        self.info('Bookmark "{0}" : "{1}"'.format(bookmark, self.config.get_bookmark_url(bookmark)))

    def list(self):
        self.list_bookmarks()

    def change(self, bookmark, url):
        self.config.check_bookmark_exists(bookmark)
        self.config.save_bookmark(bookmark, url)
        self.success('"{0}" changed to "{1}"'.format(bookmark, url))

    def remove(self, bookmark):
        self.config.check_bookmark_exists(bookmark)
        self.config.delete_bookmark(bookmark)
        self.success('Bookmark "{0}" deleted'.format(bookmark))

@click.group()
@click.pass_context
@click.option('--config_file', type=click.File('w+'), default=CONFIG_FILE)
def cli(ctx, config_file):
    ctx.obj = {'bkm' : BKM(Config(CONFIG_FILE, config_file))}

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
#!/usr/bin/env python
import click, webbrowser, ConfigParser
from os.path import expanduser

CONFIG_DIR = '{0}/.bookmarks'.format(expanduser("~"))
CONFIG_FILE = '{0}/bookmarks'.format(CONFIG_DIR)

@click.group()
@click.pass_context
@click.option('--config_file', type=click.File('wb'), default=CONFIG_FILE)
def cli(ctx, config_file):
    ctx.obj['config'] = ConfigParser.ConfigParser()
    ctx.obj['config'].read(CONFIG_FILE)
    ctx.obj['config_file'] = config_file

@cli.command()
@click.pass_context
@click.argument('bookmark', nargs=1)
def open(ctx, bookmark):
    __check_bookmark_exists(ctx, bookmark)
    __open_bookmark(ctx, bookmark)

@cli.command()
@click.pass_context
@click.argument('bookmark', nargs=1)
@click.argument('url', nargs=1)
def add(ctx, bookmark, url):
    __check_bookmark_doesnt_exist(ctx, bookmark)
    __save_bookmark(ctx, bookmark, url)
    __success('"{0}" added for "{1}"'.format(bookmark, url))

@cli.command()
@click.pass_context
@click.argument('bookmark', nargs=1)
def show(ctx, bookmark):
    __check_bookmark_exists(ctx, bookmark)
    __show_bookmark(ctx, bookmark)

@cli.command()
@click.pass_context
def list(ctx):
    __list_bookmarks(ctx)


@cli.command()
@click.pass_context
@click.argument('bookmark', nargs=1)
@click.argument('url', nargs=1)
def change(ctx, bookmark, url):
    __check_bookmark_exists(ctx, bookmark)
    __save_bookmark(ctx, bookmark, url)
    __success('"{0}" changed to "{1}"'.format(bookmark, url))

@cli.command()
@click.pass_context
@click.argument('bookmark', nargs=1)
def remove(ctx, bookmark):
    __check_bookmark_exists(ctx, bookmark)
    __delete_bookmark(ctx, bookmark)
    __success('Bookmark "{0}" deleted')


def __save_bookmark(ctx, bookmark, url):
    ctx.obj['config'].set('bookmarks', bookmark, url)
    __write_config_file(ctx)

def __delete_bookmark(ctx, bookmark):
    ctx.obj['config'].remove_option('bookmarks', bookmark)
    __write_config_file(ctx)

def __write_config_file(ctx):
    ctx.obj['config'].write(ctx.obj['config_file'])

def __check_bookmark_exists(ctx, bookmark):
    if not ctx.obj['config'].has_option('bookmarks', bookmark):
        __error('Bookmark "{0}" doesn\'t exist'.format(bookmark))

def __check_bookmark_doesnt_exist(ctx, bookmark):
    if ctx.obj['config'].has_option('bookmarks', bookmark):
        __error('Bookmark "{0}" exist'.format(bookmark))

def __show_bookmark(ctx, bookmark):
    url = __get_bookmark_url(ctx, bookmark)
    __info('Bookmark "{0}" : "{1}"'.format(bookmark, url))

def __list_bookmarks(ctx):
    rows = []
    for bookmark in ctx.obj['config'].options('bookmarks'):
        rows.append([bookmark, ctx.obj['config'].get('bookmarks', bookmark)])

    widths = [max(map(len, col)) for col in zip(*rows)]
    for row in rows:
        __info(" : ".join((val.ljust(width) for val, width in zip(row, widths))))
    __info('')
    __info('{} bookmarks'.format(len(rows)))

def __get_bookmark_url(ctx, bookmark):
    return ctx.obj['config'].get('bookmarks', bookmark)

def __open_bookmark(ctx, bookmark):
    try:
        url = __get_bookmark_url(ctx, bookmark)
        webbrowser.open(url, new=2)
    except ConfigParser.NoOptionError:
        __error('No bookmark named "{0}"'.format(bookmark))

def __error(msg):
    click.echo(click.style(msg, bg='red', fg='white'))
    exit()

def __success(msg):
    click.echo(click.style(msg, fg='green'))

def __info(msg):
    click.echo(click.style(msg, fg='yellow'))

if __name__ == '__main__':
    cli(obj={})
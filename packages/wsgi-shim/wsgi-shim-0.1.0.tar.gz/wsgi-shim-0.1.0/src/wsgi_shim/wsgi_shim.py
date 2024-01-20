# wsgi_shim.py
"""
Phusion Passenger WSGI shim

Ultimately, the only thing this really needs to do is to define
a callable called "application" roughly like this:

    from WSGI_MODULE import WSGI_APP as application

However, because we assume users do not have direct access to the server logs
to debug their code, this bit of code (and the accompanying documentation)
helps catch many initial setup/configuration errors without users needing
to ask sysadmins to find snippets in the server error logs.

This is not WSGI middleware; it does not capture exceptions thrown by the
application.  It is up to the developer to log messages to an accessible
file to aid in further debugging and to gather site statistics.
(This could be a future enhancement for this project, though.)
"""
import argparse
import datetime
import functools
import grp
import importlib.resources
import importlib.util
import os
import pwd
import re
import sys
import textwrap
import tomllib
from contextlib import contextmanager
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from types import ModuleType
from typing import cast
from typing import NoReturn
from typing import Protocol
from typing import Self
from wsgiref.types import StartResponse
from wsgiref.types import WSGIApplication
from wsgiref.types import WSGIEnvironment


class WSGIConfigException(Exception):
    pass


def is_safe_gid(file_gid: int) -> bool:
    """Returns False (indicating an unsafe file_gid) when the file_gid
    matches the user's default group and that default group's name is
    not that same string as the username."""
    passwd_entry = pwd.getpwuid(os.getuid())
    if passwd_entry.pw_gid == file_gid:
        if passwd_entry.pw_name != grp.getgrgid(passwd_entry.pw_gid).gr_name:
            return False
    return True


def is_path_world_readable(path: Path) -> bool:
    if not path.exists():
        raise WSGIConfigException(f"does not exist: '{path}'")
    p = Path('/')
    for part in path.parts:
        p = p / part
        mode = 0o001 if p.is_dir() else 0o004
        if (p.stat().st_mode & mode) != mode:
            return False
    return True


def check_path_is_world_readable(path: Path) -> None:
    if not is_path_world_readable(path):
        raise WSGIConfigException(f"not world readable: '{path}'")


def check_path_is_not_world_readable(path: Path) -> None:
    if is_path_world_readable(path):
        raise WSGIConfigException(f"is world readable: '{path}'")


def is_path_world_or_unsafe_gid_writable(path: Path) -> bool:
    if not path.exists():
        raise WSGIConfigException(f"does not exist: '{path}'")
    p = Path('/')
    for part in path.parts:
        p = p / part
        p_stat = p.stat()
        mode = 0o003 if p.is_dir() else 0o002
        if (p_stat.st_mode & mode) == mode:
            return True
        if not is_safe_gid(p_stat.st_gid):
            mode = 0o030 if p.is_dir() else 0o020
            if (p.stat().st_mode & mode) == mode:
                return True
    return False


def check_path_is_not_world_or_unsafe_gid_writable(path: Path) -> None:
    if is_path_world_or_unsafe_gid_writable(path):
        raise WSGIConfigException(f"is world (or unsafe group) writable: '{path}'")


def check_venv_path(passenger_python: Path, passenger_app_root: Path):
    if sys.prefix == sys.base_prefix:
        raise WSGIConfigException('Must be run from inside a virtual environment')
    passenger_venv_path = passenger_python.parent.parent
    running_venv_path = Path(sys.prefix)
    if running_venv_path != passenger_venv_path:
        raise WSGIConfigException(
            'Running virtual environment does not match '
            'passenger_python in config.toml.',
        )
    if running_venv_path.is_relative_to(passenger_app_root):
        raise WSGIConfigException(
            'Virtual environment cannot be '
            'inside passenger_app_root',
        )
    venv_stat = os.stat(running_venv_path)
    venv_mask = 0o002 if is_safe_gid(venv_stat.st_gid) else 0o022
    if (venv_stat.st_mode & venv_mask) != 0:
        raise WSGIConfigException(
            f'virtual environment at {running_venv_path} '
            f'is not adequately write protected.',
        )


@dataclass
class Config:
    passenger_user: str = ''
    passenger_group: str = ''
    passenger_python: str = ''
    wsgi_chdir: str = ''
    wsgi_app: str = ''
    environment: dict[str, tuple[str, bool]] = field(default_factory=dict)
    maintenance_mode_path: Path = Path('/dev/null/nonexistent')
    passenger_python_path: Path = Path('/dev/null/nonexistent')

    @classmethod
    def from_toml_dict(cls, data, passenger_app_root: Path) -> Self:
        retval = cls()
        for section, required in [
            ('passenger', True),
            ('wsgi', False),
            ('secret_files', False),
            ('environment', False),
        ]:
            if not isinstance(data.get(section, {}), dict):
                raise WSGIConfigException(f'"{section}" is not a section')
            if required and section not in data:
                raise WSGIConfigException(f'Missing required [{section}]')
        for section, key, attrib in [
            ('passenger', 'passenger_user', 'passenger_user'),
            ('passenger', 'passenger_group', 'passenger_group'),
            ('passenger', 'passenger_python', 'passenger_python'),
            ('wsgi', 'chdir', 'wsgi_chdir'),
            ('wsgi', 'app', 'wsgi_app'),
        ]:
            value = data.get(section, {}).get(key, '')
            if not isinstance(value, str):
                raise WSGIConfigException(f'{section}.{key} not a string')
            setattr(retval, attrib, value)
        retval.maintenance_mode_path = passenger_app_root / 'tmp' / 'maint.txt'
        retval.passenger_python_path = Path(retval.passenger_python)
        environment_sections = [('secret_files', True), ('environment', False)]
        for section, is_secret_file in environment_sections:
            for key, value in data.get(section, {}).items():
                if re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]*', key) is None:
                    raise WSGIConfigException(f'invalid key "{key}" in [{section}]')
                if not isinstance(value, str):
                    raise WSGIConfigException(f'{section}.{key} not a string')
                if key in retval.environment:
                    raise WSGIConfigException(
                        f'key "{key}" duplicated across sections: '
                        f'{", ".join(name for name, _ in environment_sections)}',
                    )
                retval.environment[key] = (value, is_secret_file)
        return retval

    def check_user_group(self):
        running_user = pwd.getpwuid(os.getuid()).pw_name
        running_group = grp.getgrgid(os.getgid()).gr_name
        running = (running_user, running_group)
        configured = (self.passenger_user, self.passenger_group)
        if running != configured:
            raise WSGIConfigException(
                f'running user.group {running} does not '
                f'match config.toml settings {configured}.',
            )

    def check_secret_files(self):
        # Check that the secret_files exist and have appropriate permissions.
        # Note: Like ssh, we refuse to run if a secrets file is too widely
        # accessible.
        for key, (filename, is_secret_file) in self.environment.items():
            if is_secret_file:
                path = Path(filename)
                if not path.is_absolute():
                    raise WSGIConfigException(
                        f'secret_files.{key} '
                        f'is not an absolute path',
                    )
                if not os.access(path, os.R_OK):
                    raise WSGIConfigException(
                        f'secret_files.{key} '
                        f'is missing or not readable',
                    )
                config_stat = os.stat(path)
                config_mask = 0o007 if is_safe_gid(config_stat.st_gid) else 0o077
                if (config_stat.st_mode & config_mask) != 0:
                    raise WSGIConfigException(
                        f'secret_files.{key} '
                        f'is not adequately protected.',
                    )

    def update_os_environment(self) -> None:
        for key, (value, _) in self.environment.items():
            if key in os.environ:
                raise WSGIConfigException(f'os.environ already has key "{key}"')
            os.environ[key] = value

    def in_maintenance_mode(self) -> bool:
        return self.maintenance_mode_path.exists()


def load_config(file: Path):
    try:
        with open(file, "rb") as f:
            data = tomllib.load(f)  # assumes utf-8 encoding
    except FileNotFoundError as e:
        raise WSGIConfigException(f'Config file not found: {str(e)}')
    except PermissionError as e:
        raise WSGIConfigException(f'Config file error: {str(e)}')
    except tomllib.TOMLDecodeError as e:
        raise WSGIConfigException(f'Config file syntax error: {str(e)}')
    return data


def import_module_from_file_location(
        module_path: Path,
) -> ModuleType:
    # See: https://docs.python.org/3.11/library/importlib.html
    #      #importing-a-source-file-directly
    module_name = module_path.stem
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None:
        raise WSGIConfigException(
            f'Cannot load {module_name} from {module_path}: '
            f'spec_from_file_location returned None.',
        )
    importlib.invalidate_caches()
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    assert spec.loader is not None  # keep mypy happy
    spec.loader.exec_module(module)
    return module


def application503(
        _environ: WSGIEnvironment,
        start_response: StartResponse,
        html: str,
) -> list[bytes]:
    html_as_bytes = html.encode('utf-8')
    start_response(
        '503 Service Unavailable',
        [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(html_as_bytes))),
            ('Retry-After', '60'),
        ],
    )
    return [html_as_bytes]


html_template = textwrap.dedent('''\
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="utf-8"/>
    <title>{title} (503)</title>
    </head>
    <body>
    <h1>{title}</h1>
    <p>{reason}</p>
    {details}</body>
    </html>
''')


def get_app(passenger_app_root: Path | None = None) -> WSGIApplication:
    """
    Returns the appropriate application callable to use.
    """
    try:
        if passenger_app_root is None:  # pragma: no cover
            passenger_app_root = Path.cwd()
        config_file = passenger_app_root / 'config.toml'
        toml_dict = load_config(config_file)
        config = Config.from_toml_dict(toml_dict, passenger_app_root)
        check_venv_path(config.passenger_python_path, passenger_app_root)
        config.check_user_group()
        if config.in_maintenance_mode():
            return cast(
                WSGIApplication,
                functools.partial(
                    application503,
                    html=html_template.format(
                        title='Maintenance',
                        reason='The developer of this site has put it into '
                               'maintenance mode.  Please try again later.',
                        details=f'<p>{datetime.datetime.now()}</p>',
                    ),
                ),
            )
        config.check_secret_files()
        config.update_os_environment()
        # See: https://docs.python.org/3.11/library/importlib.html
        #      #importing-programmatically
        chdir_path = Path.cwd() / Path(config.wsgi_chdir)
        if not chdir_path.is_dir():
            raise WSGIConfigException(
                f'[wsgi].chdir "{chdir_path}" must be a directory',
            )
        s = config.wsgi_app.rsplit('.', maxsplit=1)
        if len(s) != 2:
            raise WSGIConfigException(
                '[wsgi].app must of the form module.app_name',
            )
        submodule_name, app_name = s
        # Note: doing a chdir is generally frowned upon but Django needs it
        # (otherwise, we'd just add chdir_path to sys.path).
        os.chdir(chdir_path)
        for d in (str(chdir_path), ''):
            while d in sys.path:
                sys.path.remove(d)
        sys.path.insert(0, str(chdir_path))
        try:
            # FIXME: verify os.environ and cwd
            module = importlib.import_module(submodule_name)
            app = getattr(module, app_name)
            return app
        except (ModuleNotFoundError, PermissionError, AttributeError) as exc_info:
            raise WSGIConfigException(
                f'Cannot import {config.wsgi_app} from {config.wsgi_chdir}: '
                f'{str(exc_info)}',
            )
    except WSGIConfigException as exc_info:
        # Configuration Error Mode
        return cast(
            WSGIApplication,
            functools.partial(
                application503,
                html=html_template.format(
                    title='Error Page',
                    reason='This site has experienced a configuration '
                           'error or exception.',
                    details=textwrap.dedent(f'''\
                        <pre>
                        passenger_app_root: {passenger_app_root}
                               process uid: {pwd.getpwuid(os.getuid()).pw_name}
                               process gid: {grp.getgrgid(os.getgid()).gr_name}
                                 timestamp: {datetime.datetime.now()}

                        Exception Details
                        {{}}
                        </pre>
                    ''').format(str(exc_info)),
                ),
            ),
        )


class HasExitError(Protocol):
    def exit(self, status=0, message=None) -> NoReturn:
        ...  # pragma no cover

    def error(self, message) -> NoReturn:
        ...  # pragma no cover


@dataclass
class Args:
    command: str
    sitedir: str
    approot: str
    docroot: str
    verbose: bool
    puppet: bool
    site_path: Path
    approot_path: Path
    docroot_path: Path
    parser: HasExitError


def cli_parse(argv=None) -> Args:
    if argv is None:
        argv = sys.argv
    args = argv[1:]
    parser = argparse.ArgumentParser(
        description="Create/check directory structure for Passenger Python web app",
    )
    parser.add_argument('command', choices=['install', 'check'])
    parser.add_argument(
        '-a', '--approot', default='www-approot',
        help='AppRoot relative to sitedir',
    )
    parser.add_argument(
        '-d', '--docroot', default='www-docroot',
        help='DocRoot relative to sitedir',
    )
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument(
        '-p', '--puppet', action='store_true',
        help='output puppet configuration',
    )
    parser.add_argument(
        'sitedir',
        help='absolute path of the site directory',
    )
    args = parser.parse_args(args=args)
    site_path = Path(args.sitedir)
    if not site_path.is_absolute():
        parser.error('sitedir must start with a "/".')
    approot_rel_path = Path(args.approot)
    docroot_rel_path = Path(args.docroot)
    for rel_path, name in [(approot_rel_path, 'AppRoot'), (docroot_rel_path, 'DocRoot')]:
        if rel_path.is_absolute():
            parser.error(f'{name} must be relative (no leading "/").')
        if len(rel_path.parts) != 1:
            parser.error(f'{name} can only be a single part (no internal "/").')
        if rel_path.parts[0] in ('.', '..'):
            parser.error(f'{name} cannot be "." or ".."')
    args.site_path = site_path
    args.approot_path = site_path / approot_rel_path
    args.docroot_path = site_path / docroot_rel_path
    args.parser = parser
    return cast(Args, args)


@contextmanager
def temp_umask(mask: int):
    old_mask = os.umask(mask)
    try:
        yield
    finally:
        os.umask(old_mask)


def get_umask() -> int:
    mask = os.umask(0o777)  # to get the umask, we must change it
    os.umask(mask)  # change it right back
    return mask


def cleanup(items: list[Path]) -> None:
    for item in reversed(items):
        if item.is_dir():
            try:
                item.rmdir()
            except OSError as exc_info:
                if exc_info.strerror != 'Directory not empty':
                    raise
        else:
            item.unlink(missing_ok=True)


def create_new_directory(path: Path, other_readable: bool = False) -> None:
    # create with no group/other permissions
    with temp_umask(0o077):
        path.mkdir()
    # now that the directory exists, check group
    path_stat = os.stat(path)
    current_mode = path_stat.st_mode
    new_mode = current_mode
    if other_readable:
        new_mode |= 0o005  # o=rx
    if is_safe_gid(path_stat.st_gid):
        # group is safe, update group bits to what they would have been based on umask
        new_mode |= 0o070 & ~get_umask()
    if new_mode != current_mode:
        path.chmod(new_mode)


def create_new_file(path: Path, content: str = '', other_readable: bool = False) -> None:
    # create with no group/other permissions
    with temp_umask(0o077):
        with open(path, mode='x') as f:
            f.write(content)
    # now that the directory exists, check group
    path_stat = os.stat(path)
    current_mode = path_stat.st_mode
    new_mode = current_mode
    if other_readable:
        new_mode |= 0o004  # o=r
    if is_safe_gid(path_stat.st_gid):
        # group is safe, update group bits to what they would have been based on umask
        new_mode |= 0o060 & ~get_umask()
    if new_mode != current_mode:
        path.chmod(new_mode)


def puppet_block(args: Args) -> str:
    return textwrap.dedent(f"""
        Requesting these attributes:
        passenger_enabled     => true,
        passenger_user        => '{args.approot_path.owner()}',
        passenger_group       => '{args.approot_path.group()}',
        passenger_app_root    => '{args.approot_path}',
        passenger_restart_dir => '{args.approot_path / 'tmp'}',
        passenger_app_type    => 'wsgi',
        passenger_python      => '{Path(sys.prefix) / 'bin' / 'python'}';
        """)


def cli_install(args: Args) -> None:
    # Keep track of what we created to know what to clean-up in case of error
    created_paths: list[Path] = list()
    # Create the directories
    restart_dir_path = args.approot_path / 'tmp'
    for dir_path in [args.docroot_path, args.approot_path, restart_dir_path]:
        try:
            create_new_directory(dir_path, other_readable=True)
        except FileExistsError:
            cleanup(created_paths)
            raise WSGIConfigException(
                f"Error: will not overwrite existing: "
                f"'{dir_path}'",
            )
        created_paths.append(dir_path)
    # File paths and contents
    passenger_wsgi_py_path = args.approot_path / 'passenger_wsgi.py'
    passenger_wsgi_py = textwrap.dedent('''
        # Created with wsgi_shim
        import wsgi_shim

        application = wsgi_shim.get_app()
    ''')[1:]
    config_toml_path = args.approot_path / 'config.toml'
    with importlib.resources.files('wsgi_shim.templates').joinpath(
            'config.toml',
    ).open('r') as f:
        config_template = f.read()
    config_toml = config_template.format(
        web_doc_root=args.docroot_path,
        user=args.approot_path.owner(),
        group=args.approot_path.group(),
        passenger_app_root=args.approot_path,
        passenger_restart_dir=restart_dir_path,
        passenger_python=Path(sys.prefix) / 'bin' / 'python',
    )
    restart_txt_path = restart_dir_path / 'restart.txt'
    maint_txt_path = restart_dir_path / 'maint.txt'
    # create the files
    for path, content in [
        (passenger_wsgi_py_path, passenger_wsgi_py),
        (config_toml_path, config_toml),
        (restart_txt_path, ''),
        (maint_txt_path, ''),
    ]:
        try:
            create_new_file(
                path=path,
                content=content,
                other_readable=False,
            )
        except FileExistsError:
            cleanup(created_paths)
            raise WSGIConfigException(
                f"Error: will not overwrite existing: "
                f"'{path}'",
            )
        created_paths.append(path)
    if args.verbose:
        print('Success.  Created the following:')
        for path in created_paths:
            print(f'    {path}')
    if args.puppet:
        print(puppet_block(args))


def cli_check(args: Args) -> None:
    passenger_wsgi_py_path = args.approot_path / 'passenger_wsgi.py'
    check_path_is_not_world_readable(passenger_wsgi_py_path)
    if not passenger_wsgi_py_path.is_file():
        raise WSGIConfigException(f"not a file: '{passenger_wsgi_py_path}'")
    contents = passenger_wsgi_py_path.read_text()
    try:
        compile(contents, str(passenger_wsgi_py_path), mode='exec')
    except (SyntaxError, ValueError) as exc_info:
        raise WSGIConfigException(f"Cannot parse: '{passenger_wsgi_py_path}': {exc_info}")
    except IsADirectoryError:
        raise WSGIConfigException(f"not a file: '{passenger_wsgi_py_path}'")
    restart_dir_path = args.approot_path / 'tmp'
    check_path_is_world_readable(restart_dir_path)
    if not restart_dir_path.is_dir():
        raise WSGIConfigException(f"not a directory: '{restart_dir_path}'")
    restart_txt_path = restart_dir_path / 'restart.txt'
    if restart_txt_path.exists():
        check_path_is_not_world_readable(restart_txt_path)
        if not restart_txt_path.is_file():
            raise WSGIConfigException(f"not a file: '{restart_txt_path}'")
    maint_txt_path = restart_dir_path / 'maint.txt'
    if maint_txt_path.exists():
        check_path_is_not_world_readable(maint_txt_path)
        if not maint_txt_path.is_file():
            raise WSGIConfigException(f"not a file: '{maint_txt_path}'")
    config_toml_path = args.approot_path / 'config.toml'
    check_path_is_not_world_readable(config_toml_path)
    toml_dict = load_config(config_toml_path)
    config = Config.from_toml_dict(toml_dict, args.approot_path)
    check_venv_path(config.passenger_python_path, args.approot_path)
    config.check_secret_files()
    if args.verbose:
        print('Check passed')
    if args.puppet:
        print(puppet_block(args))


def cli_backend(argv=None) -> None:
    args = cli_parse(argv)
    check_path_is_world_readable(args.site_path)
    if not args.site_path.is_dir():
        raise WSGIConfigException(f'not a directory: {args.site_path}')
    running_python_path = Path(sys.prefix) / 'bin' / 'python'
    check_venv_path(running_python_path, args.approot_path)
    if args.command == 'install':
        cli_install(args)
    elif args.command == 'check':
        cli_check(args)


def cli():  # pragma no cover
    try:
        cli_backend()
        return_code = 0
    except WSGIConfigException as exc_info:
        print(f'{str(exc_info)}', file=sys.stderr)
        return_code = 1
    raise SystemExit(return_code)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

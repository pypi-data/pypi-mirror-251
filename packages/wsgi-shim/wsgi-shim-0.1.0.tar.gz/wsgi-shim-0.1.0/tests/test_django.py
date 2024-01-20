import importlib.resources
import re
import subprocess
import sys
import textwrap
from pathlib import Path

from wsgi_shim.wsgi_shim import cli_backend

from tests.conftest import gen_config_toml_contents
from tests.conftest import run_passenger_wsgi_py


# @pytest.mark.skip
def test_install_passenger_wsgi_py_django(tmp_path_world_readable, passenger_block):
    site_dir_path = tmp_path_world_readable
    cli_backend(argv=['wsgi-shim', 'install', str(site_dir_path)])
    passenger_app_root_path = site_dir_path / 'www-approot'

    # The command 'django-admin startproject mysite' is run in a subprocess
    # (rather than via django.core.management.execute_from_command_line) so
    # as not to configure settings before they are set up.
    subprocess.run(
        [Path(sys.executable).parent / 'django-admin', 'startproject', 'mysite'],
        cwd=site_dir_path,
    )
    mysite_path = site_dir_path / 'mysite'
    assert mysite_path.exists()
    subprocess.run(
        [sys.executable, 'manage.py', 'startapp', 'user'],
        cwd=mysite_path,
    )
    mysite_user_path = mysite_path / 'user'
    assert mysite_user_path.exists()
    models_py_path = mysite_user_path / 'models.py'
    models_py_path.write_text(
        textwrap.dedent("""
        from django.contrib.auth.models import AbstractUser

        class User(AbstractUser):
            pass
    """)[1:],
    )
    admin_py_path = mysite_user_path / 'admin.py'
    admin_py_path.write_text(
        textwrap.dedent("""
        from django.contrib import admin
        from django.contrib.auth.admin import UserAdmin
        from .models import User

        admin.site.register(User, UserAdmin)
    """)[1:],
    )
    settings_py_dir_path = mysite_path / 'mysite'
    settings_py_file_path = settings_py_dir_path / 'settings.py'

    with importlib.resources.files('tests').joinpath('django_local_settings.py').open('r') as f:
        local_settings_py_contents = f.read()
    local_settings_py_file_path = settings_py_dir_path / 'local_settings.py'
    local_settings_py_file_path.write_text(local_settings_py_contents)

    with open(settings_py_file_path, mode='a') as f:
        f.write(
            textwrap.dedent("""
        from mysite import local_settings
        SECRET_KEY = local_settings.update_secret_key(SECRET_KEY)
        DEBUG = local_settings.update_debug(DEBUG)
        local_settings.update_allowed_hosts(ALLOWED_HOSTS)
        local_settings.update_installed_apps(INSTALLED_APPS)
        local_settings.update_middleware(MIDDLEWARE)
        local_settings.update_databases(DATABASES)
        LOGGING = local_settings.get_logging()
        STATIC_ROOT = local_settings.get_static_root(BASE_DIR)
        AUTH_USER_MODEL = local_settings.get_auth_user_model()
        """),
        )
    log_dir_path = site_dir_path / 'log'
    log_dir_path.mkdir()
    log_file_path = log_dir_path / 'logfile'
    log_file_path.touch()
    secrets_dir_path = site_dir_path / 'secrets'
    secrets_dir_path.mkdir()
    credentials_file_path = secrets_dir_path / 'credentials.env'
    credentials_file_path.write_text(
        textwrap.dedent("""
    DJANGO_SECRET_KEY=__________placeholder_django_secret_key___________
    DB_NAME=placeholder_db_name
    DB_USER=placeholder_db_user
    DB_PASS=placeholder_db_pass
    DB_HOST=placeholder_db_host
    DB_PORT=3306
    """),
    )
    config_toml_path = passenger_app_root_path / 'config.toml'
    config_toml_contents = gen_config_toml_contents(
        {
            'passenger': passenger_block,
            'wsgi': {
                'chdir': str(mysite_path),
                'app': 'mysite.wsgi.application',
            },
            'secret_files': {
                'MYSITESECRETS': str(credentials_file_path),
            },
            'environment': {
                'MYSITEURL': 'placeholder',
                'LOG_FILENAME': str(log_file_path),
                'DJANGO_SETTINGS_MODULE': 'mysite.settings',
            },
        },
    )
    config_toml_path.write_text(config_toml_contents)
    restart_dir_path = passenger_app_root_path / 'tmp'
    maint_txt_path = restart_dir_path / 'maint.txt'
    maint_txt_path.unlink()
    html, status, headers, err = run_passenger_wsgi_py(passenger_app_root_path)
    log = log_file_path.read_text()
    assert err == []
    assert re.search(r'The install worked successfully', html)
    assert status == '200 OK'
    assert len(headers) == 6
    assert log == ''

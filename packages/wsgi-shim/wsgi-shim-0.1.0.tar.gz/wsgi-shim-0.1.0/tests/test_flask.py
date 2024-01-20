import re

from wsgi_shim.wsgi_shim import cli_backend

from tests.conftest import run_passenger_wsgi_py


def test_install_passenger_wsgi_py_normal_flask(
        tmp_path_world_readable,
        passenger_block,
):
    site_dir_path = tmp_path_world_readable
    cli_backend(
        [
            'wsgi-shim',
            'install',
            str(site_dir_path),
        ],
    )
    log_file_path = site_dir_path / 'logfile'
    passenger_app_root_path = site_dir_path / 'www-approot'
    config_toml_path = passenger_app_root_path / 'config.toml'
    config_toml_path.write_text(f"""
    [passenger]
    {passenger_block}
    [wsgi]
    app = "tests.flask_example.app"
    [environment]
    LOG_FILENAME = "{log_file_path}"
    """)
    restart_dir_path = passenger_app_root_path / 'tmp'
    maint_txt_path = restart_dir_path / 'maint.txt'
    maint_txt_path.unlink()
    html, status, headers, err = run_passenger_wsgi_py(passenger_app_root_path)
    assert err == []
    assert re.search(r'Hello, World', html)
    assert status == '200 OK'
    assert len(headers) == 2
    log = log_file_path.read_text()
    assert "INFO tests.flask_example MainThread : Request: /" in log

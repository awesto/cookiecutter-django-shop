from __future__ import unicode_literals

import os
import click
from cookiecutter.config import get_user_config
from cookiecutter.log import configure_logger
from cookiecutter.main import cookiecutter
from cookiecutter import prompt
from cookiecutter.replay import dump, load


@click.command()
@click.option(
    '--no-input', is_flag=True,
    help='Do not prompt for parameters and only use cookiecutter.json file content',
)
@click.option(
    '-v', '--verbose', is_flag=True,
    help='Print debug information', default=False
)
@click.option(
    '--replay', is_flag=True,
    help='Do not prompt for parameters and only use information entered previously',
)
@click.option(
    '-f', '--overwrite-if-exists', is_flag=True,
    help='Overwrite the contents of the output directory if it already exists'
)
@click.option(
    '-o', '--output-dir', default='.', type=click.Path(),
    help='Where to output the generated project dir into'
)
@click.option(
    '--config-file', type=click.Path(), default=None,
    help='User configuration file'
)
@click.option(
    '--default-config', is_flag=True,
    help='Do not load a config file. Use the defaults instead'
)
def main(no_input, verbose, replay, overwrite_if_exists, output_dir, config_file, default_config):
    template_name = os.path.basename(os.path.dirname(__file__))
    if replay:
        context = None
    else:
        config_dict = get_user_config(
            config_file=config_file,
            default_config=default_config,
        )
        context = load(config_dict['replay_dir'], template_name)['cookiecutter']
    configure_logger(stream_level='DEBUG' if verbose else 'INFO')
    cookiecutter(template_name,
                 no_input=no_input,
                 extra_context=context,
                 replay=replay,
                 overwrite_if_exists=overwrite_if_exists,
                 output_dir=output_dir,
                 config_file=config_file,
                 default_config=default_config)


if __name__ == '__main__':
    main()

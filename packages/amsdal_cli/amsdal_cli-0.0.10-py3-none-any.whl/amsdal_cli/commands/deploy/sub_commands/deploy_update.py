from pathlib import Path

from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager

from amsdal_cli.commands.deploy.app import sub_app


@sub_app.command(name='update')
def update_command(deploy_id: str) -> None:
    """
    Update the app status.
    """
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()
    manager.update_deployment_status(deploy_id)

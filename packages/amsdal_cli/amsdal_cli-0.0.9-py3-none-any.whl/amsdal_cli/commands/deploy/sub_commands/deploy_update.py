from amsdal.manager import AmsdalManager

from amsdal_cli.commands.deploy.app import sub_app


@sub_app.command(name='update')
def update_command(deploy_id: str) -> None:
    """
    Update the app status.
    """
    manager = AmsdalManager()
    manager.authenticate()
    manager.setup()
    manager.update_deployment_status(deploy_id)

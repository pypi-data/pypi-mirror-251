from amsdal.manager import AmsdalManager

from amsdal_cli.commands.deploy.app import sub_app


@sub_app.command(name='destroy')
def destroy_command(deploy_id: str) -> None:
    """
    Destroy the app on the server.
    """
    manager = AmsdalManager()
    manager.authenticate()
    manager.setup()
    manager.destroy_deployment(deploy_id)

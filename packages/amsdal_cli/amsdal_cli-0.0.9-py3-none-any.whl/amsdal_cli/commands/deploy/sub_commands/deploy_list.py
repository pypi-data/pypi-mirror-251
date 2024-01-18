from amsdal.manager import AmsdalManager

from amsdal_cli.commands.deploy.app import sub_app


@sub_app.command(name='list')
def list_command() -> None:
    """
    List the apps on the server.
    """
    manager = AmsdalManager()
    manager.authenticate()
    manager.setup()
    manager.list_deployments()

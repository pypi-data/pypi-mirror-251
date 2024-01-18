from amsdal.manager import AmsdalManager

from amsdal_cli.commands.deploy.app import sub_app


@sub_app.callback(name='deploy', invoke_without_command=True)
def deploy_command() -> None:
    """
    Deploy the app to the server.
    """
    manager = AmsdalManager()
    manager.authenticate()
    manager.setup()
    manager.deploy()

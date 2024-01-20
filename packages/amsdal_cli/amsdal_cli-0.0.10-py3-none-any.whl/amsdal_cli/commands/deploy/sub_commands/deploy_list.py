from pathlib import Path

from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print
from rich.table import Table

from amsdal_cli.commands.deploy.app import sub_app


@sub_app.command(name='list')
def list_command() -> None:
    """
    List the apps on the server.
    """
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()
    deployments = manager.list_deployments()

    if deployments:
        data_table = Table()

        data_table.add_column('Deploy ID', justify='center')
        data_table.add_column('Status')
        for deployment in deployments:
            data_table.add_row(
                deployment.deploy_id,
                deployment.status,
            )

        print(data_table)

    else:
        print('No deployments found.')

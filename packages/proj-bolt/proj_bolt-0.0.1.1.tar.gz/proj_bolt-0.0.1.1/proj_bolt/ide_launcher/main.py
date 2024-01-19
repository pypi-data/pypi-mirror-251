from .launcher import *

ide_dict = {
    "pycharm": PyCharmLauncher,
    "vscode": VSCodeLauncher,
    "webstorm": WebStormLauncher,
    "idea": IntelliJIDEALauncher,
}


def launch_ide(ide: str, project_path: str):
    """
    Launch the specified IDE with the specified project path

    :param ide: (str) the name of the IDE to be launched
    :param project_path: (str) the path of the project to be opened
    :return: (None)
    """
    ide = ide.lower()
    if ide not in ide_dict:
        raise ValueError(f"IDE {ide} is not supported. Supported IDEs are {list(ide_dict.keys())}")

    ide_launcher = ide_dict[ide]()
    ide_launcher.launch(project_path=project_path)


__all__ = ["launch_ide"]

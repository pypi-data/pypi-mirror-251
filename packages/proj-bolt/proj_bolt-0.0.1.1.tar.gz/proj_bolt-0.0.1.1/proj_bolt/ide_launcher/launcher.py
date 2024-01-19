import os
import abc
import pathlib
import traceback
import subprocess
from typing import Union


class BaseIDELauncher(abc.ABC):
    """
    Base class for IDE launcher

    IDELauncher is designed to help users launch their IDEs from command line.

    User interface:

    `launch(project_path: Union[str, pathlib.Path])`: launch the IDE with the specified project path
    """
    @property
    @abc.abstractmethod
    def ide_name(self) -> str:
        """user-friendly name of the IDE"""
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def ide_home_env_var_name(self) -> str:
        """the environment variable name of the IDE home directory, this should be a existing os environment variable"""
        raise NotImplementedError()

    def launch(self, project_path: Union[str, pathlib.Path]):
        """
        Launch the IDE with the specified project path

        :param project_path: (Union[str, pathlib.Path]) the path of the project to be opened
        :return: (None)
        """
        project_path = pathlib.Path(project_path)

        # Check if project directory already exists
        if not project_path.exists():
            raise FileNotFoundError(f"Project directory {project_path} does not exist.")

        # Check whether the environment variable is set
        if self.ide_home_env_var_name is not None:
            if self.ide_home_env_var_name not in os.environ:
                raise EnvironmentError(
                    f"{self.ide_name} home environment variable {self.ide_home_env_var_name} is not set. Please set it first. It should be the path to the home directory of {self.ide_name}.")

        # Launch the IDE in a new process
        ide_home_dir = pathlib.Path(os.environ.get(self.ide_home_env_var_name))
        try:
            ide_exec_path = self.get_ide_exec_path(ide_home_dir, platform=os.name)
            subprocess.Popen([ide_exec_path, project_path.absolute().as_posix()], start_new_session=True)
        except Exception as e:
            raise RuntimeError(f"Failed to launch {self.ide_name}: {e}.\nTraceback: {traceback.format_exc()}.\nPlease submit an issue on GitHub: Thanks!") from e

    @abc.abstractmethod
    def get_ide_exec_path(self, ide_home_dir: pathlib.Path, platform: str) -> pathlib.Path:
        """find the executable path of the IDE, given the ide home directory and the platform"""
        raise NotImplementedError()


class PyCharmLauncher(BaseIDELauncher):
    @property
    def ide_name(self) -> str:
        return "PyCharm"

    @property
    def ide_home_env_var_name(self) -> str:
        return "PYCHARM_HOME"

    def get_ide_exec_path(self, ide_home_dir: pathlib.Path, platform: str) -> pathlib.Path:
        if platform == "nt":
            return ide_home_dir / "bin" / "pycharm64.exe"
        else:
            return ide_home_dir / "bin" / "pycharm.sh"


class VSCodeLauncher(BaseIDELauncher):
    @property
    def ide_name(self) -> str:
        return "VSCode"

    @property
    def ide_home_env_var_name(self) -> str:
        return "VSCODE_HOME"

    def get_ide_exec_path(self, ide_home_dir: pathlib.Path, platform: str) -> pathlib.Path:
        if platform == "nt":
            return ide_home_dir / "Code.exe"
        else:
            return ide_home_dir / "code"


class WebStormLauncher(BaseIDELauncher):
    @property
    def ide_name(self) -> str:
        return "WebStorm"

    @property
    def ide_home_env_var_name(self) -> str:
        return "WEBSTORM_HOME"

    def get_ide_exec_path(self, ide_home_dir: pathlib.Path, platform: str) -> pathlib.Path:
        if platform == "nt":
            return ide_home_dir / "bin" / "webstorm64.exe"
        else:
            return ide_home_dir / "bin" / "webstorm.sh"


class IntelliJIDEALauncher(BaseIDELauncher):
    @property
    def ide_name(self) -> str:
        return "IntelliJ IDEA"

    @property
    def ide_home_env_var_name(self) -> str:
        return "IDEA_HOME"

    def get_ide_exec_path(self, ide_home_dir: pathlib.Path, platform: str) -> pathlib.Path:
        if platform == "nt":
            return ide_home_dir / "bin" / "idea64.exe"
        else:
            return ide_home_dir / "bin" / "idea.sh"


__all__ = ["PyCharmLauncher", "VSCodeLauncher", "WebStormLauncher", "IntelliJIDEALauncher"]

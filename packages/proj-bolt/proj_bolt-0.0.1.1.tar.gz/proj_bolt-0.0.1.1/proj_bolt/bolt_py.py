import shutil
import pathlib
import argparse
from typing import Optional
from datetime import datetime

from .template import READMEMarkdownTemplate, LicenceTemplate
from .template.bolt_py import GitIgnorePyTemplate, SetupPyTemplate


def create_python_project(
        proj_name: str,
        author: str,
        parent_dir: str = ".",
        is_pypi_proj: bool = False,
        is_git_proj: bool = False,
):
    """Create a Template Python project

    Args:
        proj_name: (str) name of the project
        author: (str) author of the project
        parent_dir: (str) parent directory where the project will be created. Defaults to the current directory.
        is_pypi_proj: (bool) specify if it's a PyPI project. If set, appropriate setup files will be generated.
        is_git_proj: (bool) specify if it's a Git project. If set, a git repository will be initialized.

    Returns:
        None
    """
    # 创建项目目录, 若已存在则报错
    print(f"new version!!")
    proj_path = pathlib.Path(parent_dir) / proj_name
    proj_path.mkdir(parents=True, exist_ok=False)  # 创建项目文件夹

    try:
        # 使用模板文件创建和写入文件
        (proj_path / 'README.md').write_text(READMEMarkdownTemplate.render(project_name=proj_name))
        (proj_path / 'requirements.txt').touch()

        # 如果 is_pypi_proj 为 True
        if is_pypi_proj:
            # 从模板中创建 PyPI 项目所需文件
            (proj_path / 'setup.py').write_text(SetupPyTemplate.render(project_name=proj_name, author=author))
            (proj_path / 'MANIFEST.in').touch()

            (proj_path / 'LICENSE').write_text(LicenceTemplate.render(author=author, year=datetime.now().year))

            pkg_path = proj_path / proj_name
            pkg_path.mkdir(parents=True, exist_ok=True)

            (pkg_path / '__init__.py').touch()

        # 如果 is_git_proj 为 True
        if is_git_proj:
            # 创建 Git 项目所需文件
            (proj_path / '.gitignore').write_text(GitIgnorePyTemplate.render())
    except Exception as e:
        # 如果出错, 则删除项目目录
        proj_path.rmdir()
        # use rmtree instead
        shutil.rmtree(proj_path)
        raise e


def query_user_for_input(prompt: str, default: Optional[str] = None) -> str:
    """
    Query the user for input with a default value.

    :param prompt: The prompt to display to the user.
    :param default: The default value to use if the user doesn't provide input.
    :return: The user's input or the default value.
    """
    user_input = input(f"{prompt} [{'default: ' + default if default else ''}] > ").strip()
    return user_input or default


def main():
    parser = argparse.ArgumentParser(description='Create a Template Python project.')

    parser.add_argument('-n', metavar='PROJECT_NAME', help='Name of the project.')
    parser.add_argument('-p', '--parent-dir', default=None, help='Parent directory where the project will be created. Defaults to the current directory.')
    parser.add_argument('--pypi', action='store_true', default=None, help='Specify if it\'s a PyPI project. If set, appropriate setup files will be generated.')
    parser.add_argument('--git', action='store_true', default=None, help='Specify if it\'s a Git project. If set, a git repository will be initialized.')
    parser.add_argument("--author", metavar="AUTHOR", default=None, help="The author of the project.")

    args = parser.parse_args()

    if not args.n:
        args.n = query_user_for_input("Please enter the project name:")

    if not args.author:
        args.author = query_user_for_input("Please enter the author name:")

    if args.parent_dir is None:
        args.parent_dir = query_user_for_input("Please enter the parent directory for the project:", ".")

    if args.pypi is None:
        args.pypi = query_user_for_input("Is it a PyPI project? (y/n):", "n").lower() == 'y'

    if args.git is None:
        args.git = query_user_for_input("Is it a Git project? (y/n):", "n").lower() == 'y'

    create_python_project(
        proj_name=args.n,
        is_git_proj=args.git,
        is_pypi_proj=args.pypi,
        parent_dir=args.parent_dir,
        author=args.author,
    )

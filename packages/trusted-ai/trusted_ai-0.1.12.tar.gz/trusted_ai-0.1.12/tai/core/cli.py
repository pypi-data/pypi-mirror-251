import argparse
import shutil
from git import Repo
from pathlib import Path
import subprocess
import yaml

from tai.core.utils import color, create_template_user_config
from tai.core.gitea_controller import GiteaController


ADMIN_CONFIG_PATH = "/Users/Ekaterina/Documents/ISPwork/trusted-ai/tai/core/gitea_conf.yaml"
GITEA_URL = "git.ai.intra.ispras.ru/"
GITEA_CONFIG_PATH = "user_gitea_config.yaml"

def main():
    """Main function with running commands.

    :param mode: `new` for creation new package and `help` for text description
    :type mode: str

    :param pkg_name: name of your <package name> (for mode `new`)
    :type pkg_name: str

    :param --local-repo-path: path to folder where you want to create repo
    :type local-repo-path: str

    :param --config-path: path to config file with your creds
    :type config-path: str

    :param --username: gitea username
    :type username: str

    :param --email: gitea email
    :type email: str

    :param --full-name: gitea full name
    :type full-name: str

    :param --password: gitea password
    :type password: str
    """
    parser = argparse.ArgumentParser(prog="trusted-ai")
    parser.add_argument("mode", type=str, choices=["new", "help", "create-config"])
    parser.add_argument("pkg_name", type=str, nargs="?")
    parser.add_argument("--local-repo-path", type=str, default=Path.cwd())
    parser.add_argument("--config-path", type=str, nargs="?", default=GITEA_CONFIG_PATH)

    parser.add_argument("--username", type=str, nargs="?", help="Username for Gitea.")
    parser.add_argument("--email", type=str, nargs="?", help="Email for Gitea.")
    parser.add_argument("--full-name", type=str, nargs="*", help="Full name for Gitea.")
    parser.add_argument("--password", type=str, nargs="?", help="Password for Gitea.")

    args = parser.parse_args()

    if args.mode == "help":
        print("Hello! \n It's TAI project, that will help you create your own little-package for MLM.")
        print(
            f"Type this command for creation new package:\n\t" + color.BOLD + color.GREEN + 
            f"tai new " + color.END + color.BLUE + color.BOLD +
            f"<package_name> --local-repo-path <your path> --config-path <your config>"
            + color.END)
        print(
            f"If you don't have configuration file for Gitea, yo can create it with command:\n\t" +
            color.BOLD + color.GREEN +
            f"tai create-config " + color.END + color.BLUE + color.BOLD +
            f"--config-path <path to config> " +
            f"--username <your username> --email <your email> --full-name <your full name> --password <your password>" +
            color.END
            )

    elif args.mode == "new":
        gc = GiteaController(admin_config_path=ADMIN_CONFIG_PATH)
        if args.config_path is None:
            conf_path = GITEA_CONFIG_PATH
        else:
            conf_path = args.config_path
        gc.create_user_config(user_config_path=conf_path)
        exist_repo = gc.check_users_repo(repo_name=args.pkg_name)
        if exist_repo==True:
            raise NameError(f"Repository with name {args.pkg_name} already exists!")
        else:
            gc.create_repo(repo_name=args.pkg_name)

        create_new_repo(package_name=args.pkg_name, local_repo_path=args.local_repo_path, gitea_controller=gc)

    elif args.mode == "create-config":
        if args.config_path is None:
            conf_path = GITEA_CONFIG_PATH
        else:
            conf_path = args.config_path
        full_name = " ".join(args.full_name) if args.full_name else args.full_name
        create_template_user_config(conf_path=conf_path,
                                    email=args.email,
                                    full_name=full_name,
                                    username=args.username,
                                    password=args.password,
                                    )
    else:
        raise ValueError("You can choose only these modes: new, help.")


def create_new_repo(package_name, local_repo_path, gitea_controller):
    """
    Create a new git repository with a package for your Model|Dataset|Executor.

    This function creates a repo in <local_repo_path> with the following structure::
        
        tai/
        ├── pyproject.toml  # pdm configuration file for your project
        ├── .gitignore
        ├── .venv           # virtual venv for your project
        └── contrib/
            └── <organization or username>/
                └── <package name>/
                    └── __init__.py

    :param package_name: Package name
    :type package_name: str
    :param local_repo_path: path to folder where you want to create repo
    """
    file_path = Path(local_repo_path) / "tai" / "contrib" / gitea_controller.user_config["username"] / package_name
    file_path.mkdir(exist_ok=True, parents=True)
    open(file_path / "__init__.py", "a").close()

    shutil.copyfile(Path(__file__).parent / ".gitignore_template", Path(local_repo_path) / ".gitignore")

    Repo.init(local_repo_path)
    repo = Repo(local_repo_path)
    repo.index.add(['.gitignore'])

    command = ["pdm", "init"]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, cwd=local_repo_path)

    input_data_list = ["0", # TODO: add Python interpreter selection 
                       f"{gitea_controller.user_config['username']}_{package_name}",
                       "0.1.0",
                       "y",
                       "Some description...",
                       "0",
                       "MIT",
                       gitea_controller.user_config["username"],
                       gitea_controller.user_config["email"],
                       "==3.12.*"]

    for input_data in input_data_list:
        process.stdin.write(input_data + "\n")
        process.stdin.flush()

    output = process.communicate()
    print("Output:", "\n".join(output))

    process.stdin.close()
    process.stdout.close()
    process.stderr.close()

    shutil.rmtree(Path(local_repo_path) / "src")
    shutil.rmtree(Path(local_repo_path) / "tests")

    repo.index.add([".gitignore", "tai", "pyproject.toml"])

    username = gitea_controller.user_config['username']
    password = gitea_controller.user_config['password']

    repo_url = f"https://{username}:{password}@" + GITEA_URL + username + "/" + package_name + ".git"

    repo.config_writer().set_value("user", "name", gitea_controller.user_config["username"]).release()
    repo.config_writer().set_value("user", "email", gitea_controller.user_config["email"]).release()
    repo.index.commit("Initial commit.")
    if "origin" in repo.remotes:
        origin = repo.remotes.origin
    else:
        origin = repo.create_remote("origin", repo_url)
    repo.git.push("--set-upstream", origin, "master")


if __name__ == "__main__":
    main()
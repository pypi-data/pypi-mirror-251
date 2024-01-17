import giteapy
from giteapy.rest import ApiException
from tai.core.utils import read_config


class GiteaController:
    def __init__(self, admin_config_path: str):
        config = read_config(admin_config_path)
        gitea_configuration = create_conf(config["admin_token"], config["username"], config["password"])
        self.admin_api_object = giteapy.ApiClient(gitea_configuration)
        self.admin_api = giteapy.AdminApi(self.admin_api_object)
        self.user_api = None
        self.user_config = None
    
    def create_user_config(self, user_config_path: str):
        self.user_config = read_config(user_config_path)
        self.user_config_path = user_config_path
        configuration = giteapy.Configuration()
        configuration.host = "https://git.ai.intra.ispras.ru/api/v1"
        configuration.username = self.user_config["username"]
        configuration.password = self.user_config["password"]
        # if "token" in self.user_config:
        #     configuration.api_key =  self.user_config["token"]
        self.user_api = giteapy.UserApi(giteapy.ApiClient(configuration))


    def check_user_existing(self, username):
        user_exist = None
        try:
            users = self.admin_api.admin_get_all_users()
            for user in users:
                if user.login == username:
                    user_exist = True
                    break
            user_exist = False
        except giteapy.rest.ApiException as error:
            user_exist = False
            print(error.body)
        return user_exist
    
    def create_new_user(self):
        status = None
        try:
            if self.user_config is None:
                raise ValueError("Create user config! Call GiteaController.create_user_config(<config_path>).")
            user_creds = {
                "email": self.user_config["email"],
                "full_name": self.user_config["full_name"],
                "password": self.user_config["password"],
                "username": self.user_config["username"],
                "must_change_password": False,
            }
            self.admin_api.admin_create_user(body=user_creds)
            status = True
        except giteapy.rest.ApiException as error:
            status = False
            print(error.body)
        return status
    
    def create_repo(self, repo_name: str):
        status = None
        if self.user_config is None:
            raise ValueError("Create user config! Call GiteaController.create_user_config(<config_path>).")
        user_exist = self.check_user_existing(username=self.user_config["username"])
        if user_exist is False:
            print("Creating new user.")
            self.create_new_user()
        try:
            repository = giteapy.CreateRepoOption(name=repo_name)
            self.admin_api.admin_create_repo(username=self.user_config["username"], repository=repository)
            status = True
        except giteapy.rest.ApiException as error:
            status = False
            print(error)
        return status
    
    def remove_repo(self, repo_name):
        status = None
        try:
            api_instance = giteapy.RepositoryApi(self.admin_api_object)
            api_instance.repo_delete(owner=self.user_config["username"],
                                     repo=repo_name)
            status = True
        except ApiException as error:
            status = False
            print("Exception when calling AdminApi->repo_delete: %s\n" % error)
        return status
    
    def remove_user(self, username):
        repos = self.user_api.user_current_list_repos()
        for rep in repos:
            print(rep)
            self.remove_repo(rep.name)
        self.admin_api.admin_delete_user(username)
    
    def check_users_repo(self, repo_name):
        exist_status = None
        try:
            repos = self.user_api.user_current_list_repos()
            for repo in repos:
                if repo.name == repo_name:
                    exist_status = True
                    break
            exist_status = False
        except ApiException as error:
            print("Exception when calling UserApi->user_current_list_repos: %s\n" % error)
        return exist_status


def create_conf(api_key, username, password):
    configuration = giteapy.Configuration()
    configuration.host = "https://git.ai.intra.ispras.ru/api/v1"
    configuration.username = username
    configuration.password = password
    configuration.api_key['access_token'] = api_key
    configuration.api_key['sudo'] = api_key
    configuration.api_key['Authorization'] = api_key
    configuration.api_key['Sudo'] = api_key
    configuration.api_key['token'] = api_key

    return configuration

if __name__ == "__main__":
    gc = GiteaController(admin_config_path="/Users/Ekaterina/Documents/ISPwork/trusted-ai/tai/core/gitea_conf.yaml")
    # gc.check_user_existing(username="pp")
    gc.create_user_config("/Users/Ekaterina/Documents/ISPwork/trusted-ai/user_gitea_config.yaml")

    # status = gc.create_repo(repo_name="other_repo")
    # # print(status)

    # gc.check_users_repo(repo_name="other_repo")

    # gc.remove_repo("kekrepo")

    # gc.admin_api.admin_delete_user("test_user_6")

    gc.remove_user("test_user")
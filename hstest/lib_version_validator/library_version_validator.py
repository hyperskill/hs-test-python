import github_releases
import installed_version


class ValidatorTestLibrary:

    def __init__(self) -> None:
        super().__init__()
        self.latest_release_version = ""
        self.current_version = ""
        self.feedback = ""

    def version_validation(self):
        self.latest_release_version = github_releases.get_latest_release().tag_name.replace("v", "", 1)
        self.current_version = installed_version.get_installed_version()
        if int(self.latest_release_version.replace(".", "", 2)) != int(self.current_version.replace(".", "", 2)):
            self.feedback = f"You need update your testing library: latest version {self.latest_release_version}  " \
                            f"you installed version {self.current_version}" \
                            f"Please download latest version from: {github_releases.get_latest_release().html_url}" \
                            f"and install it with command: pip install hs-test-python --upgrade"
            return False
        else:
            return True


if __name__ == '__main__':
    ValidatorTestLibrary().version_validation()

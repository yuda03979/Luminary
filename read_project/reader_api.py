import os
import re
from read_project.reader import LocalReader, GitHubReader


class ReaderApi:

    def __init__(self, path: str, branch: str = "main"):
        self.path = path
        self.branch = branch
        self.write_txt_files()

    def write_txt_files(self):
        # Check if it's a valid GitHub repository URL
        github_pattern = r"^(https?://github\.com/[\w-]+/[\w.-]+)$"
        if re.match(github_pattern, self.path):
            print(f"path {self.path} identified as github repo.")
            GitHubReader(
                repo_url=self.path,
                branch=self.branch
            )

        # Check if it's a valid local directory path
        elif os.path.isdir(self.path):
            print(f"path {self.path} identified as local project.")
            LocalReader(project_path=self.path)

        # Return None if the path is neither a valid GitHub URL nor a local directory
        else:
            raise f"cant read this path: {self.path}"

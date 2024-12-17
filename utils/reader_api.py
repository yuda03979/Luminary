import os
import re
import json
import shutil
import tempfile
import subprocess
import time

from globals import GLOBALS


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




class LocalReader:
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.output_directory = GLOBALS.analized_proj_folder
        os.makedirs(self.output_directory, exist_ok=True)
        self.completed_files = []  # Track completed files
        self.read_project()

    def read_project(self):
        for root, dirs, files in os.walk(self.project_path):
            relative_root = os.path.relpath(root, self.project_path)
            if relative_root == ".":
                relative_root = ""

            # Process files
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.join(relative_root, file)

                # Read and save file content
                self._read_and_save_file(file_path, relative_path)

        # Ensure all files are processed before building the structure
        while len(self.completed_files) < len(self._get_all_files(self.project_path)):
            time.sleep(0.1)  # Wait briefly for file writing to finish

        # Build the project structure
        project_structure = {os.path.basename(self.project_path): self._build_structure(self.project_path)}

        # Save the project structure as a JSON file
        structure_file_path = os.path.join(self.output_directory, "project_structure.json")
        with open(structure_file_path, "w", encoding="utf-8") as structure_file:
            json.dump(project_structure, structure_file, indent=4)

    def _build_structure(self, current_path):
        """
        Recursively build the structure of the project directory.
        """
        structure = {}
        for item in os.listdir(current_path):
            item_path = os.path.join(current_path, item)
            if os.path.isdir(item_path):
                # If it's a directory, recursively build its structure
                structure[item] = self._build_structure(item_path)
            else:
                # If it's a file, just add it to the structure
                structure.setdefault("__files__", []).append(item)
        return structure

    def _read_and_save_file(self, file_path, relative_path):
        """
        Read a file and save its content to a .txt file.
        """
        output_file_path = os.path.join(self.output_directory, relative_path + ".txt")
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        print(f"Writing: {output_file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        except (UnicodeDecodeError, IOError):
            # Handle binary or unreadable files
            content = "This file is binary or could not be read."

        # Save content to a .txt file
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(content)

        # Mark this file as completed
        self.completed_files.append(output_file_path)

    def _get_all_files(self, directory):
        """
        Get all files in the directory recursively.
        """
        all_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                all_files.append(os.path.join(root, file))
        return all_files


class GitHubReader:
    def __init__(self, repo_url: str, branch: str = "main"):
        self.repo_url = repo_url
        self.branch = branch
        self.output_directory = GLOBALS.analized_proj_folder
        os.makedirs(self.output_directory, exist_ok=True)
        self.process_repository()

    def process_repository(self):
        """
        Clone the GitHub repository, process its content using Local, and clean up.
        """
        temp_dir = os.path.abspath(tempfile.mkdtemp())
        try:
            if self._clone_repository(temp_dir):
                LocalReader(project_path=temp_dir)
            else:
                print(f"couldn't clone the repository: {self.repo_url}, branch: {self.branch}")

        finally:
            # Clean up: Remove the temporary directory
            shutil.rmtree(temp_dir)

    def _clone_repository(self, temp_dir):
        # Start the cloning process
        print(f"Cloning repository from {self.repo_url} to {temp_dir}...")
        try:
            result = subprocess.run(
                ["git", "clone", "-b", self.branch, self.repo_url, temp_dir],
                check=True,  # Raise an error if the clone fails
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            # Wait for the cloning process to complete
            print(result.stdout.decode())  # Print the output from the cloning command
            print("Repository cloned successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error cloning repository: {e.stderr.decode()}")
            return False

        # Ensure the repository was successfully cloned
        while not os.path.isdir(temp_dir):
            print("Waiting for cloning to complete...")
            time.sleep(1)  # Wait a bit before checking again

        # Ensure that the cloned repository contains files (i.e., it's not empty)
        while not any(os.scandir(temp_dir)):  # Check if directory is not empty
            print("Waiting for repository files to be fully cloned...")
            time.sleep(1)

        print(f"Cloning completed. The repository is ready at {temp_dir}")
        return True

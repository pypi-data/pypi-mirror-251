from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import os
import sys

class CustomInstall(install):
    def run(self):
        # Run the standard setuptools install process
        install.run(self)

        # Function to execute shell commands
        def execute_command(command, cwd=None):
            try:
                subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, cwd=cwd)
            except subprocess.CalledProcessError as e:
                print(f"Error: {command} failed.")
                print(f"Command output: {e.output.decode()}")
                sys.exit(1)

        # Check if Node.js and npm are installed
        for command in ['node --version', 'npm --version']:
            execute_command(command)

        # Define the directory where your Node.js code is located
        node_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'yol', 'trace_display')

        # Run `npm install` and `npm run build`
        for command in ['npm install', 'npm run build']:
            execute_command(command, cwd=node_dir)

setup(
    cmdclass={
        'install': CustomInstall,
    },
    # The rest of the setup configuration will be read from setup.cfg
)

from setuptools import setup, find_namespace_packages, find_packages
import os
from setuptools import setup
from setuptools.command.install import install
import subprocess
import traceback
from glob import glob
from threading import Thread

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# This function will collect all files within the specified directory
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

class CustomInstall(install):
    def remove_quarantine(self, plugin_paths, log_file_path):
        base_command = '/usr/bin/xattr -rd com.apple.quarantine'
        with open(log_file_path, 'a') as log_file:
            for plugin_path in plugin_paths:
                command = f"{base_command} '{plugin_path}'"
                log_file.write(f"Trying the following: {command}\n")
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    log_file.write(f"Successfully removed quarantine attribute from {plugin_path}\n")
                    log_file.write(result.stdout)
                else:
                    log_file.write(f"Failed to remove quarantine attribute from {plugin_path}:\n")
                    log_file.write(result.stderr)
                    log_file.write(result.stdout)
                if result.stdout or result.stderr:
                    log_file.write(result.stdout)
                    log_file.write(result.stderr)

    def run(self):
        try:
        # Run the standard install process
            install.run(self)

            indigo_plugins_path = '/Library/Application Support/Perceptive Automation/Indigo 2023.2/Plugins'
            indigo_disabled_plugins_path = '/Library/Application Support/Perceptive Automation/Indigo 2023.2/Plugins (Disabled)'
            log_file_path = os.path.join(self.install_lib, 'plugin_gifsicle', 'post_install.log')

            plugin_paths = glob(os.path.join(indigo_plugins_path, '*.indigoPlugin'))
            plugin_paths += glob(os.path.join(indigo_disabled_plugins_path, '*.indigoPlugin'))
            # Construct the base xattr command to remove the quarantine attribute
            base_command = '/usr/bin/xattr -rd com.apple.quarantine'

            quarantine_thread = Thread(target=self.remove_quarantine, args=(plugin_paths, log_file_path))
            quarantine_thread.start()
            quarantine_thread.join()  # Optionally wait for the thread to finish


        except Exception as e:
            print("An unexpected error occurred: ", e)
            print(traceback.format_exc())
            raise  # Re-raise the exception to ensure it's not silently ignored

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Call the function and specify the path to the binaries
binary_files = package_files('plugin_gifsicle/gifsicle_binaries')
print(f"{binary_files}")

setup(
    cmdclass= {'install': CustomInstall      },
    zip_safe=False,
    author='GlennNZ',
    description='Package providing Gifsicle binaries for specific system architectures, primarily for Indigo plugin usage',
    license='MIT',
    long_description=long_description,
    include_package_data=True,
    long_description_content_type="text/markdown",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    # Instructing setuptools to include binary files found by MANIFEST.in
    package_data={
        'plugin_gifsicle': ['gifsicle_binaries/arm/*', 'gifsicle_binaries/x86/*'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
    ],
    python_requires='>=3.10',
)

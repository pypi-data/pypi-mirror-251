from setuptools import setup, find_namespace_packages, find_packages
import os
from setuptools import setup
from setuptools.command.install import install
import subprocess
import traceback

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
    def run(self):
        # Run the standard install process
        install.run(self)
        # Determine the installation path of the package
        package_path = os.path.join(self.install_lib, 'plugin_gifsicle')

        ## Hard code here as no way to access target.  Will need regular updates.
        ## given -t is being used with pip, move must occur first and then pip libraries downloaded - so should correctly
        ## remove quarantine bit from indigo plugin Bundles
        indigo_plugins_path = '/Library/Application Support/Perceptive Automation/Indigo 2023.2/Plugins'
        indigo_disabled_plugins_path = '/Library/Application Support/Perceptive Automation/Indigo 2023.2/Plugins (Disabled)'
        # Log file path (you could also include a timestamp or other distinguishing info if needed)
        log_file_path = os.path.join(package_path, 'post_install.log')
        # Traverse up to get the bundle directory
        # Construct the xattr command to run in the Indigo Plugins directory
        # add recursive - seems like -d enough, but previous advice to run recursively - so add that here
        command = f'xattr -rd com.apple.quarantine "{indigo_plugins_path}"'
        command_disabled = f'xattr -rd com.apple.quarantine "{indigo_disabled_plugins_path}"'
        # Open the log file for writing
        with open(log_file_path, 'a') as log_file:
            # Write initial log entry
            log_file.write(f"Running post-install script in {indigo_plugins_path}\n")
            log_file.write(f"Running command: {command}\n{command_disabled}\n")
            # Execute the command, passing the string directly to the shell
            try:
                subprocess.check_call(command, shell=True, stderr=log_file, stdout=log_file)
                log_file.write(f"Successfully removed quarantine attribute from all files in {indigo_plugins_path}\n")
                subprocess.check_call(command_disabled, shell=True, stderr=log_file, stdout=log_file)
                log_file.write(f"Successfully removed quarantine attribute from all files in {indigo_disabled_plugins_path}\n")
            except subprocess.CalledProcessError as e:
                log_file.write(f"Failed to remove quarantine attribute: {e}\n")
            except FileNotFoundError:
                log_file.write("xattr command not found, ensure it is available and in the PATH\n")
            except Exception as e:
                log_file.write("Unknown exception caught {e}\n")
                log_file.write(traceback.format_exc())


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

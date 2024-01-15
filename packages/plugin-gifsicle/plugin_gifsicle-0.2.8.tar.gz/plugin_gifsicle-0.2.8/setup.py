from setuptools import setup, find_namespace_packages, find_packages
import os
from setuptools import setup
from setuptools.command.install import install
import subprocess
import traceback
from glob import glob

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
        try:
        # Run the standard install process
            install.run(self)

            indigo_plugins_path = '/Library/Application Support/Perceptive Automation/Indigo 2023.2/Plugins'
            indigo_disabled_plugins_path = '/Library/Application Support/Perceptive Automation/Indigo 2023.2/Plugins (Disabled)'
            log_file_path = os.path.join(self.install_lib, 'plugin_gifsicle', 'post_install.log')

            # Construct the base xattr command to remove the quarantine attribute
            base_command = 'xattr -d com.apple.quarantine'

            # Open the log file for writing
            with open(log_file_path, 'a') as log_file:
                # Find all .indigoPlugin bundles in the main and disabled plugins directories
                plugin_paths = glob(os.path.join(indigo_plugins_path, '*.indigoPlugin'))
                plugin_paths += glob(os.path.join(indigo_disabled_plugins_path, '*.indigoPlugin'))

                # Remove quarantine from individual .indigoPlugin bundles
                for plugin_path in plugin_paths:
                    try:
                        subprocess.check_call([base_command, plugin_path], shell=False, stderr=log_file, stdout=log_file)
                        log_file.write(f"Successfully removed quarantine attribute from {plugin_path}\n")
                    except subprocess.CalledProcessError as e:
                        log_file.write(f"Failed to remove quarantine attribute from {plugin_path}: {e}\n")
                    except FileNotFoundError:
                        log_file.write(f"xattr command not found, ensure it is available and in the PATH\n")
                    except Exception as e:
                        log_file.write(f"Unknown exception caught for {plugin_path}: {e}\n")
                        log_file.write(traceback.format_exc())

                # Now remove quarantine recursively from the directories
                try:
                    subprocess.check_call(f"xattr -rd com.apple.quarantine '{indigo_plugins_path}'", shell=True, stderr=log_file, stdout=log_file)
                    log_file.write(f"Successfully removed quarantine attribute recursively from {indigo_plugins_path} directory\n")
                    subprocess.check_call(f"xattr -rd com.apple.quarantine '{indigo_disabled_plugins_path}'", shell=True, stderr=log_file, stdout=log_file)
                    log_file.write(f"Successfully removed quarantine attribute recursively from {indigo_disabled_plugins_path} directory\n")
                except subprocess.CalledProcessError as e:
                    log_file.write(f"Failed to remove quarantine attribute recursively: {e}\n")
                except FileNotFoundError:
                    log_file.write("xattr command not found, ensure it is available and in the PATH\n")
                except Exception as e:
                    log_file.write(f"Unknown recursive unquarantine exception caught: {e}\n")
                    log_file.write(traceback.format_exc())
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

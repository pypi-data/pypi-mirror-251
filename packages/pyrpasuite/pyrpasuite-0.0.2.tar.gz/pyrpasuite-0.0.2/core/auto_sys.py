import subprocess
import os
from AppOpener import open
import pyautogui
import glob
import shutil
import configparser
import psutil


class AutoSys:
    """
    A class to automate system operations.
    """

    def __init__(self):
        self.process = None

    def open_application(self, application_name:str) -> bool:
        """
        Open an application.

        :param application_name: The name of the application to open.
        :return: True if the application was opened successfully, False otherwise.
        """
        try:
            # Try to open the application using subprocess.Popen
            self.process = subprocess.Popen(application_name)
        except Exception as e:
            try:
                # If subprocess.Popen fails, try AppOpener
                open(application_name, match_closest=True, output=True,throw_error=True)
            except Exception as e:
                print(f"Failed to open {application_name} with error: {e}")
                return False
        return True
    
    def click(self, x, y):
        """
        Perform a mouse click at the specified coordinates.

        :param x: The x-coordinate for the click.
        :param y: The y-coordinate for the click.
        """
        pyautogui.click(x=x,y=y)
        
    def type_text(self, text):
        """
        Type a text string.

        :param text: The text to type.
        """
        pyautogui.typewrite(text)

    def close_application(self):
        """
        Close the currently open application.
        """
        if self.process:
            self.process.terminate()
    
    def send_hotkey(self, *keys):
        """
        Sends a hotkey (or sequence of keys) to the active window.
        Example: AutoSys.send_hotkey('win','d')

        :param keys: A sequence of keys to be pressed together.
        """
        pyautogui.hotkey(keys)
    
    # def print_memory_usage(self):
    #     """
    #     Print the current memory usage.

    #     :return: The percentage of memory used and the amount of memory used in GB.
    #     """
    #     total_memory, used_memory, _ = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
    #     memory_usage = round((used_memory / total_memory) * 100, 2)
    #     used_memory_gb = used_memory/1024
    #     return memory_usage,used_memory_gb
        
    def get_memory_usage(self):
        """
        Print the current memory usage.

        :return: The percentage of memory used and the amount of memory used in GB.
        """
        try:
            # Get virtual memory usage info
            mem_info = psutil.virtual_memory()

            # Total memory in GB
            total_memory_gb = mem_info.total / (1024.0 ** 3)

            # Used memory in GB
            used_memory_gb = (mem_info.total - mem_info.available) / (1024.0 ** 3)

            # Memory usage percentage
            memory_usage_percentage = mem_info.percent

            return memory_usage_percentage, used_memory_gb
        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    def get_files(self,directory,identifier):
        """
        Get a list of files in a directory that match a certain identifier.

        :param directory: The directory to search in.
        :param identifier: The identifier to match.
        :return: A list of file paths.
        """
        listpath = glob.glob(directory+identifier)
        return listpath      
    
    def run_shell_command(self,command):
        """
        Run a shell command.

        :param command: The command to run.
        :return: The output of the command.
        """
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        return output
    
    def move_file(self,source_path:str,destination_path:str):
        """
        Move a file from one location to another.

        :param source_path: The path of the file to move.
        :param destination_path: The destination path.
        """
        shutil.move(source_path,destination_path)
    
    def copy_file(self,source_path:str,destination_path:str):
        """
        Copy a file from one location to another.

        :param source_path: The path of the file to copy.
        :param destination_path: The destination path.
        """
        shutil.copy2(source_path,destination_path)
    
    def for_each_file_in_folder(self,path:str, subdirectory:bool=False, identifier=None):
        """
        Yield each file in a folder.

        :param path: The path of the folder.
        :param subdirectory: Whether to include subdirectories.
        :param identifier: An identifier to match.
        :return: The path of each file.
        """
        try:
            if subdirectory:
                if identifier is None:
                    for dirpath, dirnames, filenames in os.walk(path):
                        for filename in filenames:
                            yield os.path.join(dirpath, filename)
                else:
                    for dirpath, dirnames, filenames in os.walk(path):
                        for filename in glob.glob(os.path.join(dirpath, identifier)):
                            yield filename
            else:
                if identifier is None:
                    for filename in os.listdir(path):
                        yield os.path.join(path, filename)
                else:
                    for filename in glob.glob(os.path.join(path, identifier)):
                        yield filename
        except FileNotFoundError:
            yield f"Unable to locate {path}"
        except Exception as e:
            yield f"An error occurred: {str(e)}"
    
    def read_config(self, config_file):
        """
        Read a configuration file.

        :param config_file: The path of the configuration file.
        :return: The configuration object.
        """
        config = configparser.ConfigParser()
        config.read(config_file)
        return config

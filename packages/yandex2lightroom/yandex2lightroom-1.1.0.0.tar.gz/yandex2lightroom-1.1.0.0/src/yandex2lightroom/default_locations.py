import sys
import os
import platform


class DefaultLocations:
    def __init__(self):
        """
            constructor defines a user specific chromedriver directory which can be used as a default value.
            Windows: <user home>/AppData/local/Programs/ChromeDriver
            Linux:  <user home>/.local/ChromeDriver
            macOS:  <user home>/Library/Application Support/ChromeDriver
        """
        self.chromeDriverPrefix = None
        self.downloadPrefix = None

    def get_chromedriver_location(self):
        """
             defines a user specific chromedriver directory which can be used as a default value.
             Windows: <user home>/AppData/local/Programs/ChromeDriver
             Linux:  <user home>/.local/ChromeDriver
             macOS:  <user home>/Library/Application Support/ChromeDriver
         """
        if self.chromeDriverPrefix is not None:
            return self.chromeDriverPrefix
        home_directory = os.path.expanduser('~')
        if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
            self.chromeDriverPrefix = os.path.join(home_directory, 'AppData', 'local', 'Programs', 'ChromeDriver')
        elif sys.platform.startswith('linux'):
            self.chromeDriverPrefix = os.path.join(home_directory, '.local', 'ChromeDriver')
        elif sys.platform.startswith('darwin'):
            self.chromeDriverPrefix = os.path.join(home_directory, 'Library', 'Application Support', 'ChromeDriver')
        else:
            self.chromeDriverPrefix = None
        return self.chromeDriverPrefix

    def get_download_location(self):
        """
             gets the user download folder
             Windows: <user home>/AppData/local/Programs/ChromeDriver
             Linux:  <user home>/.local/ChromeDriver
             macOS:  <user home>/Library/Application Support/ChromeDriver
         """
        if self.downloadPrefix is not None:
            return self.downloadPrefix
        home_directory = os.path.expanduser('~')
        if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
            self.downloadPrefix = os.path.join(home_directory, 'Downloads')
        elif sys.platform.startswith('linux'):
            self.downloadPrefix = os.path.join(home_directory, '.local', 'Downloads')
        elif sys.platform.startswith('darwin'):
            self.downloadPrefix = os.path.join(home_directory, 'Downloads')
        else:
            self.downloadPrefix = None
        return self.downloadPrefix

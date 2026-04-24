import re
import os
import subprocess

class ConfigParser:
    def __init__(self):
        self.config_path = os.path.expanduser("~/.config/i3/config")

    def get_value(self, pattern):
        """Finds a value in the config using regex"""
        if not os.path.exists(self.config_path): return None
        with open(self.config_path, "r") as f:
            for line in f:
                match = re.search(pattern, line)
                if match:
                    return match.group(1)
        return None

    def update_value(self, pattern, replacement):
        """Replaces a value in the config safely"""
        if not os.path.exists(self.config_path): return

        with open(self.config_path, "r") as f:
            lines = f.readlines()

        with open(self.config_path, "w") as f:
            for line in lines:
                if re.search(pattern, line):
                    f.write(re.sub(pattern, replacement, line))
                else:
                    f.write(line)

        # Reload i3 live
        subprocess.run(["i3-msg", "reload"])

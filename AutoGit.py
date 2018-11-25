import os
import time
import subprocess
import re
import config

sleep_time = 3
DIR = config.DIR


def loop():
    for i in DIR:
        os.chdir(i)
        try:
            add = subprocess.check_output("git add .",shell=True)
        except subprocess.CalledProcessError as e:
            add = e.output
        pattern = "nothing to commit, working tree clean"
        try:
            commit = subprocess.check_output("git commit -m \"AutoSave --AutoGit\"", shell=True)
        except subprocess.CalledProcessError as e:
            commit = e.output

        if re.search(pattern, commit.decode('utf-8')) is not None:
            return 0
        else:
            print(time.asctime(time.localtime(time.time())))
            print(add.decode('utf-8'))
            print(commit.decode('utf-8'))
            os.system("git push")
            print("One loop end.")
            return 0


if __name__ == '__main__':
    loop()

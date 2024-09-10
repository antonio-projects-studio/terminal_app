from terminal_app.ssh import SSHClient
from terminal_app.curlify import Curlify
from requests import Request
import time
import json
import pprint
# remote = SSHClient("MLSpace")
# ssh_stdin, ssh_stdout, ssh_stderr = remote.exec_command("ls -alrt")

# exit_code = ssh_stdout.channel.recv_exit_status()  # handles async exit error
# for line in ssh_stdout:
#     print(line.strip())
    

remote = SSHClient("MLSpace")
stdin, stdout, stderr = remote.exec_command('ls')
for line in stdout:
    print(line.strip())

print(remote.http_request(Request("GET", url="http://localhost:7773/1:jazzXR/status")))
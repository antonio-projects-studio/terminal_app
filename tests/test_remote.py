from terminal_app.ssh import SSHClient

remote = SSHClient("MLSpace")
ssh_stdin, ssh_stdout, ssh_stderr = remote.exec_command("ls -alrt")

exit_code = ssh_stdout.channel.recv_exit_status()  # handles async exit error
for line in ssh_stdout:
    print(line.strip())

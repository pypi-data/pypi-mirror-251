import os

import paramiko
import typer

from searchpi.command_executer import CommandExecuter


def searchpi(nmap_command: str, ssh_username: str, ssh_key_filename: str):
    # searchpi 192.168.1.0/24 pomponchik ~/.ssh/id_rsa.pub
    os.path.expanduser(ssh_key_filename)

    executer = CommandExecuter(['nmap', '-sn', nmap_command])
    executer.run()

    prefix = 'Nmap scan report for '
    filtered_stdout = (x for x in executer.stdout if x.startswith(prefix))
    ip_addresses = [x.removeprefix(prefix).strip() for x in filtered_stdout]
    ip_addresses.reverse()

    result = []
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for address in ip_addresses:
        try:
            ssh.connect(address, username=ssh_username, key_filename=ssh_key_filename)
            result.append(address)
            ssh.close()
            break
        #except (BadHostKeyException, AuthenticationException, SSHException, socket.error) as e:
        except paramiko.ssh_exception.AuthenticationException:
            result.append(address)
            break

    if not result:
        print("I can't find your Raspberry Pi :(")

    print(f'ssh {ssh_username}@{result[0]}')


def main():
    typer.run(searchpi)

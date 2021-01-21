#!/usr/bin/env python3

from simple_automation import Manager
from tasks import TaskZsh

# TODO somehow offload definitions into vault
#vault = Vault("myvault.enc", type='gpg')

# -------- Create Manager --------
manager = Manager()
manager.set("zsh.install", False)

# -------- Define Groups --------
desktop = manager.add_group("desktop")
desktop.set("global.is_desktop", True)

# -------- Define Hosts --------
my_laptop = manager.add_host("my_laptop", ssh_host="localhost")
my_laptop.set_ssh_port(2222)
my_laptop.add_group(desktop)
my_laptop.hostname = "chef"
# TODO my_laptop.set("root_pw", vault_key="")

# -------- Define Tasks --------
task_zsh = manager.add_task(TaskZsh)


def run(context):
    x = context.remote_exec(["echo", "blahh"])
    print(f"{x.return_code=} {x.stdout=} {x.stderr=}")
    task_zsh.exec(context)

if __name__ == "__main__":
    manager.main(run)

#!/usr/bin/env python3

from simple_automation import GpgVault, SymmetricVault, Manager
from tasks import TaskZsh, TaskTrackPortage, TaskTrackInstalledPackages

import os

# TODO - error on using unbound variables in templates

class MySite: # TODO (Inventory):
    def __init__(self, manager):
        self.manager = manager

    def register_vaults(self):
        # -------- Load vault --------
        self.vault = self.manager.add_vault(GpgVault, file="myvault.gpg", recipient="<redacted>")
        #vault = self.manager.add_vault(SymmetricVault, file="myvault_keyfile_static.asc", keyfile="/dev/null")
        #vault = self.manager.add_vault(SymmetricVault, file="myvault_keyfile_env.asc", keyfile=os.environ.get("MY_KEYFILE") or "/dev/null")
        #vault = self.manager.add_vault(SymmetricVault, file="myvault_key_ask.asc")
        #vault = self.manager.add_vault(SymmetricVault, file="myvault_key_env.asc", key=os.environ.get("MY_KEY"))

    def register_tasks(self):
        # -------- Register Tasks --------
        self.manager.add_task(TaskZsh)
        self.manager.add_task(TaskTrackPortage)
        self.manager.add_task(TaskTrackInstalledPackages)

    def register_globals(self):
        # -------- Set global variables --------
        self.manager.set("tasks.zsh.enabled", False)
        self.manager.set("tracking.repo_url", "https://<redacted>@github.com/oddlama/tracked-system-settings")
        self.manager.set("vault", self.vault)

    def register_inventory(self):
        # -------- Define Groups --------
        desktops = self.manager.add_group("desktops")
        desktops.set("system.is_desktop", True)

        # -------- Define Hosts --------
        my_laptop = self.manager.add_host("my_laptop", ssh_host="root@localhost")
        my_laptop.set_ssh_port(2222)
        my_laptop.add_group(desktops)
        my_laptop.hostname = "chef"
        my_laptop.root_pw = self.vault.get("my_laptop.root_pw")

    def run(self, context):
        """
        This function will be executed for each host context,
        and is your main customization point.
        """
        context.run_task(TaskZsh)
        context.run_task(TaskTrackPortage)
        context.run_task(TaskTrackInstalledPackages)

        # TODO if context.host == my_laptop
        # TODO if context.host in desktops: //i.e. desktops in context.hosts.groups

if __name__ == "__main__":
    # -------- Create and run Manager --------
    Manager(MySite).main()

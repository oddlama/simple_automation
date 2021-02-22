#!/usr/bin/env python3

from simple_automation import run_inventory, Inventory, GpgVault
from tasks import TaskZsh, TaskTrackPortage, TaskTrackInstalledPackages

class MySite(Inventory):
    # -------- Register Tasks --------
    tasks = [TaskZsh, TaskTrackPortage, TaskTrackInstalledPackages]

    def register_vaults(self):
        # -------- Load vault --------
        self.vault = self.manager.add_vault(GpgVault, file="myvault.gpg", recipient="your_keyid_or_mail")
        #self.vault = self.manager.add_vault(SymmetricVault, file="myvault_key_ask.asc")
        #vault = self.manager.add_vault(SymmetricVault, file="myvault_keyfile_static.asc", keyfile="/dev/null")
        #vault = self.manager.add_vault(SymmetricVault, file="myvault_keyfile_env.asc", keyfile=os.environ.get("MY_KEYFILE") or "/dev/null")
        #vault = self.manager.add_vault(SymmetricVault, file="myvault_key_env.asc", key=os.environ.get("MY_KEY"))

    def register_globals(self):
        # -------- Set global variables --------
        self.manager.set("tasks.zsh.enabled", False)
        self.manager.copy("tracking.repo_url", self.vault)
        self.manager.set("vault", self.vault)

    def register_inventory(self):
        # -------- Define Groups --------
        desktops = self.manager.add_group("desktops")
        desktops.set("system.is_desktop", True)
        desktops.set("tasks.zsh.enabled", True)

        # -------- Define Hosts --------
        my_laptop = self.manager.add_host("my_laptop", ssh_host="root@localhost")
        my_laptop.set_ssh_port(2222)
        my_laptop.add_group(desktops)
        my_laptop.hostname = "chef"

    def run(self, context):
        context.run_task(TaskZsh)
        context.run_task(TaskTrackPortage)
        context.run_task(TaskTrackInstalledPackages)

# -------- Run the inventory --------
if __name__ == "__main__":
    run_inventory(MySite)

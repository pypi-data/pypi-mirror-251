# import os
# import warnings

# from milatools.cli.init_command import get_windows_home_path_in_wsl
# from milatools.cli.utils import SSHConfig, T, running_inside_WSL

# HOSTS = ["mila", "mila-cpu", "*.server.mila.quebec !login*.server.mila.quebec"]


# def warn_if_using_WSL_and_mila_init_not_done_on_Windows():
#     linux_ssh_config = SSHConfig("~/.ssh/config")
#     if running_inside_WSL() and not _mila_init_also_done_on_windows(linux_ssh_config):
#         warnings.warn(
#             T.orange(
#                 "It seems like you are using the Windows Subsystem for Linux, and "
#                 "haven't yet set-up your SSH config file on the Windows side.\n"
#                 "Make sure to also `pip install milatools` and run `mila init` "
#                 "from a powershell window (assuming you also already installed Python "
#                 "on Windows) so that you can use `mila code` from within WSL without "
#                 "errors."
#             )
#         )


# def _mila_init_also_done_on_windows(linux_ssh_config: SSHConfig) -> bool:
#     assert running_inside_WSL()
#     windows_ssh_config_file_path = get_windows_home_path_in_wsl() / ".ssh/config"
#     if not os.path.exists(windows_ssh_config_file_path):
#         return False
#     windows_ssh_config = SSHConfig(windows_ssh_config_file_path)

#     for host in linux_ssh_config.hosts():
#         if host not in HOSTS:
#             continue  # skip any entries that aren't added by `mila init`
#         linux_entry = linux_ssh_config.host(host)

#     configured_hosts = windows_ssh_config.hosts()

#     if any(host not in configured_hosts for host in ["mila", "mila-cpu"]):
#         return False
#     # TODO: Could do something fancier like checking that the entries we generate are
#     # there, but this should be enough
#     return True

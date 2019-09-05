#!/usr/bin/env python
import os
import sys

from django.core.management import BaseCommand
#
# class Manager(BaseManager):
#     def startup(self):
#         if (command == "runserver"):
#             initialize_background_processes()
#             generate_log_server_connection()
#         elif (command == "syncdb"):
#             generate_db_creation_log()
#         # etc.
#
#     def shutdown(self):
#         send_process_shutdown_signals()
#         close_log_server_connection()
#
# if __name__ == "__main__":
#     manager = Manager()


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "firstsite.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

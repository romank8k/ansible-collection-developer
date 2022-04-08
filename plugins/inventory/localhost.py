from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
    name: localhost
    plugin_type: inventory
'''

import sys

from ansible.plugins.inventory import BaseInventoryPlugin

class InventoryModule(BaseInventoryPlugin):
    NAME = 'localhost'

    def verify_file(self, path):
        valid = False
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(('localhost.yml')):
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)

        self.inventory.add_host('localhost')
        self.inventory.set_variable('localhost', 'ansible_connection', 'local')
        self.inventory.set_variable('localhost', 'ansible_python_interpreter', sys.executable)

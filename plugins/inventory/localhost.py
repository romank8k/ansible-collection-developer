from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
    name: localhost
    plugin_type: inventory
    options:
        plugin:
            description: Plugin name
            required: true
            choices: ['romank8k.developer.localhost']
'''

import os
import sys

from ansible.plugins.inventory import BaseInventoryPlugin

class InventoryModule(BaseInventoryPlugin):
    NAME = 'localhost'

    def __init__(self):
        super(InventoryModule, self).__init__()

    def verify_file(self, path):
        valid = False
        if super(InventoryModule, self).verify_file(path):
            if os.path.basename(path) == 'localhost.yml':
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache=False):
        super(InventoryModule, self).parse(inventory, loader, path, cache=cache)

        self.inventory.add_host('localhost')
        self.inventory.set_variable('localhost', 'ansible_connection', 'local')
        self.inventory.set_variable('localhost', 'ansible_python_interpreter', sys.executable)

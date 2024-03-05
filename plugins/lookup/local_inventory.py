from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    lookup: local_inventory
    description:
      - Serialize inventory with hosts defaulting to localhost.
      - Similar to `ansible-inventory --list --export --yaml`.
"""

RETURN = """
  _list:
    description:
      - Inventory with hosts replaced with localhost.
"""

from ansible.cli.inventory import InventoryCLI
from ansible.plugins.lookup import LookupBase
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader

class LookupModule(LookupBase):
    def __init__(self, **kwargs):
        self.hosts_seen = []

    def run(self, terms, variables, **kwargs):
        inventory = InventoryManager(loader=DataLoader(), sources=variables['inventory_file'])

        return [{
            'all': self._serialize_group(inventory.groups, inventory.groups['all'])
        }]

    def _serialize_group(self, inventory_groups, curr_group):
        group = {}
        if curr_group.child_groups:
            group['children'] = {}
            for child_group in curr_group.child_groups:
                if child_group.name == 'ungrouped' and not child_group.child_groups:
                    continue
                group['children'][child_group.name] = self._serialize_group(inventory_groups, child_group)

        if curr_group.hosts:
            group['hosts'] = {
                'localhost': {}
            }
            for host in curr_group.hosts:
                if host.name in self.hosts_seen:
                    # Similar to 'ansible/cli/inventory.py',
                    # avoid defining host vars more than once.
                    continue
                self.hosts_seen.append(host.name)

                hostvars = host.get_vars()
                InventoryCLI._remove_internal(hostvars)
                if hostvars:
                    group['hosts']['localhost'] = hostvars

        groupvars = curr_group.get_vars()
        InventoryCLI._remove_internal(groupvars)
        if groupvars:
            group['vars'] = groupvars

        return group

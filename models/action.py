from core.models import action
from core import auth, helpers

from plugins.batfish.includes import batfish


class _batfish(action._action):
    
    src_ip = str()
    dst_ip = str()
    dst_port = int()

    def do_action(self, data):

from az.bgp import BaseAdapter, get_adapter
from sh import ssh


class SSHWrapper(BaseAdapter):
    def __init__(self, params):
        self._adapter = None
        super(SSHWrapper, self).__init__(params)

    def init_adapter(self, cfg):
        if not cfg.get('adapter'):
            raise RuntimeError("Required parameter missing for ssh_wrapper: adapter")

        config = {
            'as': self._as,
            'config': cfg.get('adapter_config', {})
        }

        self._adapter = get_adapter(cfg['adapter'])(config)

        host = cfg.get('host', 'localhost')
        user = cfg.get('user')
        identity = cfg.get('identity')

        run = ssh.bake(host)

        if user:
            run = run.bake('-u {}'.format(user))

        if identity:
            run = run.bake('-i {}'.format(identity))

        self._adapter.run = run

    def __getattribute__(self, name):
        public_api = ('get_routed_ips',
                      'route_ips',
                      'unroute_ips')

        if name in public_api:
            return getattr(self._adapter, name)

        return object.__getattribute__(self, name)


def exports(**kwargs):
    return SSHWrapper

class SaltCli(object):
    """
    Salt Master operations
    """
    def __init__(self):
        import salt.config
        import salt.wheel
        import salt.client
        import salt.runner
        self.opts = salt.config.master_config('/etc/salt/master')
        self.opts['quiet'] = True
        self.wheel = salt.wheel.WheelClient(self.opts)
        self.runner = salt.runner.RunnerClient(self.opts)
        self.local = salt.client.LocalClient()

    def lstAcptKey(self):
        """
        List Accepted Keys
        """
        return self.wheel.cmd('key.list', ['accepted'])

    def lstPreKey(self):
        """
        List Unaccepted Keys (minions_pre)
        """
        return self.wheel.cmd('key.list', ['pre'])

    def acptKey(self, name):
        """
        Accept Key (minions_pre)
        """
        self.wheel.cmd('key.accept', [name])

    def acptKeyAll(self):
        """
        Accept all Keys from Unaccepted Keys (minions_pre)
        """
        try:
            lists = self.wheel.cmd('key.list', ['pre'])
            self.wheel.cmd('key.accept', lists['minions_pre'])
            return True
        except Exception, e:
            logger('(SaltCli.acptKeyAll) Fail to accept all minion keys', 'E')
            return False

    def delKey(self, name):
        """
        Delete minion Key
        """
        return self.wheel.cmd_async({'fun': 'key.delete', 'match': name})

    def getInstID(self, name):
        """
        Get EC2 instance ID from minion
        Sample output: {'my_ec2-vm': 'i-zaq123456wsx09876'}
        """
        return self.local.cmd(name, 'cmd.run',
                              ['wget -q -O - http://instance-data/latest/meta-data/instance-id'])

    def getDown(self):
        return self.runner.cmd('manage.down')

    def getUp(self):
        return self.runner.cmd('manage.up')

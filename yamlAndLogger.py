#!/usr/bin/env python
import logging

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
class YmlTool(object):
    """
    yml search
    """
    def __init__(self):
        import re
        import yaml
        self.yaml = yaml
        self.search = re.search

    def do_find(self, data, condition):
        """
        do_find(ymlLoadFile, '<keyword_to_find>')
        """
        if isinstance(data, dict):
            for key, value in data.items():
                match = self.search(condition, key)
                if match:
                    return {key: data[key]}
                else:
                    if self.do_find(value, condition):
                        return {key: data[key]}
                    continue
        elif isinstance(data, list):
            for line in data:
                match = self.search(condition, data)
                if match:
                    return True
        elif isinstance(data, str):
            match = self.search(condition, data)
            if match:
                return True
    def do_update(self, data, keyword, items):
        """
        do_update(file.yml, dictionary key, {'key':'new_text'})
        remark: update will not modify the yml
        """
        self.data = data
        try:
            self.data[keyword].update(items)
        except Exception, e:
            logger('(YmlTool.do_update) Unable to update the dictionary', 'E')
            sys.exit(1)
        return self.data
    def do_load(self, ymlfile):
        """
        do_load('data.yml')
        """
        try:
            config = self.yaml.load(file(ymlfile, 'r'))
            return config
        except self.yaml.YAMLError, exc:
            logger('(YmlTool.do_load) Fail to load %s file' % (ymlfile), 'E')
            sys.exit(1)
        except IOError:
            logger('(YmlTool.do_load) %s not found' % (ymlfile), 'E')
            sys.exit(1)
    def do_write(self, data, ymlfile):
        try:
            self.yaml.dump(data, file(ymlfile, 'w'), default_flow_style=False)
            logger('(YmlTool.do_write) Successfully dumping data into %s' % (ymlfile), 'I')
        except self.yaml.YAMLError, exc:
            logger('(YmlTool.do_write) Unable to write data.yml file', 'E')
            sys.exit(1)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def logger(logline, loglevel):
    """
    Logging and print the logs in stdout
    """
    logging.basicConfig(filename='/tmp/test.log', level=logging.INFO,
                        format='%(asctime)s myscriptname[%(process)d]: %(levelname)s  %(message)s',
                        datefmt='%b %d %T(%Z)')
    loglist = {'I':'INFO', 'W':'WARNING', 'E':'ERROR'}
    if loglevel == 'I':
        logging.info(logline)
    elif loglevel == 'W':
        logging.warning(logline)
    elif loglevel == 'E':
        logging.error(logline)
    print "%s: %s" %(loglist[loglevel], logline)

"""LEXOR: LOG Writer Style

This style displays message nodes provided by other lexor parsing and
converting styles.

"""

from lexor import init
from lexor.core.writer import NodeWriter

INFO = init(
    version=(0, 0, 1, 'final', 0),
    lang='lexor',
    type='writer',
    description='Display messages from parsed/converted documents.',
    url='http://jmlopez-rod.github.io/lexor-lang/lexor-writer-log',
    author='Manuel Lopez',
    author_email='jmlopez.rod@gmail.com',
    license='BSD License',
    path=__file__
)
DEFAULTS = {
    'explanation': 'off',
    'module': 'off',
}


class MsgNW(NodeWriter):
    """Display messages stored in the nodes. """

    def __init__(self, writer):
        NodeWriter.__init__(self, writer)
        self.log = writer.root

    def start(self, node):
        mod = self.log.modules[node['module']]
        exp = self.log.explanation[node['module']]
        mod_msg = mod.MSG[node['code']]
        code_index = exp.get(node['code'], None)
        pos = node['position']
        name = ''
        if self.writer.defaults['module'] in ['true', 'on']:
            name = '[{name}]'
        msg = '{fname}:{line}:{column:2}: %s[{code}] {msg}\n' % name
        msg = msg.format(fname=node['uri'],
                         line=pos[0], column=pos[1],
                         name=node['module'],
                         code=node['code'],
                         msg=mod_msg.format(*node['arg']))
        self.write(msg)
        if self.writer.defaults['explanation'] in ['true', 'on']:
            if code_index is not None:
                self.write('%s\n' % mod.MSG_EXPLANATION[code_index])
            else:
                self.write('\n    No description found.\n\n')


MAPPING = {
    'msg': MsgNW,
}
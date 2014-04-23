# =============================================================================
# Copyright [2014] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================

"""Advanced search and discovery tool.

This tool was built to allow you to query the worlds largest database. The
query strings will be rendered in your local web browser as standard HTML
content. At this time this tool is not compatible with most Server Operating
Systems as they are generally headless and the tool does require access to a
local web browser.
"""


import argparse
import base64
import httplib
import urllib

import asd


def arg_parser():
    """Setup argument Parsing."""
    parser = argparse.ArgumentParser(
        usage='%(prog)s',
        description='Gather information quickly and efficiently',
        epilog='Licensed "Apache 2.0"'
    )

    query_search = argparse.ArgumentParser(add_help=False)

    services = ['nova', 'swift', 'glance', 'keystone', 'heat', 'cinder',
                'ceilometer', 'trove', 'python', 'openstack', 'linux',
                'ubuntu', 'centos', 'mysql', 'rabbitmq', 'lvm', 'kernel',
                'networking', 'ipv4', 'ipv6', 'neutron', 'quantum', 'custom']

    meta = 'Gather information quickly and efficiently from trusted sources'

    subpar = parser.add_subparsers(title='Search Options', metavar=meta)
    for service in services:
        action = subpar.add_parser(
            service,
            parents=[query_search],
            help='Look for "%s" Information' % service
        )
        action.set_defaults(topic=service)
        action.add_argument(
            '--now',
            default=False,
            action='store_true',
            help='Perform a more CPU intense search, will produce faster'
                 ' results.'
        )
        action.add_argument('--query', nargs='*', required=True)
    return parser


class ExternalInformationIndexer(object):
    def __init__(self, config):
        standard_salt = 'aHR0cDovL2xtZ3RmeS5jb20vP3E9'
        optimized_salt = 'aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS93ZWJocCNxPQ=='
        self.config = config

        if self.config.get('now', False) is True:
            self.definition_salt = optimized_salt
        else:
            self.definition_salt = standard_salt

        query = self.config.get('query')
        topic = self.config.get('topic')

        if topic != 'custom':
            query.insert(0, '"%s"' % topic)

        self.query = urllib.quote(' '.join(query))

        with asd.Timer() as time:
            self.indexer()

        print('Advanced Search completed in %s Seconds' % time.interval)

    def indexer(self):
        """Builds the query content for our targeted search."""
        prefix = base64.decodestring(self.definition_salt)
        self.fetch_results(query_text='%s%s' % (prefix, self.query))

    @staticmethod
    def fetch_results(query_text):
        """Opens a web browser tab containing the search information.

        Sends a query request to the Index engine for the provided search
        criteria.

        :param query_text: ``str``
        """
        import webbrowser
        if webbrowser.open(url=query_text) is not True:
            encoder = 'dGlueXVybC5jb20='
            api = 'L2FwaS1jcmVhdGUucGhwP3VybD0lcw=='
            conn = httplib.HTTPConnection(host=base64.decodestring(encoder))
            conn.request('GET', base64.decodestring(api) % query_text)
            resp = conn.getresponse()

            if resp.status >= 300:
                raise httplib.CannotSendRequest('failed to make request...')

            print("It seems that you are not executing from a desktop\n"
                  "operating system or you don't have a brownser installed.\n"
                  "Here is the link to the content that you're looking for.\n")

            print('\nContent: %s\n' % resp.read())


def main():
    """Run Main Program."""
    parser = arg_parser()
    config = vars(parser.parse_args())
    ExternalInformationIndexer(config=config)


if __name__ == '__main__':
    main()

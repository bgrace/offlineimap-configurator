#! /usr/bin/env python

import argparse, yaml

parser = argparse.ArgumentParser()
parser.add_argument('input', type=str)

args = parser.parse_args()
f = file(args.input, 'r')
configuration = yaml.load(f)
f.close()

for account in configuration['accounts']:
    account['account_name'] = account['from']['username'].lower().replace('@', '_').replace('.', '_')

accounts = [account['account_name'] for account in configuration['accounts']]

print "[general]"
if 'general' in configuration:
    for k,v in configuration['general'].items():
        print "{0} = {1}".format(k, v)

print "accounts = {0}\n".format(', '.join(accounts))

yaml_to_offlineimap_keys = {
    'username': 'remoteuser',
    'host': 'remotehost',
    'port': 'remoteport',
    'password': 'remotepass'
}

# Make sure that each email address is appropriately constrained, if we have constraints
if 'allowed_address_domains' in configuration:
    allowed_address_from_domains = configuration['allowed_address_domains'].get('from', [])
    allowed_address_to_domains = configuration['allowed_address_domains'].get('to', [])

    for account in configuration['accounts']:
        from_username, from_domain = account['from']['username'].split('@')
        to_username, to_domain = account['to']['username'].split('@')
        assert from_domain in allowed_address_from_domains, \
            "Unexpected from domain {0} for user {1}@{2}".format(from_domain, from_username, from_domain)
        assert to_domain in allowed_address_to_domains, \
            "Unexpected to domain {0} for user {1}@{2}".format(to_domain, to_username, to_domain)

for account in configuration['accounts']:
    account_name = account['account_name']
    account_from_repository = account_name+"_from"
    account_to_repository = account_name+"_to"

    # Create the Account block, which points to the configuration block from the two mailboxes
    print "[Account {0}]".format(account_name)
    print "localrepository = {0}".format(account_to_repository)
    print "remoterepository = {0}\n".format(account_from_repository)

    # Create the Repository configuration block for the "from" mailbox
    print "[Repository {0}]".format(account_from_repository)

    from_configuration = dict(configuration['defaults']['all'].items() +
                              configuration['defaults']['from'].items() +
                              account['from'].items())

    for k, v in from_configuration.items():
        print "{0} = {1}".format(yaml_to_offlineimap_keys.get(k, k), v)

    print "\n[Repository {0}]".format(account_to_repository)
    to_configuration = dict(configuration['defaults']['all'].items() +
                              configuration['defaults']['to'].items() +
                              account['to'].items())

    for k, v in to_configuration.items():
        print "{0} = {1}".format(yaml_to_offlineimap_keys.get(k, k), v)

    print "\n"





    

        

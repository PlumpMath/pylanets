from . import hullfilters

def combat(ship):
    return hullfilters.combat(ship['hull'])

def combat_large(ship):
    return hullfilters.combat_large(ship['hull'])

def combat_small(ship):
    return hullfilters.combat_small(ship['hull'])

def transport(ship):
    return hullfilters.transport(ship['hull'])

def transport_large(ship):
    return hullfilters.transport_large(ship['hull'])

def transport_small(ship):
    return hullfilters.transport_small(ship['hull'])

def special(ship):
    return hullfilters.special(ship['hull'])

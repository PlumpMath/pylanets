def combat(hull):
    return not transport(hull) and not special(hull)

def combat_large(hull):
    return combat(hull) and hull['mass'] >= 180

def combat_small(hull):
    return combat(hull) and hull['mass'] < 180

def transport(hull):
    return any(map(lambda x:x in hull['name'].lower(), ['transport',
                                                        'freighter']))

def transport_large(hull):
    return transport(hull) and hull['cargo'] >= 500

def transport_small(hull):
    return transport(hull) and hull['cargo'] < 500

def special(hull):
    return any(map(lambda x:x in hull['name'].lower(), ['probe',
                                                        'explorer',
                                                        'tanker',
                                                        'survey',
                                                        'tantrum',
                                                        'refinery',
                                                        'research',
                                                        'alchemy',
                                                        'stargate',
                                                        'neutronic']))

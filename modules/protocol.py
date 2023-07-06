def get_name():
    return f"GET_NAME:"

def put_name(str):
    return f"PUT_NAME:{str}"

def send_conf(conf):
    return f"SEND_CONF:{conf}"

def send_all(msg):
    return f"BROADCAST:{msg}"

def send_turn(option):
    return f"SEND_TURN:{option}"

def send_letter(letter):
    return f"SEND_LETTER:{letter}"

def send_word(word):
    return f"SEND_WORD:{word}"

def send_ranking(ranking):
    return f"SEND_RANKING:{ranking}"

def game_over():
    return f"GAME_OVER:"


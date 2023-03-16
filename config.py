TRd_size = 5

nanowire_length = 512

def read_args(args):
    global nanowire_length
    nanowire_length = args.length

def get_nanowire_size():
    return nanowire_length
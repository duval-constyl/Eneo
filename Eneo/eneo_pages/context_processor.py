from .session import Session

def piece_rechange(request):
    return{'piece_rechange': Session(request)}
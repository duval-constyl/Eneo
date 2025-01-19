class Session():
    def __init__(self, request):
        self.session = request.session

        piece_rechange = self.session.get('session_key')

        if 'session_key' not in request.session:
            piece_rechange = self.session['session_key'] = {}

            self.piece_rechange = piece_rechange
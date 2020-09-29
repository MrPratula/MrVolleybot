
class User:

    def __init__(self,
                 chat_id=None,
                 name=None,
                 surname=None,
                 nickname=None,
                 number=None,
                 bday=None,
                 delays=None,
                 absences=None,
                 fines0=None,
                 fines1=None,
                 active=None):

        self.chat_id = chat_id
        self.name = name
        self.surname = surname
        self.nickname = nickname
        self.number = number
        self.bday = bday
        self.delays = delays
        self.absence = absences
        self.fines0 = fines0
        self.fines1 = fines1
        self.active = active

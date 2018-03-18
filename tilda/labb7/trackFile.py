class Track:
    def __init__(self, trackID, songID, artistName, trackName):
        self.trackID = trackID
        self.songID = songID
        self.artistName = artistName
        self.trackName = trackName

    def __str__(self):
        idspase = 23
        return self.trackID + ' ' * (idspase - len(self.trackID)) + self.songID + ' ' * (idspase - len(self.songID)) + \
               self.artistName + ' ' * (120 - len(self.artistName)) + self.trackName

    def __lt__(self, other):
        if self.artistName < other.artistName:
            return True
        else:
            return False


class Track2:
    def __init__(self, artistID, artistName, trackName,	tracklength, year):
        self.artistID = artistID
        self.artistName = artistName
        self.trackName = trackName
        self.tracklength = float(tracklength)
        self.year = year

    def __str__(self):
        pass

    def __lt__(self, other):
        if self.tracklength < other.tracklength:
            return True
        else:
            return False
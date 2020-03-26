# user's information


class userInfo:
    def __init__(self):
        # info on all landmarks currently considered by user
        self.data = []
        # user latitude
        self.userLatitude = "-75.2509766"
        # user longitude
        self.userLongitude = "-0.071389"
        # landmarks per page
        self.paginationNumber = 12
        # criteria in which landmarks are sorted
        self.sortType = 'Distance'
        # radius in which landmarks are displayed
        self.radius = 1000000
        # is the user using a mobile device
        self.isMobile = False


user = userInfo()

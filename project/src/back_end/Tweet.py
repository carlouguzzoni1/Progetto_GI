class Tweet():

    nTweet=0

    def __init__(self,kwargs):
        for key,value in kwargs.items():
            setattr(self,key,value)
        
    def __str__(self):
        return(str(self.__dict__))

    def getFieldContent(self, field_name):
        return self.field_name

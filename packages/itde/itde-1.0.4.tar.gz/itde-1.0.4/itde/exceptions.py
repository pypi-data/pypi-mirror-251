class ITDEBaseException(BaseException):
    """ 
        InnerTube Data Extractor Base Exception 
    """


class KeyNotFound(ITDEBaseException, KeyError):
    """ 
        Thrown when a required key is not found within the data 
    """


class EndpointNotFound(ITDEBaseException):
    """ 
        Thrown when no endpoint is found in the data
    """


class UnexpectedState(ITDEBaseException):
    """ 
        Thrown when an unexpected state occurs 
        (most likely something in the data structure has changed)
    """


class UnregisteredElement(ITDEBaseException):
    """ 
        Unregistered Element Base Exception
    """


class UnregisteredShelfType(UnregisteredElement):
    """ 
        Thrown when a shelf type has not been registered
    """


class UnregisteredItemType(UnregisteredElement):
    """ 
        Thrown when a item type has not been registered
    """

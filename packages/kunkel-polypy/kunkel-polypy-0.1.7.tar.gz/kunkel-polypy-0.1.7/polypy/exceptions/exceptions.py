# custom error handling

class RequestStatusCodeError(Exception):
    """handles an API request status code != 200"""

    def __init__(self, status_code, reason):
        self.status_code = status_code
        self.reason = reason

    def error_msg(self):
        msg = "\nError!: Response status code: {} > {}.\n".format(self.status_code, self.reason)
        return msg
    
    


class NoDataInResponse(Exception):
    """handles no aggregate data from an API response"""
    
    def __init__(self, request_url, function):
        self.request_url = request_url
        self.function = function

    def error_msg(self):
        request_url = str(request_url)
        function = str(self.function)

        msg = "\nError!: No data in response object in <Function: {}> | <Request:{}>\n".format(function, request_url)
        return msg
    


class EmptyParameter(Exception):
    """handles a required program parameter not being present(p=None/p=Null)"""

    def __init__(self, function):
        self.function = function

    def error_msg(self):

        function = str(self.function)

        msg = "\nError!: Missing required program parameter in <Function: {}>\n".format(function)
        return msg


class InvalidParameterType(Exception):
    """handles recieving a parameter with a type that was unexpected"""

    def __init__(self, parameter, expected_type: type, function):
        self.parameter = parameter
        self.type = expected_type
        self.function = function

    def error_msg(self):
        parameter_type = str(type(self.parameter))
        parameter = str(self.parameter)
        expected_type = self.type
        function = str(self.function)

        msg = "Error!: Expected a {} type parameter, got a {} type instead in <Function: {}> | <Parameter: {}>\nTip: ALL parameters in'request_parameters.yaml should be of <class 'str'> type.\n".format(expected_type, parameter_type, function, parameter)
        return msg
    


class ErrorMessage(Exception):
    """Custom Error messages for built in Exceptions"""

    not_dict_type = "Error!: Expected parameters wrapped in a <dict> object, got a different type instead."


def data_type_validation_int(value, input: str):
    if type(value) is not int:
        raise TypeError(
            __message_validation__(input) + 'int.')


def data_type_validation_str(value, input: str):
    if type(value) is not str:
        raise TypeError(
            __message_validation__(input) + 'str.')


def data_type_validation_float(value, input: str):
    if type(value) is not float:
        raise TypeError(
            __message_validation__(input) + 'float.')


def data_type_validation_float_and_int(value, input):
    if (type(value) is not float) and (type(value) is not int):
        raise TypeError(
            __message_validation__(input) + 'float or int.')


def __message_validation__(input):
    return 'The value of {input} field must be '.format(input=input)

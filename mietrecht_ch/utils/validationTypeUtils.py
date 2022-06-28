from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException


def data_type_validation_int(value, input: int):
    if type(value) is not int:
        raise TypeError(
            'The value of {input} field must be {int}.'.format(input=input, int=int))


def data_type_validation_str(value, input: str):
    if type(value) is not str:
        raise TypeError(
            'The value of {input} field must be {str}.'.format(input=input, str=str))


def data_type_validation_float(value, input: float):
    if type(value) is not float:
        raise TypeError(
            'The value of {input} field must be {float}.'.format(input=input, float=float))


def data_type_validation_float_and_int(value, input):
    if (type(value) is not float) and (type(value) is not int):
        raise TypeError(
            'The value of {input} field must be {float} or {int}.'.format(input=input, float=float, int=int))

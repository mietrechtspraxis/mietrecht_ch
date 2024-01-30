from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException

def data_empty_value(value, input: str):
    if value is None or value == "":
        raise BadRequestException(
            __empty_value_message__(input))


def __empty_value_message__(input):
    return 'No value provided for {input}.'.format(input=input)

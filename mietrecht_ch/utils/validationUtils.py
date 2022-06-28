from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException


def data_validation(value, input: str):
    if value is None or value is "":
        raise BadRequestException(
            'No value provided for {input}'.format(input=input))

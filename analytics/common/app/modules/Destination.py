from common.utils import logging  # pylint: disable=import-error


class Destination:  # pylint: disable=too-few-public-methods
    def __init__(self, destination):
        pass

    def send(self, result):
        pass


def import_destination_types(logger):
    types = {}

    try:
        from modules.KafkaDestination import KafkaDestination  # pylint: disable=import-error
        types["kafka"] = KafkaDestination
    except Exception as error:
        logger.error("Error loading Kafka Destination%s\n" % (error,))
    try:
        from modules.FileDestination import FileDestination  # pylint: disable=import-error
        types["file"] = FileDestination
    except Exception as error:
        logger.error("Error loading FileDestination: %s\n" % (error,))

    return types


logger = logging.get_logger('DestinationTypes', is_static=True)

destination_types = import_destination_types(logger)


def create_instance(request):
    try:
        return destination_types[request["destination"]["type"]](request["destination"])
    except Exception as error:
        logger.error("Error creating destination: %s %s\n" % (request, error))
        return None

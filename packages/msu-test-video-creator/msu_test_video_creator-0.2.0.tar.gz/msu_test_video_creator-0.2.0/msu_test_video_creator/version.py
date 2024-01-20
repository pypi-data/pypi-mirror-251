import importlib.metadata

_DISTRIBUTION_METADATA = importlib.metadata.metadata('msu-test-video-creator')


class Version:

    @staticmethod
    def name():
        return _DISTRIBUTION_METADATA['Version']
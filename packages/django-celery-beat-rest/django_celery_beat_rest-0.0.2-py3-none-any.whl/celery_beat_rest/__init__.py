from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution('django-celery-beat-rest').version
except DistributionNotFound:
    pass

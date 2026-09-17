class MylError(Exception):
    """Base para errores esperables y estructurados del prototipo."""


class CatalogError(MylError):
    pass


class IllegalAction(MylError):
    pass


class UnsupportedCard(MylError):
    pass


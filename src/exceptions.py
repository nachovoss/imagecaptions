class CaptionError(Exception):
    """Base class for exceptions in the caption service."""
    pass

class ModelLoadError(CaptionError):
    """Raised when the model fails to load."""
    pass

class CaptionGenerationError(CaptionError):
    """Raised during failures in caption generation."""
    pass

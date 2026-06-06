"""Template profiling — inspect .pptx templates and generate config."""

from .profile_template import profile_template
from .generate_config import generate_config

__all__ = ["profile_template", "generate_config"]
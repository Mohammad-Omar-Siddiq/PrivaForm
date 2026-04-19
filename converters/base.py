from abc import ABC, abstractmethod
from pathlib import Path

class BaseConverter(ABC):
    """Abstract base class for all format converters"""
    
    def __init__(self, input_file: str, output_file: str):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
    
    @abstractmethod
    def convert(self) -> bool:
        """Convert file. Return True if successful."""
        pass
    
    @abstractmethod
    def validate_input(self) -> bool:
        """Validate input file format."""
        pass
    
    def get_file_size(self) -> int:
        """Get input file size in bytes."""
        return self.input_file.stat().st_size
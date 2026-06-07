# Copyright (C) 2026 Mohammad Omar Mohammad Siddiq Sheikh
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


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

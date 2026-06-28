# Copyright (C) 2026 Mohammad Omar Mohammad Siddiq Sheikh
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import os
import tempfile

from pypdf import PdfReader, PdfWriter


class PdfCompressor:
    """Compress a PDF with local, offline structural optimization."""

    def __init__(self, input_file: str, output_file: str, log_widget=None):
        self.input_file = input_file
        self.output_file = output_file
        self.log_widget = log_widget

    def log(self, message: str):
        if self.log_widget:
            self.log_widget.insert('end', message + '\n')
            self.log_widget.see('end')

    def compress(self) -> bool:
        if not self.input_file:
            self.log("Error: No input PDF provided.")
            return False

        temp_path = None

        try:
            input_size = os.path.getsize(self.input_file)
            self.log("Reading PDF...")

            reader = PdfReader(self.input_file, strict=False)
            writer = PdfWriter()

            for index, page in enumerate(reader.pages, 1):
                try:
                    page.compress_content_streams()
                except Exception as err:
                    self.log(f"  Note: Page {index} stream compression skipped: {err}")
                writer.add_page(page)
                self.log(f"Optimized page {index}")

            if reader.metadata:
                writer.add_metadata(dict(reader.metadata))

            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                temp_path = temp_file.name
                writer.write(temp_file)

            self.log("Applying PDF stream optimization...")
            if not self._optimize_with_pikepdf(temp_path):
                os.replace(temp_path, self.output_file)
                temp_path = None

            output_size = os.path.getsize(self.output_file)
            saved = input_size - output_size
            if saved > 0:
                percent = (saved / input_size) * 100 if input_size else 0
                self.log(f"Saved {self._format_size(saved)} ({percent:.1f}%).")
            else:
                self.log("File was already well optimized; saved PDF is not smaller.")

            return True
        except Exception as e:
            self.log(f"Error compressing PDF: {e}")
            return False
        finally:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass

    def _optimize_with_pikepdf(self, source_path: str) -> bool:
        try:
            import pikepdf

            with pikepdf.Pdf.open(source_path) as pdf:
                pdf.save(
                    self.output_file,
                    compress_streams=True,
                    recompress_flate=True,
                    object_stream_mode=pikepdf.ObjectStreamMode.generate,
                )
            return True
        except Exception as err:
            self.log(f"  Note: Advanced optimization skipped: {err}")
            return False

    def _format_size(self, size: int) -> str:
        for unit in ('bytes', 'KB', 'MB', 'GB'):
            if size < 1024 or unit == 'GB':
                if unit == 'bytes':
                    return f"{size} {unit}"
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} GB"

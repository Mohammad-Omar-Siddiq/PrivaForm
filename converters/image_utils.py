# Copyright (C) 2026 Mohammad Omar Mohammad Siddiq Sheikh
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import io


def image_to_pdf_bytes(image, default_format: str, image_quality: int = 100) -> bytes:
    """Return encoded image bytes for img2pdf, optionally applying JPEG compression."""
    quality = max(1, min(100, int(image_quality)))
    if image.mode != 'RGB':
        image = image.convert('RGB')

    buf = io.BytesIO()
    if quality < 100:
        image.save(buf, format='JPEG', quality=quality, optimize=True)
    else:
        image.save(buf, format=default_format)

    return buf.getvalue()

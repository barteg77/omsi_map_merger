# Copyright 2024 Bartosz Gajewski
#
# This file is part of OMSI Map Merger.
#
# OMSI Map Merger is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# OMSI Map Merger is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OMSI Map Merger. If not, see <http://www.gnu.org/licenses/>.

import logging

logger = logging.getLogger(__name__)

def decoded(file_name: str, encodings: list[str]) -> str:
    for encoding in encodings:
        activity_description: str = f"reading file \"{file_name}\" with encoding  \"{encoding}\"."
        try:
            with open(file_name, encoding=encoding) as f:
                content = f.read()
                logger.debug("Succeeded " + activity_description)
                return content
        except UnicodeError:
            logger.debug("Failed " + activity_description)
    else:
        raise UnicodeError(f"Tried to decode file with encodings: {", ".join(encodings)}, all failed.")

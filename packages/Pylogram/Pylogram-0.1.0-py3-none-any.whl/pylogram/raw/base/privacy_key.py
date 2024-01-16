#  Pylogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2023 Dan <https://github.com/delivrance>
#  Copyright (C) 2023-2024 Pylakey <https://github.com/pylakey>
#
#  This file is part of Pylogram.
#
#  Pylogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pylogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pylogram.  If not, see <http://www.gnu.org/licenses/>.

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from pylogram import raw
from pylogram.raw.core import TLObject

PrivacyKey = Union[raw.types.PrivacyKeyAbout, raw.types.PrivacyKeyAddedByPhone, raw.types.PrivacyKeyChatInvite, raw.types.PrivacyKeyForwards, raw.types.PrivacyKeyPhoneCall, raw.types.PrivacyKeyPhoneNumber, raw.types.PrivacyKeyPhoneP2P, raw.types.PrivacyKeyProfilePhoto, raw.types.PrivacyKeyStatusTimestamp, raw.types.PrivacyKeyVoiceMessages]


# noinspection PyRedeclaration
class PrivacyKey:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 10 constructors available.

        .. currentmodule:: pylogram.raw.types

        .. autosummary::
            :nosignatures:

            PrivacyKeyAbout
            PrivacyKeyAddedByPhone
            PrivacyKeyChatInvite
            PrivacyKeyForwards
            PrivacyKeyPhoneCall
            PrivacyKeyPhoneNumber
            PrivacyKeyPhoneP2P
            PrivacyKeyProfilePhoto
            PrivacyKeyStatusTimestamp
            PrivacyKeyVoiceMessages
    """

    QUALNAME = "pylogram.raw.base.PrivacyKey"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead.")

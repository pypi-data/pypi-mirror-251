# Copyright (c) 2023 Austin S. Hemmelgarn
# SPDX-License-Identifier: MITNFA

'''A command to apply an XSLT document to a group of storage pools.'''

from __future__ import annotations

from typing import Final, final

from ._mixin import StoragePoolMixin
from .._base.xslt import XSLTCommand


@final
class _PoolXSLT(XSLTCommand, StoragePoolMixin):
    pass


xslt: Final = _PoolXSLT(
    name='xslt',
)

__all__ = [
    'xslt'
]

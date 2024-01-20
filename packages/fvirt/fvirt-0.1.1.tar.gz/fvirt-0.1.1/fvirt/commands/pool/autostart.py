# Copyright (c) 2023 Austin S. Hemmelgarn
# SPDX-License-Identifier: MITNFA

'''A command to set the autostart state for one or more storage pools.'''

from __future__ import annotations

from typing import Final, final

from ._mixin import StoragePoolMixin
from .._base.autostart import AutostartCommand


@final
class _PoolAutostart(AutostartCommand, StoragePoolMixin):
    pass


autostart: Final = _PoolAutostart(
    name='autostart',
)

__all__ = (
    'autostart',
)

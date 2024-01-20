# Copyright (c) 2023 Austin S. Hemmelgarn
# SPDX-License-Identifier: MITNFA

'''Command for dumping info for an object.'''

from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING, Self

import click

from .command import Command
from .objects import is_object_mixin

if TYPE_CHECKING:
    from .state import State


class InfoCommand(Command):
    '''Class for commands that prints detailed info about an object.

       This completely encapsulates the callback and all the other
       required info.'''
    def __init__(
        self: Self,
        name: str,
        epilog: str | None = None,
        hidden: bool = False,
        deprecated: bool = False,
    ) -> None:
        assert is_object_mixin(self)

        def cb(
            ctx: click.Context,
            state: State,
            entity: str,
            parent: str | None = None,
        ) -> None:
            output = f'{ self.NAME.title() }: { entity }\n'

            with state.hypervisor as hv:
                if self.HAS_PARENT:
                    assert parent is not None
                    assert self.PARENT_NAME is not None
                    obj = self.get_sub_entity(ctx, hv, parent, entity)
                    output += f'  { self.PARENT_NAME.title() }: { parent }\n'
                else:
                    obj = self.get_entity(ctx, hv, entity)

                for item in self.DISPLAY_PROPS.values():
                    value = getattr(obj, item.prop, None)

                    if value is not None and value != '':
                        if item.use_units:
                            v = state.convert_units(value)
                        else:
                            v = value

                        output += f'  { item.name }: { item.color(v) }\n'

            click.echo(output.rstrip())

        params = self.mixin_params(required=True)

        if self.HAS_PARENT:
            header = dedent(f'''
            Show detailed information about a { self.NAME }.

            The { self.PARENT_METAVAR } argument should specify which {
            self.PARENT_NAME } to look for the { self.NAME } in.
            ''').lstrip().rstrip()
        else:
            header = f'Show detailed information about a { self.NAME }.'

        docstr = header + '\n\n' + dedent(f'''
        A specific { self.NAME } must be specified to retrieve
        information about.
        ''')

        super().__init__(
            name=name,
            help=docstr,
            epilog=epilog,
            callback=cb,
            params=params,
            hidden=hidden,
            deprecated=deprecated,
        )

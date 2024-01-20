# copyright (c) 2023 austin s. hemmelgarn
# spdx-license-identifier: mitnfa

'''Base class used for fvirt commands that apply XSLT documents to objects.'''

from __future__ import annotations

import logging

from textwrap import dedent
from typing import TYPE_CHECKING, Final, Self

import click

from .exitcode import ExitCode
from .match import MatchCommand, get_match_or_entity
from .objects import is_object_mixin
from ...util.match import MatchArgument

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .state import State

LOGGER: Final = logging.getLogger(__name__)


class XSLTCommand(MatchCommand):
    '''Command class for applying XSLT documents to objects.

       This handles the required callback, as well as all the required
       options and generation of the help text.'''
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
                entity: str | None,
                match: MatchArgument | None,
                xslt: str,
                parent: str | None = None
        ) -> None:
            import concurrent.futures

            from lxml import etree

            from ...libvirt.runner import RunnerResult, run_entity_method, run_sub_entity_method
            from ...util.report import summary

            xform = etree.XSLT(etree.parse(xslt))

            with state.hypervisor as hv:
                uri = hv.uri

                if self.HAS_PARENT:
                    assert self.PARENT_ATTR is not None

                    parent_obj = self.get_parent_obj(ctx, hv, parent)

                    futures: Sequence[concurrent.futures.Future] = [state.pool.submit(
                        run_sub_entity_method,
                        uri=uri,
                        hvprop=self.PARENT_ATTR,
                        parentprop=self.LOOKUP_ATTR,
                        method='apply_xslt',
                        ident=(parent_obj.name, e.name),
                        arguments=[xform],
                    ) for e in get_match_or_entity(
                        hv=hv,
                        obj=self,
                        match=match,
                        entity=entity,
                        ctx=ctx,
                    )]
                else:
                    futures = [state.pool.submit(
                        run_entity_method,
                        uri=uri,
                        hvprop=self.LOOKUP_ATTR,
                        method='apply_xslt',
                        ident=e.name,
                        arguments=[xform],
                    ) for e in get_match_or_entity(
                        hv=hv,
                        obj=self,
                        match=match,
                        entity=entity,
                        ctx=ctx,
                    )]

            success = 0

            for f in concurrent.futures.as_completed(futures):
                try:
                    match f.result():
                        case RunnerResult(attrs_found=False) as r:
                            name = r.ident

                            if parent is not None:
                                name = r.ident[1]

                            LOGGER.critical(f'Unexpected internal error processing { self.NAME } "{ name }"')
                            ctx.exit(ExitCode.OPERATION_FAILED)
                        case RunnerResult(entity_found=False) as r if parent is None:
                            LOGGER.error(f'{ self.NAME } "{ r.ident }" disappeared before we could modify it.')

                            if state.fail_fast:
                                break
                        case RunnerResult(entity_found=False) as r:
                            LOGGER.critical(f'{ self.PARENT_NAME } "{ r.ident[0] }" not found when trying to modify { self.NAME } "{ r.ident[1] }".')
                            break  # Can't recover in this case, but we should still print our normal summary.
                        case RunnerResult(entity_found=True, sub_entity_found=False) as r:
                            LOGGER.warning(f'{ self.NAME } "{ r.ident[1] }" disappeared before we could modify it.')

                            if state.fail_fast:
                                break
                        case RunnerResult(method_success=False) as r:
                            name = r.ident

                            if parent is not None:
                                name = r.ident[1]

                            LOGGER.error(f'Failed to modify { self.NAME } "{ name }".')

                            if state.fail_fast:
                                break
                        case RunnerResult(method_success=True) as r:
                            name = r.ident

                            if parent is not None:
                                name = r.ident[1]

                            LOGGER.info(f'Successfully modified { self.NAME } "{ name }".')
                            success += 1
                        case _:
                            raise RuntimeError
                except Exception as e:
                    LOGGER.error('Encountered unexpected error while attempting to modify { self.NAME }', exc_info=e)

                    if state.fail_fast:
                        break

            click.echo(f'Finished modifying specified { self.NAME }s using XSLT document at { xslt }.')
            click.echo('')
            click.echo(summary(
                total=len(futures),
                success=success,
            ))

            if success != len(futures):
                ctx.exit(ExitCode.OPERATION_FAILED)

        if self.HAS_PARENT:
            header = f'''
            Apply an XSLT document to one or more { self.NAME }s in a given { self.PARENT_NAME }.

            A { self.PARENT_NAME } must be exlicitly specified with the { self.PARENT_METAVAR }
            argument.
            '''
        else:
            header = f'Apply an XSLT document to one or more { self.NAME }s.'

        body = f'''
        Either a specific { self.NAME } name to modify should be specified as
        { self.METAVAR }, or matching parameters should be specified using the --match
        option, which will then cause all matching { self.NAME }s to be modified.

        XSLT must be a path to a valid XSLT document. It must specify an
        output element, and the output element must specify an encoding
        of UTF-8. Note that xsl:strip-space directives may cause issues
        in the XSLT processor.

        This command supports fvirt's fail-fast logic. In fail-fast mode,
        the first { self.NAME } which the XSLT document fails to apply to will
        cause the operation to stop, and any failure will result in a
        non-zero exit code.

        This command does not support fvirt's idempotent mode. It's
        behavior will not change regardless of whether idempotent mode
        is enabled or not.'''

        docstr = dedent(f'{ header }\n{ body }').lstrip()

        params = (
            click.Argument(
                param_decls=('xslt',),
                nargs=1,
                type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True),
                required=True,
            ),
        ) + self.mixin_params()

        super().__init__(
            name=name,
            help=docstr,
            epilog=epilog,
            callback=cb,
            params=params,
            hidden=hidden,
            deprecated=deprecated,
        )

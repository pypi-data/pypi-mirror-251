# Copyright (c) 2023 Austin S. Hemmelgarn
# SPDX-License-Identifier: MITNFA

'''Pydantic models for storage pool templating.'''

from __future__ import annotations

import functools

from ipaddress import IPv4Address, IPv6Address
from typing import Annotated, Final, Self
from uuid import UUID

from pydantic import Field, model_validator

from ._types import FilePath, Hostname, Model, NonEmptyString, V_YesNo

FORMATS: Final = {
    'auto': {'fs', 'netfs'},
    'bsd': {'disk'},
    'cifs': {'netfs'},
    'dos': {'disk'},
    'dvh': {'disk'},
    'ext2': {'fs'},
    'ext3': {'fs'},
    'ext4': {'fs'},
    'gfs2': {'fs'},
    'gfs': {'fs'},
    'gluster': {'netfs'},
    'gpt': {'disk'},
    'hfs+': {'fs'},
    'iso9660': {'fs'},
    'mac': {'disk'},
    'nfs': {'netfs'},
    'ocfs2': {'fs'},
    'pc98': {'disk'},
    'sun': {'disk'},
    'udf': {'fs'},
    'ufs': {'fs'},
    'vfat': {'fs'},
    'vmfs': {'fs'},
    'xfs': {'fs'},
}

FORMAT_TYPES: Final = functools.reduce(lambda x, y: x | y, FORMATS.values())

SOURCE_DIR_TYPES: Final = {
    'netfs',
    'gluster',
}

OPTIONAL_SOURCE_DEVICE_TYPES: Final = {
    'zfs',
}

SINGLE_SOURCE_DEVICE_TYPES: Final = {
    'fs',
    'disk',
    'iscsi',
    'iscsi-direct',
}

MULTI_SOURCE_DEVICE_TYPES: Final = {
    'logical',
}

SOURCE_DEVICE_TYPES: Final = SINGLE_SOURCE_DEVICE_TYPES | MULTI_SOURCE_DEVICE_TYPES

SINGLE_SOURCE_HOST_TYPES: Final = {
    'iscsi',
    'iscsi-direct',
}

MULTI_SOURCE_HOST_TYPES: Final = {
    'netfs',
    'rbd',
    'gluster',
}

SOURCE_HOST_TYPES: Final = SINGLE_SOURCE_HOST_TYPES | MULTI_SOURCE_HOST_TYPES

SOURCE_INITIATOR_TYPES: Final = {
    'iscsi-direct',
}

SOURCE_ADAPTER_TYPES: Final = {
    'scsi',
}

SOURCE_NAME_TYPES: Final = {
    'rbd',
    'gluster',
    'zfs',
    'vstorage',
}

SOURCE_TYPES: Final = functools.reduce(lambda x, y: x | y, (
    FORMAT_TYPES,
    SOURCE_DIR_TYPES,
    OPTIONAL_SOURCE_DEVICE_TYPES,
    SOURCE_DEVICE_TYPES,
    SOURCE_HOST_TYPES,
    SOURCE_INITIATOR_TYPES,
    SOURCE_ADAPTER_TYPES,
    SOURCE_NAME_TYPES,
))

COW_TYPES: Final = {
    'dir',
    'fs',
}

FEATURES_TYPES: Final = functools.reduce(lambda x, y: x | y, (
    COW_TYPES,
))

TARGET_TYPES: Final = {
    'dir',
    'fs',
    'netfs',
    'logical',
    'disk',
    'iscsi',
    'scsi',
    'vstorage'
}

TYPES: Final = {
    'multipath',
} | SOURCE_TYPES | TARGET_TYPES


class PoolFeatures(Model):
    '''Model representing features for a storage pool.'''
    cow: V_YesNo | None = Field(
        default=None,
        description='Whether to globally support COW semantics for the pool. ' +
                    f'Only supported for pools of the following types: {", ".join(COW_TYPES)}',
    )


class PoolSource(Model):
    '''Model representing the source for a storage pool.'''
    format: Annotated[str, Field(pattern=f'^({"|".join(FORMATS.keys())})$')] | None = Field(
        default=None,
        description='Format for the storage pool source. Valid values depend on the pool type. ' +
                    'See https://libvirt.org/storage.html for more information.',
    )
    dir: Annotated[str, Field(pattern='^/.*$')] | None = Field(
        default=None,
        description='Directory on the remote server to use for storing volumes. ' +
                    f'Only supported for pools of the following types: {", ".join(SOURCE_DIR_TYPES)}',
    )
    devices: list[NonEmptyString] | None = Field(
        default=None,
        min_length=1,
        description='A list of devices used to store pool data. ' +
                    f'Only supported for pools of the following types: {", ".join(SOURCE_DEVICE_TYPES | OPTIONAL_SOURCE_DEVICE_TYPES)}',
    )
    hosts: list[Hostname | IPv4Address | IPv6Address] | None = Field(
        default=None,
        min_length=1,
        description='A list of network hosts used to store pool data. ' +
                    f'Only supported for pools of the following types: {", ".join(SOURCE_HOST_TYPES)}',
    )
    initiator: NonEmptyString | None = Field(
        default=None,
        description='The iSCSI initiator to use for this pool. ' +
                    f'Only supported for pools of the following types: {", ".join(SOURCE_INITIATOR_TYPES)}',
    )
    adapter: NonEmptyString | None = Field(
        default=None,
        description='The host bus adapter to use for this pool.' +
                    f'Only supported for pools of the following types: {", ".join(SOURCE_ADAPTER_TYPES)}',
    )
    name: NonEmptyString | None = Field(
        default=None,
        description='The name of the source pool to use for this pool.' +
                    f'Only supported for pools of the following types: {", ".join(SOURCE_NAME_TYPES)}',
    )

    @model_validator(mode='after')
    def check_props(self: Self) -> Self:
        if not self.model_fields_set:
            raise ValueError('An empty pool source should be represented by not including it in PoolInfo.')

        return self


class PoolTarget(Model):
    '''Model representing the target for a storage pool.'''
    path: FilePath = Field(
        description='The path to the directory to use as the target for this pool.'
    )


class PoolInfo(Model):
    '''Model representing a storage pool for templating.'''
    type: str = Field(
        pattern=f'^({"|".join(TYPES)})$',
        description='The type of storage pool.'
    )
    name: NonEmptyString = Field(
        description='The name of the storage pool.',
    )
    uuid: UUID | None = Field(
        default=None,
        description='UUID of the storage pool. If not specified, libvirt will automatically assign a newly generated UUID.',
    )
    features: PoolFeatures | None = Field(
        default=None,
        description='Features configuration for the storage pool. ' +
                    f'Only supported for pools of the following types: {", ".join(FEATURES_TYPES)}',
    )
    source: PoolSource | None = Field(
        default=None,
        description='Source configuration for the storage pool. ' +
                    f'Only supported for pools of the following types: {", ".join(SOURCE_TYPES)}',
    )
    target: PoolTarget | None = Field(
        default=None,
        description='Target configuration for the storage pool. ' +
                    f'Only supported for pools of the following types: {", ".join(TARGET_TYPES)}',
    )

    @model_validator(mode='after')
    def check_features(self: Self) -> Self:
        if self.features is None:
            return self

        if self.features.cow is not None and self.type not in COW_TYPES:
            raise ValueError('The "cow" feature may only be specified for "dir" or "fs" type pools.')

        return self

    @model_validator(mode='after')
    def check_source(self: Self) -> Self:
        if self.type not in SOURCE_TYPES:
            if self.source is not None:
                raise ValueError(f'Sources are not supported for "{ self.type }" type pools.')

            return self

        if self.source is None:
            raise ValueError(f'Source must be specified for "{ self.type }" type pools.')

        invalid_source_props = set(PoolSource.__annotations__.keys())

        if self.type in FORMAT_TYPES:
            if self.source.format is None:
                raise ValueError(f'Source format must be specified for "{ self.type }" type pools.')
            elif self.source.format not in FORMATS:
                raise ValueError(f'Unrecognized source format "{ self.source.format }".')
            elif self.type not in FORMATS[self.source.format]:
                raise ValueError(f'Source format "{ self.source.format }" not supported for "{ self.type }" type pools.')

            invalid_source_props.discard('format')

        if self.type in SOURCE_DIR_TYPES:
            if self.source.dir is None:
                raise ValueError(f'Source directory must be specified for "{ self.type }" type pools.')

            invalid_source_props.discard('dir')

        if self.type in OPTIONAL_SOURCE_DEVICE_TYPES:
            invalid_source_props.discard('devices')

        if self.type in SOURCE_DEVICE_TYPES:
            if self.source.devices is None:
                raise ValueError(f'Source device must be specified for "{ self.type }" type pools.')

            invalid_source_props.discard('devices')

            if self.type in SINGLE_SOURCE_DEVICE_TYPES:
                if len(self.source.devices) != 1:
                    raise ValueError(f'Only one source device may be specified for "{ self.type }" type pools.')

        if self.type in SOURCE_HOST_TYPES:
            if not self.source.hosts:
                raise ValueError(f'Source host must be specified for "{ self.type }" type pools.')

            invalid_source_props.discard('hosts')

            if self.type in SINGLE_SOURCE_HOST_TYPES:
                if len(self.source.hosts) != 1:
                    raise ValueError(f'Only one source host may be specified for "{ self.type }" type pools.')

        if self.type in SOURCE_INITIATOR_TYPES:
            if not self.source.initiator:
                raise ValueError(f'Source initiator must be specified for "{ self.type }" type pools.')

            invalid_source_props.discard('initiator')

        if self.type in SOURCE_ADAPTER_TYPES:
            if not self.source.adapter:
                raise ValueError(f'Source adapter must be specified for "{ self.type }" type pools.')

            invalid_source_props.discard('adapter')

        if self.type in SOURCE_NAME_TYPES:
            if not self.source.name:
                raise ValueError(f'Source name must be specified for "{ self.type }" type pools.')

            invalid_source_props.discard('name')

        for prop in invalid_source_props:
            if getattr(self.source, prop) is not None:
                raise ValueError(f'Source { prop } is not supported for "{ self.type }" type pools.')

        return self

    @model_validator(mode='after')
    def check_target(self: Self) -> Self:
        if self.type in TARGET_TYPES:
            if self.target is None:
                raise ValueError(f'Target must be specified for "{ self.type }" type pools.')
        else:
            if self.target is not None:
                raise ValueError(f'Target is not supported for "{ self.type }" type pools.')

            return self

        return self

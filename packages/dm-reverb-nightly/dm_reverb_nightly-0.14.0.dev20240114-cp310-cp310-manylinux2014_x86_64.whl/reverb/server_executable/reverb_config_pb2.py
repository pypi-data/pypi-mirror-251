# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: reverb/server_executable/reverb_config.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from reverb.cc.checkpointing import checkpoint_pb2 as reverb_dot_cc_dot_checkpointing_dot_checkpoint__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,reverb/server_executable/reverb_config.proto\x12\x0f\x64\x65\x65pmind.reverb\x1a(reverb/cc/checkpointing/checkpoint.proto\"\\\n\x12ReverbServerConfig\x12\x38\n\x06tables\x18\x01 \x03(\x0b\x32(.deepmind.reverb.PriorityTableCheckpoint\x12\x0c\n\x04port\x18\x02 \x01(\x05\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'reverb.server_executable.reverb_config_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REVERBSERVERCONFIG._serialized_start=107
  _REVERBSERVERCONFIG._serialized_end=199
# @@protoc_insertion_point(module_scope)

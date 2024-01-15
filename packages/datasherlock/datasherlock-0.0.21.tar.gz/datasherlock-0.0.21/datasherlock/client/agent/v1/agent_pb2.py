# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: client/agent/v1/agent.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from validate import validate_pb2 as validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1b\x63lient/agent/v1/agent.proto\x12\x0f\x63lient.agent.v1\x1a\x17validate/validate.proto\"\x12\n\x10HeartbeatRequest\"B\n\x11HeartbeatResponse\x12-\n\x04meta\x18\x01 \x01(\x0b\x32\x19.client.agent.v1.MetaInfoR\x04meta\"\x82\x01\n\x0f\x41skAgentRequest\x12/\n\x08question\x18\x01 \x01(\tB\x13\xfa\x42\x10\x8a\x01\x02\x10\x01\x9a\x01\x08\"\x06r\x04\x10\x03\x18\x64R\x08question\x12\x1e\n\x05\x65rror\x18\x03 \x01(\tB\x08\xfa\x42\x05\x8a\x01\x02\x10\x00R\x05\x65rror\x12\x1e\n\x05query\x18\x04 \x01(\tB\x08\xfa\x42\x05\x8a\x01\x02\x10\x00R\x05query\"}\n\x10\x41skAgentResponse\x12\x10\n\x03sql\x18\x01 \x01(\tR\x03sql\x12\x14\n\x05\x65rror\x18\x02 \x01(\tR\x05\x65rror\x12-\n\x04meta\x18\x03 \x01(\x0b\x32\x19.client.agent.v1.MetaInfoR\x04meta\x12\x12\n\x04\x64\x61ta\x18\x04 \x01(\tR\x04\x64\x61ta\"\xaa\x01\n\x08MetaInfo\x12\x1a\n\x08\x64\x61tabase\x18\x01 \x01(\tR\x08\x64\x61tabase\x12\x1a\n\x08username\x18\x02 \x01(\tR\x08username\x12\x12\n\x04host\x18\x03 \x01(\tR\x04host\x12\x12\n\x04type\x18\x04 \x01(\tR\x04type\x12\x16\n\x06schema\x18\x05 \x01(\tR\x06schema\x12\x16\n\x06tables\x18\x06 \x03(\tR\x06tables\x12\x0e\n\x02id\x18\x07 \x01(\tR\x02id2\xb2\x01\n\x0c\x41gentService\x12L\n\x03\x41sk\x12 .client.agent.v1.AskAgentRequest\x1a!.client.agent.v1.AskAgentResponse\"\x00\x12T\n\tHeartbeat\x12!.client.agent.v1.HeartbeatRequest\x1a\".client.agent.v1.HeartbeatResponse\"\x00\x42\xc4\x01\n\x13\x63om.client.agent.v1B\nAgentProtoP\x01ZCgithub.com/datasherlocks/cloud/internal/gen/client/agent/v1;agentv1\xa2\x02\x03\x43\x41X\xaa\x02\x0f\x43lient.Agent.V1\xca\x02\x0f\x43lient\\Agent\\V1\xe2\x02\x1b\x43lient\\Agent\\V1\\GPBMetadata\xea\x02\x11\x43lient::Agent::V1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'client.agent.v1.agent_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\023com.client.agent.v1B\nAgentProtoP\001ZCgithub.com/datasherlocks/cloud/internal/gen/client/agent/v1;agentv1\242\002\003CAX\252\002\017Client.Agent.V1\312\002\017Client\\Agent\\V1\342\002\033Client\\Agent\\V1\\GPBMetadata\352\002\021Client::Agent::V1'
  _globals['_ASKAGENTREQUEST'].fields_by_name['question']._options = None
  _globals['_ASKAGENTREQUEST'].fields_by_name['question']._serialized_options = b'\372B\020\212\001\002\020\001\232\001\010\"\006r\004\020\003\030d'
  _globals['_ASKAGENTREQUEST'].fields_by_name['error']._options = None
  _globals['_ASKAGENTREQUEST'].fields_by_name['error']._serialized_options = b'\372B\005\212\001\002\020\000'
  _globals['_ASKAGENTREQUEST'].fields_by_name['query']._options = None
  _globals['_ASKAGENTREQUEST'].fields_by_name['query']._serialized_options = b'\372B\005\212\001\002\020\000'
  _globals['_HEARTBEATREQUEST']._serialized_start=73
  _globals['_HEARTBEATREQUEST']._serialized_end=91
  _globals['_HEARTBEATRESPONSE']._serialized_start=93
  _globals['_HEARTBEATRESPONSE']._serialized_end=159
  _globals['_ASKAGENTREQUEST']._serialized_start=162
  _globals['_ASKAGENTREQUEST']._serialized_end=292
  _globals['_ASKAGENTRESPONSE']._serialized_start=294
  _globals['_ASKAGENTRESPONSE']._serialized_end=419
  _globals['_METAINFO']._serialized_start=422
  _globals['_METAINFO']._serialized_end=592
  _globals['_AGENTSERVICE']._serialized_start=595
  _globals['_AGENTSERVICE']._serialized_end=773
# @@protoc_insertion_point(module_scope)

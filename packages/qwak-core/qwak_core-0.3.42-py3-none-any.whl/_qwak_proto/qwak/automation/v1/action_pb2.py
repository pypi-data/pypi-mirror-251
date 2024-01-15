# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qwak/automation/v1/action.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from _qwak_proto.qwak.automation.v1 import common_pb2 as qwak_dot_automation_dot_v1_dot_common__pb2
from _qwak_proto.qwak.automation.v1 import auto_scaling_pb2 as qwak_dot_automation_dot_v1_dot_auto__scaling__pb2
from _qwak_proto.qwak.batch_job.v1 import batch_job_service_pb2 as qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2
from _qwak_proto.qwak.user_application.common.v0 import resources_pb2 as qwak_dot_user__application_dot_common_dot_v0_dot_resources__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fqwak/automation/v1/action.proto\x12\x12qwak.automation.v1\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1fqwak/automation/v1/common.proto\x1a%qwak/automation/v1/auto_scaling.proto\x1a)qwak/batch_job/v1/batch_job_service.proto\x1a/qwak/user_application/common/v0/resources.proto\"\x99\x01\n\x06\x41\x63tion\x12@\n\x0c\x62uild_deploy\x18\x01 \x01(\x0b\x32(.qwak.automation.v1.BuildAndDeployActionH\x00\x12\x43\n\x0f\x62\x61tch_execution\x18\x02 \x01(\x0b\x32(.qwak.automation.v1.BatchExecutionActionH\x00\x42\x08\n\x06\x61\x63tion\"Q\n\x14\x42\x61tchExecutionAction\x12\x39\n\x11\x65xecute_batch_job\x18\x01 \x01(\x0b\x32\x1e.qwak.batchjob.BatchJobRequest\"\xcd\x01\n\x14\x42uildAndDeployAction\x12\x31\n\nbuild_spec\x18\x01 \x01(\x0b\x32\x1d.qwak.automation.v1.BuildSpec\x12\x45\n\x14\x64\x65ployment_condition\x18\x02 \x01(\x0b\x32\'.qwak.automation.v1.DeploymentCondition\x12;\n\x0f\x64\x65ployment_spec\x18\x03 \x01(\x0b\x32\".qwak.automation.v1.DeploymentSpec\"d\n\x13\x44\x65ploymentCondition\x12@\n\x0c\x62uild_metric\x18\x01 \x01(\x0b\x32(.qwak.automation.v1.BuildMetricConditionH\x00\x42\x0b\n\tcondition\"\x89\x01\n\x14\x42uildMetricCondition\x12\x13\n\x0bmetric_name\x18\x01 \x01(\t\x12I\n\x13threshold_direction\x18\x02 \x01(\x0e\x32,.qwak.automation.v1.MetricThresholdDirection\x12\x11\n\tthreshold\x18\x03 \x01(\t\"\xdf\x01\n\x0e\x44\x65ploymentSpec\x12;\n\x0f\x64\x65ployment_size\x18\x01 \x01(\x0b\x32\".qwak.automation.v1.DeploymentSize\x12G\n\x10\x61\x64vanced_options\x18\x02 \x01(\x0b\x32-.qwak.automation.v1.AdvancedDeploymentOptions\x12\x1f\n\x17selected_variation_name\x18\x03 \x01(\t\x12\x14\n\x0c\x65nvironments\x18\x04 \x03(\t\x12\x10\n\x08\x65nv_vars\x18\x05 \x03(\t\"\x9b\x02\n\x19\x41\x64vancedDeploymentOptions\x12%\n\x1dnumber_of_http_server_workers\x18\x01 \x01(\x05\x12\x1f\n\x17http_request_timeout_ms\x18\x02 \x01(\x05\x12\x13\n\x0b\x64\x61\x65mon_mode\x18\x03 \x01(\x08\x12\x1b\n\x13\x63ustom_iam_role_arn\x18\x04 \x01(\t\x12\x42\n\x13\x61uto_scaling_config\x18\x05 \x01(\x0b\x32%.qwak.automation.v1.AutoScalingConfig\x12\x16\n\x0emax_batch_size\x18\x06 \x01(\x05\x12(\n deployment_process_timeout_limit\x18\x07 \x01(\x05\"\xad\x02\n\x0e\x44\x65ploymentSize\x12\x16\n\x0enumber_of_pods\x18\x01 \x01(\x05\x12\x0f\n\x03\x63pu\x18\x02 \x01(\x02\x42\x02\x18\x01\x12\x19\n\rmemory_amount\x18\x03 \x01(\x05\x42\x02\x18\x01\x12\x38\n\x0cmemory_units\x18\x04 \x01(\x0e\x32\x1e.qwak.automation.v1.MemoryUnitB\x02\x18\x01\x12;\n\rgpu_resources\x18\x05 \x01(\x0b\x32 .qwak.automation.v1.GpuResourcesB\x02\x18\x01\x12`\n\x1c\x63lient_pod_compute_resources\x18\x06 \x01(\x0b\x32:.qwak.user_application.common.v0.ClientPodComputeResources\"\xb6\x03\n\tBuildSpec\x12<\n\x10git_model_source\x18\x01 \x01(\x0b\x32\".qwak.automation.v1.GitModelSource\x12\x41\n\nparameters\x18\x02 \x03(\x0b\x32-.qwak.automation.v1.BuildSpec.ParametersEntry\x12\x0c\n\x04tags\x18\x03 \x03(\t\x12\x12\n\nbase_image\x18\x04 \x01(\t\x12\x18\n\x10\x61ssumed_iam_role\x18\x05 \x01(\t\x12/\n\x08resource\x18\x06 \x01(\x0b\x32\x1d.qwak.automation.v1.Resources\x12\x10\n\x08main_dir\x18\x07 \x01(\t\x12\x1c\n\x14\x64\x65pendency_file_path\x18\x08 \x01(\t\x12\x10\n\x08\x65nv_vars\x18\t \x03(\t\x12\x16\n\x0egpu_compatible\x18\n \x01(\x08\x12.\n\npush_image\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x1a\x31\n\x0fParametersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xf9\x01\n\tResources\x12=\n\rcpu_resources\x18\x01 \x01(\x0b\x32 .qwak.automation.v1.CpuResourcesB\x02\x18\x01H\x00\x12=\n\rgpu_resources\x18\x02 \x01(\x0b\x32 .qwak.automation.v1.GpuResourcesB\x02\x18\x01H\x00\x12\x62\n\x1c\x63lient_pod_compute_resources\x18\x03 \x01(\x0b\x32:.qwak.user_application.common.v0.ClientPodComputeResourcesH\x00\x42\n\n\x08resource\"h\n\x0c\x43puResources\x12\x0b\n\x03\x63pu\x18\x01 \x01(\x02\x12\x15\n\rmemory_amount\x18\x02 \x01(\x05\x12\x34\n\x0cmemory_units\x18\x03 \x01(\x0e\x32\x1e.qwak.automation.v1.MemoryUnit\"Q\n\x0cGpuResources\x12-\n\x08gpu_type\x18\x01 \x01(\x0e\x32\x1b.qwak.automation.v1.GpuType\x12\x12\n\ngpu_amount\x18\x02 \x01(\x05\"w\n\x0eGitModelSource\x12\x0f\n\x07git_uri\x18\x01 \x01(\t\x12#\n\x1bgit_credentials_secret_name\x18\x02 \x01(\t\x12\x12\n\ngit_branch\x18\x03 \x01(\t\x12\x1b\n\x13git_ssh_secret_name\x18\x04 \x01(\t*w\n\x07GpuType\x12\x0b\n\x07INVALID\x10\x00\x12\x0e\n\nNVIDIA_K80\x10\x01\x12\x0f\n\x0bNVIDIA_V100\x10\x02\x12\x0f\n\x0bNVIDIA_A100\x10\x03\x12\r\n\tNVIDIA_T4\x10\x04\x12\x0f\n\x0bNVIDIA_A10G\x10\x05\x12\r\n\tNVIDIA_L4\x10\x06*+\n\nMemoryUnit\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x07\n\x03MIB\x10\x01\x12\x07\n\x03GIB\x10\x02\x42!\n\x1d\x63om.qwak.ai.automation.api.v1P\x01\x62\x06proto3')

_GPUTYPE = DESCRIPTOR.enum_types_by_name['GpuType']
GpuType = enum_type_wrapper.EnumTypeWrapper(_GPUTYPE)
_MEMORYUNIT = DESCRIPTOR.enum_types_by_name['MemoryUnit']
MemoryUnit = enum_type_wrapper.EnumTypeWrapper(_MEMORYUNIT)
INVALID = 0
NVIDIA_K80 = 1
NVIDIA_V100 = 2
NVIDIA_A100 = 3
NVIDIA_T4 = 4
NVIDIA_A10G = 5
NVIDIA_L4 = 6
UNKNOWN = 0
MIB = 1
GIB = 2


_ACTION = DESCRIPTOR.message_types_by_name['Action']
_BATCHEXECUTIONACTION = DESCRIPTOR.message_types_by_name['BatchExecutionAction']
_BUILDANDDEPLOYACTION = DESCRIPTOR.message_types_by_name['BuildAndDeployAction']
_DEPLOYMENTCONDITION = DESCRIPTOR.message_types_by_name['DeploymentCondition']
_BUILDMETRICCONDITION = DESCRIPTOR.message_types_by_name['BuildMetricCondition']
_DEPLOYMENTSPEC = DESCRIPTOR.message_types_by_name['DeploymentSpec']
_ADVANCEDDEPLOYMENTOPTIONS = DESCRIPTOR.message_types_by_name['AdvancedDeploymentOptions']
_DEPLOYMENTSIZE = DESCRIPTOR.message_types_by_name['DeploymentSize']
_BUILDSPEC = DESCRIPTOR.message_types_by_name['BuildSpec']
_BUILDSPEC_PARAMETERSENTRY = _BUILDSPEC.nested_types_by_name['ParametersEntry']
_RESOURCES = DESCRIPTOR.message_types_by_name['Resources']
_CPURESOURCES = DESCRIPTOR.message_types_by_name['CpuResources']
_GPURESOURCES = DESCRIPTOR.message_types_by_name['GpuResources']
_GITMODELSOURCE = DESCRIPTOR.message_types_by_name['GitModelSource']
Action = _reflection.GeneratedProtocolMessageType('Action', (_message.Message,), {
  'DESCRIPTOR' : _ACTION,
  '__module__' : 'qwak.automation.v1.action_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.Action)
  })
_sym_db.RegisterMessage(Action)

BatchExecutionAction = _reflection.GeneratedProtocolMessageType('BatchExecutionAction', (_message.Message,), {
  'DESCRIPTOR' : _BATCHEXECUTIONACTION,
  '__module__' : 'qwak.automation.v1.action_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.BatchExecutionAction)
  })
_sym_db.RegisterMessage(BatchExecutionAction)

BuildAndDeployAction = _reflection.GeneratedProtocolMessageType('BuildAndDeployAction', (_message.Message,), {
  'DESCRIPTOR' : _BUILDANDDEPLOYACTION,
  '__module__' : 'qwak.automation.v1.action_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.BuildAndDeployAction)
  })
_sym_db.RegisterMessage(BuildAndDeployAction)

DeploymentCondition = _reflection.GeneratedProtocolMessageType('DeploymentCondition', (_message.Message,), {
  'DESCRIPTOR' : _DEPLOYMENTCONDITION,
  '__module__' : 'qwak.automation.v1.action_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.DeploymentCondition)
  })
_sym_db.RegisterMessage(DeploymentCondition)

BuildMetricCondition = _reflection.GeneratedProtocolMessageType('BuildMetricCondition', (_message.Message,), {
  'DESCRIPTOR' : _BUILDMETRICCONDITION,
  '__module__' : 'qwak.automation.v1.action_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.BuildMetricCondition)
  })
_sym_db.RegisterMessage(BuildMetricCondition)

DeploymentSpec = _reflection.GeneratedProtocolMessageType('DeploymentSpec', (_message.Message,), {
  'DESCRIPTOR' : _DEPLOYMENTSPEC,
  '__module__' : 'qwak.automation.v1.action_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.DeploymentSpec)
  })
_sym_db.RegisterMessage(DeploymentSpec)

AdvancedDeploymentOptions = _reflection.GeneratedProtocolMessageType('AdvancedDeploymentOptions', (_message.Message,), {
  'DESCRIPTOR' : _ADVANCEDDEPLOYMENTOPTIONS,
  '__module__' : 'qwak.automation.v1.action_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.AdvancedDeploymentOptions)
  })
_sym_db.RegisterMessage(AdvancedDeploymentOptions)

DeploymentSize = _reflection.GeneratedProtocolMessageType('DeploymentSize', (_message.Message,), {
  'DESCRIPTOR' : _DEPLOYMENTSIZE,
  '__module__' : 'qwak.automation.v1.action_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.DeploymentSize)
  })
_sym_db.RegisterMessage(DeploymentSize)

BuildSpec = _reflection.GeneratedProtocolMessageType('BuildSpec', (_message.Message,), {

  'ParametersEntry' : _reflection.GeneratedProtocolMessageType('ParametersEntry', (_message.Message,), {
    'DESCRIPTOR' : _BUILDSPEC_PARAMETERSENTRY,
    '__module__' : 'qwak.automation.v1.action_pb2'
    # @@protoc_insertion_point(class_scope:qwak.automation.v1.BuildSpec.ParametersEntry)
    })
  ,
  'DESCRIPTOR' : _BUILDSPEC,
  '__module__' : 'qwak.automation.v1.action_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.BuildSpec)
  })
_sym_db.RegisterMessage(BuildSpec)
_sym_db.RegisterMessage(BuildSpec.ParametersEntry)

Resources = _reflection.GeneratedProtocolMessageType('Resources', (_message.Message,), {
  'DESCRIPTOR' : _RESOURCES,
  '__module__' : 'qwak.automation.v1.action_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.Resources)
  })
_sym_db.RegisterMessage(Resources)

CpuResources = _reflection.GeneratedProtocolMessageType('CpuResources', (_message.Message,), {
  'DESCRIPTOR' : _CPURESOURCES,
  '__module__' : 'qwak.automation.v1.action_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.CpuResources)
  })
_sym_db.RegisterMessage(CpuResources)

GpuResources = _reflection.GeneratedProtocolMessageType('GpuResources', (_message.Message,), {
  'DESCRIPTOR' : _GPURESOURCES,
  '__module__' : 'qwak.automation.v1.action_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.GpuResources)
  })
_sym_db.RegisterMessage(GpuResources)

GitModelSource = _reflection.GeneratedProtocolMessageType('GitModelSource', (_message.Message,), {
  'DESCRIPTOR' : _GITMODELSOURCE,
  '__module__' : 'qwak.automation.v1.action_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.GitModelSource)
  })
_sym_db.RegisterMessage(GitModelSource)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\035com.qwak.ai.automation.api.v1P\001'
  _DEPLOYMENTSIZE.fields_by_name['cpu']._options = None
  _DEPLOYMENTSIZE.fields_by_name['cpu']._serialized_options = b'\030\001'
  _DEPLOYMENTSIZE.fields_by_name['memory_amount']._options = None
  _DEPLOYMENTSIZE.fields_by_name['memory_amount']._serialized_options = b'\030\001'
  _DEPLOYMENTSIZE.fields_by_name['memory_units']._options = None
  _DEPLOYMENTSIZE.fields_by_name['memory_units']._serialized_options = b'\030\001'
  _DEPLOYMENTSIZE.fields_by_name['gpu_resources']._options = None
  _DEPLOYMENTSIZE.fields_by_name['gpu_resources']._serialized_options = b'\030\001'
  _BUILDSPEC_PARAMETERSENTRY._options = None
  _BUILDSPEC_PARAMETERSENTRY._serialized_options = b'8\001'
  _RESOURCES.fields_by_name['cpu_resources']._options = None
  _RESOURCES.fields_by_name['cpu_resources']._serialized_options = b'\030\001'
  _RESOURCES.fields_by_name['gpu_resources']._options = None
  _RESOURCES.fields_by_name['gpu_resources']._serialized_options = b'\030\001'
  _GPUTYPE._serialized_start=2759
  _GPUTYPE._serialized_end=2878
  _MEMORYUNIT._serialized_start=2880
  _MEMORYUNIT._serialized_end=2923
  _ACTION._serialized_start=252
  _ACTION._serialized_end=405
  _BATCHEXECUTIONACTION._serialized_start=407
  _BATCHEXECUTIONACTION._serialized_end=488
  _BUILDANDDEPLOYACTION._serialized_start=491
  _BUILDANDDEPLOYACTION._serialized_end=696
  _DEPLOYMENTCONDITION._serialized_start=698
  _DEPLOYMENTCONDITION._serialized_end=798
  _BUILDMETRICCONDITION._serialized_start=801
  _BUILDMETRICCONDITION._serialized_end=938
  _DEPLOYMENTSPEC._serialized_start=941
  _DEPLOYMENTSPEC._serialized_end=1164
  _ADVANCEDDEPLOYMENTOPTIONS._serialized_start=1167
  _ADVANCEDDEPLOYMENTOPTIONS._serialized_end=1450
  _DEPLOYMENTSIZE._serialized_start=1453
  _DEPLOYMENTSIZE._serialized_end=1754
  _BUILDSPEC._serialized_start=1757
  _BUILDSPEC._serialized_end=2195
  _BUILDSPEC_PARAMETERSENTRY._serialized_start=2146
  _BUILDSPEC_PARAMETERSENTRY._serialized_end=2195
  _RESOURCES._serialized_start=2198
  _RESOURCES._serialized_end=2447
  _CPURESOURCES._serialized_start=2449
  _CPURESOURCES._serialized_end=2553
  _GPURESOURCES._serialized_start=2555
  _GPURESOURCES._serialized_end=2636
  _GITMODELSOURCE._serialized_start=2638
  _GITMODELSOURCE._serialized_end=2757
# @@protoc_insertion_point(module_scope)

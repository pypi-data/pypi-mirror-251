# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorboard/compat/proto/config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tensorboard.compat.proto import cost_graph_pb2 as tensorboard_dot_compat_dot_proto_dot_cost__graph__pb2
from tensorboard.compat.proto import graph_pb2 as tensorboard_dot_compat_dot_proto_dot_graph__pb2
from tensorboard.compat.proto import step_stats_pb2 as tensorboard_dot_compat_dot_proto_dot_step__stats__pb2
from tensorboard.compat.proto import cluster_pb2 as tensorboard_dot_compat_dot_proto_dot_cluster__pb2
from tensorboard.compat.proto import debug_pb2 as tensorboard_dot_compat_dot_proto_dot_debug__pb2
from tensorboard.compat.proto import rewriter_config_pb2 as tensorboard_dot_compat_dot_proto_dot_rewriter__config__pb2
from tensorboard.compat.proto import rpc_options_pb2 as tensorboard_dot_compat_dot_proto_dot_rpc__options__pb2
from tensorboard.compat.proto import coordination_config_pb2 as tensorboard_dot_compat_dot_proto_dot_coordination__config__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%tensorboard/compat/proto/config.proto\x12\x0btensorboard\x1a)tensorboard/compat/proto/cost_graph.proto\x1a$tensorboard/compat/proto/graph.proto\x1a)tensorboard/compat/proto/step_stats.proto\x1a&tensorboard/compat/proto/cluster.proto\x1a$tensorboard/compat/proto/debug.proto\x1a.tensorboard/compat/proto/rewriter_config.proto\x1a*tensorboard/compat/proto/rpc_options.proto\x1a\x32tensorboard/compat/proto/coordination_config.proto\"\xec\x07\n\nGPUOptions\x12\'\n\x1fper_process_gpu_memory_fraction\x18\x01 \x01(\x01\x12\x14\n\x0c\x61llow_growth\x18\x04 \x01(\x08\x12\x16\n\x0e\x61llocator_type\x18\x02 \x01(\t\x12\x1f\n\x17\x64\x65\x66\x65rred_deletion_bytes\x18\x03 \x01(\x03\x12\x1b\n\x13visible_device_list\x18\x05 \x01(\t\x12\"\n\x1apolling_active_delay_usecs\x18\x06 \x01(\x05\x12$\n\x1cpolling_inactive_delay_msecs\x18\x07 \x01(\x05\x12\x1c\n\x14\x66orce_gpu_compatible\x18\x08 \x01(\x08\x12:\n\x0c\x65xperimental\x18\t \x01(\x0b\x32$.tensorboard.GPUOptions.Experimental\x1a\xa4\x05\n\x0c\x45xperimental\x12L\n\x0fvirtual_devices\x18\x01 \x03(\x0b\x32\x33.tensorboard.GPUOptions.Experimental.VirtualDevices\x12#\n\x1bnum_virtual_devices_per_gpu\x18\x0f \x01(\x05\x12\x1a\n\x12use_unified_memory\x18\x02 \x01(\x08\x12#\n\x1bnum_dev_to_dev_copy_streams\x18\x03 \x01(\x05\x12\x1d\n\x15\x63ollective_ring_order\x18\x04 \x01(\t\x12\x1d\n\x15timestamped_allocator\x18\x05 \x01(\x08\x12#\n\x1bkernel_tracker_max_interval\x18\x07 \x01(\x05\x12 \n\x18kernel_tracker_max_bytes\x18\x08 \x01(\x05\x12\"\n\x1akernel_tracker_max_pending\x18\t \x01(\x05\x12\'\n\x1finternal_fragmentation_fraction\x18\n \x01(\x01\x12\x1d\n\x15use_cuda_malloc_async\x18\x0b \x01(\x08\x12,\n$disallow_retry_on_allocation_failure\x18\x0c \x01(\x08\x12 \n\x18gpu_host_mem_limit_in_mb\x18\r \x01(\x02\x12$\n\x1cgpu_host_mem_disallow_growth\x18\x0e \x01(\x08\x12$\n\x1cgpu_system_memory_size_in_mb\x18\x10 \x01(\x05\x1aS\n\x0eVirtualDevices\x12\x17\n\x0fmemory_limit_mb\x18\x01 \x03(\x02\x12\x10\n\x08priority\x18\x02 \x03(\x05\x12\x16\n\x0e\x64\x65vice_ordinal\x18\x03 \x03(\x05\"\x9f\x03\n\x10OptimizerOptions\x12+\n#do_common_subexpression_elimination\x18\x01 \x01(\x08\x12\x1b\n\x13\x64o_constant_folding\x18\x02 \x01(\x08\x12$\n\x1cmax_folded_constant_in_bytes\x18\x06 \x01(\x03\x12\x1c\n\x14\x64o_function_inlining\x18\x04 \x01(\x08\x12\x36\n\topt_level\x18\x03 \x01(\x0e\x32#.tensorboard.OptimizerOptions.Level\x12\x46\n\x10global_jit_level\x18\x05 \x01(\x0e\x32,.tensorboard.OptimizerOptions.GlobalJitLevel\x12\x16\n\x0e\x63pu_global_jit\x18\x07 \x01(\x08\" \n\x05Level\x12\x06\n\x02L1\x10\x00\x12\x0f\n\x02L0\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\"C\n\x0eGlobalJitLevel\x12\x0b\n\x07\x44\x45\x46\x41ULT\x10\x00\x12\x10\n\x03OFF\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x12\x08\n\x04ON_1\x10\x01\x12\x08\n\x04ON_2\x10\x02\"\xf0\x02\n\x0cGraphOptions\x12\x1e\n\x16\x65nable_recv_scheduling\x18\x02 \x01(\x08\x12\x38\n\x11optimizer_options\x18\x03 \x01(\x0b\x32\x1d.tensorboard.OptimizerOptions\x12\x18\n\x10\x62uild_cost_model\x18\x04 \x01(\x03\x12\x1e\n\x16\x62uild_cost_model_after\x18\t \x01(\x03\x12\x14\n\x0cinfer_shapes\x18\x05 \x01(\x08\x12\x1a\n\x12place_pruned_graph\x18\x06 \x01(\x08\x12 \n\x18\x65nable_bfloat16_sendrecv\x18\x07 \x01(\x08\x12\x15\n\rtimeline_step\x18\x08 \x01(\x05\x12\x34\n\x0frewrite_options\x18\n \x01(\x0b\x32\x1b.tensorboard.RewriterConfigJ\x04\x08\x01\x10\x02R%skip_common_subexpression_elimination\"A\n\x15ThreadPoolOptionProto\x12\x13\n\x0bnum_threads\x18\x01 \x01(\x05\x12\x13\n\x0bglobal_name\x18\x02 \x01(\t\"0\n\x0fSessionMetadata\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\x03\"\x9f\x0f\n\x0b\x43onfigProto\x12?\n\x0c\x64\x65vice_count\x18\x01 \x03(\x0b\x32).tensorboard.ConfigProto.DeviceCountEntry\x12$\n\x1cintra_op_parallelism_threads\x18\x02 \x01(\x05\x12$\n\x1cinter_op_parallelism_threads\x18\x05 \x01(\x05\x12\x1f\n\x17use_per_session_threads\x18\t \x01(\x08\x12H\n\x1csession_inter_op_thread_pool\x18\x0c \x03(\x0b\x32\".tensorboard.ThreadPoolOptionProto\x12\x18\n\x10placement_period\x18\x03 \x01(\x05\x12\x16\n\x0e\x64\x65vice_filters\x18\x04 \x03(\t\x12,\n\x0bgpu_options\x18\x06 \x01(\x0b\x32\x17.tensorboard.GPUOptions\x12\x1c\n\x14\x61llow_soft_placement\x18\x07 \x01(\x08\x12\x1c\n\x14log_device_placement\x18\x08 \x01(\x08\x12\x30\n\rgraph_options\x18\n \x01(\x0b\x32\x19.tensorboard.GraphOptions\x12\x1f\n\x17operation_timeout_in_ms\x18\x0b \x01(\x03\x12,\n\x0brpc_options\x18\r \x01(\x0b\x32\x17.tensorboard.RPCOptions\x12,\n\x0b\x63luster_def\x18\x0e \x01(\x0b\x32\x17.tensorboard.ClusterDef\x12\x1d\n\x15isolate_session_state\x18\x0f \x01(\x08\x12(\n share_cluster_devices_in_session\x18\x11 \x01(\x08\x12;\n\x0c\x65xperimental\x18\x10 \x01(\x0b\x32%.tensorboard.ConfigProto.Experimental\x1a\x32\n\x10\x44\x65viceCountEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a\x92\t\n\x0c\x45xperimental\x12\x1f\n\x17\x63ollective_group_leader\x18\x01 \x01(\t\x12\x15\n\rexecutor_type\x18\x03 \x01(\t\x12\x1a\n\x12recv_buf_max_chunk\x18\x04 \x01(\x05\x12\x19\n\x11use_numa_affinity\x18\x05 \x01(\x08\x12\x35\n-collective_deterministic_sequential_execution\x18\x06 \x01(\x08\x12\x17\n\x0f\x63ollective_nccl\x18\x07 \x01(\x08\x12\x36\n.share_session_state_in_clusterspec_propagation\x18\x08 \x01(\x08\x12\x1f\n\x17\x64isable_thread_spinning\x18\t \x01(\x08\x12(\n share_cluster_devices_in_session\x18\n \x01(\x08\x12\x36\n\x10session_metadata\x18\x0b \x01(\x0b\x32\x1c.tensorboard.SessionMetadata\x12!\n\x19optimize_for_static_graph\x18\x0c \x01(\x08\x12\x1a\n\x12\x65nable_mlir_bridge\x18\r \x01(\x08\x12T\n\x13mlir_bridge_rollout\x18\x11 \x01(\x0e\x32\x37.tensorboard.ConfigProto.Experimental.MlirBridgeRollout\x12&\n\x1e\x65nable_mlir_graph_optimization\x18\x10 \x01(\x08\x12\'\n\x1f\x64isable_output_partition_graphs\x18\x0e \x01(\x08\x12#\n\x1bxla_fusion_autotuner_thresh\x18\x0f \x01(\x03\x12\x10\n\x08use_tfrt\x18\x12 \x01(\x08\x12\'\n\x1f\x64isable_functional_ops_lowering\x18\x15 \x01(\x08\x12\'\n\x1fxla_prefer_single_graph_cluster\x18\x16 \x01(\x08\x12\x43\n\x13\x63oordination_config\x18\x17 \x01(\x0b\x32&.tensorboard.CoordinationServiceConfig\x12)\n!disable_optimize_for_static_graph\x18\x18 \x01(\x08\x12\x30\n(disable_eager_executor_streaming_enqueue\x18\x1a \x01(\x08\"\xde\x01\n\x11MlirBridgeRollout\x12#\n\x1fMLIR_BRIDGE_ROLLOUT_UNSPECIFIED\x10\x00\x12\x1f\n\x1bMLIR_BRIDGE_ROLLOUT_ENABLED\x10\x01\x12 \n\x1cMLIR_BRIDGE_ROLLOUT_DISABLED\x10\x02\"\x04\x08\x03\x10\x03\"\x04\x08\x04\x10\x04*%MLIR_BRIDGE_ROLLOUT_SAFE_MODE_ENABLED*.MLIR_BRIDGE_ROLLOUT_SAFE_MODE_FALLBACK_ENABLEDJ\x04\x08\x02\x10\x03J\x04\x08\x13\x10\x14J\x04\x08\x14\x10\x15J\x04\x08\x19\x10\x1a\"\xe5\x04\n\nRunOptions\x12\x37\n\x0btrace_level\x18\x01 \x01(\x0e\x32\".tensorboard.RunOptions.TraceLevel\x12\x15\n\rtimeout_in_ms\x18\x02 \x01(\x03\x12\x1c\n\x14inter_op_thread_pool\x18\x03 \x01(\x05\x12\x1f\n\x17output_partition_graphs\x18\x05 \x01(\x08\x12\x30\n\rdebug_options\x18\x06 \x01(\x0b\x32\x19.tensorboard.DebugOptions\x12*\n\"report_tensor_allocations_upon_oom\x18\x07 \x01(\x08\x12:\n\x0c\x65xperimental\x18\x08 \x01(\x0b\x32$.tensorboard.RunOptions.Experimental\x1a\xd3\x01\n\x0c\x45xperimental\x12\x1c\n\x14\x63ollective_graph_key\x18\x01 \x01(\x03\x12\x1c\n\x14use_run_handler_pool\x18\x02 \x01(\x08\x12\\\n\x18run_handler_pool_options\x18\x03 \x01(\x0b\x32:.tensorboard.RunOptions.Experimental.RunHandlerPoolOptions\x1a)\n\x15RunHandlerPoolOptions\x12\x10\n\x08priority\x18\x01 \x01(\x03\"R\n\nTraceLevel\x12\x0c\n\x08NO_TRACE\x10\x00\x12\x12\n\x0eSOFTWARE_TRACE\x10\x01\x12\x12\n\x0eHARDWARE_TRACE\x10\x02\x12\x0e\n\nFULL_TRACE\x10\x03J\x04\x08\x04\x10\x05\"\xc6\x03\n\x0bRunMetadata\x12*\n\nstep_stats\x18\x01 \x01(\x0b\x32\x16.tensorboard.StepStats\x12-\n\ncost_graph\x18\x02 \x01(\x0b\x32\x19.tensorboard.CostGraphDef\x12/\n\x10partition_graphs\x18\x03 \x03(\x0b\x32\x15.tensorboard.GraphDef\x12@\n\x0f\x66unction_graphs\x18\x04 \x03(\x0b\x32\'.tensorboard.RunMetadata.FunctionGraphs\x12\x36\n\x10session_metadata\x18\x05 \x01(\x0b\x32\x1c.tensorboard.SessionMetadata\x1a\xb0\x01\n\x0e\x46unctionGraphs\x12/\n\x10partition_graphs\x18\x01 \x03(\x0b\x32\x15.tensorboard.GraphDef\x12\x35\n\x16pre_optimization_graph\x18\x02 \x01(\x0b\x32\x15.tensorboard.GraphDef\x12\x36\n\x17post_optimization_graph\x18\x03 \x01(\x0b\x32\x15.tensorboard.GraphDef\":\n\x10TensorConnection\x12\x13\n\x0b\x66rom_tensor\x18\x01 \x01(\t\x12\x11\n\tto_tensor\x18\x02 \x01(\t\"\xb4\x03\n\x0f\x43\x61llableOptions\x12\x0c\n\x04\x66\x65\x65\x64\x18\x01 \x03(\t\x12\r\n\x05\x66\x65tch\x18\x02 \x03(\t\x12\x0e\n\x06target\x18\x03 \x03(\t\x12,\n\x0brun_options\x18\x04 \x01(\x0b\x32\x17.tensorboard.RunOptions\x12\x38\n\x11tensor_connection\x18\x05 \x03(\x0b\x32\x1d.tensorboard.TensorConnection\x12\x43\n\x0c\x66\x65\x65\x64_devices\x18\x06 \x03(\x0b\x32-.tensorboard.CallableOptions.FeedDevicesEntry\x12\x45\n\rfetch_devices\x18\x07 \x03(\x0b\x32..tensorboard.CallableOptions.FetchDevicesEntry\x12\x17\n\x0f\x66\x65tch_skip_sync\x18\x08 \x01(\x08\x1a\x32\n\x10\x46\x65\x65\x64\x44\x65vicesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x33\n\x11\x46\x65tchDevicesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\x84\x01\n\x18org.tensorflow.frameworkB\x0c\x43onfigProtosP\x01ZUgithub.com/tensorflow/tensorflow/tensorflow/go/core/protobuf/for_core_protos_go_proto\xf8\x01\x01\x62\x06proto3')



_GPUOPTIONS = DESCRIPTOR.message_types_by_name['GPUOptions']
_GPUOPTIONS_EXPERIMENTAL = _GPUOPTIONS.nested_types_by_name['Experimental']
_GPUOPTIONS_EXPERIMENTAL_VIRTUALDEVICES = _GPUOPTIONS_EXPERIMENTAL.nested_types_by_name['VirtualDevices']
_OPTIMIZEROPTIONS = DESCRIPTOR.message_types_by_name['OptimizerOptions']
_GRAPHOPTIONS = DESCRIPTOR.message_types_by_name['GraphOptions']
_THREADPOOLOPTIONPROTO = DESCRIPTOR.message_types_by_name['ThreadPoolOptionProto']
_SESSIONMETADATA = DESCRIPTOR.message_types_by_name['SessionMetadata']
_CONFIGPROTO = DESCRIPTOR.message_types_by_name['ConfigProto']
_CONFIGPROTO_DEVICECOUNTENTRY = _CONFIGPROTO.nested_types_by_name['DeviceCountEntry']
_CONFIGPROTO_EXPERIMENTAL = _CONFIGPROTO.nested_types_by_name['Experimental']
_RUNOPTIONS = DESCRIPTOR.message_types_by_name['RunOptions']
_RUNOPTIONS_EXPERIMENTAL = _RUNOPTIONS.nested_types_by_name['Experimental']
_RUNOPTIONS_EXPERIMENTAL_RUNHANDLERPOOLOPTIONS = _RUNOPTIONS_EXPERIMENTAL.nested_types_by_name['RunHandlerPoolOptions']
_RUNMETADATA = DESCRIPTOR.message_types_by_name['RunMetadata']
_RUNMETADATA_FUNCTIONGRAPHS = _RUNMETADATA.nested_types_by_name['FunctionGraphs']
_TENSORCONNECTION = DESCRIPTOR.message_types_by_name['TensorConnection']
_CALLABLEOPTIONS = DESCRIPTOR.message_types_by_name['CallableOptions']
_CALLABLEOPTIONS_FEEDDEVICESENTRY = _CALLABLEOPTIONS.nested_types_by_name['FeedDevicesEntry']
_CALLABLEOPTIONS_FETCHDEVICESENTRY = _CALLABLEOPTIONS.nested_types_by_name['FetchDevicesEntry']
_OPTIMIZEROPTIONS_LEVEL = _OPTIMIZEROPTIONS.enum_types_by_name['Level']
_OPTIMIZEROPTIONS_GLOBALJITLEVEL = _OPTIMIZEROPTIONS.enum_types_by_name['GlobalJitLevel']
_CONFIGPROTO_EXPERIMENTAL_MLIRBRIDGEROLLOUT = _CONFIGPROTO_EXPERIMENTAL.enum_types_by_name['MlirBridgeRollout']
_RUNOPTIONS_TRACELEVEL = _RUNOPTIONS.enum_types_by_name['TraceLevel']
GPUOptions = _reflection.GeneratedProtocolMessageType('GPUOptions', (_message.Message,), {

  'Experimental' : _reflection.GeneratedProtocolMessageType('Experimental', (_message.Message,), {

    'VirtualDevices' : _reflection.GeneratedProtocolMessageType('VirtualDevices', (_message.Message,), {
      'DESCRIPTOR' : _GPUOPTIONS_EXPERIMENTAL_VIRTUALDEVICES,
      '__module__' : 'tensorboard.compat.proto.config_pb2'
      # @@protoc_insertion_point(class_scope:tensorboard.GPUOptions.Experimental.VirtualDevices)
      })
    ,
    'DESCRIPTOR' : _GPUOPTIONS_EXPERIMENTAL,
    '__module__' : 'tensorboard.compat.proto.config_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.GPUOptions.Experimental)
    })
  ,
  'DESCRIPTOR' : _GPUOPTIONS,
  '__module__' : 'tensorboard.compat.proto.config_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.GPUOptions)
  })
_sym_db.RegisterMessage(GPUOptions)
_sym_db.RegisterMessage(GPUOptions.Experimental)
_sym_db.RegisterMessage(GPUOptions.Experimental.VirtualDevices)

OptimizerOptions = _reflection.GeneratedProtocolMessageType('OptimizerOptions', (_message.Message,), {
  'DESCRIPTOR' : _OPTIMIZEROPTIONS,
  '__module__' : 'tensorboard.compat.proto.config_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.OptimizerOptions)
  })
_sym_db.RegisterMessage(OptimizerOptions)

GraphOptions = _reflection.GeneratedProtocolMessageType('GraphOptions', (_message.Message,), {
  'DESCRIPTOR' : _GRAPHOPTIONS,
  '__module__' : 'tensorboard.compat.proto.config_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.GraphOptions)
  })
_sym_db.RegisterMessage(GraphOptions)

ThreadPoolOptionProto = _reflection.GeneratedProtocolMessageType('ThreadPoolOptionProto', (_message.Message,), {
  'DESCRIPTOR' : _THREADPOOLOPTIONPROTO,
  '__module__' : 'tensorboard.compat.proto.config_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.ThreadPoolOptionProto)
  })
_sym_db.RegisterMessage(ThreadPoolOptionProto)

SessionMetadata = _reflection.GeneratedProtocolMessageType('SessionMetadata', (_message.Message,), {
  'DESCRIPTOR' : _SESSIONMETADATA,
  '__module__' : 'tensorboard.compat.proto.config_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.SessionMetadata)
  })
_sym_db.RegisterMessage(SessionMetadata)

ConfigProto = _reflection.GeneratedProtocolMessageType('ConfigProto', (_message.Message,), {

  'DeviceCountEntry' : _reflection.GeneratedProtocolMessageType('DeviceCountEntry', (_message.Message,), {
    'DESCRIPTOR' : _CONFIGPROTO_DEVICECOUNTENTRY,
    '__module__' : 'tensorboard.compat.proto.config_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.ConfigProto.DeviceCountEntry)
    })
  ,

  'Experimental' : _reflection.GeneratedProtocolMessageType('Experimental', (_message.Message,), {
    'DESCRIPTOR' : _CONFIGPROTO_EXPERIMENTAL,
    '__module__' : 'tensorboard.compat.proto.config_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.ConfigProto.Experimental)
    })
  ,
  'DESCRIPTOR' : _CONFIGPROTO,
  '__module__' : 'tensorboard.compat.proto.config_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.ConfigProto)
  })
_sym_db.RegisterMessage(ConfigProto)
_sym_db.RegisterMessage(ConfigProto.DeviceCountEntry)
_sym_db.RegisterMessage(ConfigProto.Experimental)

RunOptions = _reflection.GeneratedProtocolMessageType('RunOptions', (_message.Message,), {

  'Experimental' : _reflection.GeneratedProtocolMessageType('Experimental', (_message.Message,), {

    'RunHandlerPoolOptions' : _reflection.GeneratedProtocolMessageType('RunHandlerPoolOptions', (_message.Message,), {
      'DESCRIPTOR' : _RUNOPTIONS_EXPERIMENTAL_RUNHANDLERPOOLOPTIONS,
      '__module__' : 'tensorboard.compat.proto.config_pb2'
      # @@protoc_insertion_point(class_scope:tensorboard.RunOptions.Experimental.RunHandlerPoolOptions)
      })
    ,
    'DESCRIPTOR' : _RUNOPTIONS_EXPERIMENTAL,
    '__module__' : 'tensorboard.compat.proto.config_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.RunOptions.Experimental)
    })
  ,
  'DESCRIPTOR' : _RUNOPTIONS,
  '__module__' : 'tensorboard.compat.proto.config_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.RunOptions)
  })
_sym_db.RegisterMessage(RunOptions)
_sym_db.RegisterMessage(RunOptions.Experimental)
_sym_db.RegisterMessage(RunOptions.Experimental.RunHandlerPoolOptions)

RunMetadata = _reflection.GeneratedProtocolMessageType('RunMetadata', (_message.Message,), {

  'FunctionGraphs' : _reflection.GeneratedProtocolMessageType('FunctionGraphs', (_message.Message,), {
    'DESCRIPTOR' : _RUNMETADATA_FUNCTIONGRAPHS,
    '__module__' : 'tensorboard.compat.proto.config_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.RunMetadata.FunctionGraphs)
    })
  ,
  'DESCRIPTOR' : _RUNMETADATA,
  '__module__' : 'tensorboard.compat.proto.config_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.RunMetadata)
  })
_sym_db.RegisterMessage(RunMetadata)
_sym_db.RegisterMessage(RunMetadata.FunctionGraphs)

TensorConnection = _reflection.GeneratedProtocolMessageType('TensorConnection', (_message.Message,), {
  'DESCRIPTOR' : _TENSORCONNECTION,
  '__module__' : 'tensorboard.compat.proto.config_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.TensorConnection)
  })
_sym_db.RegisterMessage(TensorConnection)

CallableOptions = _reflection.GeneratedProtocolMessageType('CallableOptions', (_message.Message,), {

  'FeedDevicesEntry' : _reflection.GeneratedProtocolMessageType('FeedDevicesEntry', (_message.Message,), {
    'DESCRIPTOR' : _CALLABLEOPTIONS_FEEDDEVICESENTRY,
    '__module__' : 'tensorboard.compat.proto.config_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.CallableOptions.FeedDevicesEntry)
    })
  ,

  'FetchDevicesEntry' : _reflection.GeneratedProtocolMessageType('FetchDevicesEntry', (_message.Message,), {
    'DESCRIPTOR' : _CALLABLEOPTIONS_FETCHDEVICESENTRY,
    '__module__' : 'tensorboard.compat.proto.config_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.CallableOptions.FetchDevicesEntry)
    })
  ,
  'DESCRIPTOR' : _CALLABLEOPTIONS,
  '__module__' : 'tensorboard.compat.proto.config_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.CallableOptions)
  })
_sym_db.RegisterMessage(CallableOptions)
_sym_db.RegisterMessage(CallableOptions.FeedDevicesEntry)
_sym_db.RegisterMessage(CallableOptions.FetchDevicesEntry)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030org.tensorflow.frameworkB\014ConfigProtosP\001ZUgithub.com/tensorflow/tensorflow/tensorflow/go/core/protobuf/for_core_protos_go_proto\370\001\001'
  _CONFIGPROTO_DEVICECOUNTENTRY._options = None
  _CONFIGPROTO_DEVICECOUNTENTRY._serialized_options = b'8\001'
  _CALLABLEOPTIONS_FEEDDEVICESENTRY._options = None
  _CALLABLEOPTIONS_FEEDDEVICESENTRY._serialized_options = b'8\001'
  _CALLABLEOPTIONS_FETCHDEVICESENTRY._options = None
  _CALLABLEOPTIONS_FETCHDEVICESENTRY._serialized_options = b'8\001'
  _GPUOPTIONS._serialized_start=401
  _GPUOPTIONS._serialized_end=1405
  _GPUOPTIONS_EXPERIMENTAL._serialized_start=729
  _GPUOPTIONS_EXPERIMENTAL._serialized_end=1405
  _GPUOPTIONS_EXPERIMENTAL_VIRTUALDEVICES._serialized_start=1322
  _GPUOPTIONS_EXPERIMENTAL_VIRTUALDEVICES._serialized_end=1405
  _OPTIMIZEROPTIONS._serialized_start=1408
  _OPTIMIZEROPTIONS._serialized_end=1823
  _OPTIMIZEROPTIONS_LEVEL._serialized_start=1722
  _OPTIMIZEROPTIONS_LEVEL._serialized_end=1754
  _OPTIMIZEROPTIONS_GLOBALJITLEVEL._serialized_start=1756
  _OPTIMIZEROPTIONS_GLOBALJITLEVEL._serialized_end=1823
  _GRAPHOPTIONS._serialized_start=1826
  _GRAPHOPTIONS._serialized_end=2194
  _THREADPOOLOPTIONPROTO._serialized_start=2196
  _THREADPOOLOPTIONPROTO._serialized_end=2261
  _SESSIONMETADATA._serialized_start=2263
  _SESSIONMETADATA._serialized_end=2311
  _CONFIGPROTO._serialized_start=2314
  _CONFIGPROTO._serialized_end=4265
  _CONFIGPROTO_DEVICECOUNTENTRY._serialized_start=3042
  _CONFIGPROTO_DEVICECOUNTENTRY._serialized_end=3092
  _CONFIGPROTO_EXPERIMENTAL._serialized_start=3095
  _CONFIGPROTO_EXPERIMENTAL._serialized_end=4265
  _CONFIGPROTO_EXPERIMENTAL_MLIRBRIDGEROLLOUT._serialized_start=4019
  _CONFIGPROTO_EXPERIMENTAL_MLIRBRIDGEROLLOUT._serialized_end=4241
  _RUNOPTIONS._serialized_start=4268
  _RUNOPTIONS._serialized_end=4881
  _RUNOPTIONS_EXPERIMENTAL._serialized_start=4580
  _RUNOPTIONS_EXPERIMENTAL._serialized_end=4791
  _RUNOPTIONS_EXPERIMENTAL_RUNHANDLERPOOLOPTIONS._serialized_start=4750
  _RUNOPTIONS_EXPERIMENTAL_RUNHANDLERPOOLOPTIONS._serialized_end=4791
  _RUNOPTIONS_TRACELEVEL._serialized_start=4793
  _RUNOPTIONS_TRACELEVEL._serialized_end=4875
  _RUNMETADATA._serialized_start=4884
  _RUNMETADATA._serialized_end=5338
  _RUNMETADATA_FUNCTIONGRAPHS._serialized_start=5162
  _RUNMETADATA_FUNCTIONGRAPHS._serialized_end=5338
  _TENSORCONNECTION._serialized_start=5340
  _TENSORCONNECTION._serialized_end=5398
  _CALLABLEOPTIONS._serialized_start=5401
  _CALLABLEOPTIONS._serialized_end=5837
  _CALLABLEOPTIONS_FEEDDEVICESENTRY._serialized_start=5734
  _CALLABLEOPTIONS_FEEDDEVICESENTRY._serialized_end=5784
  _CALLABLEOPTIONS_FETCHDEVICESENTRY._serialized_start=5786
  _CALLABLEOPTIONS_FETCHDEVICESENTRY._serialized_end=5837
# @@protoc_insertion_point(module_scope)

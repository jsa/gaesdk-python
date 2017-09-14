#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Provides utility functions to create grpc stub and make grpc call."""

from grpc.beta import implementations

from google.appengine.ext.remote_api import remote_api_pb
from google.appengine.ext.remote_api import remote_api_stub
from google.appengine.tools.devappserver2 import grpc_service_pb2


def create_stub(grpc_apiserver_host):
  """Creates a grpc_service.CallHandler stub.

  Args:
    grpc_apiserver_host: String, the host that CallHandler service listens on.
      Should be in the format of hostname:port.

  Returns:
    A CallHandler stub.
  """
  # See http://www.grpc.io/grpc/python/_modules/grpc/beta/implementations.html:
  # the method insecure_channel requires explicitly two parameters (host, port)
  # here our host already contain port number, so the second parameter is None.
  prefix = 'http://'
  if grpc_apiserver_host.startswith(prefix):
    grpc_apiserver_host = grpc_apiserver_host[len(prefix):]
  channel = implementations.insecure_channel(grpc_apiserver_host, None)
  return grpc_service_pb2.beta_create_CallHandler_stub(channel)


def make_grpc_call_from_remote_api(stub, request):
  """Translate remote_api_pb.Request to gRPC call.

  Args:
    stub: A grpc_service_pb2.beta_create_CallHandler_stub object.
    request: A remote_api_pb.Request message.

  Returns:
    A remote_api_pb.Response message.
  """
  # Translate remote_api_pb.Request into grpc_service_pb2.Request
  request_pb = grpc_service_pb2.Request(
      service_name=request.service_name(),
      method=request.method(),
      request=request.request())
  if request.has_request_id():
    request_pb.request_id = request.request_id()

  response_pb = stub.HandleCall(request_pb, remote_api_stub.TIMEOUT_SECONDS)

  # Translate grpc_service_pb2.Response back to remote_api_pb.Response
  response = remote_api_pb.Response()
  # TODO: b/36590656#comment3 continuously complete exception handling.
  response.set_response(response_pb.response)
  if response_pb.HasField('rpc_error'):
    response.mutable_rpc_error().ParseFromString(
        response_pb.rpc_error.SerializeToString())
  if response_pb.HasField('application_error'):
    response.mutable_application_error().ParseFromString(
        response_pb.application_error.SerializeToString())
  return response

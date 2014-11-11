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
"""Handles the generation of quickstart-web.xml based on servlet annotations."""

from __future__ import with_statement

import os
import subprocess

from google.appengine.tools import java_utils


_QUICKSTART_JAR_PATH = os.path.join(
    'google', 'appengine', 'javamanagedvm', 'appengine-java-vmruntime',
    'quickstartgenerator.jar')


def quickstart_generator(war_path, sdk_root=None):
  """Run the quickstart-web.xml generator on the given Java app.

  If the generator succeeds in creating quickstart-web.xml, this method returns
  its contents. Otherwise, it raises RuntimeError. If there was already a
  quickstart-web.xml when this method started, it is removed before generation
  is attempted.

  Args:
    war_path: a string that is the path to a Java app. It should name a
      directory that contains a WEB-INF subdirectory.
    sdk_root: a string that is the path to an App Engine SDK with Java support.

  Returns:
    a string that is the contents of the generated quickstart-web.xml.

  Raises:
    CalledProcessError: if the quickstart generation fails.
    IOError: if the quickstart generation apparently succeeds but the
      quickstart-web.xml file is not created. (This should not happen.)
  """
  if not sdk_root:
    sdk_root = os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.dirname(java_utils.__file__))))

  quickstart_xml_path = os.path.join(war_path, 'WEB-INF', 'quickstart-web.xml')
  if os.path.exists(quickstart_xml_path):
    os.remove(quickstart_xml_path)

  java_home, exec_suffix = java_utils.JavaHomeAndSuffix()
  java_command = os.path.join(java_home, 'bin', 'java') + exec_suffix

  quickstartgenerator_jar = os.path.join(sdk_root, _QUICKSTART_JAR_PATH)
  command = [java_command, '-jar', quickstartgenerator_jar, war_path]
  subprocess.check_call(command)

  with open(quickstart_xml_path) as f:
    return f.read()

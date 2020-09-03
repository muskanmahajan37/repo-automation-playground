# Copyright 2020 Google LLC.
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


IGNORED_METHOD_NAMES = (
    'run_command',
    'parse_command_line_args',
    'main'
)

REGION_TAG_GREP_ARGS = (
    'grep', '-hr', 'START', '.',

    # Language-specific arguments
    '--include=*.py', '--exclude=*/lib/*',
    '--include=*.js', '--exclude=*/node_modules/*',
)

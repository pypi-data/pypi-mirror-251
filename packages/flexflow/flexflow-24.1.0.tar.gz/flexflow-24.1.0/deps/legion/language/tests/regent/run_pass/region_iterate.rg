-- Copyright 2023 Stanford University
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--     http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.

import "regent"

task f() : int
  var r = region(ispace(ptr, 5), int)

  var p0 = dynamic_cast(ptr(int, r), 0)
  var p1 = dynamic_cast(ptr(int, r), 1)
  var p2 = dynamic_cast(ptr(int, r), 2)
  var p3 = dynamic_cast(ptr(int, r), 3)
  var p4 = dynamic_cast(ptr(int, r), 4)

  @p0 = 5
  @p1 = 40
  @p2 = 300
  @p3 = 2000
  @p4 = 10000

  var s = 0
  for p in r do
    s = s + @p
  end

  return s
end

task main()
  regentlib.assert(f() == 12345, "test failed")
end
regentlib.start(main)

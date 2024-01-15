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

-- fails-with:
-- constraint_pack4.rg:28: invalid cast missing constraint $s * $r
--   var x = t { a = r, b = s }
--             ^

import "regent"

fspace t {
  a : region(int),
  b : region(int),
} where b * a end

task f(r : region(int), s : region(int))
  var x = t { a = r, b = s }
end
f:compile()

# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# @@@ END COPYRIGHT @@@

from ...lib import hpdci
import setup
import cleanup
# Import you own test modules, one line for each.
import tcase1
import tcase2
import tcase3
import tcase4

def sq_testunit(hptestmgr, testlist=[]):

    cleanup._init(hptestmgr, testlist)
    setup._init(hptestmgr, testlist)

    # Auto execute your test modules, one line for each.
    hpdci.auto_execute_module_tests(tcase1, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase2, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase3, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase4, hptestmgr, testlist)

    cleanup._init(hptestmgr, testlist)
   
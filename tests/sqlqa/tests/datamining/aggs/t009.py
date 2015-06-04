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
from ...lib import gvars
import defs

_testmgr = None
_testlist = []
_dci = None

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""test009"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test009
    # ints500.sql
    # jclear
    # 22 Apr 1997
    # Test for the new aggreate functions.
    # Tests Variance and StdDev on an integer column with 500 values.
    ##expectfile ${test_dir}/test009exp test009
    stmt = """select
Variance (int500) as "Var",
StdDev (int500) as "StDev"
from ints500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    # expect 1 row with the following values:
    # 	Var    3.70137614761394820E+017
    # 	StDev  6.08389361150731210E+008
    #
    
    _testmgr.testcase_end(desc)

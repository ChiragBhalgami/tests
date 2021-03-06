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
    
def test001(desc="""test068"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test068
    # Sequence function tests: test for CHAR(10)
    # 1. running functions -- count max min
    # 2. moving functions with 2 arguments
    # 3. moving functions with 3 arguments
    #
    stmt = """select count (*) from vwseqtb68;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test068.exp""", 's1')
    # expect count = 100
    
    stmt = """select a, d,
runningcount(d) as rcount_d,
runningmax(d) as rmax_d,
runningmin(d) as rmin_d
from vwseqtb68 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    # expect the count to run from 1-99 with dupe at row 70
    # expect max at row 6 = 'Bdkytnlllk', 59 = 'Ovigmwrqjc', 70 = 'Slblafivnp'
    # expect the min at all rows = 'Aedrmcurrb'
    
    # 2. moving functions -- count max min -- 2 arguments
    stmt = """select a, d,
movingcount(d, 4) as mcount_d,
movingmax(d, 4) as mmax_d,
movingmin(d, 4) as mmin_d
from vwseqtb68 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test068.exp""", 's2')
    # expect the count to run 1 - 4, then all 4's
    # expect max at row 6 = 'Bdkytnlllk', 59 = 'Ovigmwrqjc', 99 = 'Zelyinywmg'
    # expect min at row 6 = 'Avvpwacsnu', 59 = 'Nsinbltgct', 99 = 'Xuoaacpwbd'
    
    # 3. moving functions -- count max min -- 3 arguments
    stmt = """select a, d,
movingcount(d, 4, 90) as mcount_d
---      , movingmax(d, 4, 90) as mmax_d,		XXXX assertion failure
---        movingmin(d, 4, 90) as mmin_d		XXXX assertion failure
from vwseqtb68 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test068.exp""", 's3')
    # expect the count to run 1 - 4, then all 4's
    # expect max at row 16 = 'Fakwkqkyyr', 70 = 'Slblafivnp', 93 = 'Xibjvxepuf'
    # expect min at row 16 = 'Edqteiwndv', 70 = 'Rspjywuyil', 93 = 'Xaxwbhelcf'
    
    _testmgr.testcase_end(desc)


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
    
def test001(desc="""test108"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test108
    # jc
    # 2002-08-06
    # Test for the fix to the Average functions:
    # Treat NULL not as a 0 but as a NULL and don't count the row as a row.
    #    create table seqtb108 (a bit precision int (4) unsigned,
    #                           b bit precision int (3) unsigned);
    #
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into seqtb108 values
(1, 5), (2, 5), (3, null), (4, 2), (5, 4), (6, 4), (7, null), (8, 5), (9, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 9)
    
    stmt = """select a, b,
RUNNINGSUM (b) as rsum,
cast (RUNNINGAVG (b) as dec (18,3)) as ravg,
cast (MOVINGAVG (b, 5) as dec (18,3)) as mvavg
from seqtb108 sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test108.exp""", 's2')
    
    # Expecting
    #     A   B  RSum    RAvg    MvAvg
    #  ---------------------------------
    #     1   5   5     5.000    5.000
    #     2   5   10    5.000    5.000
    #     3   ?   10    5.000    5.000
    #     4   2   12    4.000    4.000
    #     5   4   16    4.000    4.000
    #     6   4   20    4.000    3.750
    #     7   ?   20    4.000    3.333
    #     8   5   25    4.166    3.750
    #     9   3   28    4.000    4.000
    
    # test with all NULLs in column B
    
    stmt = """delete from seqtb108;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into seqtb108 values           -- 10 rows
(1, null), (2, null), (3, null), (4, null), (5, null),
(6, null), (7, null), (8, null), (9, null), (10, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 10)
    
    stmt = """select a, b,
RUNNINGSUM (b) as rsum,
cast (RUNNINGAVG (b) as dec (18,3)) as ravg,
cast (MOVINGAVG (b, 5) as dec (18,3)) as mvavg
from seqtb108 sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test108.exp""", 's4')
    
    # Expecting all NULLs
    
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)


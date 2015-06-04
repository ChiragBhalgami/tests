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
    
def test001(desc="""test006"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test006
    # JClear
    # 1998-11-11
    # Sampling tests: tests on a vertically partitioned table (samptb3 & vwsamptb3)
    # 1. First-N
    #
    stmt = """select * from vwsamptb3 
sample first 10 rows
sort by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test006.exp""", 's1')
    # expect 10 rows with a values from 1-10
    
    stmt = """select * from vwsamptb3 
sample first 10 rows
sort by a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test006.exp""", 's2')
    # expect 10 rows with a values from 1-10
    
    stmt = """select * from vwsamptb3 
sample first 10 rows
sort by a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test006.exp""", 's3')
    # expect 10 rows with a values from 100-91
    
    stmt = """select * from vwsamptb3 
sample first 10 rows
order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test006.exp""", 's4')
    # expect 10 rows with a values from 1-10
    
    stmt = """select * from vwsamptb3 
sample first 10 rows
sort by a asc
order by a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test006.exp""", 's5')
    # expect 10 rows with a values from 10-1
    
    stmt = """select avg (b) from vwsamptb3 
sample first 10 rows;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test006.exp""", 's6')
    # expect avg b = 21290.200
    
    stmt = """select sum (b) from vwsamptb3 
sample first 10 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test006.exp""", 's7')
    # expect sum b = 212902
    
    _testmgr.testcase_end(desc)

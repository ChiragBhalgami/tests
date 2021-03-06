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
    
def test001(desc="""test016"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test016
    # JClear
    # 1998-11-02
    # Sampling tests: tests on a VP table using params
    # 2. Periodic
    #
    stmt = """set param ?zero 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?five 5;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?ten 10;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?fifty 50;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?twentyfive 25;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?hundred 100;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """select * from vwsamptb3 
sample periodic ?five rows every ?ten rows
sort by a;"""
    output = _dci.cmdexec(stmt)
    # expect 50 rows with a values from 1-5, 10-15 etc.
    
    stmt = """select * from vwsamptb3 
sample periodic ?five rows every ?ten rows
sort by a asc;"""
    output = _dci.cmdexec(stmt)
    # expect 50 rows with a values from 1-5, 10-15 etc.
    
    stmt = """select * from vwsamptb3 
sample periodic ?five rows every ?ten rows
sort by a desc;"""
    output = _dci.cmdexec(stmt)
    # expect 50 rows with a values from 1-5, 10-15 etc.
    
    stmt = """select * from vwsamptb3 
sample periodic ?five rows every ?ten rows
sort by a
order by a desc;"""
    output = _dci.cmdexec(stmt)
    # expect 50 rows with a values from 1-5, 10-15 etc.
    
    stmt = """select * from vwsamptb3 
where a between ?zero and ?hundred
sample periodic ?five rows every ?ten rows
sort by a;"""
    output = _dci.cmdexec(stmt)
    # expect 50 rows with a values from 1-5, 10-15 etc.
    
    # 3. Balance
    stmt = """select * from vwsamptb3 
sample by first of ?hundred
balance when a < ?fifty then ?twentyfive
when a > ?fifty then ?twentyfive
end
sort by a;"""
    output = _dci.cmdexec(stmt)
    # expect 10 rows with a values from 1-10
    
    stmt = """select * from vwsamptb3 
sample by first of ?hundred exact
balance when a < ?fifty then ?twentyfive
when a > ?fifty then ?twentyfive
end
sort by a;"""
    output = _dci.cmdexec(stmt)
    # expect 10 rows with a values from 1-10
    
    _testmgr.testcase_end(desc)


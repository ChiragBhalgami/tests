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
    
def test001(desc="""test017"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testx017
    # jclear
    # 1997-05-05
    # Extra tests on NIST database
    # IN with subquery & order by column number
    
    stmt = """select distinct a.empname from STAFF a
where a.empnum in
(select b.empnum from WORKS b
where a.empnum = b.empnum)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test017.exp""", 's1')
    #
    
    stmt = """select distinct a.empname from VWSTAFF a
where a.empnum in
(select b.empnum from VWWORKS b
where a.empnum = b.empnum)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test017.exp""", 's2')
    #
    
    _testmgr.testcase_end(desc)


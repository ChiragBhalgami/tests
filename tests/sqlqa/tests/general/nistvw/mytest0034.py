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

# TEST:0034 UPDATE table with SET column in <WHERE clause>!

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # setup
    stmt = """UPDATE STAFF
SET GRADE = 2*GRADE
WHERE GRADE = 13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    # PASS:0034 If 2 rows are updated?
    
    stmt = """SELECT COUNT(*)
FROM VWSTAFF
WHERE GRADE = 26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0034.exp""", """s1""")
    # PASS:0034 If count = 2?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update STAFF
set GRADE = GRADE/2
where GRADE = 26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    
    stmt = """select count (*) from VWSTAFF
where GRADE = 13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0034.exp""", """s2""")
    # pass if count = 2
    
    # END TEST >>> 0034 <<< END TEST

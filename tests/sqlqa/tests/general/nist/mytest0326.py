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

# TEST:0326 (2 pr.,1 son),P.K e, no F.K, modify P.K!

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
    
    # setup
    stmt = """DELETE  FROM STAFF3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """INSERT INTO STAFF3
SELECT * FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    stmt = """SELECT EMPNUM FROM STAFF3
WHERE EMPNUM = 'E1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0326.exp""", """test0326c""")
    # PASS:0326 If 1 row selected and EMPNUM = E1?
    stmt = """UPDATE STAFF3
SET EMPNAME = 'Alace'
WHERE EMPNAME = 'Alice';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """SELECT EMPNUM FROM STAFF3
WHERE EMPNAME = 'Alice';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # PASS:0326 If 0 rows selected, SQLCODE = 100, end of data?
    
    # cleanup
    stmt = """delete from staff3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    stmt = """COMMIT WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # END TEST >>> 0326 <<< END TEST
    

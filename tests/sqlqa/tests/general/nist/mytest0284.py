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

# TEST:0284 INSERT, SELECT char. strings with blank!

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
    stmt = """INSERT INTO STAFF(EMPNUM,EMPNAME)
VALUES ('E6','Ed');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO STAFF(EMPNUM,EMPNAME)
VALUES ('E7','Ed ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO STAFF(EMPNUM,EMPNAME)
VALUES ('E8','Ed                  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """SELECT COUNT(*) FROM STAFF
WHERE EMPNAME = 'Ed';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0284.exp""", """test0284d""")
    
    # PASS:0284 If count = 4?
    stmt = """SELECT COUNT(*) FROM STAFF
WHERE EMPNAME = 'Ed ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0284.exp""", """test0284e""")
    
    # PASS:0284 If count = 4?
    stmt = """SELECT COUNT(*) FROM STAFF
WHERE EMPNAME = 'Ed                ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0284.exp""", """test0284f""")
    
    # PASS:0284 If count = 4?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """select count (*) from staff;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0284.exp""", """test0284h""")
    # pass if count = 5
    
    # END TEST >>> 0284 <<< END TEST
    

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

# TEST:0269 BETWEEN value expressions in wrong order!

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
    
    stmt = """SELECT COUNT(*)
FROM VWWORKS
WHERE HOURS BETWEEN 80 AND 40;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0269.exp""", """s1""")
    # PASS:0269 If count = 0   ?
    
    # setup
    stmt = """INSERT INTO WORKS
VALUES('E6','P6',-60);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT COUNT(*)
FROM VWWORKS
WHERE HOURS BETWEEN -40 AND -80;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0269.exp""", """s2""")
    # PASS:0269 If count = 0?
    
    stmt = """SELECT COUNT(*)
FROM VWWORKS
WHERE HOURS BETWEEN -80 AND -40;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0269.exp""", """s3""")
    # PASS:0269 If count = 1?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count (*) from VWWORKS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0269.exp""", """s4""")
    # pass if count = 12
    
    # END TEST >>> 0269 <<< END TEST
    

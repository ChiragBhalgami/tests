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

# TEST:0237 FIPS sizing - identifier length 18!

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """DELETE FROM CHARACTER18TABLE18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # setup
    stmt = """INSERT INTO CHARACTERS18VIEW18
VALUES ('VALU');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0237 If 1 row is inserted?
    
    stmt = """COMMIT WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE CHARACTER18TABLE18
SET CHARS18NAME18CHARS = 'VAL4'
WHERE CHARS18NAME18CHARS = 'VALU';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # PASS:0237 If 1 row is updated?
    
    stmt = """COMMIT WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT *
FROM CHARACTERS18VIEW18 CANWEPARSELENGTH18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0237.exp""", """s1""")
    #- FROM CANWEPARSELENGTH18.CHARACTERS18VIEW18;    XXXXXX
    # PASS:0237 If LONGNAME18LONGNAME = 'VAL4' ?
    
    stmt = """SELECT CORRELATIONNAMES18.CHARS18NAME18CHARS
FROM CHARACTER18TABLE18 CORRELATIONNAMES18
WHERE CORRELATIONNAMES18.CHARS18NAME18CHARS = 'VAL4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0237.exp""", """s2""")
    
    # PASS:0237 If CORRELATIONNAMES18.CHARS18NAME18CHARS = 'VAL4'?
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # restore
    stmt = """DELETE FROM CHARACTER18TABLE18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """COMMIT WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count (*) from CHARACTERS18VIEW18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0237.exp""", """s3""")
    #pass if count = 0
    
    # END TEST >>> 0237 <<< END TEST
    

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

# test0024
# JClear
# 1999-04-07
# VALUES tests: using NIST test0024
#
# TEST:0024 INSERT:<query spec.> is empty: SQLCODE = 100!

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
    stmt = """INSERT INTO TEMP_S
SELECT EMPNUM,GRADE,CITY
FROM VWSTAFF
WHERE GRADE > 13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)
    # PASS:0024 If 0 rows selected, SQLCODE = 100, end of data?
    
    stmt = """values ((
select count (*) FROM TEMP_S
));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test024.exp""", """test024b""")
    # pass if count = 0
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """delete from TEMP_S;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """values ((
select count (*) FROM TEMP_S
));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test024.exp""", """test024c""")
    # pass if count = 0
    
    # END TEST >>> 0024 <<< END TEST
    

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

# TEST:0512 <value expression> for IN predicate!

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
    stmt = """SELECT MIN(PNAME)
FROM PROJ, WORKS, STAFF
WHERE PROJ.PNUM = WORKS.PNUM
AND WORKS.EMPNUM = STAFF.EMPNUM
AND BUDGET - GRADE * HOURS * 100 IN
(-4400, -1000, 4000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0512.exp""", """test0512a""")
    # PASS:0512 If PNAME = 'CALM'?
    stmt = """SELECT CITY, COUNT(*)
FROM PROJ
GROUP BY CITY
HAVING (MAX(BUDGET) - MIN(BUDGET)) / 2
IN (2, 20000, 10000)
ORDER BY CITY DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0512.exp""", """test0512b""")
    # PASS:0512 If in first row: CITY = 'Vienna' AND count = 2?
    # PASS:0512 AND in second row: CITY = 'Deale' AND count = 3?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # END TEST >>> 0512 <<< END TEST
    

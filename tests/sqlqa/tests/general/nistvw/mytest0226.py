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

# TEST:0226 FIPS sizing - 10 tables in SQL statement!
# FIPS sizing TEST

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """SELECT EMPNUM, EMPNAME
FROM VWSTAFF
WHERE EMPNUM IN
(SELECT EMPNUM  FROM VWWORKS
WHERE PNUM IN
(SELECT PNUM  FROM VWPROJ
WHERE PTYPE IN
(SELECT PTYPE  FROM VWPROJ
WHERE PNUM IN
(SELECT PNUM  FROM VWWORKS
WHERE EMPNUM IN
(SELECT EMPNUM  FROM VWWORKS
WHERE PNUM IN
(SELECT PNUM   FROM VWPROJ
WHERE PTYPE IN
(SELECT PTYPE  FROM VWPROJ
WHERE CITY IN
(SELECT CITY  FROM VWSTAFF
WHERE EMPNUM IN
(SELECT EMPNUM  FROM VWWORKS
WHERE HOURS = 20
AND PNUM = 'P2' )))))))))
order by empnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0226.exp""", """s1""")
    
    # PASS:0226 If 4 rows selected excluding EMPNUM='E5', EMPNAME='Ed'?
    
    # END TEST >>> 0226 <<< END TEST
    

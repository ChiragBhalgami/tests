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

# TEST:0155 CREATE Table with Unique (...), INSERT via SELECT!

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """select count(*)
from VWWORKS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0155.exp""", """s1""")
    # PASS:0155 If count = 12?
    
    # setup
    stmt = """insert into WORKS
select 'E3',pnum,100
from VWPROJ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    # PASS:0155 If ERROR, unique constraint, 0 rows inserted?
    
    stmt = """select count(*)
from VWWORKS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0155.exp""", """s3""")
    # PASS:0155 If count = 12?
    
    # restore
    #     ROLLBACK WORK;
    

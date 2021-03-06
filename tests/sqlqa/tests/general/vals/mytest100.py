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
    
    stmt = """create table valtb100 (a int not null not droppable primary key, b int, c int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into valtb100 values (1, 2, 3), (2, 3, 4), (3, 4, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    stmt = """values ('Just fine:', (select count (*) from valtb100));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test100.exp""", """test100c""")
    # expect 1 row with values: 'Just fine:' & 3
    
    stmt = """values ('Omigod:', (select * from valtb100));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    # expect a decent error message, e.g. subselect should select only 1 row
    

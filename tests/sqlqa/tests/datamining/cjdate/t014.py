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
    
def test001(desc="""test014"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test014
    # JClear
    # 1999-06-02
    # CJDate tests (5th ed. p161): subquery with IN & NOT IN
    # "Get supplier names for suppliers who supply part P2"
    #
    stmt = """select sname
from s 
where snum in
(select snum
from spj 
where pnum = 'p2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test014.exp""", 's1')
    # expect 1 row with value Adams
    
    #- select sname
    #-   from vps
    #-     where snum in
    #-       (select snum
    #-          from vpspj
    #- 	   where pnum = 'p2');
    # expect 1 row with value Adams
    
    stmt = """select sname
from hps 
where snum in
(select snum
from hpspj 
where pnum = 'p2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test014.exp""", 's2')
    # expect 1 row with value Adams
    
    # "Get supplier names for suppliers who do not supply part P2"
    #
    stmt = """select sname
from s 
where snum not in
(select snum
from spj 
where pnum = 'p2')
order by sname;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test014.exp""", 's3')
    # expect 4 rows with values Blake Clark Jones Smith
    
    #- select sname
    #-   from vps
    #-     where snum not in
    #-       (select snum
    #-          from vpspj
    #- 	   where pnum = 'p2')
    #- 	     order by sname;
    # expect 4 rows with values Blake Clark Jones Smith
    
    stmt = """select sname
from hps 
where snum not in
(select snum
from hpspj 
where pnum = 'p2')
order by sname;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test014.exp""", 's4')
    # expect 4 rows with values Blake Clark Jones Smith
    
    _testmgr.testcase_end(desc)


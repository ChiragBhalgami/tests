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
    
def test001(desc="""test086"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test086
    # JClear
    # 1999-01-20
    # Sequence functions - natural right join : moving functions (3 args)
    #        movingcount
    #        movingsum
    #        movingmax
    #        movingmin
    #        movingavg
    #        movingvariance
    #        movingstddev
    #
    # check the data first
    stmt = """select id, pay, doa
from seqtb81t1 natural right join seqtb81t2 
where id = id and pay > 15000.0
order by id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test086.exp""", 's1')
    
    # count, sum, max, min, avg
    stmt = """select id, lname, doa,
cast (pay as smallint) as pay,
cast (movingcount (pay, 3, 50) as smallint) as mcount,
cast (movingsum (pay, 3, 50) as int) as msum,
cast (movingmax (pay, 3, 50) as smallint) as mmax,
cast (movingmin (pay, 3, 50) as smallint) as mmin,
cast (movingavg (pay, 3, 50) as smallint) as mavg
from seqtb81t1 natural right join seqtb81t2 
where id = id and pay > 15000.0
sample first 20 rows
sort by id
sequence by id
order by id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test086.exp""", 's2')
    # expect 20 rows
    
    # avg, variance, stddev
    stmt = """select id, lname, doa,
cast (pay as smallint) as pay,
cast (movingavg (pay, 3, 50) as dec (15,3)) as mavg,
cast (movingvariance (pay, 3, 50) as dec (15,3)) as mvariance,
cast (movingstddev (pay, 3, 50) as dec (15,3)) as mstddev
from seqtb81t1 natural right join seqtb81t2 
where id = id and pay > 15000.0
sample first 20 rows
sort by id
sequence by id
order by id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test086.exp""", 's3')
    # expect 20 rows
    
    _testmgr.testcase_end(desc)


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
import defs

_testmgr = None
_testlist = []
_dci = None

# single column char key
# 150,000 recs
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """Create Table btpnl23
(
char0_20            Character(8)          not null,
sdec0_uniq          PIC S9(9)             not null,
varchar0_20         varchar(16)      not null,
ubin0_20            PIC 9(7)V9(2) COMP    not null,
sbin0_uniq          Numeric(18) signed    not null,
udec0_4             Decimal(9) unsigned   not null,
sbin1_500           Numeric(4) signed     not null,
sdec1_100           Decimal(18) signed    not null,
char1_uniq          Character(128)        not null,
varchar1_2          varchar(8)       not null,
primary key ( char1_uniq  DESC ) not droppable
)
store by primary key
attributes extent(1024,1024), maxextents 512
;"""
    output = _dci.cmdexec(stmt)

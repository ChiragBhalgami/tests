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
    
    stmt = """create table tab_rem_emp_original
(
sdec0_2             PIC S9(9)             not null,
varchar0_100        varchar(16)      not null,
char0_4             Character(8)          not null,
sbin0_uniq          Numeric(18) signed    not null,
udec0_100           Decimal(9) unsigned   not null,
ubin0_uniq          PIC 9(7)V9(2) COMP    not null,
sdec1_20            Decimal(18) signed    not null,
varchar1_10         varchar(8)       not null,
sbin1_1000          Numeric(4) signed     not null,
char1_10            Character(4)          not null,
primary key ( sbin0_uniq ) not droppable
)
store by primary key
location """ + gvars.g_disc1 + """
hash partition(
add location """ + gvars.g_disc2 + """,
add location """ + gvars.g_disc3 + """,
add location """ + gvars.g_disc4 + """
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tab_rem_ten_original
(
sdec0_2             PIC S9(9)             not null,
varchar0_100        varchar(16)      not null,
char0_4             Character(8)          not null,
sbin0_uniq          Numeric(18) signed    not null,
udec0_100           Decimal(9) unsigned   not null,
ubin0_uniq          PIC 9(7)V9(2) COMP    not null,
sdec1_20            Decimal(18) signed    not null,
varchar1_10         varchar(8)       not null,
sbin1_1000          Numeric(4) signed     not null,
char1_10            Character(4)          not null,
primary key ( sbin0_uniq ) not droppable
)
store by primary key
location """ + gvars.g_disc1 + """
range partition (
add first key 100 location """ + gvars.g_disc2 + """,
add first key 200 location """ + gvars.g_disc3 + """,
add first key 300 location """ + gvars.g_disc4 + """
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tab_rem_lrg_original
(
sdec0_2             PIC S9(9)             not null,
varchar0_100        varchar(16)      not null,
char0_4             Character(8)          not null,
sbin0_uniq          Numeric(18) signed    not null primary key,
udec0_100           Decimal(9) unsigned   not null,
ubin0_uniq          PIC 9(7)V9(2) COMP    not null,
sdec1_20            Decimal(18) signed    not null,
varchar1_10         varchar(8)       not null,
sbin1_1000          Numeric(4) signed     not null,
char1_10            Character(4)          not null
)
location """ + gvars.g_disc1 + """
;"""
    output = _dci.cmdexec(stmt)
    

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

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """create table date_dim
(
d_date_sk                 integer               not null,
d_date_id                 char(16)              not null,
d_date                    date                          ,
d_month_seq               integer                       ,
d_week_seq                integer                       ,
d_quarter_seq             integer                       ,
d_year                    integer                       ,
d_dow                     integer                       ,
d_moy                     integer                       ,
d_dom                     integer                       ,
d_qoy                     integer                       ,
d_fy_year                 integer                       ,
d_fy_quarter_seq          integer                       ,
d_fy_week_seq             integer                       ,
d_day_name                char(9)                       ,
d_quarter_name            char(6)                       ,
d_holiday                 char(1)                       ,
d_weekend                 char(1)                       ,
d_following_holiday       char(1)                       ,
d_first_dom               integer                       ,
d_last_dom                integer                       ,
d_same_day_ly             integer                       ,
d_same_day_lq             integer                       ,
d_current_day             char(1)                       ,
d_current_week            char(1)                       ,
d_current_month           char(1)                       ,
d_current_quarter         char(1)                       ,
d_current_year            char(1)                       ,
primary key (d_date_sk)
)"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ hash2 partition attributes extent (256) maxextents 700;"""
    output = _dci.cmdexec(stmt)
    

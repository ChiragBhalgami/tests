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
    
    stmt = """create table web_site
(
web_site_sk               integer               not null,
web_site_id               char(16)              not null,
web_rec_start_date        date                          ,
web_rec_end_date          date                          ,
web_name                  varchar(50)                   ,
web_open_date_sk          integer                       ,
web_close_date_sk         integer                       ,
web_class                 varchar(50)                   ,
web_manager               varchar(40)                   ,
web_mkt_id                integer                       ,
web_mkt_class             varchar(50)                   ,
web_mkt_desc              varchar(100)                  ,
web_market_manager        varchar(40)                   ,
web_company_id            integer                       ,
web_company_name          char(50)                      ,
web_street_number         char(10)                      ,
web_street_name           varchar(60)                   ,
web_street_type           char(15)                      ,
web_suite_number          char(10)                      ,
web_city                  varchar(60)                   ,
web_county                varchar(30)                   ,
web_state                 char(2)                       ,
web_zip                   char(10)                      ,
web_country               varchar(20)                   ,
web_gmt_offset            decimal(5,2)                  ,
web_tax_percentage        decimal(5,2)                  ,
primary key (web_site_sk)
)"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ no partition attributes extent (256) maxextents 700;"""
    output = _dci.cmdexec(stmt)
    

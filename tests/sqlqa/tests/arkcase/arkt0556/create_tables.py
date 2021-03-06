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
    
def test001(desc="""create tables"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    prop_template = defs.test_dir + '/../../lib/t4properties.template'
    prop_file = defs.work_dir + '/t4properties'
    hpdci.create_jdbc_propfile(prop_template, prop_file, defs.w_catalog, defs.w_schema)
    
    stmt = """drop table b2uwl02;"""
    output = _dci.cmdexec(stmt)
    stmt = """Create Table b2uwl02 
(
char0_n10           Character(2)
default 'AD' heading 'char0_n10 with default AD',
sbin0_uniq          Smallint                   not null,
sdec0_n500          Decimal(18)                        ,
date0_uniq          Date                 no default not null,
int0_yTOm_nuniq     Interval year(5) to month    no default,    

int1_hTOs_1000      Interval hour(2) to second(0)   not null,
date1_n4            Date                               ,
real1_uniq          Real                    no default not null,
ubin1_n2            Numeric(4) unsigned        no default,
udec1_100           Decimal(2) unsigned        not null,    

char2_2             Character(2)               not null,
sbin2_nuniq         Largeint                           ,
sdec2_500           Decimal(9) signed       no default not null,
date2_uniq          Date                       not null,
int2_dTOf6_n2       Interval day to second(6)      no default,
real2_500           Real                       not null,    

real3_n1000         Real                               ,
int3_yTOm_4         Interval year(1) to month no default not null,
date3_n2000         Date                            no default,
udec3_n100          Decimal(9) unsigned                ,
ubin3_n2000         Numeric(4) unsigned                ,
char3_4             Character(8)             no default not null,
sdec4_n20           Decimal(4)                  no default,
int4_yTOm_uniq      Interval year(5) to month   not null,
sbin4_n1000         Smallint                           ,
time4_1000          Time                   no default not null,
char4_n10           Character(8)               no default,
real4_2000          Real                       not null,    

char5_n20           Character(8)                       ,
sdec5_10            Decimal(9) signed       no default not null,
ubin5_n500          Numeric(9) unsigned       no default,
real5_uniq          Real                       not null,
dt5_yTOmin_n500     Timestamp(0)            ,
int5_hTOs_500       Interval hour to second(0) no default not null,    

int6_dTOf6_nuniq    Interval day to second(6)     no default,
sbin6_nuniq         Largeint                      no default,
double6_n2          Float(23)                          ,
sdec6_4             Decimal(4) signed       no default not null,
char6_n100          Character(8)               no default,
date6_100           Date                       not null,    

time7_uniq          Time                       not null,
sbin7_n20           Smallint                      no default,
char7_500           Character(8)            no default not null,
int7_hTOs_nuniq     Interval hour(2) to second(0)        ,
udec7_n10           Decimal(4) unsigned                ,
real7_n4            Real                               ,
ubin8_10            Numeric(4) unsigned        not null,
int8_y_n1000        Interval year(3)                   ,
date8_10            Date                    no default not null,
char8_n1000         Character(8)               no default,
double8_n10         Double Precision           no default,
sdec8_4             Decimal(9) unsigned        not null,    

sdec9_uniq          Decimal(18) signed       no default not null,
real9_n20           Real                               ,
time9_n4            Time                               ,
char9_100           Character(2)             no default not null,
int9_dTOf6_2000     Interval day to second(6)   no default not null,
ubin9_n4            Numeric(9) unsigned         no default,    

ubin10_n2           Numeric(4) unsigned         no default,
char10_nuniq        Character(8)                       ,
int10_d_uniq        Interval day(6)            not null,
ts10_n2             Timestamp                          ,
real10_100          Real                       not null,
udec10_uniq         Decimal(9) unsigned     no default not null,    

udec11_2000         Decimal(9) unsigned   no default not null,
int11_h_n10         Interval hour(1)           no default,
sbin11_100          Integer                    not null,
time11_20           Time                       not null,
char11_uniq         Character(8)               not null,
double11_n100       Double Precision                   ,
real12_n20          Real                               ,
ubin12_2            Numeric(4) unsigned     no default not null,
dt12_mTOh_1000      Timestamp(0)        no default not null,
sdec12_n1000        Decimal(18) signed           no default,
char12_n2000        Character(8)                no default,
int12_yTOm_100      Interval year to month     not null,    

int13_yTOm_n1000    Interval year to month             ,
udec13_500          Decimal(9) unsigned     no default not null,
sbin13_n100         PIC S9(9)V9 COMP           no default,
ts13_uniq           Timestamp                  not null,
char13_1000         Character(8)               not null,
real13_n1000        Real                               ,    

sbin14_1000         Integer                no default not null,
double14_nuniq      Float(23)                 no default,
udec14_100          Decimal(4) unsigned        not null,
char14_n500         Character(8)                       ,
int14_d_500         Interval day(3)         no default not null,
ts14_n100           Timestamp               no default,    

dt15_mTOh_n100      Timestamp(0)                 no default,
double15_uniq       Double Precision           not null,
sbinneg15_nuniq     Largeint                           ,
sdecneg15_100       Decimal(9) signed       no default not null,
int15_dTOf6_n100    Interval day to second(6)     no default,
char15_100          Character(8)               not null,
dt16_m_n10          date                     ,
int16_h_20          Interval hour           no default not null,
ubin16_n10          Numeric(4) unsigned        no default,
sdec16_uniq         Decimal(18) signed         not null,
char16_n20          Character(5)        ,   -- len = 2,4
real16_10           Real                  no default not null,    

int17_y_n10         Interval year(1)         no default,
dt17_yTOmin_uniq    Timestamp(0)    not null,
real17_n100         Real                               ,
sbin17_uniq         Largeint  no default not null,  -- range: 0-149999
sdec17_nuniq        Decimal(18)                no default,
char17_2            Character(8)               not null
)
store by ( sbin0_uniq )
--   attributes audit
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table btuns01;"""
    output = _dci.cmdexec(stmt)
    stmt = """Create Table btuns01 
(
char0_20            Character(8)          not null,
sbin0_2             Numeric(18) signed    not null,
udec0_10            Decimal(9) unsigned   not null,
varchar0_2          varchar(16)      not null,
sdec0_1000          PIC S9(9)             not null,
ubin0_20            PIC 9(7)V9(2) COMP    not null,    

char1_2             Character(16)         not null,
sdec1_uniq          Decimal(18) signed    not null,
sbin1_100           Numeric(4) signed     not null,
varchar1_uniq       varchar(8)       not null
) no partition
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table b2unl15;"""
    output = _dci.cmdexec(stmt)
    stmt = """Create Table b2unl15 
(
char0_100           Character(8)          not null,
sbin0_uniq          Integer               not null,
sdec0_n10           Decimal(4)           default 9,
int0_yTOm_n1000     Interval year(2) to month    no default,
date0_nuniq         Date                         no default,    

real1_uniq          Real                  not null,
ts1_n100            Timestamp                     ,
ubin1_500           Numeric(4) unsigned      no default not null,
int1_dTOf6_nuniq    Interval day to second(6)       no default,
udec1_50p           Decimal(9) unsigned   not null    
-- , primary key ( real1_uniq ) not droppable
) 
-- store by primary key
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table b2uns09;"""
    output = _dci.cmdexec(stmt)
    stmt = """Create Table b2uns09 
(
char0_100       Character(5)  no default not null, -- len = 2,4
sbin0_100       Integer                     no default not null,
int0_dTOf6_n100 Interval day to second(6)          no default,
sdec0_nuniq     Decimal(9)                           no default,
time0_nuniq     Time                             ,    

dt1_mTOh_n20        Timestamp(0),
udec1_2             Decimal(9) unsigned      not null,
int1_h_n10          Interval hour(1)   default interval '8' hour,
ubin1_uniq          Numeric(9) unsigned      not null,
real1_uniq          Real                     no default not null,    

primary key  ( real1_uniq) not droppable
) no partition
store by primary key
attributes
--  audit,
blocksize 4096;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table b2pns01;"""
    output = _dci.cmdexec(stmt)
    stmt = """create table b2pns01 
(
char0_n10           Character(2)
default 'AD' heading 'char0_n10 with default AD',
sbin0_uniq          Smallint                       not null,
sdec0_n500          Decimal(18)                    ,
date0_uniq          Date                     no default not null,
int0_yTOm_nuniq     Interval year(5) to month      no default,
int1_hTOs_1000      Interval hour(2) to second     not null,
date1_n4            Date                           ,
real1_uniq          Real                    no default not null,
ubin1_n2            Numeric(4) unsigned            no default,
udec1_100           Decimal(2) unsigned            not null
) no partition
attribute
--  audit,
blocksize 4096;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table b2pns03;"""
    output = _dci.cmdexec(stmt)
    stmt = """create table b2pns03 
(
sbin0_4             Integer             default 3 not null,
time0_uniq          Time                          not null,
varchar0_uniq       VarChar(8)         no default not null,
sdec0_n1000         Decimal(9)                    no default,
int0_dTOf6_4        Interval day to second(6)     not null,
ts1_n100            Timestamp     heading 'ts1_n100 allowing nulls',
ubin1_20            Numeric(9) unsigned  no default not null,
int1_yTOm_n100      Interval year(1) to month     no default,
double1_2           Double Precision              not null,
udec1_nuniq         Decimal(4) unsigned           ,
primary key ( time0_uniq  DESC)
) number of partitions 3
store by primary key
attribute
blocksize 4096;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table b3uns03;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE b3uns03 
(
VARCHAR0_AAZZ09BP_100          VARCHAR(8)
, CHAR0_ASCII_500                CHAR(8)
, UDEC0_UNIQ                     DECIMAL( 9, 0 ) UNSIGNED NOT NULL
, VARCHAR0_ISO_UNIQ              VARCHAR(8)
, CHAR0_ISOASC_UNIQ              CHAR(8)
, NVARCHAR1_09_UNIQ              VARCHAR(16)
, VARCHAR1_20                    VARCHAR(8)
, NCHAR1_AZ_20                   CHAR(16)
, NVARCHAR_AZAZ_100              VARCHAR(16)
, NCHAR1_UNIQ                    CHAR(16)
, PRIMARY KEY (UDEC0_UNIQ)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table b2uns01;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create Table b2uns01 
(
char0_n10           Character(2)
default 'AD' heading 'char0_n10 with default AD',
sbin0_uniq          Smallint              not null,
sdec0_n500          Decimal(18)                   ,
date0_uniq          Date                     no default not null,
int0_yTOm_nuniq     Interval year(5) to month         no default,    

int1_hTOs_1000      Interval hour(2) to second  not null,
date1_n4            Date                          ,
real1_uniq          Real                     no default not null,
ubin1_n2            Numeric(4) unsigned               no default,
udec1_100           Decimal(2) unsigned    not null
) no partition
attributes
-- audit,)
blocksize 4096;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table b3uns01;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE b3uns01 
(
CHAR0_09_UNIQ                  CHAR(8) NOT NULL
, VARCHAR0_MONEY_100             VARCHAR(8)
, CHAR0_AZ_UNIQ                  CHAR(8)
, VARCHAR0_AZAZ_20               VARCHAR(15)
, CHAR0_AAZY_UNIQ                CHAR(8)
, VARCHAR1_AAZZB_500             VARCHAR(8)
, CHAR1_AAZZ09BP_UNIQ            CHAR(8)
, UDEC1_UNIQ                     DECIMAL( 9, 0 ) UNSIGNED
, VARCHAR1_ASCII_UNIQ            VARCHAR(8)
, VARCHAR1_UNIQ                  VARCHAR(8)
, PRIMARY KEY (CHAR0_09_UNIQ)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table b3uns05;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE b3uns05 
(
CHAR0_AAZY_20                  CHAR(1)
, NCHAR0_UNIQ                    CHAR(16)
, CHAR0_09_COLDESCAN_100         CHAR(8)
, SBIN0_UNIQ                     NUMERIC( 18, 0) NOT NULL
, CHAR0_AAZZ09BP_COLDESCAN_100   CHAR(8)
, NCHAR1_UNIQ                    CHAR(16)
, NVARCHAR1_AZAZ_10              VARCHAR(16)
, CHAR1_AZ_2                     CHAR(8)
, CHAR1_COLCHSET_4               CHAR(8)
, CHAR1_AAZZB_COLCASEINS_500     CHAR(8)
, PRIMARY KEY (SBIN0_UNIQ)
);"""
    output = _dci.cmdexec(stmt)

    tablelist = [['b2uwl02', '5000'], ['btuns01', '1500'], ['b2unl15', '150000'],
                 ['b2uns09', '1500'], ['b2pns01', '1500'], ['b2pns03', '1500'],
                 ['b3uns03', '1500'], ['b2uns01', '1500'], ['b3uns01', '1500'],
                 ['b3uns05', '1500']]
    delim = ','
    for t in tablelist:
        name = t[0]
        row_count = t[1]
        table = defs.my_schema + '.' + name
        data_file = defs.test_dir + '/' + name + '.dat'
        output = _testmgr.data_loader(defs.work_dir, prop_file, table, data_file, delim)
        _dci.expect_loaded_msg(output)

        stmt = """select count(*) from """ + name + """;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_str_token(output, row_count)

    _testmgr.testcase_end(desc)


# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
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
import setup

_testmgr = None
_testlist = []
_dci = None

# internal function
def my_verify(table, num_rows, min, max, increment):
    global _testmgr
    global _testlist
    global _dci

    if min == 'DEFAULT':
        min = 1

    if max == 'DEFAULT':
        max = 9223372036854775806

    if increment == 'DEFAULT':
       increment = 1

    # Put all inserts in a transation.  This is only to test user transaction
    # works for with IDENTITY.
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Try 2 different types of inserts first
    val = 1
    stmt = """insert into """ + table + """(c2, c3) values (""" + str(val) + """,""" + str(val) + """);"""
    output = _dci.cmdexec(stmt)
    if val <= num_rows:
        _dci.expect_inserted_msg(output, 1)
    else:
        _dci.expect_error_msg(output, '8934')

    val += 1
    stmt = """insert into """ + table + """ values(DEFAULT,""" + str(val) + """,""" + str(val) + """);"""
    output = _dci.cmdexec(stmt)
    if val <= num_rows:
        _dci.expect_inserted_msg(output, 1)
    else:
        _dci.expect_error_msg(output, '8934')

    # The rest are extra inserts if needed
    while val < num_rows:
       val += 1
       stmt = """insert into """ + table + """(c2, c3) values (""" + str(val) + """,""" + str(val) + """);"""
       output = _dci.cmdexec(stmt)
       _dci.expect_inserted_msg(output, 1)

    # The last one is just a negative test
    if min + num_rows * increment > max:
       val += 1
       stmt = """insert into """ + table + """(c2, c3) values (""" + str(val) + """,""" + str(val) + """);"""
       output = _dci.cmdexec(stmt)
       # could be error 1579 or 8934
       _dci.expect_error_msg(output)

    stmt = """select * from """ + table + """ order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, num_rows)

    # make sure that no key was generated outside of the range.
    stmt = """select * from """ + table + """ where c1<""" + str(min) + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)

    stmt = """select * from """ + table + """ where c1>""" + str(max) + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)

    # make sure the increment is correct
    val = min
    count = 0
    while (count < num_rows):
        stmt = """select * from """ + table + """ where c1=""" + str(val) + """;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output, 1)
        count += 1
        val += increment

    # roll back everything
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from """ + table + """ order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)


def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()

def test001(desc="""attr: START WITH"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # Maximum value for largeint IDENTITY is 9223372036854775806
    # This should fail
    stmt = """create table t1 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(START WITH 9223372036854775807) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1573')

    # START WITH 9223372036854775806 should fail.  Not enough room for cache.
    stmt = """create table t2 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(START WITH 9223372036854775806) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1577')

    # START WITH 9223372036854775797 should have room for 10 inserts
    stmt = """create table t3 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(START WITH 9223372036854775797) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t3', 10, 9223372036854775797, 'DEFAULT', 'DEFAULT')

    # START WITH 50 should have plenty of room until it reaches maximum.
    stmt = """create table t4 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(START WITH 50) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t4', 100, 50, 'DEFAULT', 'DEFAULT')

    # Clean up
    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t3 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t4 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test002(desc="""attr: MINVALUE"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # Maximum value for largeint IDENTITY is 9223372036854775806
    # This should fail
    stmt = """create table t1 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(MINVALUE 9223372036854775807) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1570')

    # This should fail, MINVALUE needs to be smaller than the default MAXVALUE
    stmt = """create table t2 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(MINVALUE 9223372036854775806) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1570')

    # This should fail, MINVALUE cannot be a negative number
    stmt = """create table t3 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(MINVALUE -1) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1572')

    # This should fail, MINVALUE cannot be 0 either
    stmt = """create table t4 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(MINVALUE 0) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1571')

    # This should fail, MINVALUE needs to be smaller than MAXVALUE
    stmt = """create table t5 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(MINVALUE 9223372036854775805 MAXVALUE 9223372036854775804) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1570')

    # MINVALUE 9223372036854775806 should allow 2 inserts
    stmt = """create table t6 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(MINVALUE 9223372036854775805) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t6', 2, 9223372036854775805, 'DEFAULT', 'DEFAULT')

    # NO MINVALUE with MAXVALUE 2 shuld allows 2 inserts
    stmt = """create table t7 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(NO MINVALUE MAXVALUE 2) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t7', 2, 'DEFAULT', 2, 'DEFAULT')

    # Clean up
    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t3 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t4 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t5 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t6 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t7 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test003(desc="""attr: MAXVALUE"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # Maximum value for largeint IDENTITY is 9223372036854775806
    # This should fail
    stmt = """create table t1 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(MAXVALUE 9223372036854775807) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1576')
  
    # This should fail, MAXVALUE should not be the same as MINVALUE
    stmt = """create table t2 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(MAXVALUE 1) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1570')

    # This should fail, MAXVALUE cannot be a negative number
    stmt = """create table t3 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(MAXVALUE -1) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1572')

    # This should fail, MAXVALUE cannot be 0 either
    stmt = """create table t4 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(MAXVALUE 0) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1571')

    # This should fail, MINVALUE needs to be smaller than MAXVALUE
    stmt = """create table t5 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(MAXVALUE 1 MINVALUE 2) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1570')

    # MAXVALUE 2 shuld allows 2 inserts
    stmt = """create table t6 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(MAXVALUE 2) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t6', 2, 'DEFAULT', 2, 'DEFAULT')

    # MINVALUE 9223372036854775806 with NO MAXVALUE should allow 2 inserts
    stmt = """create table t7 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(MINVALUE 9223372036854775805 NO MAXVALUE) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t7', 2, 9223372036854775805, 'DEFAULT', 'DEFAULT')
 
    # Clean up
    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t3 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t4 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t5 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t6 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t7 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test004(desc="""attr: INCREMENT BY"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # Maximum value for largeint IDENTITY is 9223372036854775806
    # This should fail
    stmt = """create table t1 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(INCREMENT BY 9223372036854775807) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1575')

    # This should fail, INCREMENT BY a negative number is not allowed
    stmt = """create table t2 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(INCREMENT BY -1) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1572')

    # This should fail, INCREMENT BY 0 is not allowed either
    stmt = """create table t3 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(INCREMENT BY 0) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1571')

    # increment by 10
    stmt = """create table t4 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(INCREMENT BY 10) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t4', 100, 'DEFAULT', 'DEFAULT', 10)

    # Clean up
    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t3 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t4 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test005(desc="""attr: NO CYCLE"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # Specifying NO CYCLE really does not make any difference.  SQL Reference
    # Manual clearly says that NO CYCLE is the only cycle option supported, 
    # so it is the default value anyway.  This is just to make sure that the
    # syntax does not get rejected.
    # MAXVALUE 2 shuld allows 2 inserts
    stmt = """create table t1 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(MAXVALUE 2 NO CYCLE) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t1', 2, 'DEFAULT', 2, 'DEFAULT')

    # Clean up
    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test006(desc="""attr: no attribute"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # Try 50 inserts
    stmt = """create table t1 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t1', 50, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # Clean up
    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test007(desc="""attr: mixed attributes"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # This should fail.  INCREMENT BY shouldn't be bigger than the difference
    # between MAXVALUE and MINVALUE
    stmt = """create table t1 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(START WITH 1
 INCREMENT BY 20
 MAXVALUE 10
 MINVALUE 1
 NO CYCLE) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1575')

    # This should fail.  START WITH must be greater than or equal to MINVALUE
    # and less than or equal to MAXVALUE
    stmt = """create table t2 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(START WITH 99
 INCREMENT BY 1
 MAXVALUE 101
 MINVALUE 100
 NO CYCLE) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1573')

    # This should fail.  START WITH must be greater than or equal to MINVALUE
    # and less than or equal to MAXVALUE
    stmt = """create table t3 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(START WITH 99
 INCREMENT BY 1
 MAXVALUE 98
 MINVALUE 97
 NO CYCLE) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1573')
 
    # 1 - 11 increment by 10 should allow 2 inserts
    stmt = """create table t4 (
c1 largeint GENERATED ALWAYS AS IDENTITY 
(START WITH 1 
 INCREMENT BY 10 
 MAXVALUE 11 
 MINVALUE 1 
 NO CYCLE) not null not droppable,
c2 int not null not droppable, c3 smallint);""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t4', 2, 1, 11, 10)

    # 9223372036854775802 - 9223372036854775806 increment by 1 should allow
    # 5 inserts
    stmt = """create table t5 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(START WITH 9223372036854775802
 INCREMENT BY 1
 MAXVALUE 9223372036854775806
 MINVALUE 9223372036854775802
 NO CYCLE) not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t5', 5, 9223372036854775802, 9223372036854775806, 1)

    # Clean up
    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t3 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t4 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t5 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test008(desc="""key: primary key"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # primary key asc
    stmt = """create table t1 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint,
primary key (c1)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t1', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # primary key desc
    stmt = """create table t2 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint,
primary key (c1 desc)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t2', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # multiple primary keys 
    stmt = """create table t3 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint,
primary key (c1 desc, c2 asc)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t3', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # Clean up
    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t3 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test009(desc="""key: clustering key"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # single clustering key
    stmt = """create table t1 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint
) store by (c1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t1', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # multiple clustering keys
    stmt = """create table t2 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint
) store by (c1, c2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t2', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # single primary key asc + single clustering key
    stmt = """create table t3 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint,
primary key (c1)
) store by (c1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t3', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # single primary key desc + single clustering key
    stmt = """create table t4 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint,
primary key (c1 desc)
) store by (c1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t4', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # multiple primary keys + multiple clustering keys
    stmt = """create table t5 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint,
primary key (c1 desc, c2 asc)
) store by (c1, c2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t5', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # Clean up
    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t3 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t4 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t5 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test010(desc="""key: salting key"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # single primary key asc + single salting key
    stmt = """create table t1 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint,
primary key (c1)
) salt using 5 partitions on (c1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t1', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # single primary key desc + single salting key
    stmt = """create table t2 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint,
primary key (c1 desc)
) salt using 5 partitions on (c1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t2', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # multiple primary keys + multiple salting keys
    stmt = """create table t3 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint,
primary key (c1 desc, c2 asc)
) salt using 5 partitions on (c1, c2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t3', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # single clustering key + single salting key
    stmt = """create table t4 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint
) store by (c1) salt using 5 partitions on (c1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t4', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # multiple clustering keys + multiple salting keys
    stmt = """create table t5 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint
) store by (c1, c2) salt using 5 partitions on (c1, c2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t5', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # single primary key asc + single clustering key + single salting key
    stmt = """create table t6 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint,
primary key (c1)
) store by (c1) salt using 5 partitions on (c1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t6', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # single primary key desc + single clustering key + single salting key
    stmt = """create table t7 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint,
primary key (c1 desc)
) store by (c1) salt using 5 partitions on (c1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t7', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # multiple primary keys + multiple clustering keys + multiple salting keys
    stmt = """create table t8 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint,
primary key (c1 desc, c2 asc)
) store by (c1, c2) salt using 5 partitions on (c1, c2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t8', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # Clean up
    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t3 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t4 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t5 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t6 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t7 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t8 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test011(desc="""columns and data types"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # IDENTITY can only be largeint, int unsigned, or smallint unsigned.

    # largeint as IDENTITY
    stmt = """create table t1 (
c1 largeint GENERATED ALWAYS AS IDENTITY,
c2 int,
c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t1', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # int unsigned as IDENTITY
    stmt = """create table t2 (
c1 int unsigned GENERATED ALWAYS AS IDENTITY,
c2 largeint,
c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t2', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # smallint unsigned as IDENTITY
    stmt = """create table t3 (
c1 smallint unsigned GENERATED ALWAYS AS IDENTITY,
c2 largeint,
c3 int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t3', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # This should fail.  Int as IDENTITY is not allowed
    stmt = """create table t4 (c1 int GENERATED ALWAYS AS IDENTITY);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1510')

    # This should fail.  Smallint as IDENTITY is not allowed
    stmt = """create table t5 (c1 smallint GENERATED ALWAYS AS IDENTITY);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1510')

    # This should fail.  Char as IDENTITY is not allowed
    stmt = """create table t6 (c1 char(10) GENERATED ALWAYS AS IDENTITY);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1510')

    # IDENTITY column by default is NOT NULL, SQL automatically adds it
    # if it is not specified.
    stmt = """create table t7 (c1 largeint GENERATED ALWAYS AS IDENTITY);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl t7;"""
    output =  _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _dci.expect_any_substr(output, 'NOT NULL')

    # This should fail.  2 IDENTITY columns is not allowed.
    stmt = """create table t8 (
c1 largeint GENERATED ALWAYS AS IDENTITY,
c2 largeint GENERATED ALWAYS AS IDENTITY,
c3 int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1511')

    # Clean up
    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t3 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t4 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t5 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t6 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t7 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t8 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test012(desc="""constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # This should fail, the constraint c1 > 300 is outside the range of
    # MINVALUE and MAXVALUE
    stmt = """create table t1 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(MINVALUE 100 MAXVALUE 200) not null not droppable,
c2 int not null not droppable, c3 smallint,
check (c1 > 300));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    # inserts should all fail
    stmt = """insert into t1(c2, c3) values (1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')

    stmt = """insert into t1 values(DEFAULT,2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')

    # This should work, the constraint is consistent with the range of
    # MINVALUE and MAXVALUE
    stmt = """create table t2 (
c1 largeint GENERATED ALWAYS AS IDENTITY
(MINVALUE 100 MAXVALUE 200) not null not droppable,
c2 int not null not droppable, c3 smallint,
check (c1 >= 100 and c1 <= 200));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t2', 5, 100, 200, 'DEFAULT')

    # Clean up
    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t2 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test013(desc="""indexes and unique indexes"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # index asc
    stmt = """create table t1 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create index t1idx on t1 (c1 asc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t1', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # index desc
    stmt = """create table t2 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create index t2idx on t2 (c1 desc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t2', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # unique index asc
    stmt = """create table t3 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create unique index t3idx on t3 (c1 asc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t3', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # unique index desc
    stmt = """create table t4 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create unique index t4idx on t4 (c1 desc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t4', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # index no populate
    stmt = """create table t5 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create index t5idx on t5 (c1 asc) no populate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t5', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    stmt = """insert into t5 values (DEFAULT,1,1),(DEFAULT,2,2),(DEFAULT,3,3),(DEFAULT,4,4),(DEFAULT,5,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    stmt = """populate index t5idx on t5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from t5 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 5)

    # unique index no populate
    stmt = """create table t6 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create unique index t6idx on t6 (c1 asc) no populate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t6', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    stmt = """insert into t6 values (DEFAULT,1,1),(DEFAULT,2,2),(DEFAULT,3,3),(DEFAULT,4,4),(DEFAULT,5,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    stmt = """populate index t6idx on t6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from t6 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 5)

    # Clean up
    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t3 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t4 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t5 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t6 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test014(desc="""modify ALWAYS value"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create table t1 (
c1 largeint GENERATED ALWAYS AS IDENTITY not null not droppable,
c2 int not null not droppable, c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # delete from should work, even though we have an empty table
    stmt = """delete from t1 where c1>0 or c2=0 and c3>0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)

    # The following cases should all fail.  An IDENTITY column defined as
    # ALWAYS does not allow the user to touch it.

    stmt = """insert into t1 values(1,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3428')

    stmt = """update t1 set c1=-1 where c1<=9223372036854775806;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3428')

    # Clean up
    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test015(desc="""insert|upsert...select"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # insert|upsert...select should fail if target table has
    # ALWAYS IDENTITY column as well.

    stmt = """create table t1 (
c1 largeint GENERATED ALWAYS AS IDENTITY (MINVALUE 9991),
c2 int,
c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into t1 values (DEFAULT,1,1),(DEFAULT,2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    # Insert should fail.  Target table has ALWAYS IDEINTITY column
    stmt = """create table t2 (
c1 largeint GENERATED ALWAYS AS IDENTITY (MINVALUE 9991),
c2 int,
c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into t2 select * from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3428')

    # Upsert should fail.  Target table has ALWAYS IDEINTITY column
    stmt = """create table t3 (
c1 largeint GENERATED ALWAYS AS IDENTITY (MINVALUE 9991),
c2 int,
c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """upsert into t3 select * from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3428')

    # Insert should work.  Target table has no IDENTITY column
    stmt = """create table t4 (
c1 largeint,
c2 int,
c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t4 select * from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)

    stmt = """select * from t4 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    _dci.expect_str_token(output, '9991')
    _dci.expect_str_token(output, '9992')

    # Upsert should work.  Target table has no IDEINTITY column
    stmt = """create table t5 (
c1 largeint,
c2 int,
c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """upsert into t5 select * from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from t5 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    _dci.expect_str_token(output, '9991')
    _dci.expect_str_token(output, '9992')

    # Clean up
    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t3 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t4 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t5 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test016(desc="""create set table"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # A SET table is not supported in Trafodion right now, with or without
    # IDENTITY.  If it were supported, this is the test for it.

    # A SET table automatically discards duplicate rows.  Since the ALWAYS
    # IDENTITY column is always different, there won't be duplicate rows to
    # begin with.  This is only to make sure that a SET table can be created
    # with the IDENTITY column.  For ALWAYS IDENTITY column, it really has 
    # no difference between a SET table and a regular table.

    stmt = """create set table t1 (
c1 largeint GENERATED ALWAYS AS IDENTITY (MINVALUE 9991),
c2 int,
c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4222')

    # insert 2 rows with the same values for c2 and c3
    # stmt = """insert into t1 values (DEFAULT,1,1),(DEFAULT,1,1);"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_inserted_msg(output)

    # expect both rows to be inserted
    # stmt = """select * from t1 order by 1;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_selected_msg(output, 2)
    # _dci.expect_str_token(output, '9991')
    # _dci.expect_str_token(output, '9992')

    # Clean up
    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)
   
    _testmgr.testcase_end(desc)

def test017(desc="""create table as"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create table t1 (
c1 largeint GENERATED ALWAYS AS IDENTITY (MINVALUE 9991),
c2 int,
c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into t1 values (DEFAULT,1,1),(DEFAULT,2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    # Without the IDENTITY column
    stmt = """create table t2 as select c2, c3 from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)

    stmt = """select * from t2 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)

    # With the IDENTITY column
    stmt = """create table t3 as select * from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)

    # The new table's c1 should just be a regular, non-IDENTITY column
    stmt = """showddl table t3;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, 'IDENTITY')

    # Insert one more row, a user value should be able to be specified for c1
    stmt = """insert into t3 values (9999, 3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)   

    # double check the rows 
    stmt = """select * from t3 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    _dci.expect_str_token(output, '9991')
    _dci.expect_str_token(output, '9992')
    _dci.expect_str_token(output, '9999')

    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t3 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test018(desc="""create table like"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create table t1 (
c1 largeint GENERATED ALWAYS AS IDENTITY (MINVALUE 9991),
c2 int,
c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # This should work
    stmt = """create table t2 like t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _dci.expect_any_substr(output, 'IDENTITY')
    _dci.expect_any_substr(output, '9991')

    my_verify('t2', 5, 9991, 'DEFAULT', 'DEFAULT')

    # This should fail.  ALWAYS IDENTITY does not allow the user to insert 
    # values
    stmt = """create table t3 like t1 as select * from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3428')

    # This should fail.  Numbers of columns mismatch
    stmt = """create table t4 like t1 as select c2, c2 from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4023')

    # This should fail.  DEAFAULT can't be used in select
    stmt = """create table t5 like t1 as select DEFAULT, c2, c2 from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4096')

    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t3 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t4 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t5 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test019(desc="""create volatile table"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # a volatile table should be similar to a regular table
    stmt = """create volatile table volt_t1 (
c1 largeint GENERATED ALWAYS AS IDENTITY,
c2 int,
c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('volt_t1', 5, 'DEFAULT', 'DEFAULT', 'DEFAULT')

    # A SET volatile table automatically discards duplicate rows. This is
    # not supported in Trafodion right now.
    stmt = """create set volatile table volt_t2 (
c1 largeint GENERATED ALWAYS AS IDENTITY (MINVALUE 9991),
c2 int,
c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4222')

    # Clean up
    # Volatile table can't be dropped.  Nothiong to clean up.

    _testmgr.testcase_end(desc)

def test020(desc="""alter table: add column"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # alter table add an IDENTITY column is not supported

    stmt = """create table t1 (
c2 int,
c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """alter table t1 add column c1 largeint GENERATED ALWAYS AS IDENTITY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1514')

    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test021(desc="""alter table: alter column"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # alter table alter an IDENTIY column (MAXVALUE, INCREMENT BY) is supported

    #----------------------------------------------------
    # TEST MAXVALUE
    #----------------------------------------------------
    stmt = """create table t1 (
c1 largeint GENERATED ALWAYS AS IDENTITY,
c2 int,
c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # This should fail, MAXVALUE cannot be a negative number
    stmt = """alter table t1 alter column c1 set MAXVALUE -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1572')

    # This should fail, MAXVALUE cannot be 0 either
    stmt = """alter table t1 alter column c1 set MAXVALUE 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1571')

    # This should fail, MINVALUE (default is 1) needs to be smaller than 
    # MAXVALUE
    stmt = """alter table t1 alter column c1 set MAXVALUE 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1570')

    # MAXVALUE 2 should allow 2 inserts
    stmt = """alter table t1 alter column c1 set MAXVALUE 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t1', 2, 'DEFAULT', 2, 'DEFAULT')

    # Try a table with data in it already
    # Use (NO CACHE) to turn off cache in this test.  The default CACHE size
    # is 25.  By design, the user will not see an error until the cache is 
    # exhuased. It's easier to conduct this negative test with no cache.
    stmt = """create table t2 (
c1 largeint GENERATED ALWAYS AS IDENTITY (NO CACHE),
c2 int,
c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # insert 4 rows, that should bring c1 up to 4.
    stmt = """insert into t2 values (DEFAULT,1,1),(DEFAULT,2,2),(DEFAULT,3,3),(DEFAULT,4,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)

    stmt = """showddl t2;"""
    output = _dci.cmdexec(stmt)

    # Changing MAXVALUE 2 when c1 is already at 4.  Unfortunately, this error
    # is not caught at the alter table time.  It will only be caught at the
    # next insert (AND when the cache is exhaused, which is always true in this
    # case).
    stmt = """alter table t2 alter column c1 set MAXVALUE 2;"""
    output = _dci.cmdexec(stmt)
    # _dci.expect_error_msg(output)

    stmt = """showddl t2;"""
    output = _dci.cmdexec(stmt)

    # This should see error.  The check of MAXVALUE 2 should kick in now.
    stmt = """insert into t2 values (DEFAULT,5,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1579')

    #----------------------------------------------------
    # TEST INCREMENT BY
    #----------------------------------------------------
    stmt = """create table t3 (
c1 largeint GENERATED ALWAYS AS IDENTITY,
c2 int,
c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # This should fail, INCREMENT BY a negative number is not allowed
    stmt = """alter table t3 alter column c1 set INCREMENT BY -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1572')

    # This should fail, INCREMENT BY 0 is not allowed either
    stmt = """alter table t3 alter column c1 set INCREMENT BY 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1571')

    # increment by 10
    stmt = """alter table t3 alter column c1 set INCREMENT BY 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    my_verify('t3', 5, 'DEFAULT', 'DEFAULT', 10)

    #----------------------------------------------------
    # Alter other attributes are not supported
    #----------------------------------------------------
    stmt = """create table t4 (
c1 largeint GENERATED ALWAYS AS IDENTITY,
c2 int,
c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """alter table t4 alter column c1 set START WITH 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1592')

    stmt = """alter table t4 alter column c1 set MINVALUE 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1592')

    # NO CYCLE really is the only option supported for cycle, and
    # it's the default.  It's fine if it does not return an error.
    stmt = """alter table t4 alter column c1 set NO CYCLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t3 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t4 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test022(desc="""merge"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # Merge is not allowed with IDENTITY column defined in the table

    stmt = """create table t1 (
c1 largeint GENERATED ALWAYS AS IDENTITY,
c2 int,
c3 smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into t1 values (DEFAULT,1,1),(DEFAULT,2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)

    stmt = """merge into t1 on c2=1 when matched then update set c2=3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3241')

    stmt = """merge into t1 on c2=1 when matched then update set c2=3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3241')

    stmt = """merge into t1 on c2=3 when matched then update set c2=3 when not matched then insert (c2,c3) values (3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3241')

    stmt = """merge into t1 on c2=3 when matched then update set c2=3 when not matched then insert (c1,c2,c3) values (DEFAULT,3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3241')

    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)


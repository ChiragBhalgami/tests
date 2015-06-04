-- @@@ START COPYRIGHT @@@
--
-- (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
--
--  Licensed under the Apache License, Version 2.0 (the "License");
--  you may not use this file except in compliance with the License.
--  You may obtain a copy of the License at
--
--      http://www.apache.org/licenses/LICENSE-2.0
--
--  Unless required by applicable law or agreed to in writing, software
--  distributed under the License is distributed on an "AS IS" BASIS,
--  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
--  See the License for the specific language governing permissions and
--  limitations under the License.
--
-- @@@ END COPYRIGHT @@@
control query default CANCEL_MINIMUM_BLOCKING_INTERVAL '1';

set schema TEST_SCHEMA_1;
 
Prepare xx  from
   create table f31_lineitem1 store by (l_orderkey,l_linenumber) as
     select l_orderkey,l_partkey,l_linenumber,l_quantity,l_extendedprice,l_discount,l_tax 
     from TEST_SCHEMA_2.lineitem;

infostats xx;

execute xx;

get statistics for qid current;

exit
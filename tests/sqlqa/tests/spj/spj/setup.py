# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014-2015 Hewlett-Packard Development Company, L.P.
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
_dbrootdci = None

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    global _dbrootdci

    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    _dci.setup_schema(defs.my_schema)
    _dbrootdci = _testmgr.get_dbroot_dci_proc()

    # set up spj path
    defs.set_spjpath()

    stmt = """grant component privilege manage_library on sql_operations to "public";"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_complete_msg(output)

    stmt = "create library " + defs.spjrs_lib + " file '" + defs.spjrs_path + "';"
    output = _dci.cmdexec(stmt)

    stmt = "create library " + defs.spjcall_lib + " file '" + defs.spjcall_path + "';"
    output = _dci.cmdexec(stmt)

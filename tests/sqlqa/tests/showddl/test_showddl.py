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

import unittest
import tests.lib.hpdci as hpdci
# The arguments need to be parsed and saved before importing test modules,
# as they will be used even in defvars.py, which is evaluated as part of
# the import
hpdci.prog_parse_args_from_initfile()

import tests.showddl.ddl01.tunit
import tests.showddl.ddl03.tunit
import tests.showddl.ddl04.tunit
import tests.showddl.ddl06.tunit
import tests.showddl.ddl07.tunit

class TestShowddl(unittest.TestCase):
    """Regression Test: showddl"""

    # @classmethod def setUpClass(cls) and @classmethod def tearDownClass(cls)
    # only work for python 2.7 and 3.2.
    # @classmethod
    # def setUpClass(cls):
    # @classmethod
    # def tearDownClass(cls):

    _testmgr = hpdci.HPTestMgr()

    def __init__(self, *args, **kwargs):
        super(TestShowddl, self).__init__(*args, **kwargs)
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def run_testunit(self, testunit, testlist=[]):
        try:
           self._testmgr.testunit_begin(testunit)
           testunit.sq_testunit(self._testmgr, testlist)
           status = self._testmgr.testunit_end(testunit)
        except:
           # kill all hpdci processes
           self._testmgr.delete_all_dci_procs()
           raise

        self.assertTrue(status, '*** MISMATCH(es) *** found')

    # NOTE @unittest.skip('skip this test') only work for python 2.7 

    # @unittest.skip('skip this test')
    def test_ddl01(self):
        # == NO GLOBAL TABLES
        testlist = []
        self.run_testunit(tests.showddl.ddl01.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_ddl03(self):
        # == NO GLOBAL TABLES
        testlist = []
        self.run_testunit(tests.showddl.ddl03.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_ddl04(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.showddl.ddl04.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_ddl06(self):
        # == GLOBAL TABLES: g_sqldpop
        testlist=[]
        self.run_testunit(tests.showddl.ddl06.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_ddl07(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.showddl.ddl07.tunit, testlist)

if __name__ == "__main__":
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestShowddl)
    unittest.TextTestRunner(verbosity=2).run(suite)


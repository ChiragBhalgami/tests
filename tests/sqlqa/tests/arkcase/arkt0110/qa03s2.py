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
    
    stmt = """SELECT * FROM """ + gvars.g_schema_arkcasedb + """.parts WHERE partname in (
'a','b','c','d','e','f','g'
,'h','i','j','k','l','m'
,'n','o','p','q','r','s','t'
,'a1','b1','c1','d1','e1','f1','g1'
,'h1','i1','j1','k1','l1','m1'
,'n1','o1','p1','q1','r1','s1','t1'
,'a2','b2','c2','d2','e2','f2','g2'
,'h2','i2','j2','k2','l2','m2'
,'n2','o2','p2','q2','r2','s2','t2'
,'a3','b3','c3','d3','e3','f3','g3'
,'h3','i3','j3','k3','l3','m3'
,'n3','o3','p3','q3','r3','s3','t3'
,'a4','b4','c4','d4','e4','f4','g4'
,'h4','i4','j4','k4','l4','m4'
,'n4','o4','p4','q4','r4','s4','t4'
,'a5','b5','c5','d5','e5','f5','g5'
,'h5','i5','j5','k5','l5','m5'
,'n5','o5','p5','q5','r5','s5','t5'
,'a6','b6','c6','d6','e6','f6','g6'
,'h6','i6','j6','k6','l6','m6'
,'n6','o6','p6','q6','r6','s6','t6'
,'a7','b7','c7','d7','e7','f7','g7'
,'h7','i7','j7','k7','l7','m7'
,'n7','o7','p7','q7','r7','s7','t7'
,'a8','b8','c8','d8','e8','f8','g8'
,'h8','i8','j8','k8','l8','m8'
,'n8','o8','p8','q8','r8','s8','t8'
,'a9','b9','c9','d9','e9','f9','g9'
,'h9','i9','j9','k9','l9','m9'
,'n9','o9','p9','q9','r9','s9','t9'
,'a0','b0','c0','d0','e0','f0','g0'
,'h0','i0','j0','k0','l0','m0'
,'n0','o0','p0','q0','r0','s0','t0'
,'aa','ba','ca','da','ea','fa','ga'
,'ha','ia','ja','ka','la','ma'
,'na','oa','pa','qa','ra','sa','ta'
,'ab','bb','cb','db','eb','fb','gb'
,'hb','ib','jb','kb','lb','mb'
,'nb','ob','pb','qb','rb','sb','tb'
,'ac','cc','cc','dc','ec','fc','gc'
,'hc','ic','jc','kc','lc','mc'
,'nc','oc','pc','qc','rc','sc','tc'
,'ad','bd','cd','dd','ed','fd','gd'
,'hd','id','jd','kd','ld','md'
,'nd','od','pd','qd','rd','sd','td'
,'ae','be','ce','de','ee','fe','ge'
,'he','ie','je','ke','le','me'
,'ne','oe','pe','qe','re','se','te'
,'af','bf','cf','df','ef','ff','gf'
,'hf','if','jf','kf','lf','mf'
,'nf','of','pf','qf','rf','sf','tf'
,'a1','b1','c1','d1','e1','f1','g1'
,'h1','i1','j1','k1','l1','m1'
,'n1','o1','p1','q1','r1','s1','t1'
,'a2','b2','c2','d2','e2','f2','g2'
,'h2','i2','j2','k2','l2','m2'
,'n2','o2','p2','q2','r2','s2','t2'
,'a3','b3','c3','d3','e3','f3','g3'
,'h3','i3','j3','k3','l3','m3'
,'n3','o3','p3','q3','r3','s3','t3'
,'a4','b4','c4','d4','e4','f4','g4'
,'h4','i4','j4','k4','l4','m4'
,'n4','o4','p4','q4','r4','s4','t4'
,'a5','b5','c5','d5','e5','f5','g5'
,'h5','i5','j5','k5','l5','m5'
,'n5','o5','p5','q5','r5','s5','t5'
,'a6','b6','c6','d6','e6','f6','g6'
,'h6','i6','j6','k6','l6','m6'
,'n6','o6','p6','q6','r6','s6','t6'
,'a7','b7','c7','d7','e7','f7','g7'
,'h7','i7','j7','k7','l7','m7'
,'n7','o7','p7','q7','r7','s7','t7'
,'a8','b8','c8','d8','e8','f8','g8'
,'h8','i8','j8','k8','l8','m8'
,'n8','o8','p8','q8','r8','s8','t8'
,'a9','b9','c9','d9','e9','f9','g9'
,'h9','i9','j9','k9','l9','m9'
,'n9','o9','p9','q9','r9','s9','t9'
,'a0','b0','c0','d0','e0','f0','g0'
,'h0','i0','j0','k0','l0','m0'
,'n0','o0','p0','q0','r0','s0','t0'
,'aa','ba','ca','da','ea','fa','ga'
,'ha','ia','ja','ka','la','ma'
,'na','oa','pa','qa','ra','sa','ta'
,'ab','bb','cb','db','eb','fb','gb'
,'hb','ib','jb','kb','lb','mb'
,'nb','ob','pb','qb','rb','sb','tb'
,'ac','cc','cc','dc','ec','fc','gc'
,'hc','ic','jc','kc','lc','mc'
,'nc','oc','pc','qc','rc','sc','tc'
,'ad','bd','cd','dd','ed','fd','gd'
,'hd','id','jd','kd','ld','md'
,'nd','od','pd','qd','rd','sd','td'
,'ae','be','ce','de','ee','fe','ge'
,'he','ie','je','ke','le','me'
,'ne','oe','pe','qe','re','se','te'
,'af','bf','cf','df','ef','ff','gf'
,'hf','if','jf','kf','lf','mf'
,'nf','of','pf','qf','rf','sf','tf'
,'1a1','1b1','1c1','1d1','1e1','1f1','1g1'
,'1h1','1i1','1j1','1k1','1l1','1m1'
,'1n1','1o1','1p1','1q1','1r1','1s1','1t1'
,'1a2','1b2','1c2','1d2','1e2','1f2','1g2'
,'1h2','1i2','1j2','1k2','1l2','1m2'
,'1n2','1o2','1p2','1q2','1r2','1s2','1t2'
,'1a3','1b3','1c3','1d3','1e3','1f3','1g3'
,'1h3','1i3','1j3','1k3','1l3','1m3'
,'1n3','1o3','1p3','1q3','1r3','1s3','1t3'
,'1a4','1b4','1c4','1d4','1e4','1f4','1g4'
,'1h4','1i4','1j4','1k4','1l4','1m4'
,'1n4','1o4','1p4','1q4','1r4','1s4','1t4'
,'1a5','1b5','1c5','1d5','1e5','1f5','1g5'
,'1h5','1i5','1j5','1k5','1l5','1m5'
,'1n5','1o5','1p5','1q5','1r5','1s5','1t5'
,'1a6','1b6','1c6','1d6','1e6','1f6','1g6'
,'1h6','1i6','1j6','1k6','1l6','1m6'
,'1n6','1o6','1p6','1q6','1r6','1s6','1t6'
,'1a7','1b7','1c7','1d7','1e7','1f7','1g7'
,'1h7','1i7','1j7','1k7','1l7','1m7'
,'1n7','1o7','1p7','1q7','1r7','1s7','1t7'
,'1a8','1b8','1c8','1d8','1e8','1f8','1g8'
,'1h8','1i8','1j8','1k8','1l8','1m8'
,'1n8','1o8','1p8','1q8','1r8','1s8','1t8'
,'1a9','1b9','1c9','1d9','1e9','1f9','1g9'
,'1h9','1i9','1j9','1k9','1l9','1m9'
,'1n9','1o9','1p9','1q9','1r9','1s9','1t9'
,'1a0','1b0','1c0','1d0','1e0','1f0','1g0'
,'1h0','1i0','1j0','1k0','1l0','1m0'
,'1n0','1o0','1p0','1q0','1r0','1s0','1t0'
,'1aa','1ba','1ca','1da','1ea','1fa','1ga'
,'1ha','1ia','1ja','1ka','1la','1ma'
,'1na','1oa','1pa','1qa','1ra','1sa','1ta'
,'1ab','1bb','1cb','1db','1eb','1fb','1gb'
,'1hb','1ib','1jb','1kb','1lb','1mb'
,'1nb','1ob','1pb','1qb','1rb','1sb','1tb'
,'1ac','1cc','1cc','1dc','1ec','1fc','1gc'
,'1hc','1ic','1jc','1kc','1lc','1mc'
,'1nc','1oc','1pc','1qc','1rc','1sc','1tc'
,'1ad','1bd','1cd','1dd','1ed','1fd','1gd'
,'1hd','1id','1jd','1kd','1ld','1md'
,'1nd','1od','1pd','1qd','1rd','1sd','1td'
,'1ae','1be','1ce','1de','1ee','1fe','1ge'
,'1he','1ie','1je','1ke','1le','1me'
,'1ne','1oe','1pe','1qe','1re','1se','1te'
,'1af','1bf','1cf','1df','1ef','1ff','1gf'
,'1hf','1if','1jf','1kf','1lf','1mf'
,'1nf','1of','1pf','1qf','1rf','1sf','1tf'
,'2a1','2b1','2c1','2d1','2e1','2f1','2g1'
,'2h1','2i1','2j1','2k1','2l1','2m1'
,'2n1','2o1','2p1','2q1','2r1','2s1','2t1'
,'2a2','2b2','2c2','2d2','2e2','2f2','2g2'
,'2h2','2i2','2j2','2k2','2l2','2m2'
,'2n2','2o2','2p2','2q2','2r2','2s2','2t2'
,'2a3','2b3','2c3','2d3','2e3','2f3','2g3'
,'2h3','2i3','2j3','2k3','2l3','2m3'
,'2n3','2o3','2p3','2q3','2r3','2s3','2t3'
,'2a4','2b4','2c4','2d4','2e4','2f4','2g4'
,'2h4','2i4','2j4','2k4','2l4','2m4'
,'2n4','2o4','2p4','2q4','2r4','2s4','2t4'
,'2a5','2b5','2c5','2d5','2e5','2f5','2g5'
,'2h5','2i5','2j5','2k5','2l5','2m5'
,'2n5','2o5','2p5','2q5','2r5','2s5','2t5'
,'2a6','2b6','2c6','2d6','2e6','2f6','2g6'
,'2h6','2i6','2j6','2k6','2l6','2m6'
,'2n6','2o6','2p6','2q6','2r6','2s6','2t6'
,'2a7','2b7','2c7','2d7','2e7','2f7','2g7'
,'2h7','2i7','2j7','2k7','2l7','2m7'
,'2n7','2o7','2p7','2q7','2r7','2s7','2t7'
,'2a8','2b8','2c8','2d8','2e8','2f8','2g8'
,'2h8','2i8','2j8','2k8','2l8','2m8'
,'2n8','2o8','2p8','2q8','2r8','2s8','2t8'
,'2a9','2b9','2c9','2d9','2e9','2f9','2g9'
,'2h9','2i9','2j9','2k9','2l9','2m9'
,'2n9','2o9','2p9','2q9','2r9','2s9','2t9'
,'2a0','2b0','2c0','2d0','2e0','2f0','2g0'
,'2h0','2i0','2j0','2k0','2l0','2m0'
,'2n0','2o0','2p0','2q0','2r0','2s0','2t0'
,'2aa','2ba','2ca','2da','2ea','2fa','2ga'
,'2ha','2ia','2ja','2ka','2la','2ma'
,'2na','2oa','2pa','2qa','2ra','2sa','2ta'
,'2ab','2bb','2cb','2db','2eb','2fb','2gb'
,'2hb','2ib','2jb','2kb','2lb','2mb'
,'2nb','2ob','2pb','2qb','2rb','2sb','2tb'
,'2ac','2cc','2cc','2dc','2ec','2fc','2gc'
,'2hc','2ic','2jc','2kc','2lc','2mc'
,'2nc','2oc','2pc','2qc','2rc','2sc','2tc'
,'2ad','2bd','2cd','2dd','2ed','2fd','2gd'
,'2hd','2id','2jd','2kd','2ld','2md'
,'2nd','2od','2pd','2qd','2rd','2sd','2td'
,'2ae','2be','2ce','2de','2ee','2fe','2ge'
,'2he','2ie','2je','2ke','2le','2me'
,'2ne','2oe','2pe','2qe','2re','2se','2te'
,'2af','2bf','2cf','2df','2ef','2ff','2gf'
,'2hf','2if','2jf','2kf','2lf','2mf'
,'2nf','2of','2pf','2qf','2rf','2sf','2tf'
,'3a1','3b1','3c1','3d1','3e1','3f1','3g1'
,'3h1','3i1','3j1','3k1','3l1','3m1'
,'3n1','3o1','3p1','3q1','3r1','3s1','3t1'
,'3a2','3b2','3c2','3d2','3e2','3f2','3g2'
,'3h2','3i2','3j2','3k2','3l2','3m2'
,'3n2','3o2','3p2','3q2','3r2','3s2','3t2'
,'3a3','3b3','3c3','3d3','3e3','3f3','3g3'
,'3h3','3i3','3j3','3k3','3l3','3m3'
,'3n3','3o3','3p3','3q3','3r3','3s3','3t3'
,'3a4','3b4','3c4','3d4','3e4','3f4','3g4'
,'3h4','3i4','3j4','3k4','3l4','3m4'
,'3n4','3o4','3p4','3q4','3r4','3s4','3t4'
,'3a5','3b5','3c5','3d5','3e5','3f5','3g5'
,'3h5','3i5','3j5','3k5','3l5','3m5'
,'3n5','3o5','3p5','3q5','3r5','3s5','3t5'
,'3a6','3b6','3c6','3d6','3e6','3f6','3g6'
,'3h6','3i6','3j6','3k6','3l6','3m6'
,'3n6','3o6','3p6','3q6','3r6','3s6','3t6'
,'3a7','3b7','3c7','3d7','3e7','3f7','3g7'
,'3h7','3i7','3j7','3k7','3l7','3m7'
,'3n7','3o7','3p7','3q7','3r7','3s7','3t7'
,'3a8','3b8','3c8','3d8','3e8','3f8','3g8'
,'3h8','3i8','3j8','3k8','3l8','3m8'
,'3n8','3o8','3p8','3q8','3r8','3s8','3t8'
,'3a9','3b9','3c9','3d9','3e9','3f9','3g9'
,'3h9','3i9','3j9','3k9','3l9','3m9'
,'3n9','3o9','3p9','3q9','3r9','3s9','3t9'
,'3a0','3b0','3c0','3d0','3e0','3f0','3g0'
,'3h0','3i0','3j0','3k0','3l0','3m0'
,'3n0','3o0','3p0','3q0','3r0','3s0','3t0'
,'3aa','3ba','3ca','3da','3ea','3fa','3ga'
,'3ha','3ia','3ja','3ka','3la','3ma'
,'3na','3oa','3pa','3qa','3ra','3sa','3ta'
,'3ab','3bb','3cb','3db','3eb','3fb','3gb'
,'3hb','3ib','3jb','3kb','3lb','3mb'
,'3nb','3ob','3pb','3qb','3rb','3sb','3tb'
,'3ac','3cc','3cc','3dc','3ec','3fc','3gc'
,'3hc','3ic','3jc','3kc','3lc','3mc'
,'3nc','3oc','3pc','3qc','3rc','3sc','3tc'
,'3ad','3bd','3cd','3dd','3ed','3fd','3gd'
,'3hd','3id','3jd','3kd','3ld','3md'
,'3nd','3od','3pd','3qd','3rd','3sd','3td'
,'3ae','3be','3ce','3de','3ee','3fe','3ge'
,'3he','3ie','3je','3ke','3le','3me'
,'3ne','3oe','3pe','3qe','3re','3se','3te'
,'3af','3bf','3cf','3df','3ef','3ff','3gf'
,'3hf','3if','3jf','3kf','3lf','3mf'
,'3nf','3of','3pf','3qf','3rf','3sf','3tf'
,'POWER MODULE'
,'4a1','4b1','4c1','4d1','4e1','4f1','4g1'
,'4h1','4i1','4j1','4k1','4l1','4m1'
,'4n1','4o1','4p1','4q1','4r1','4s1','4t1'
,'4a2','4b2','4c2','4d2','4e2','4f2','4g2'
,'4h2','4i2','4j2','4k2','4l2','4m2'
,'4n2','4o2','4p2','4q2','4r2','4s2','4t2'
,'4a3','4b3','4c3','4d3','4e3','4f3','4g3'
,'4h3','4i3','4j3','4k3','4l3','4m3'
,'4n3','4o3','4p3','4q3','4r3','4s3','4t3'
,'4a4','4b4','4c4','4d4','4e4','4f4','4g4'
,'4h4','4i4','4j4','4k4','4l4','4m4'
,'4n4','4o4','4p4','4q4','4r4','4s4','4t4'
,'4a5','4b5','4c5','4d5','4e5','4f5','4g5'
,'4h5','4i5','4j5','4k5','4l5','4m5'
,'4n5','4o5','4p5','4q5','4r5','4s5','4t5'
,'4a6','4b6','4c6','4d6','4e6','4f6','4g6'
,'4h6','4i6','4j6','4k6','4l6','4m6'
,'4n6','4o6','4p6','4q6','4r6','4s6','4t6'
,'4a7','4b7','4c7','4d7','4e7','4f7','4g7'
,'4h7','4i7','4j7','4k7','4l7','4m7'
,'4n7','4o7','4p7','4q7','4r7','4s7','4t7'
,'4a8','4b8','4c8','4d8','4e8','4f8','4g8'
,'4h8','4i8','4j8','4k8','4l8','4m8'
,'4n8','4o8','4p8','4q8','4r8','4s8','4t8'
,'4a9','4b9','4c9','4d9','4e9','4f9','4g9'
,'4h9','4i9','4j9','4k9','4l9','4m9'
,'4n9','4o9','4p9','4q9','4r9','4s9','4t9'
,'4a0','4b0','4c0','4d0','4e0','4f0','4g0'
,'4h0','4i0','4j0','4k0','4l0','4m0'
,'4n0','4o0','4p0','4q0','4r0','4s0','4t0'
,'4aa','4ba','4ca','4da','4ea','4fa','4ga'
,'4ha','4ia','4ja','4ka','4la','4ma'
,'4na','4oa','4pa','4qa','4ra','4sa','4ta'
,'4ab','4bb','4cb','4db','4eb','4fb','4gb'
,'4hb','4ib','4jb','4kb','4lb','4mb'
,'4nb','4ob','4pb','4qb','4rb','4sb','4tb'
,'4ac','4cc','4cc','4dc','4ec','4fc','4gc'
,'4hc','4ic','4jc','4kc','4lc','4mc'
,'4nc','4oc','4pc','4qc','4rc','4sc','4tc'
,'4ad','4bd','4cd','4dd','4ed','4fd','4gd'
,'4hd','4id','4jd','4kd','4ld','4md'
,'4nd','4od','4pd','4qd','4rd','4sd','4td'
,'DECIMAL ARITH'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    

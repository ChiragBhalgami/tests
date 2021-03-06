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
    
    stmt = """insert into t003t2 values
(101,'1','aa','0101','ABCDEFGH','aaaa0101','A'),
(102,'1','bb','0102','BCDEFGHI','aaaa0102','B'),
(103,'1','cc','0103','CDEFGHIJ','cccc0103','C'),
(104,'1','dd','0104','DEFGHIJK','cccc0104','D'),
(105,'1','ee','0105','EFGHIJKL','eeee0105','E'),
(106,'2','ff','0106','FGHIJKLM','eeee0106','F'),
(107,'2','gg','0107','GHIJKLMN','gggg0107','G'),
(108,'2','hh','0108','HIJKLMNO','gggg0108','H'),
(109,'2','ii','0109','IJKLMNOP','iiii0109','I'),
(110,'2','jj','0110','JKLMNOPQ','iiii0110','J'),
(111,'3','kk','0111','KLMNOPQR','kkkk0111','K'),
(112,'3','ll','0112','LMNOPQRS','kkkk0112','L'),
(113,'3','mm','0113','MNOPQRST','mmmm0113','M'),
(114,'3','nn','0114','NOPQRSTU','mmmm0114','N'),
(115,'3','oo','0115','OPQRSTUV','oooo0115','O'),
(116,'4','pp','0116','PQRSTUVW','oooo0116','P'),
(117,'4','qq','0117','QRSTUVWX','qqqq0117','Q'),
(118,'4','rr','0118','RSTUVWXY','qqqq0118','R'),
(119,'4','ss','0119','STUVWXYZ','ssss0119','S'),
(120,'4','tt','0120','TUWVXYZA','ssss0120','T'),
(121,'1','aa','0121','ABCDEFGH','aaaa0121','A'),
(122,'1','bb','0122','BCDEFGHI','aaaa0122','B'),
(123,'1','cc','0123','CDEFGHIJ','cccc0123','C'),
(124,'1','dd','0124','DEFGHIJK','cccc0124','D'),
(125,'1','ee','0125','EFGHIJKL','eeee0125','E'),
(126,'2','ff','0126','FGHIJKLM','eeee0126','F'),
(127,'2','gg','0127','GHIJKLMN','gggg0127','G'),
(128,'2','hh','0128','HIJKLMNO','gggg0128','H'),
(129,'2','ii','0129','IJKLMNOP','iiii0129','I'),
(130,'2','jj','0130','JKLMNOPQ','iiii0130','J'),
(131,'3','kk','0131','KLMNOPQR','kkkk0131','K'),
(132,'3','ll','0132','LMNOPQRS','kkkk0132','L'),
(133,'3','mm','0133','MNOPQRST','mmmm0133','M'),
(134,'3','nn','0134','NOPQRSTU','mmmm0134','N'),
(135,'3','oo','0135','OPQRSTUV','oooo0135','O'),
(136,'4','pp','0136','PQRSTUVW','oooo0136','P'),
(137,'4','qq','0137','QRSTUVWX','qqqq0137','Q'),
(138,'4','rr','0138','RSTUVWXY','qqqq0138','R'),
(139,'4','ss','0139','STUVWXYZ','ssss0139','S'),
(140,'4','tt','0140','TUWVXYZA','ssss0140','T'),
(141,'1','aa','0141','ABCDEFGH','aaaa0141','A'),
(142,'1','bb','0142','BCDEFGHI','aaaa0142','B'),
(143,'1','cc','0143','CDEFGHIJ','cccc0143','C'),
(144,'1','dd','0144','DEFGHIJK','cccc0144','D'),
(145,'1','ee','0145','EFGHIJKL','eeee0145','E'),
(146,'2','ff','0146','FGHIJKLM','eeee0146','F'),
(147,'2','gg','0147','GHIJKLMN','gggg0147','G'),
(148,'2','hh','0148','HIJKLMNO','gggg0148','H'),
(149,'2','ii','0149','IJKLMNOP','iiii0149','I'),
(150,'2','jj','0150','JKLMNOPQ','iiii0150','J'),
(151,'3','kk','0151','KLMNOPQR','kkkk0151','K'),
(152,'3','ll','0152','LMNOPQRS','kkkk0152','L'),
(153,'3','mm','0153','MNOPQRST','mmmm0153','M'),
(154,'3','nn','0154','NOPQRSTU','mmmm0154','N'),
(155,'3','oo','0155','OPQRSTUV','oooo0155','O'),
(156,'4','pp','0156','PQRSTUVW','oooo0156','P'),
(157,'4','qq','0157','QRSTUVWX','qqqq0157','Q'),
(158,'4','rr','0158','RSTUVWXY','qqqq0158','R'),
(159,'4','ss','0159','STUVWXYZ','ssss0159','S'),
(160,'4','tt','0160','TUWVXYZA','ssss0160','T'),
(161,'1','aa','0161','ABCDEFGH','aaaa0161','A'),
(162,'1','bb','0162','BCDEFGHI','aaaa0162','B'),
(163,'1','cc','0163','CDEFGHIJ','cccc0163','C'),
(164,'1','dd','0164','DEFGHIJK','cccc0164','D'),
(165,'1','ee','0165','EFGHIJKL','eeee0165','E'),
(166,'2','ff','0166','FGHIJKLM','eeee0166','F'),
(167,'2','gg','0167','GHIJKLMN','gggg0167','G'),
(168,'2','hh','0168','HIJKLMNO','gggg0168','H'),
(169,'2','ii','0169','IJKLMNOP','iiii0169','I'),
(170,'2','jj','0170','JKLMNOPQ','iiii0170','J'),
(171,'3','kk','0171','KLMNOPQR','kkkk0171','K'),
(172,'3','ll','0172','LMNOPQRS','kkkk0172','L'),
(173,'3','mm','0173','MNOPQRST','mmmm0173','M'),
(174,'3','nn','0174','NOPQRSTU','mmmm0174','N'),
(175,'3','oo','0175','OPQRSTUV','oooo0175','O'),
(176,'4','pp','0176','PQRSTUVW','oooo0176','P'),
(177,'4','qq','0177','QRSTUVWX','qqqq0177','Q'),
(178,'4','rr','0178','RSTUVWXY','qqqq0178','R'),
(179,'4','ss','0179','STUVWXYZ','ssss0179','S'),
(180,'4','tt','0180','TUWVXYZA','ssss0180','T'),
(181,'1','aa','0181','ABCDEFGH','aaaa0181','A'),
(182,'1','bb','0182','BCDEFGHI','aaaa0182','B'),
(183,'1','cc','0183','CDEFGHIJ','cccc0183','C'),
(184,'1','dd','0184','DEFGHIJK','cccc0184','D'),
(185,'1','ee','0185','EFGHIJKL','eeee0185','E'),
(186,'2','ff','0186','FGHIJKLM','eeee0186','F'),
(187,'2','gg','0187','GHIJKLMN','gggg0187','G'),
(188,'2','hh','0188','HIJKLMNO','gggg0188','H'),
(189,'2','ii','0189','IJKLMNOP','iiii0189','I'),
(190,'2','jj','0190','JKLMNOPQ','iiii0190','J'),
(191,'3','kk','0191','KLMNOPQR','kkkk0191','K'),
(192,'3','ll','0192','LMNOPQRS','kkkk0192','L'),
(193,'3','mm','0193','MNOPQRST','mmmm0193','M'),
(194,'3','nn','0194','NOPQRSTU','mmmm0194','N'),
(195,'3','oo','0195','OPQRSTUV','oooo0195','O'),
(196,'4','pp','0196','PQRSTUVW','oooo0196','P'),
(197,'4','qq','0197','QRSTUVWX','qqqq0197','Q'),
(198,'4','rr','0198','RSTUVWXY','qqqq0198','R'),
(199,'4','ss','0199','STUVWXYZ','ssss0199','S'),
(200,'4','tt','0200','TUWVXYZA','ssss0200','T'),
(301,'1','aa','0301','ABCDEFGH','aaaa0301','A'),
(303,'1','bb','0303','BCDEFGHI','aaaa0303','B'),
(303,'1','cc','0303','CDEFGHIJ','cccc0303','C'),
(304,'1','dd','0304','DEFGHIJK','cccc0304','D'),
(305,'1','ee','0305','EFGHIJKL','eeee0305','E'),
(306,'2','ff','0306','FGHIJKLM','eeee0306','F'),
(307,'2','gg','0307','GHIJKLMN','gggg0307','G'),
(308,'2','hh','0308','HIJKLMNO','gggg0308','H'),
(309,'2','ii','0309','IJKLMNOP','iiii0309','I'),
(310,'2','jj','0310','JKLMNOPQ','iiii0310','J'),
(311,'3','kk','0311','KLMNOPQR','kkkk0311','K'),
(312,'3','ll','0312','LMNOPQRS','kkkk0312','L'),
(313,'3','mm','0313','MNOPQRST','mmmm0313','M'),
(314,'3','nn','0314','NOPQRSTU','mmmm0314','N'),
(315,'3','oo','0315','OPQRSTUV','oooo0315','O'),
(316,'4','pp','0316','PQRSTUVW','oooo0316','P'),
(317,'4','qq','0317','QRSTUVWX','qqqq0317','Q'),
(318,'4','rr','0318','RSTUVWXY','qqqq0318','R'),
(319,'4','ss','0319','STUVWXYZ','ssss0319','S'),
(320,'4','tt','0320','TUWVXYZA','ssss0320','T'),
(321,'1','aa','0321','ABCDEFGH','aaaa0321','A'),
(322,'1','bb','0322','BCDEFGHI','aaaa0322','B'),
(323,'1','cc','0323','CDEFGHIJ','cccc0323','C'),
(324,'1','dd','0324','DEFGHIJK','cccc0324','D'),
(325,'1','ee','0325','EFGHIJKL','eeee0325','E'),
(326,'2','ff','0326','FGHIJKLM','eeee0326','F'),
(327,'2','gg','0327','GHIJKLMN','gggg0327','G'),
(328,'2','hh','0328','HIJKLMNO','gggg0328','H'),
(329,'2','ii','0329','IJKLMNOP','iiii0329','I'),
(330,'2','jj','0330','JKLMNOPQ','iiii0330','J'),
(331,'3','kk','0331','KLMNOPQR','kkkk0331','K'),
(332,'3','ll','0332','LMNOPQRS','kkkk0332','L'),
(333,'3','mm','0333','MNOPQRST','mmmm0333','M'),
(334,'3','nn','0334','NOPQRSTU','mmmm0334','N'),
(335,'3','oo','0335','OPQRSTUV','oooo0335','O'),
(336,'4','pp','0336','PQRSTUVW','oooo0336','P'),
(337,'4','qq','0337','QRSTUVWX','qqqq0337','Q'),
(338,'4','rr','0338','RSTUVWXY','qqqq0338','R'),
(339,'4','ss','0339','STUVWXYZ','ssss0339','S'),
(340,'4','tt','0340','TUWVXYZA','ssss0340','T'),
(341,'1','aa','0341','ABCDEFGH','aaaa0341','A'),
(342,'1','bb','0342','BCDEFGHI','aaaa0342','B'),
(343,'1','cc','0343','CDEFGHIJ','cccc0343','C'),
(344,'1','dd','0344','DEFGHIJK','cccc0344','D'),
(345,'1','ee','0345','EFGHIJKL','eeee0345','E'),
(346,'2','ff','0346','FGHIJKLM','eeee0346','F'),
(347,'2','gg','0347','GHIJKLMN','gggg0347','G'),
(348,'2','hh','0348','HIJKLMNO','gggg0348','H'),
(349,'2','ii','0349','IJKLMNOP','iiii0349','I'),
(350,'2','jj','0350','JKLMNOPQ','iiii0350','J'),
(351,'3','kk','0351','KLMNOPQR','kkkk0351','K'),
(352,'3','ll','0352','LMNOPQRS','kkkk0352','L'),
(353,'3','mm','0353','MNOPQRST','mmmm0353','M'),
(354,'3','nn','0354','NOPQRSTU','mmmm0354','N'),
(355,'3','oo','0355','OPQRSTUV','oooo0355','O'),
(356,'4','pp','0356','PQRSTUVW','oooo0356','P'),
(357,'4','qq','0357','QRSTUVWX','qqqq0357','Q'),
(358,'4','rr','0358','RSTUVWXY','qqqq0358','R'),
(359,'4','ss','0359','STUVWXYZ','ssss0359','S'),
(360,'4','tt','0360','TUWVXYZA','ssss0360','T'),
(361,'1','aa','0361','ABCDEFGH','aaaa0361','A'),
(362,'1','bb','0362','BCDEFGHI','aaaa0362','B'),
(363,'1','cc','0363','CDEFGHIJ','cccc0363','C'),
(364,'1','dd','0364','DEFGHIJK','cccc0364','D'),
(365,'1','ee','0365','EFGHIJKL','eeee0365','E'),
(366,'2','ff','0366','FGHIJKLM','eeee0366','F'),
(367,'2','gg','0367','GHIJKLMN','gggg0367','G'),
(368,'2','hh','0368','HIJKLMNO','gggg0368','H'),
(369,'2','ii','0369','IJKLMNOP','iiii0369','I'),
(370,'2','jj','0370','JKLMNOPQ','iiii0370','J'),
(371,'3','kk','0371','KLMNOPQR','kkkk0371','K'),
(372,'3','ll','0372','LMNOPQRS','kkkk0372','L'),
(373,'3','mm','0373','MNOPQRST','mmmm0373','M'),
(374,'3','nn','0374','NOPQRSTU','mmmm0374','N'),
(375,'3','oo','0375','OPQRSTUV','oooo0375','O'),
(376,'4','pp','0376','PQRSTUVW','oooo0376','P'),
(377,'4','qq','0377','QRSTUVWX','qqqq0377','Q'),
(378,'4','rr','0378','RSTUVWXY','qqqq0378','R'),
(379,'4','ss','0379','STUVWXYZ','ssss0379','S'),
(380,'4','tt','0380','TUWVXYZA','ssss0380','T'),
(381,'1','aa','0381','ABCDEFGH','aaaa0381','A'),
(382,'1','bb','0382','BCDEFGHI','aaaa0382','B'),
(383,'1','cc','0383','CDEFGHIJ','cccc0383','C'),
(384,'1','dd','0384','DEFGHIJK','cccc0384','D'),
(385,'1','ee','0385','EFGHIJKL','eeee0385','E'),
(386,'2','ff','0386','FGHIJKLM','eeee0386','F'),
(387,'2','gg','0387','GHIJKLMN','gggg0387','G'),
(388,'2','hh','0388','HIJKLMNO','gggg0388','H'),
(389,'2','ii','0389','IJKLMNOP','iiii0389','I'),
(390,'2','jj','0390','JKLMNOPQ','iiii0390','J'),
(391,'3','kk','0391','KLMNOPQR','kkkk0391','K'),
(392,'3','ll','0392','LMNOPQRS','kkkk0392','L'),
(393,'3','mm','0393','MNOPQRST','mmmm0393','M'),
(394,'3','nn','0394','NOPQRSTU','mmmm0394','N'),
(395,'3','oo','0395','OPQRSTUV','oooo0395','O'),
(396,'4','pp','0396','PQRSTUVW','oooo0396','P'),
(397,'4','qq','0397','QRSTUVWX','qqqq0397','Q'),
(398,'4','rr','0398','RSTUVWXY','qqqq0398','R'),
(399,'4','ss','0399','STUVWXYZ','ssss0399','S'),
(400,'4','tt','0400','TUWVXYZA','ssss0400','T'),
(501,'1','aa','0501','ABCDEFGH','aaaa0501','A'),
(502,'1','bb','0502','BCDEFGHI','aaaa0502','B'),
(503,'1','cc','0503','CDEFGHIJ','cccc0503','C'),
(504,'1','dd','0504','DEFGHIJK','cccc0504','D'),
(505,'1','ee','0505','EFGHIJKL','eeee0505','E'),
(506,'2','ff','0506','FGHIJKLM','eeee0506','F'),
(507,'2','gg','0507','GHIJKLMN','gggg0507','G'),
(508,'2','hh','0508','HIJKLMNO','gggg0508','H'),
(509,'2','ii','0509','IJKLMNOP','iiii0509','I'),
(510,'2','jj','0510','JKLMNOPQ','iiii0510','J'),
(511,'3','kk','0511','KLMNOPQR','kkkk0511','K'),
(512,'3','ll','0512','LMNOPQRS','kkkk0512','L'),
(513,'3','mm','0513','MNOPQRST','mmmm0513','M'),
(514,'3','nn','0514','NOPQRSTU','mmmm0514','N'),
(515,'3','oo','0515','OPQRSTUV','oooo0515','O'),
(516,'4','pp','0516','PQRSTUVW','oooo0516','P'),
(517,'4','qq','0517','QRSTUVWX','qqqq0517','Q'),
(518,'4','rr','0518','RSTUVWXY','qqqq0518','R'),
(519,'4','ss','0519','STUVWXYZ','ssss0519','S'),
(520,'4','tt','0520','TUWVXYZA','ssss0520','T'),
(521,'1','aa','0521','ABCDEFGH','aaaa0521','A'),
(522,'1','bb','0522','BCDEFGHI','aaaa0522','B'),
(523,'1','cc','0523','CDEFGHIJ','cccc0523','C'),
(524,'1','dd','0524','DEFGHIJK','cccc0524','D'),
(525,'1','ee','0525','EFGHIJKL','eeee0525','E'),
(526,'2','ff','0526','FGHIJKLM','eeee0526','F'),
(527,'2','gg','0527','GHIJKLMN','gggg0527','G'),
(528,'2','hh','0528','HIJKLMNO','gggg0528','H'),
(529,'2','ii','0529','IJKLMNOP','iiii0529','I'),
(530,'2','jj','0530','JKLMNOPQ','iiii0530','J'),
(531,'3','kk','0531','KLMNOPQR','kkkk0531','K'),
(532,'3','ll','0532','LMNOPQRS','kkkk0532','L'),
(533,'3','mm','0533','MNOPQRST','mmmm0533','M'),
(534,'3','nn','0534','NOPQRSTU','mmmm0534','N'),
(535,'3','oo','0535','OPQRSTUV','oooo0535','O'),
(536,'4','pp','0536','PQRSTUVW','oooo0536','P'),
(537,'4','qq','0537','QRSTUVWX','qqqq0537','Q'),
(538,'4','rr','0538','RSTUVWXY','qqqq0538','R'),
(539,'4','ss','0539','STUVWXYZ','ssss0539','S'),
(540,'4','tt','0540','TUWVXYZA','ssss0540','T'),
(541,'1','aa','0541','ABCDEFGH','aaaa0541','A'),
(542,'1','bb','0542','BCDEFGHI','aaaa0542','B'),
(543,'1','cc','0543','CDEFGHIJ','cccc0543','C'),
(544,'1','dd','0544','DEFGHIJK','cccc0544','D'),
(545,'1','ee','0545','EFGHIJKL','eeee0545','E'),
(546,'2','ff','0546','FGHIJKLM','eeee0546','F'),
(547,'2','gg','0547','GHIJKLMN','gggg0547','G'),
(548,'2','hh','0548','HIJKLMNO','gggg0548','H'),
(549,'2','ii','0549','IJKLMNOP','iiii0549','I'),
(550,'2','jj','0550','JKLMNOPQ','iiii0550','J'),
(551,'3','kk','0551','KLMNOPQR','kkkk0551','K'),
(552,'3','ll','0552','LMNOPQRS','kkkk0552','L'),
(553,'3','mm','0553','MNOPQRST','mmmm0553','M'),
(554,'3','nn','0554','NOPQRSTU','mmmm0554','N'),
(555,'3','oo','0555','OPQRSTUV','oooo0555','O'),
(556,'4','pp','0556','PQRSTUVW','oooo0556','P'),
(557,'4','qq','0557','QRSTUVWX','qqqq0557','Q'),
(558,'4','rr','0558','RSTUVWXY','qqqq0558','R'),
(559,'4','ss','0559','STUVWXYZ','ssss0559','S'),
(560,'4','tt','0560','TUWVXYZA','ssss0560','T');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 260)

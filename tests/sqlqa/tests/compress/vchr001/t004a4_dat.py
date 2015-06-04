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
    
    stmt = """insert into t004t4 values
(1,'1','aa','0001','1aa0001','aaaa0001','A this is the internal varchar project'),
(2,'1','bb','0002','1bb0002','aaaa0002','B this is the internal varchar project'),
(3,'1','cc','0003','CDEFGHIJ','cccc0003','C this is the compressed varchar project'),
(4,'1','dd','0004','DEFGHIJK','cccc0004','D this is the compressed varchar project'),
(5,'1','ee','0005','1ee0005','eeee0005','E this is the internal varchar project'),
(6,'2','ff','0006','FGHIJKLM','eeee0006','F this is the compressed varchar project'),
(7,'2','gg','0007','GHIJKLMN','gggg0007','G this is the compressed varchar project'),
(8,'2','hh','0008','HIJKLMNO','gggg0008','H this is the compressed varchar project'),
(10,'2','jj','0010','2jj0010','iiii0010','J this is the internal varchar project'),
(11,'3','kk','0011','KLMNOPQR','kkkk0011','K this is the compressed varchar project'),
(12,'3','ll','0012','LMNOPQRS','kkkk0012','L this is the compressed varchar project'),
(13,'3','mm','0013','MNOPQRST','mmmm0013','M this is the compressed varchar project'),
(14,'3','nn','0014','NOPQRSTU','mmmm0014','N this is the compressed varchar project'),
(15,'3','oo','0015','OPQRSTUV','oooo0015','O this is the compressed varchar project'),
(16,'4','pp','0016','Whitney','oooo0016','P this is the compressed varchar project'),
(17,'4','qq','0017','4qq0017','qqqq0017','Q this is the internal varchar project'),
(18,'4','rr','0018','Whitney','qqqq0018','R this is the compressed varchar project'),
(19,'4','ss','0019','4ss0019','ssss0019','S this is the internal varchar project'),
(20,'4','tt','0020','4tt0020','ssss0020','T this is the internal varchar project'),
(42,'5','ww','0042','BBCDEFGH','Fairweather','Mount Fairweather has generally harsh weather conditions'),
(50,'7','jj','0150','01500150','iiii0150','Mount McKinley or Denali in Alaska is the highest mountain peak in North America, at a height of approximately 20,320 feet (6,194 m). It is the centerpiece of Denali National Park. The mountain is also known as Bolshaya Gora, meaning Big Mountain, in Russian.'),
(51,'7','kk','0151','KLMNOPQR','kkkk0151','Mount McKinley or Denali in Alaska is the highest mountain peak in North America, at a height of approximately 20,320 feet (6,194 m). It is the centerpiece of Denali National Park. The mountain is also known as Bolshaya Gora, meaning Big Mountain, in Russian.'),
(101,'1','aa','0101','ABCDEFGH','aaaa0101','A Mount Whitney in N. America'),
(102,'1','bb','0102','BCDEFGHI','aaaa0102','B Mount Whitney in N. America'),
(103,'1','cc','0103','CDEFGHIJ','cccc0103','C Mount Whitney in N. America'),
(104,'1','dd','0104','DEFGHIJK','cccc0104','D Mount Whitney in N. America'),
(105,'1','ee','0105','EFGHIJKL','eeee0105','E Mount Whitney in N. America'),
(106,'2','ff','0106','FGHIJKLM','eeee0106','F Mount Whitney in N. America'),
(107,'2','gg','0107','GHIJKLMN','gggg0107','G Mount Whitney in N. America'),
(108,'2','hh','0108','HIJKLMNO','gggg0108','H Mount Whitney in N. America'),
(109,'6','ii','0009','IJKLMNOP','iiii0009','Mount McKinley in Alaska is the highest mountain peak in North America, at a height of approximately 20,320 feet (6,194 m). It is the centerpiece of Denali National Park. The mountain is also known as Bolshaya Gora, meaning Big Mountain, in Russ'),
(110,'2','jj','0110','JKLMNOPQ','iiii0110','J Mount Whitney in N. America'),
(121,'1','aa','0121','ABCDEFGH','aaaa0121','A Mount Whitney in N. America'),
(122,'1','bb','0122','BCDEFGHI','aaaa0122','B Mount Whitney in N. America'),
(123,'1','cc','0123','CDEFGHIJ','cccc0123','C Mount Whitney in N. America'),
(124,'1','dd','0124','DEFGHIJK','cccc0124','D Mount Whitney in N. America'),
(125,'1','ee','0125','EFGHIJKL','eeee0125','E Mount Whitney in N. America'),
(126,'2','ff','0126','FGHIJKLM','eeee0126','F Mount Whitney in N. America'),
(127,'2','gg','0127','GHIJKLMN','gggg0127','G Mount Whitney in N. America'),
(128,'2','hh','0128','HIJKLMNO','gggg0128','H Mount Whitney in N. America'),
(130,'2','jj','0130','JKLMNOPQ','iiii0130','J Mount Whitney in N. America'),
(131,'3','kk','0131','KLMNOPQR','kkkk0131','K Mount Whitney in N. America'),
(132,'3','ll','0132','LMNOPQRS','kkkk0132','L Mount Whitney in N. America'),
(133,'3','mm','0133','MNOPQRST','mmmm0133','M Mount Whitney in N. America'),
(134,'3','nn','0134','NOPQRSTU','mmmm0134','N Mount Whitney in N. America'),
(135,'3','oo','0135','OPQRSTUV','oooo0135','O Mount Whitney in N. America'),
(136,'4','pp','0136','Whitney','oooo0136','P Mount McKinley in N. America'),
(137,'4','qq','0137','Whitney','qqqq0137','Q Mount McKinley in N. America'),
(138,'4','rr','0138','Whitney','qqqq0138','R Mount McKinley in N. America'),
(139,'4','ss','0139','Whitney','ssss0139','S Mount McKinley in N. America'),
(140,'4','tt','0140','TUWVXYZA','ssss0140','T Mount Whitney in N. America'),
(141,'1','aa','0141','ABCDEFGH','aaaa0141','A Mount Whitney in N. America'),
(142,'1','bb','0142','BCDEFGHI','aaaa0142','B Mount Whitney in N. America'),
(143,'1','cc','0143','CDEFGHIJ','cccc0143','C Mount Whitney in N. America'),
(144,'1','dd','0144','DEFGHIJK','cccc0144','D Mount Whitney in N. America'),
(145,'1','ee','0145','EFGHIJKL','eeee0145','E Mount Whitney in N. America'),
(146,'2','ff','0146','FGHIJKLM','eeee0146','F Mount Whitney in N. America'),
(147,'2','gg','0147','GHIJKLMN','gggg0147','G Mount Whitney in N. America'),
(148,'2','hh','0148','HIJKLMNO','gggg0148','H Mount Whitney in N. America'),
(153,'3','mm','0153','MNOPQRST','mmmm0153','M Mount Whitney in N. America'),
(154,'3','nn','0154','NOPQRSTU','mmmm0154','N Mount Whitney in N. America'),
(155,'3','oo','0155','OPQRSTUV','oooo0155','O Mount Whitney in N. America'),
(156,'4','pp','0156','Whitney','oooo0156','P Mount McKinley in N. America'),
(157,'4','qq','0157','Whitney','qqqq0157','Q Mount McKinley in N. America'),
(158,'4','rr','0158','Whitney','qqqq0158','R Mount McKinley in N. America'),
(159,'4','ss','0159','Whitney','ssss0159','S Mount McKinley in N. America'),
(160,'4','tt','0160','TUWVXYZA','ssss0160','T Mount Whitney in N. America'),
(161,'1','aa','0161','ABCDEFGH','aaaa0161','A Mount Whitney in N. America'),
(162,'1','bb','0162','BCDEFGHI','aaaa0162','B Mount Whitney in N. America'),
(163,'1','cc','0163','CDEFGHIJ','cccc0163','C Mount Whitney in N. America'),
(164,'1','dd','0164','DEFGHIJK','cccc0164','D Mount Whitney in N. America'),
(165,'1','ee','0165','EFGHIJKL','eeee0165','E Mount Whitney in N. America'),
(166,'2','ff','0166','FGHIJKLM','eeee0166','F Mount Whitney in N. America'),
(167,'2','gg','0167','GHIJKLMN','gggg0167','G Mount Whitney in N. America'),
(168,'2','hh','0168','HIJKLMNO','gggg0168','H Mount Whitney in N. America'),
(170,'2','jj','0170','JKLMNOPQ','iiii0170','J Mount Whitney in N. America'),
(171,'3','kk','0171','KLMNOPQR','kkkk0171','K Mount Whitney in N. America'),
(172,'3','ll','0172','LMNOPQRS','kkkk0172','L Mount Whitney in N. America'),
(173,'3','mm','0173','MNOPQRST','mmmm0173','M Mount Whitney in N. America'),
(174,'3','nn','0174','NOPQRSTU','mmmm0174','N Mount Whitney in N. America'),
(175,'3','oo','0175','OPQRSTUV','oooo0175','O Mount Whitney in N. America'),
(176,'4','pp','0176','Whitney','oooo0176','P Mount McKinley in N. America'),
(177,'4','qq','0177','Whitney','qqqq0177','Q Mount McKinley in N. America'),
(178,'4','rr','0178','Whitney','qqqq0178','R Mount McKinley in N. America'),
(179,'4','ss','0179','Whitney','ssss0179','S Mount McKinley in N. America'),
(180,'4','tt','0180','TUWVXYZA','ssss0180','T Mount Whitney in N. America'),
(181,'1','aa','0181','ABCDEFGH','aaaa0181','A Mount Whitney in N. America'),
(191,'3','kk','0191','KLMNOPQR','kkkk0191','K Mount Whitney in N. America'),
(192,'3','ll','0192','LMNOPQRS','kkkk0192','L Mount Whitney in N. America'),
(193,'3','mm','0193','MNOPQRST','mmmm0193','M Mount Whitney in N. America'),
(194,'3','nn','0194','NOPQRSTU','mmmm0194','N Mount Whitney in N. America'),
(195,'3','oo','0195','OPQRSTUV','oooo0195','O Mount Whitney in N. America'),
(196,'4','pp','0196','Whitney','oooo0196','P Mount McKinley in N. America'),
(197,'4','qq','0197','Whitney','qqqq0197','Q Mount McKinley in N. America'),
(198,'4','rr','0198','Whitney','qqqq0198','R Mount McKinley in N. America'),
(199,'4','ss','0199','Whitney','ssss0199','S Mount McKinley in N. America'),
(200,'4','tt','0200','TUWVXYZA','ssss0200','T Mount Whitney in N. America'),
(209,'6','ii','0109','IJKLMNOP','iiii0109','Mount McKinley in Alaska is the highest mountain peak in North America, at a height of approximately 20,320 feet (6,194 m). It is the centerpiece of Denali National Park. The mountain is also known as Bolshaya Gora, meaning Big Mountain, in Russ'),
(229,'6','ii','0129','IJKLMNOP','iiii0129','Mount McKinley in Alaska is the highest mountain peak in North America, at a height of approximately 20,320 feet (6,194 m). It is the centerpiece of Denali National Park. The mountain is also known as Bolshaya Gora, meaning Big Mountain, in Russ'),
(249,'6','ii','0149','IJKLMNOP','iiii0149','Mount McKinley in Alaska is the highest mountain peak in North America, at a height of approximately 20,320 feet (6,194 m). It is the centerpiece of Denali National Park. The mountain is also known as Bolshaya Gora, meaning Big Mountain, in Russ'),
(269,'6','ii','0169','IJKLMNOP','iiii0169','Mount McKinley in Alaska is the highest mountain peak in North America, at a height of approximately 20,320 feet (6,194 m). It is the centerpiece of Denali National Park. The mountain is also known as Bolshaya Gora, meaning Big Mountain, in Russ'),
(270,'7','jj','0370','iiii0370','iiii0370','Mount McKinley or Denali in Alaska.tbc.'),
(273,'7','mm','0373','mmmm0373','mmmm0373','Mount McKinley or Denali in Alaska.tbc.'),
(276,'7','pp','0376','oooo0376','oooo0376','Mount McKinley or Denali in Alaska.tbc.'),
(281,'7','aa','0381','aaaa0381','aaaa0381','Mount McKinley or Denali in Alaska.tbc.'),
(284,'7','dd','0384','cccc0384','cccc0384','Mount McKinley or Denali in Alaska.tbc.'),
(287,'7','gg','0387','gggg0387','gggg0387','Mount McKinley or Denali in Alaska.tbc.'),
(290,'7','jj','0390','iiii0390','iiii0390','Mount McKinley or Denali in Alaska.tbc.'),
(293,'7','mm','0393','mmmm0393','mmmm0393','Mount McKinley or Denali in Alaska.tbc.'),
(296,'7','pp','0396','oooo0396','oooo0396','Mount McKinley or Denali in Alaska.tbc.'),
(301,'1','aa','0301','ABCDEFGH','aaaa0301','A Mount Whitney in N. America'),
(303,'1','bb','0303','BCDEFGHI','aaaa0303','B Mount Whitney in N. America'),
(303,'1','cc','0303','CDEFGHIJ','cccc0303','C Mount Whitney in N. America'),
(304,'1','dd','0304','DEFGHIJK','cccc0304','D Mount Whitney in N. America'),
(305,'1','ee','0305','EFGHIJKL','eeee0305','E Mount Whitney in N. America'),
(306,'2','ff','0306','FGHIJKLM','eeee0306','F Mount Whitney in N. America'),
(307,'2','gg','0307','GHIJKLMN','gggg0307','G Mount Whitney in N. America'),
(308,'2','hh','0308','HIJKLMNO','gggg0308','H Mount Whitney in N. America'),
(310,'2','jj','0310','JKLMNOPQ','iiii0310','J Mount Whitney in N. America'),
(311,'3','kk','0311','KLMNOPQR','kkkk0311','K Mount Whitney in N. America'),
(312,'3','ll','0312','LMNOPQRS','kkkk0312','L Mount Whitney in N. America'),
(313,'3','mm','0313','MNOPQRST','mmmm0313','M Mount Whitney in N. America'),
(314,'3','nn','0314','NOPQRSTU','mmmm0314','N Mount Whitney in N. America'),
(315,'3','oo','0315','OPQRSTUV','oooo0315','O Mount Whitney in N. America'),
(316,'4','pp','0316','Whitney','oooo0316','P Mount McKinley in N. America'),
(317,'4','qq','0317','Whitney','qqqq0317','Q Mount McKinley in N. America'),
(318,'4','rr','0318','Whitney','qqqq0318','R Mount McKinley in N. America'),
(319,'4','ss','0319','Whitney','ssss0319','S Mount McKinley in N. America'),
(320,'4','tt','0320','TUWVXYZA','ssss0320','T Mount Whitney in N. America'),
(321,'1','aa','0321','ABCDEFGH','aaaa0321','A Mount Whitney in N. America'),
(322,'1','bb','0322','BCDEFGHI','aaaa0322','B Mount Whitney in N. America'),
(323,'1','cc','0323','CDEFGHIJ','cccc0323','C Mount Whitney in N. America'),
(324,'1','dd','0324','DEFGHIJK','cccc0324','D Mount Whitney in N. America'),
(325,'1','ee','0325','EFGHIJKL','eeee0325','E Mount Whitney in N. America'),
(326,'2','ff','0326','FGHIJKLM','eeee0326','F Mount Whitney in N. America'),
(327,'2','gg','0327','GHIJKLMN','gggg0327','G Mount Whitney in N. America'),
(328,'2','hh','0328','HIJKLMNO','gggg0328','H Mount Whitney in N. America'),
(330,'2','jj','0330','JKLMNOPQ','iiii0330','J Mount Whitney in N. America'),
(346,'2','ff','0346','FGHIJKLM','eeee0346','F Mount Whitney in N. America'),
(347,'2','gg','0347','GHIJKLMN','gggg0347','G Mount Whitney in N. America'),
(348,'2','hh','0348','HIJKLMNO','gggg0348','H Mount Whitney in N. America'),
(350,'2','jj','0350','JKLMNOPQ','iiii0350','J Mount Whitney in N. America'),
(352,'3','ll','0352','LMNOPQRS','kkkk0352','L Mount Whitney in N. America'),
(353,'3','mm','0353','MNOPQRST','mmmm0353','M Mount Whitney in N. America'),
(354,'3','nn','0354','NOPQRSTU','mmmm0354','N Mount Whitney in N. America'),
(355,'3','oo','0355','OPQRSTUV','oooo0355','O Mount Whitney in N. America'),
(356,'4','pp','0356','Whitney','oooo0356','P Mount McKinley in N. America'),
(357,'4','qq','0357','Whitney','qqqq0357','Q Mount McKinley in N. America'),
(358,'4','rr','0358','Whitney','qqqq0358','R Mount McKinley in N. America'),
(359,'4','ss','0359','Whitney','ssss0359','S Mount McKinley in N. America'),
(360,'4','tt','0360','TUWVXYZA','ssss0360','T Mount Whitney in N. America'),
(362,'1','bb','0362','BCDEFGHI','aaaa0362','B Mount Whitney in N. America'),
(363,'1','cc','0363','CDEFGHIJ','cccc0363','C Mount Whitney in N. America'),
(364,'1','dd','0364','DEFGHIJK','cccc0364','D Mount Whitney in N. America'),
(365,'1','ee','0365','EFGHIJKL','eeee0365','E Mount Whitney in N. America'),
(366,'2','ff','0366','FGHIJKLM','eeee0366','F Mount Whitney in N. America'),
(367,'2','gg','0367','GHIJKLMN','gggg0367','G Mount Whitney in N. America'),
(368,'2','hh','0368','HIJKLMNO','gggg0368','H Mount Whitney in N. America'),
(371,'3','kk','0371','KLMNOPQR','kkkk0371','K Mount Whitney in N. America'),
(372,'3','ll','0372','LMNOPQRS','kkkk0372','L Mount Whitney in N. America'),
(374,'3','nn','0374','NOPQRSTU','mmmm0374','N Mount Whitney in N. America'),
(377,'4','qq','0377','Whitney','qqqq0377','Q Mount McKinley in N. America'),
(378,'4','rr','0378','Whitney','qqqq0378','R Mount McKinley in N. America'),
(379,'4','ss','0379','Whitney','ssss0379','S Mount McKinley in N. America'),
(380,'4','tt','0380','TUWVXYZA','ssss0380','T Mount Whitney in N. America'),
(382,'1','bb','0382','BCDEFGHI','aaaa0382','B Mount Whitney in N. America'),
(383,'1','cc','0383','CDEFGHIJ','cccc0383','C Mount Whitney in N. America'),
(385,'1','ee','0385','EFGHIJKL','eeee0385','E Mount Whitney in N. America'),
(386,'2','ff','0386','FGHIJKLM','eeee0386','F Mount Whitney in N. America'),
(388,'2','hh','0388','HIJKLMNO','gggg0388','H Mount Whitney in N. America'),
(391,'3','kk','0391','KLMNOPQR','kkkk0391','K Mount Whitney in N. America'),
(392,'3','ll','0392','LMNOPQRS','kkkk0392','L Mount Whitney in N. America'),
(394,'3','nn','0394','NOPQRSTU','mmmm0394','N Mount Whitney in N. America'),
(397,'4','qq','0397','Whitney','qqqq0397','Q Mount McKinley in N. America'),
(398,'4','rr','0398','Whitney','qqqq0398','R Mount McKinley in N. America'),
(400,'4','tt','0400','TUWVXYZA','ssss0400','T Mount Whitney in N. America'),
(409,'6','ii','0309','IJKLMNOP','iiii0309','Mount McKinley in Alaska is the highest mountain peak in North America, at a height of approximately 20,320 feet (6,194 m). It is the centerpiece of Denali National Park. The mountain is also known as Bolshaya Gora, meaning Big Mountain, in Russ'),
(411,'7','kk','0111','zzzz0111','kkkk0111','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(412,'7','ll','0112','zzzz0112','kkkk0112','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(413,'7','mm','0113','zzzz0113','mmmm0113','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(414,'7','nn','0114','zzzz0114','mmmm0114','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(415,'7','oo','0115','zzzz0115','oooo0115','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(416,'7','pp','0116','zzzz0116','oooo0116','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(417,'7','qq','0117','zzzz0117','qqqq0117','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(418,'7','rr','0118','zzzz0118','qqqq0118','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(419,'7','ss','0119','zzzz0119','ssss0119','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(420,'7','tt','0120','zzzz0120','ssss0120','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(429,'6','ii','0329','IJKLMNOP','iiii0329','Mount McKinley in Alaska is the highest mountain peak in North America, at a height of approximately 20,320 feet (6,194 m). It is the centerpiece of Denali National Park. The mountain is also known as Bolshaya Gora, meaning Big Mountain, in Russ'),
(449,'6','ii','0349','IJKLMNOP','iiii0349','Mount McKinley in Alaska is the highest mountain peak in North America, at a height of approximately 20,320 feet (6,194 m). It is the centerpiece of Denali National Park. The mountain is also known as Bolshaya Gora, meaning Big Mountain, in Russ'),
(469,'6','ii','0369','IJKLMNOP','iiii0369','Mount McKinley in Alaska is the highest mountain peak in North America, at a height of approximately 20,320 feet (6,194 m). It is the centerpiece of Denali National Park. The mountain is also known as Bolshaya Gora, meaning Big Mountain, in Russ'),
(482,'7','bb','0182','zzzz0182','aaaa0182','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(483,'7','cc','0183','zzzz0183','cccc0183','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(484,'7','dd','0184','zzzz0184','cccc0184','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(485,'7','ee','0185','zzzz0185','eeee0185','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(486,'7','ff','0186','zzzz0186','eeee0186','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(487,'7','gg','0187','zzzz0187','gggg0187','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(488,'7','hh','0188','zzzz0188','gggg0188','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(489,'6','ii','0389','IJKLMNOP','iiii0389','Mount McKinley in Alaska is the highest mountain peak in North America, at a height of approximately 20,320 feet (6,194 m). It is the centerpiece of Denali National Park. The mountain is also known as Bolshaya Gora, meaning Big Mountain, in Russ'),
(490,'7','jj','0190','zzzz0190','iiii0190','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(501,'7','ll','0152','EFGHIJKL','kkkk0152','G Mount McKinley in N. America'),
(505,'1','ee','0505','EFGHIJKL','eeee0505','E Mount Whitney in N. America'),
(589,'7','ii','0189','zzzz0189','iiii0189','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(631,'7','kk','0331','zzzz0331','kkkk0331','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(632,'7','ll','0332','zzzz0332','kkkk0332','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(633,'7','mm','0333','zzzz0333','mmmm0333','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(634,'7','nn','0334','zzzz0334','mmmm0334','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(635,'7','oo','0335','zzzz0335','oooo0335','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(636,'7','pp','0336','zzzz0336','oooo0336','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(637,'7','qq','0337','zzzz0337','qqqq0337','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(638,'7','rr','0338','zzzz0338','qqqq0338','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(639,'7','ss','0339','zzzz0339','ssss0339','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(640,'7','tt','0340','zzzz0340','ssss0340','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(641,'7','aa','0341','zzzz0341','aaaa0341','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(642,'7','bb','0342','zzzz0342','aaaa0342','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(643,'7','cc','0343','zzzz0343','cccc0343','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(644,'7','dd','0344','zzzz0344','cccc0344','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(645,'7','ee','0345','zzzz0345','eeee0345','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(651,'7','kk','0351','zzzz0351','kkkk0351','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(661,'7','aa','0361','zzzz0361','aaaa0361','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(675,'7','oo','0375','zzzz0375','oooo0375','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(695,'7','oo','0395','zzzz0395','oooo0395','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(699,'7','ss','0399','zzzz0399','ssss0399','It is the centerpiece of Denali National Park. The mountain is also known as Big Mountain in Russ'),
(default,default,'aa','0501',default,'aaaa0501',default),
(default,'5','ww','0043',default,'wwww0043',default),
(default,default,'ww','0044','BBCDEFGH','wwww0044',default),
(default,'5','ww','0045',default,'wwww0045','Mount Cook has generally harsh weather conditions'),
(default,default,'ww','wwww',default,'wwww0041',default);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 227)
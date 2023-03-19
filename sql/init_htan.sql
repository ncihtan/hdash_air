CREATE DATABASE IF NOT EXISTS htan;

USE htan;

DROP TABLE IF EXISTS ATLAS;

CREATE TABLE ATLAS (
   ATLAS_ID varchar(50),
   SYNAPSE_ID varchar(100),
   NAME varchar(100),
   DCC_LIAISON varchar(100),
   PRIMARY KEY (ATLAS_ID)
);

# TODO FINALIZE ATLAS AND LIAISON LIST
INSERT INTO ATLAS VALUES ("HTA1", "syn20834712", "PILOT - HTAPP", "Vesteinn");
INSERT INTO ATLAS VALUES ("HTA2", "syn23511984", "PILOT - PCAPP", "Ethan");
INSERT INTO ATLAS VALUES ("HTA3", "syn22124336", "HTAN BU", "Ethan");
INSERT INTO ATLAS VALUES ("HTA4", "syn22776798", "HTAN CHOP", "Ino");
INSERT INTO ATLAS VALUES ("HTA5", "syn23511954", "HTAN DFCI", "Ethan");
INSERT INTO ATLAS VALUES ("HTA6", "syn23511961", "HTAN Duke", "Ino");
INSERT INTO ATLAS VALUES ("HTA7", "syn22123910", "HTAN HMS", "Milen");
INSERT INTO ATLAS VALUES ("HTA8", "syn23448901", "HTAN MSK", "Ino");
INSERT INTO ATLAS VALUES ("HTA9", "syn22093319", "HTAN OHSU", "Milen");
INSERT INTO ATLAS VALUES ("HTA10", "syn23511964", "HTAN Stanford", "Milen");
INSERT INTO ATLAS VALUES ("HTA11", "syn21050481", "HTAN Vanderbilt", "Vesteinn");
INSERT INTO ATLAS VALUES ("HTA12", "syn22255320", "HTAN WUSTL", "Vesteinn");
INSERT INTO ATLAS VALUES ("HTA13", "syn24984270", "TNP SARDANA", "Dave G");
INSERT INTO ATLAS VALUES ("HTA14", "syn22041595", "TNP TMA", "Dave G");
INSERT INTO ATLAS VALUES ("HTA15", "syn25555889", "TNP SRRS", "Dave G");

import datetime
import json
import os
import random

from random_useragent.chrome import Chrome


class Android(Chrome):
    def __init__(self):
        super().__init__()

        self.android_model = [
            {
                "model": "V2121A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "PEEM00",
                "id": "RKQ1.211103.002"
            },
            {
                "model": "SPN-AL00",
                "id": "HUAWEISPN-AL00"
            },
            {
                "model": "ANY-AN00",
                "id": "HONORANY-AN00"
            },
            {
                "model": "TNN-AN00",
                "id": "HUAWEITNN-AN00"
            },
            {
                "model": "V2054A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "PEQM00",
                "id": "RP1A.200720.011"
            },
            {
                "model": "V1813BT",
                "id": "PKQ1.181030.001"
            },
            {
                "model": "LIO-AN00",
                "id": "HUAWEILIO-AN00"
            },
            {
                "model": "TNA-AN00",
                "id": "HONORTNA-AN00"
            },
            {
                "model": "LYA-AL00",
                "id": "HUAWEILYA-AL00"
            },
            {
                "model": "PEHM00",
                "id": "SKQ1.210216.001"
            },
            {
                "model": "PDYM20",
                "id": "RP1A.200720.011"
            },
            {
                "model": "ELE-AL00",
                "id": "HUAWEIELE-AL00"
            },
            {
                "model": "V2154A",
                "id": "SP1A.210812.003"
            },
            {
                "model": "EML-AL00",
                "id": "HUAWEIEML-AL00"
            },
            {
                "model": "MEIZU 18 Pro",
                "id": "RKQ1.210715.001"
            },
            {
                "model": "JEF-AN00",
                "id": "HUAWEIJEF-AN00"
            },
            {
                "model": "JNY-AL10",
                "id": "HUAWEIJNY-AL10"
            },
            {
                "model": "TAS-AN00",
                "id": "HUAWEITAS-AN00"
            },
            {
                "model": "RMX3121",
                "id": "RP1A.200720.011"
            },
            {
                "model": "ELZ-AN00",
                "id": "HONORELZ-AN00"
            },
            {
                "model": "vivo Z1",
                "id": "PKQ1.180819.001"
            },
            {
                "model": "V2136A",
                "id": "SP1A.210812.003"
            },
            {
                "model": "ANG-AN00",
                "id": "HUAWEIANG-AN00"
            },
            {
                "model": "SEA-AL10",
                "id": "HUAWEISEA-AL10"
            },
            {
                "model": "TEL-AN00a",
                "id": "HONORTEL-AN00a"
            },
            {
                "model": "V2106A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "PEGT00",
                "id": "RKQ1.200903.002"
            },
            {
                "model": "MT-A3D",
                "id": "NHG47K"
            },
            {
                "model": "V1913A",
                "id": "P00610"
            },
            {
                "model": "HLK-AL00",
                "id": "HONORHLK-AL00"
            },
            {
                "model": "LON-AL00",
                "id": "HUAWEILON-AL00"
            },
            {
                "model": "V1962A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "OXF-AN00",
                "id": "HUAWEIOXF-AN00"
            },
            {
                "model": "PACT00",
                "id": "QP1A.190711.020"
            },
            {
                "model": "MAR-AL00",
                "id": "HUAWEIMAR-AL00"
            },
            {
                "model": "V1941A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "TAS-AL00",
                "id": "HUAWEITAS-AL00"
            },
            {
                "model": "PBDM00",
                "id": "QKQ1.190918.001"
            },
            {
                "model": "PDNM00",
                "id": "RKQ1.200710.002"
            },
            {
                "model": "vivo X9s Plus",
                "id": "OPM1.171019.019"
            },
            {
                "model": "MT-A3S",
                "id": "NHG47K"
            },
            {
                "model": "OPPO R11s Plus",
                "id": "PKQ1.190414.001"
            },
            {
                "model": "MLD-AL10",
                "id": "HUAWEIMLD-AL10"
            },
            {
                "model": "V1901A",
                "id": "P00610"
            },
            {
                "model": "PAR-AL00",
                "id": "HUAWEIPAR-AL00"
            },
            {
                "model": "RMX3350",
                "id": "SP1A.210812.016"
            },
            {
                "model": "PCHM30",
                "id": "RKQ1.200903.002"
            },
            {
                "model": "RNA-AN00",
                "id": "HONORRNA-AN00"
            },
            {
                "model": "PEGM00",
                "id": "RKQ1.200903.002"
            },
            {
                "model": "PFZM10",
                "id": "SP1A.210812.016"
            },
            {
                "model": "PBEM00",
                "id": "QKQ1.190918.001"
            },
            {
                "model": "OCE-AN10",
                "id": "HUAWEIOCE-AN10"
            },
            {
                "model": "meizu 17",
                "id": "QKQ1.200223.002"
            },
            {
                "model": "V1809A",
                "id": "PKQ1.181030.001"
            },
            {
                "model": "GM1900",
                "id": "RKQ1.201022.002"
            },
            {
                "model": "CDY-AN90",
                "id": "HUAWEICDY-AN90"
            },
            {
                "model": "vivo X21UD A",
                "id": "PKQ1.180819.001"
            },
            {
                "model": "Qbao",
                "id": "NHG47K"
            },
            {
                "model": "LSA-AN00",
                "id": "HONORLSA-AN00"
            },
            {
                "model": "STK-AL00",
                "id": "HUAWEISTK-AL00"
            },
            {
                "model": "V2068A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "VOG-AL00",
                "id": "HUAWEIVOG-AL00"
            },
            {
                "model": "CDL-AN50",
                "id": "HUAWEICDL-AN50"
            },
            {
                "model": "LE2120",
                "id": "RKQ1.211103.002"
            },
            {
                "model": "V2001A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "V2057A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "PAAT00",
                "id": "QKQ1.191224.003"
            },
            {
                "model": "KB2000",
                "id": "RP1A.201005.001"
            },
            {
                "model": "RMX3366",
                "id": "RKQ1.201105.002"
            },
            {
                "model": "V1831A",
                "id": "P00610"
            },
            {
                "model": "V2164A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "VCE-AL00",
                "id": "HUAWEIVCE-AL00"
            },
            {
                "model": "NTH-AN00",
                "id": "HONORNTH-AN00"
            },
            {
                "model": "Lenovo L79031",
                "id": "RKQ1.201022.002"
            },
            {
                "model": "DVC-AN20",
                "id": "HUAWEIDVC-AN20"
            },
            {
                "model": "NOH-AL00",
                "id": "HUAWEINOH-AL00"
            },
            {
                "model": "CDY-AN00",
                "id": "HUAWEICDY-AN00"
            },
            {
                "model": "V2005A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "FRL-AN00a",
                "id": "HUAWEIFRL-AN00a"
            },
            {
                "model": "NOH-AN00",
                "id": "HUAWEINOH-AN00"
            },
            {
                "model": "PCT-AL10",
                "id": "HUAWEIPCT-AL10"
            },
            {
                "model": "ELS-AN00",
                "id": "HUAWEIELS-AN00"
            },
            {
                "model": "JER-TN10",
                "id": "HUAWEIJER-TN10"
            },
            {
                "model": "EBG-AN00",
                "id": "HUAWEIEBG-AN00"
            },
            {
                "model": "PCAM10",
                "id": "RP1A.200720.011"
            },
            {
                "model": "OCE-AN50",
                "id": "HUAWEIOCE-AN50"
            },
            {
                "model": "YAL-AL50",
                "id": "HUAWEIYAL-AL50"
            },
            {
                "model": "V2036A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "ANA-AN00",
                "id": "HUAWEIANA-AN00"
            },
            {
                "model": "SM-G9910",
                "id": "SP1A.210812.016"
            },
            {
                "model": "vivo X21",
                "id": "PKQ1.180819.001"
            },
            {
                "model": "PFDM00",
                "id": "SP1A.210812.016"
            },
            {
                "model": "PCKM00",
                "id": "RKQ1.200903.002"
            },
            {
                "model": "OPPO R9s",
                "id": "MMB29M"
            },
            {
                "model": "WLZ-AL10",
                "id": "HUAWEIWLZ-AL10"
            },
            {
                "model": "HMA-AL00",
                "id": "HUAWEIHMA-AL00"
            },
            {
                "model": "SP200",
                "id": "CMDCSP200"
            },
            {
                "model": "YAL-L21",
                "id": "HUAWEIYAL-L61"
            },
            {
                "model": "PFTM20",
                "id": "SP1A.210812.016"
            },
            {
                "model": "JEF-AN20",
                "id": "HUAWEIJEF-AN20"
            },
            {
                "model": "LRA-AL00",
                "id": "HONORLRA-AL00"
            },
            {
                "model": "V2069A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "PFJM10",
                "id": "RKQ1.211119.001"
            },
            {
                "model": "ELZ-AN10",
                "id": "HONORELZ-AN10"
            },
            {
                "model": "JSC-AL50",
                "id": "HUAWEIJSC-AL50"
            },
            {
                "model": "V1838A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "PADT00",
                "id": "QP1A.190711.020"
            },
            {
                "model": "AWM-A0",
                "id": "G66T2003270CN00MQ1"
            },
            {
                "model": "V2048A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "COL-AL10",
                "id": "HUAWEICOL-AL10"
            },
            {
                "model": "PACM00",
                "id": "QP1A.190711.020"
            },
            {
                "model": "JAT-AL00",
                "id": "HONORJAT-AL00"
            },
            {
                "model": "PBCM10",
                "id": "QKQ1.191224.003"
            },
            {
                "model": "BMH-AN10",
                "id": "HUAWEIBMH-AN10"
            },
            {
                "model": "INE-AL00",
                "id": "HUAWEIINE-AL00"
            },
            {
                "model": "OPPO R11",
                "id": "OPM1.171019.011"
            },
            {
                "model": "KKG-AN00",
                "id": "HONORKKG-AN00"
            },
            {
                "model": "V2031A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "DUB-TL00",
                "id": "HUAWEIDUB-TL00"
            },
            {
                "model": "PCKM80",
                "id": "QP1A.190711.020"
            },
            {
                "model": "PPA-AL20",
                "id": "HUAWEIPPA-AL40"
            },
            {
                "model": "PFGM00",
                "id": "SP1A.210812.016"
            },
            {
                "model": "NAM-AL00",
                "id": "HUAWEINAM-AL00"
            },
            {
                "model": "RMX2173",
                "id": "RP1A.200720.011"
            },
            {
                "model": "MED-AL00",
                "id": "HUAWEIMED-AL00"
            },
            {
                "model": "V1818CA",
                "id": "O11019"
            },
            {
                "model": "JLH-AN00",
                "id": "HONORJLH-AN00"
            },
            {
                "model": "V1921A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "EBG-AN10",
                "id": "HUAWEIEBG-AN10"
            },
            {
                "model": "JSN-AL00",
                "id": "HONORJSN-AL00"
            },
            {
                "model": "vivo X21A",
                "id": "PKQ1.180819.001"
            },
            {
                "model": "VOG-AL10",
                "id": "HUAWEIVOG-AL10"
            },
            {
                "model": "V1824A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "PBFM00",
                "id": "OPM1.171019.026"
            },
            {
                "model": "GIA-AN00",
                "id": "HONORGIA-AN00"
            },
            {
                "model": "ART-AL00x",
                "id": "HUAWEIART-AL00x"
            },
            {
                "model": "NTN-AN20",
                "id": "HONORNTN-AN30"
            },
            {
                "model": "V2080A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "PBAM00",
                "id": "OPM1.171019.026"
            },
            {
                "model": "CLT-AL01",
                "id": "HUAWEICLT-AL01"
            },
            {
                "model": "PDSM00",
                "id": "SP1A.210812.016"
            },
            {
                "model": "MRR-W29",
                "id": "HUAWEIMRR-W29"
            },
            {
                "model": "V1965A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "BRQ-AN00",
                "id": "HUAWEIBRQ-AN00"
            },
            {
                "model": "JAD-AL00",
                "id": "HUAWEIJAD-AL00"
            },
            {
                "model": "V1963A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "BLA-AL00",
                "id": "HUAWEIBLA-AL00"
            },
            {
                "model": "CMA-AN00",
                "id": "HONORCMA-AN00"
            },
            {
                "model": "PFUM10",
                "id": "RKQ1.211119.001"
            },
            {
                "model": "D1s",
                "id": "NHG47K"
            },
            {
                "model": "D2_d",
                "id": "NHG47K"
            },
            {
                "model": "RMX2200",
                "id": "QP1A.190711.020"
            },
            {
                "model": "OPPO R11t",
                "id": "OPM1.171019.011"
            },
            {
                "model": "PRA-AL00X",
                "id": "HONORPRA-AL00X"
            },
            {
                "model": "POT-AL00a",
                "id": "HUAWEIPOT-AL00a"
            },
            {
                "model": "JER-AN20",
                "id": "HUAWEIJER-AN20"
            },
            {
                "model": "PCAM00",
                "id": "RKQ1.201217.002"
            },
            {
                "model": "PCPM00",
                "id": "QP1A.190711.020"
            },
            {
                "model": "AKA-AL10",
                "id": "HONORAKA-AL10"
            },
            {
                "model": "V2131A",
                "id": "SP1A.210812.003"
            },
            {
                "model": "ALA-AN70",
                "id": "HONORALA-AN70"
            },
            {
                "model": "V1936A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "IN2010",
                "id": "RP1A.201005.001"
            },
            {
                "model": "SM-G988N",
                "id": "SP1A.210812.016"
            },
            {
                "model": "Hera-BD00",
                "id": "HinovaHera-BD00"
            },
            {
                "model": "TNY-AL00",
                "id": "HUAWEITNY-AL00"
            },
            {
                "model": "NOP-AN00",
                "id": "HUAWEINOP-AN01P"
            },
            {
                "model": "MT2110",
                "id": "RKQ1.211119.001"
            },
            {
                "model": "VP002",
                "id": "LiantongVP002"
            },
            {
                "model": "PEAM00",
                "id": "RP1A.200720.011"
            },
            {
                "model": "PEXM00",
                "id": "RKQ1.211103.002"
            },
            {
                "model": "PCHM10",
                "id": "RKQ1.200903.002"
            },
            {
                "model": "V1813A",
                "id": "P00610"
            },
            {
                "model": "PEDM00",
                "id": "RKQ1.211103.002"
            },
            {
                "model": "PGCM10",
                "id": "SP1A.210812.016"
            },
            {
                "model": "JAD-AL50",
                "id": "HUAWEIJAD-AL50"
            },
            {
                "model": "LYA-AL10",
                "id": "HUAWEILYA-AL10"
            },
            {
                "model": "V2156A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "OXF-AN10",
                "id": "HUAWEIOXF-AN10"
            },
            {
                "model": "OPPO A77",
                "id": "NMF26F"
            },
            {
                "model": "FLA-AL20",
                "id": "HUAWEIFLA-AL20"
            },
            {
                "model": "PDBM00",
                "id": "PPR1.180610.011"
            },
            {
                "model": "YAL-AL00",
                "id": "HUAWEIYAL-AL00"
            },
            {
                "model": "V2012A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "PDCM00",
                "id": "RP1A.200720.011"
            },
            {
                "model": "LE2100",
                "id": "RKQ1.201105.002"
            },
            {
                "model": "PCRT01",
                "id": "RKQ1.200903.002"
            },
            {
                "model": "V1936AL",
                "id": "QP1A.190711.020"
            },
            {
                "model": "vivo NEX S",
                "id": "QP1A.190711.020"
            },
            {
                "model": "V2183A",
                "id": "SP1A.210812.003"
            },
            {
                "model": "JSC-AN00",
                "id": "HUAWEIJSC-AN00A"
            },
            {
                "model": "V2185A",
                "id": "SP1A.210812.003"
            },
            {
                "model": "vivo X20A",
                "id": "OPM1.171019.011"
            },
            {
                "model": "TEL-TN00",
                "id": "HONORTEL-TN00"
            },
            {
                "model": "TEL-AN00",
                "id": "HONORTEL-AN00"
            },
            {
                "model": "HRY-AL00Ta",
                "id": "HONORHRY-AL00Ta"
            },
            {
                "model": "MT-S4",
                "id": "NHG47K"
            },
            {
                "model": "NOH-AN01",
                "id": "HUAWEINOH-AN01"
            },
            {
                "model": "PEUM00",
                "id": "RKQ1.211119.001"
            },
            {
                "model": "S8080",
                "id": "212021122306"
            },
            {
                "model": "V2046A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "V2055A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "vivo Y85",
                "id": "OPM1.171019.011"
            },
            {
                "model": "V2118A",
                "id": "SP1A.210812.003"
            },
            {
                "model": "YAL-AL10",
                "id": "HUAWEIYAL-AL10"
            },
            {
                "model": "N2",
                "id": "NHG47K"
            },
            {
                "model": "GLK-AL00",
                "id": "HUAWEIGLK-AL00"
            },
            {
                "model": "BTV-DL09",
                "id": "HUAWEIBEETHOVEN-DL09"
            },
            {
                "model": "HLK-AL10",
                "id": "HONORHLK-AL10"
            },
            {
                "model": "LIO-AN00m",
                "id": "HUAWEILIO-AN00m"
            },
            {
                "model": "V1818A",
                "id": "OPM1.171019.026"
            },
            {
                "model": "V2020A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "PDAM10",
                "id": "RKQ1.200903.002"
            },
            {
                "model": "V1832A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "DUK-TL30",
                "id": "HUAWEIDUK-TL30"
            },
            {
                "model": "PCLM50",
                "id": "RKQ1.200903.002"
            },
            {
                "model": "VKY-AL00",
                "id": "HUAWEIVKY-AL00"
            },
            {
                "model": "PCGM00",
                "id": "RKQ1.201217.002"
            },
            {
                "model": "XT2153-1",
                "id": "RRAA31.Q3-19-86"
            },
            {
                "model": "vivo X9s Plus L",
                "id": "OPM1.171019.019"
            },
            {
                "model": "PEMM20",
                "id": "RP1A.200720.011"
            },
            {
                "model": "V2162A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "TYH611M",
                "id": "TianyiTYH611M"
            },
            {
                "model": "CHL-AN00",
                "id": "HONORCHL-AN00"
            },
            {
                "model": "BKL-TL10",
                "id": "HUAWEIBKL-TL10"
            },
            {
                "model": "SM-E5260",
                "id": "RP1A.200720.012"
            },
            {
                "model": "V2049A",
                "id": "SP1A.210812.003"
            },
            {
                "model": "K3",
                "id": "A05VLRCHLWZWSQUQVI"
            },
            {
                "model": "PDRM00",
                "id": "RKQ1.211103.002"
            },
            {
                "model": "BAL-AL00",
                "id": "HUAWEIBAL-AL00A"
            },
            {
                "model": "HRY-AL00a",
                "id": "HONORHRY-AL00a"
            },
            {
                "model": "PEPM00",
                "id": "SP1A.210812.016"
            },
            {
                "model": "V2130A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "JAD-AL60",
                "id": "HUAWEIJAD-AL60"
            },
            {
                "model": "HWI-AL00",
                "id": "HUAWEIHWI-AL00"
            },
            {
                "model": "NOH-AL10",
                "id": "HUAWEINOH-AL10"
            },
            {
                "model": "V1934A",
                "id": "PPR1.180610.011"
            },
            {
                "model": "ELS-AN10",
                "id": "HUAWEIELS-AN10"
            },
            {
                "model": "RTE-AL00",
                "id": "HUAWEIRNA-AL00"
            },
            {
                "model": "ABR-AL00",
                "id": "HUAWEIABR-AL00"
            },
            {
                "model": "RMX2205",
                "id": "SP1A.210812.016"
            },
            {
                "model": "LE2111",
                "id": "SKQ1.210216.001"
            },
            {
                "model": "LIO-AL00",
                "id": "HUAWEILIO-AL00"
            },
            {
                "model": "BMH-AN20",
                "id": "HUAWEIBMH-AN20"
            },
            {
                "model": "D2",
                "id": "NHG47K"
            },
            {
                "model": "PFVM10",
                "id": "RP1A.200720.011"
            },
            {
                "model": "ASK-AL00x",
                "id": "HONORASK-AL00x"
            },
            {
                "model": "RMX2202",
                "id": "SKQ1.210216.001"
            },
            {
                "model": "V2020CA",
                "id": "QP1A.190711.020"
            },
            {
                "model": "CDY-TN00",
                "id": "HUAWEICDY-TN00"
            },
            {
                "model": "LIO-AN00P",
                "id": "HUAWEILIO-AN00P"
            },
            {
                "model": "JER-AN10",
                "id": "HUAWEIJER-AN10"
            },
            {
                "model": "PBAT00",
                "id": "OPM1.171019.026"
            },
            {
                "model": "JKM-AL00b",
                "id": "HUAWEIJKM-AL00b"
            },
            {
                "model": "PAL-AL00",
                "id": "HUAWEIPAL-AL00"
            },
            {
                "model": "V2073A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "PERM10",
                "id": "RKQ1.210614.002"
            },
            {
                "model": "LLD-AL30",
                "id": "HONORLLD-AL30"
            },
            {
                "model": "HUAWEI CRR-UL00",
                "id": "HUAWEICRR-UL00"
            },
            {
                "model": "NX669J",
                "id": "SKQ1.211113.001"
            },
            {
                "model": "CDY-AN20",
                "id": "HUAWEICDY-AN20"
            },
            {
                "model": "PECT30",
                "id": "RP1A.200720.011"
            },
            {
                "model": "PEGM10",
                "id": "RKQ1.201217.002"
            },
            {
                "model": "V1813T",
                "id": "O11019"
            },
            {
                "model": "SEA-AL00",
                "id": "HUAWEISEA-AL00"
            },
            {
                "model": "16th",
                "id": "OPM1.171019.026"
            },
            {
                "model": "DVC-AN00",
                "id": "HUAWEIDVC-AN00"
            },
            {
                "model": "BAC-TL00",
                "id": "HUAWEIBAC-TL00"
            },
            {
                "model": "PDNT00",
                "id": "RKQ1.211103.002"
            },
            {
                "model": "V1986A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "JKM-TL00",
                "id": "HUAWEIJKM-TL00"
            },
            {
                "model": "CLT-AL00",
                "id": "HUAWEICLT-AL00"
            },
            {
                "model": "PEHT00",
                "id": "SKQ1.210216.001"
            },
            {
                "model": "V2072A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "TET-AN50",
                "id": "HUAWEITET-AN50"
            },
            {
                "model": "PELM00",
                "id": "SP1A.210812.016"
            },
            {
                "model": "YOK-AN10",
                "id": "HONORYOR-AN00"
            },
            {
                "model": "KOZ-AL00",
                "id": "HONORKOZ-AL00"
            },
            {
                "model": "V2024A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "V1814A",
                "id": "PKQ1.180819.001"
            },
            {
                "model": "V1922A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "MEIZU 18X",
                "id": "RKQ1.210614.002"
            },
            {
                "model": "MT-S4p",
                "id": "RQ3A.210705.001"
            },
            {
                "model": "Note9",
                "id": "PKQ1.181203.001"
            },
            {
                "model": "PCAT00",
                "id": "RKQ1.201217.002"
            },
            {
                "model": "ELS-TN00",
                "id": "HUAWEIELS-TN00"
            },
            {
                "model": "V2034A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "BKL-AL20",
                "id": "HUAWEIBKL-AL20"
            },
            {
                "model": "V1816A",
                "id": "PKQ1.180819.001"
            },
            {
                "model": "JSN-AL00a",
                "id": "HONORJSN-AL00a"
            },
            {
                "model": "PDST00",
                "id": "RP1A.200720.011"
            },
            {
                "model": "TFY-AN00",
                "id": "HONORTFY-AN00"
            },
            {
                "model": "OCE-AL50",
                "id": "HUAWEIOCE-AL50"
            },
            {
                "model": "SM-N9860",
                "id": "SP1A.210812.016"
            },
            {
                "model": "RMX2201",
                "id": "QP1A.190711.020"
            },
            {
                "model": "PDVM00",
                "id": "QKQ1.200614.002"
            },
            {
                "model": "JKM-AL00",
                "id": "HUAWEIJKM-AL00"
            },
            {
                "model": "DUB-AL00a",
                "id": "HUAWEIDUB-AL00a"
            },
            {
                "model": "RMX3560",
                "id": "SP1A.210812.016"
            },
            {
                "model": "LGE-AN00",
                "id": "HONORLGE-AN00"
            },
            {
                "model": "OPPO R11s",
                "id": "OPM1.171019.011"
            },
            {
                "model": "PAAM00",
                "id": "QKQ1.191224.003"
            },
            {
                "model": "HJC-AN90",
                "id": "HONORHJC-AN90"
            },
            {
                "model": "PDPM00",
                "id": "RKQ1.211103.002"
            },
            {
                "model": "RMX3031",
                "id": "RP1A.200720.011"
            },
            {
                "model": "V1945A",
                "id": "PKQ1.190626.001"
            },
            {
                "model": "HD3201_P8X",
                "id": "LMY48Y"
            },
            {
                "model": "Hebe-BD00",
                "id": "HinovaHebe-BD00"
            },
            {
                "model": "PDKM00",
                "id": "RP1A.200720.011"
            },
            {
                "model": "SP300",
                "id": "CMDCSP300"
            },
            {
                "model": "COR-AL10",
                "id": "HUAWEICOR-AL10"
            },
            {
                "model": "PBBM00",
                "id": "PPR1.180610.011"
            },
            {
                "model": "ZTE A2020 Pro",
                "id": "PKQ1.190616.001"
            },
            {
                "model": "AQM-AL00",
                "id": "HUAWEIAQM-AL00"
            },
            {
                "model": "PCDM10",
                "id": "RP1A.200720.011"
            },
            {
                "model": "PDEM10",
                "id": "RKQ1.211103.002"
            },
            {
                "model": "V1932A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "V1938CT",
                "id": "QP1A.190711.020"
            },
            {
                "model": "DUK-AL20",
                "id": "HUAWEIDUK-AL20"
            },
            {
                "model": "SM-G9750",
                "id": "RP1A.200720.012"
            },
            {
                "model": "HRY-AL00T",
                "id": "HONORHRY-AL00T"
            },
            {
                "model": "ARS-AL00",
                "id": "HUAWEIARS-AL00"
            },
            {
                "model": "V1938T",
                "id": "QP1A.190711.020"
            },
            {
                "model": "ANE-AL00",
                "id": "HUAWEIANE-AL00"
            },
            {
                "model": "AQM-AL10",
                "id": "HONORAQM-AL10"
            },
            {
                "model": "WAS-AL00",
                "id": "HUAWEIWAS-AL00"
            },
            {
                "model": "SM-S9080",
                "id": "SP1A.210812.016"
            },
            {
                "model": "WLZ-AN00",
                "id": "HUAWEIWLZ-AN00"
            },
            {
                "model": "SNE-AL00",
                "id": "HUAWEISNE-AL00"
            },
            {
                "model": "PERM00",
                "id": "RP1A.200720.011"
            },
            {
                "model": "PCAT10",
                "id": "RP1A.200720.011"
            },
            {
                "model": "V2157A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "LE2110",
                "id": "RKQ1.211103.002"
            },
            {
                "model": "V1981A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "DBY-W09",
                "id": "HUAWEIDBY-W09"
            },
            {
                "model": "ALP-AL00",
                "id": "HUAWEIALP-AL00"
            },
            {
                "model": "V2031EA",
                "id": "QP1A.190711.020"
            },
            {
                "model": "V2123A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "V2002A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "CDY-AN95",
                "id": "HUAWEICDY-AN95"
            },
            {
                "model": "V1829A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "16T",
                "id": "PKQ1.190616.001"
            },
            {
                "model": "V1821A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "PEAT00",
                "id": "RP1A.200720.011"
            },
            {
                "model": "BND-AL00",
                "id": "HONORBND-AL00"
            },
            {
                "model": "vivo Y67A",
                "id": "MRA58K"
            },
            {
                "model": "OPPO R11 Plus",
                "id": "OPM1.171019.011"
            },
            {
                "model": "V2148A",
                "id": "SP1A.210812.003"
            },
            {
                "model": "PDYT20",
                "id": "RP1A.200720.011"
            },
            {
                "model": "RMX3122",
                "id": "RP1A.200720.011"
            },
            {
                "model": "MOA-AL20",
                "id": "HONORMOA-AL20"
            },
            {
                "model": "PBET00",
                "id": "QKQ1.190918.001"
            },
            {
                "model": "JEF-TN00",
                "id": "HUAWEIJEF-TN00"
            },
            {
                "model": "GN8003",
                "id": "MRA58K"
            },
            {
                "model": "HUAWEI MLA-AL10",
                "id": "HUAWEIMLA-AL10"
            },
            {
                "model": "TAH-AN00m",
                "id": "HUAWEITAH-AN00m"
            },
            {
                "model": "PBBT00",
                "id": "PPR1.180610.011"
            },
            {
                "model": "RMX1971",
                "id": "RKQ1.201217.002"
            },
            {
                "model": "L1531_d",
                "id": "NMF26F"
            },
            {
                "model": "S12",
                "id": "KOT49H"
            },
            {
                "model": "V2203A",
                "id": "SP1A.210812.003"
            },
            {
                "model": "MT-S1p",
                "id": "RQ2A.210505.003"
            },
            {
                "model": "ART-AL00m",
                "id": "HUAWEIART-AL00m"
            },
            {
                "model": "V1836A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "CDY-TN20",
                "id": "HUAWEICDY-TN20"
            },
            {
                "model": "MRD-AL00",
                "id": "HUAWEIMRD-AL00"
            },
            {
                "model": "SHARK KLE-A0",
                "id": "KLEN2202130CN00MR4"
            },
            {
                "model": "V2133A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "vivo Z1i",
                "id": "PKQ1.180819.001"
            },
            {
                "model": "meizu 17 Pro",
                "id": "QKQ1.200127.002"
            },
            {
                "model": "FRD-AL00",
                "id": "HUAWEIFRD-AL00"
            },
            {
                "model": "HRY-AL00",
                "id": "HONORHRY-AL00"
            },
            {
                "model": "V2061A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "V1911A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "MHA-AL00",
                "id": "HUAWEIMHA-AL00"
            },
            {
                "model": "TEL-AN10",
                "id": "HONORTEL-AN10"
            },
            {
                "model": "DUB-AL00",
                "id": "HUAWEIDUB-AL00"
            },
            {
                "model": "SM-G9860",
                "id": "RP1A.200720.012"
            },
            {
                "model": "HUAWEI CAZ-AL10",
                "id": "HUAWEICAZ-AL10"
            },
            {
                "model": "ELZ-AN20",
                "id": "HONORELZ-AN20"
            },
            {
                "model": "16s",
                "id": "PKQ1.190202.001"
            },
            {
                "model": "KOZ-AL40",
                "id": "HONORKOZ-AL40"
            },
            {
                "model": "RMX3357",
                "id": "SP1A.210812.016"
            },
            {
                "model": "HX1500",
                "id": "NHG47K"
            },
            {
                "model": "vivo NEX A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "NOH-AN50",
                "id": "HUAWEINOH-AN50"
            },
            {
                "model": "V2171A",
                "id": "SP1A.210812.003"
            },
            {
                "model": "GM1910",
                "id": "RKQ1.201022.002"
            },
            {
                "model": "vivo X7",
                "id": "LMY47V"
            },
            {
                "model": "vivo Xplay5A",
                "id": "LMY47V"
            },
            {
                "model": "V1923A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "CDY-NX9B",
                "id": "HUAWEICDY-N29B"
            },
            {
                "model": "PBBM30",
                "id": "OPM1.171019.026"
            },
            {
                "model": "PCRM00",
                "id": "RKQ1.200903.002"
            },
            {
                "model": "PGBM10",
                "id": "SP1A.210812.016"
            },
            {
                "model": "V2047A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "ONEPLUS A5010",
                "id": "PKQ1.180716.001"
            },
            {
                "model": "SHARK PRS-A0",
                "id": "PROS2203050CN00MR2"
            },
            {
                "model": "POT-AL00",
                "id": "HUAWEIPOT-AL00"
            },
            {
                "model": "PCEM00",
                "id": "RP1A.200720.011"
            },
            {
                "model": "FIG-AL10",
                "id": "HUAWEIFIG-AL10"
            },
            {
                "model": "V1732A",
                "id": "O11019"
            },
            {
                "model": "V1914A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "V1990A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "FLA-AL10",
                "id": "HUAWEIFLA-AL10"
            },
            {
                "model": "RMX2121",
                "id": "SP1A.210812.016"
            },
            {
                "model": "16s Pro",
                "id": "QKQ1.191222.002"
            },
            {
                "model": "RMX3142",
                "id": "RKQ1.201217.002"
            },
            {
                "model": "V2111A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "IN2020",
                "id": "RP1A.201005.001"
            },
            {
                "model": "RMX3361",
                "id": "RKQ1.210408.001"
            },
            {
                "model": "NX659J",
                "id": "RKQ1.200826.002"
            },
            {
                "model": "LYA-AL00P",
                "id": "HUAWEILYA-AL00P"
            },
            {
                "model": "SM-W2022",
                "id": "SP1A.210812.016"
            },
            {
                "model": "SM-A7160",
                "id": "QP1A.190711.020"
            },
            {
                "model": "NX679J",
                "id": "SKQ1.211019.001"
            },
            {
                "model": "D1s_d",
                "id": "NHG47K"
            },
            {
                "model": "V2011A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "XQ-BC72",
                "id": "61.1.A.9.83"
            },
            {
                "model": "WAS-TL10",
                "id": "HUAWEIWAS-TL10"
            },
            {
                "model": "MXW-AN00",
                "id": "HONORMXW-AN00"
            },
            {
                "model": "MT-A3Sp",
                "id": "RQ2A.210505.003"
            },
            {
                "model": "TYH622M",
                "id": "TianyiTYH622M"
            },
            {
                "model": "RMX1991",
                "id": "RKQ1.201112.002"
            },
            {
                "model": "DLI-AL10",
                "id": "HONORDLI-AL10"
            },
            {
                "model": "DVC-TN20",
                "id": "HUAWEIDVC-TN20"
            },
            {
                "model": "V2023A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "LIO-TL00",
                "id": "HUAWEILIO-TL00"
            },
            {
                "model": "PLK-TL01H",
                "id": "HONORPLK-TL01H"
            },
            {
                "model": "SM-G9600",
                "id": "QP1A.190711.020"
            },
            {
                "model": "PEMM00",
                "id": "SP1A.210812.016"
            },
            {
                "model": "PDPT00",
                "id": "RKQ1.211103.002"
            },
            {
                "model": "HMA-TL00",
                "id": "HUAWEIHMA-TL00"
            },
            {
                "model": "vivo Y66i",
                "id": "N2G47H"
            },
            {
                "model": "TET-AN00",
                "id": "HUAWEITET-AN00"
            },
            {
                "model": "16th Plus",
                "id": "OPM1.171019.026"
            },
            {
                "model": "RMX3310",
                "id": "RKQ1.211103.002"
            },
            {
                "model": "SM-N9760",
                "id": "RP1A.200720.012"
            },
            {
                "model": "RMX3092",
                "id": "RP1A.200720.011"
            },
            {
                "model": "V1809T",
                "id": "PKQ1.181030.001"
            },
            {
                "model": "RMX1901",
                "id": "RKQ1.201217.002"
            },
            {
                "model": "NX606J",
                "id": "OPM1.171019.026"
            },
            {
                "model": "SM-G9810",
                "id": "RP1A.200720.012"
            },
            {
                "model": "SM-A9080",
                "id": "SP1A.210812.016"
            },
            {
                "model": "V2163A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "Lenovo TB-X705M",
                "id": "OPM1.171019.019"
            },
            {
                "model": "EBG-TN00",
                "id": "HUAWEIEBG-TN00"
            },
            {
                "model": "vivo X9",
                "id": "N2G47H"
            },
            {
                "model": "HJC-LX9",
                "id": "HONORHJC-L29"
            },
            {
                "model": "V1829T",
                "id": "QP1A.190711.020"
            },
            {
                "model": "V1916A",
                "id": "PKQ1.190714.001"
            },
            {
                "model": "Le X620",
                "id": "HEXCNFN5902812161S"
            },
            {
                "model": "RVL-AL09",
                "id": "HUAWEIRVL-AL09"
            },
            {
                "model": "PDYM10",
                "id": "QP1A.190711.020"
            },
            {
                "model": "PDKT00",
                "id": "RP1A.200720.011"
            },
            {
                "model": "SM-G977B",
                "id": "QP1A.190711.020"
            },
            {
                "model": "70 Series",
                "id": "QP1A.190711.020"
            },
            {
                "model": "STF-AL00",
                "id": "HUAWEISTF-AL00"
            },
            {
                "model": "MED-AL20",
                "id": "HUAWEIMED-AL20"
            },
            {
                "model": "KKG-AN70",
                "id": "HONORKKG-AN70"
            },
            {
                "model": "SM-G998U",
                "id": "RP1A.200720.012"
            },
            {
                "model": "ATU-AL10",
                "id": "HUAWEIATU-AL10"
            },
            {
                "model": "vivo Y85A",
                "id": "OPM1.171019.011"
            },
            {
                "model": "NX709J",
                "id": "SKQ1.211019.001"
            },
            {
                "model": "V2059A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "APOS A8",
                "id": "LMY47V"
            },
            {
                "model": "STF-AL10",
                "id": "HUAWEISTF-AL10"
            },
            {
                "model": "V2056A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "T2",
                "id": "NMF26F"
            },
            {
                "model": "SM-G9900",
                "id": "SP1A.210812.016"
            },
            {
                "model": "MT-S4S",
                "id": "N2G47H"
            },
            {
                "model": "V2145A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "V1955A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "PDHM00",
                "id": "RKQ1.211103.002"
            },
            {
                "model": "OPPO R7sm",
                "id": "LMY47V"
            },
            {
                "model": "PCCM00",
                "id": "RKQ1.200928.002"
            },
            {
                "model": "vivo Y83A",
                "id": "O11019"
            },
            {
                "model": "vivo Y66i A",
                "id": "N2G47H"
            },
            {
                "model": "PCNM00",
                "id": "RKQ1.200903.002"
            },
            {
                "model": "OPPO A77t",
                "id": "NMF26F"
            },
            {
                "model": "V1928A",
                "id": "PKQ1.190626.001"
            },
            {
                "model": "TRT-TL10",
                "id": "HUAWEITRT-TL10"
            },
            {
                "model": "V2134A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "V1818CT",
                "id": "O11019"
            },
            {
                "model": "vivo Y71",
                "id": "OPM1.171019.011"
            },
            {
                "model": "BAC-AL00",
                "id": "HUAWEIBAC-AL00"
            },
            {
                "model": "SCM-W09",
                "id": "HUAWEISCM-W09"
            },
            {
                "model": "PEYM00",
                "id": "RP1A.200720.011"
            },
            {
                "model": "PEMT00",
                "id": "SP1A.210812.016"
            },
            {
                "model": "SM-A5160",
                "id": "QP1A.190711.020"
            },
            {
                "model": "LND-AL40",
                "id": "HONORLND-AL40"
            },
            {
                "model": "NEO-AL00",
                "id": "HUAWEINEO-AL00"
            },
            {
                "model": "RMX3161",
                "id": "RKQ1.201217.002"
            },
            {
                "model": "MEIZU 18",
                "id": "RKQ1.210715.001"
            },
            {
                "model": "vivo X7Plus",
                "id": "LMY47V"
            },
            {
                "model": "LGE-AN10",
                "id": "HONORLGE-AN10"
            },
            {
                "model": "V1838T",
                "id": "QP1A.190711.020"
            },
            {
                "model": "EVR-AL00",
                "id": "HUAWEIEVR-AL00"
            },
            {
                "model": "D310C",
                "id": "P31C.202110081529"
            },
            {
                "model": "OXP-AN00",
                "id": "HUAWEIOXF-AN00L"
            },
            {
                "model": "LND-AL30",
                "id": "HONORLND-AL30"
            },
            {
                "model": "SKW-A0",
                "id": "SKYW2103030CN00MQ5"
            },
            {
                "model": "V1831T",
                "id": "QP1A.190711.020"
            },
            {
                "model": "vivo X21UD",
                "id": "PKQ1.180819.001"
            },
            {
                "model": "ASUS_I001DB",
                "id": "RKQ1.200710.002"
            },
            {
                "model": "RMX3370",
                "id": "RKQ1.201105.002"
            },
            {
                "model": "VP005",
                "id": "UNICOMVSENSVP005"
            },
            {
                "model": "ONEPLUS A6000",
                "id": "RKQ1.201217.002"
            },
            {
                "model": "PENM00",
                "id": "RKQ1.201105.002"
            },
            {
                "model": "V2196A",
                "id": "SP1A.210812.003"
            },
            {
                "model": "V2025A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "8848 M4",
                "id": "N2G47H"
            },
            {
                "model": "V1901T",
                "id": "P00610"
            },
            {
                "model": "V2199A",
                "id": "SP1A.210812.003"
            },
            {
                "model": "DT2002C",
                "id": "RKQ1.201217.002"
            },
            {
                "model": "WKG-AN00",
                "id": "HUAWEIWKG-AN00"
            },
            {
                "model": "201906",
                "id": "O11019"
            },
            {
                "model": "JKM-AL00a",
                "id": "HUAWEIJKM-AL00a"
            },
            {
                "model": "PECM30",
                "id": "RP1A.200720.011"
            },
            {
                "model": "LDN-AL00",
                "id": "HUAWEILDN-AL00"
            },
            {
                "model": "PDEM30",
                "id": "RKQ1.211103.002"
            },
            {
                "model": "MP1602",
                "id": "NMF26O"
            },
            {
                "model": "TYH612M",
                "id": "TianyiTYH612M"
            },
            {
                "model": "VP001",
                "id": "LiantongVP001"
            },
            {
                "model": "STK-TL00",
                "id": "HUAWEISTK-TL00"
            },
            {
                "model": "PEMT20",
                "id": "SP1A.210812.016"
            },
            {
                "model": "DP780",
                "id": "LMY49F"
            },
            {
                "model": "ARE-AL00",
                "id": "HONORARE-AL00"
            },
            {
                "model": "V2115A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "V2132A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "SKR-A0",
                "id": "G66X2108250CN00MQ7"
            },
            {
                "model": "V2172A",
                "id": "SP1A.210812.003"
            },
            {
                "model": "PBCM30",
                "id": "QKQ1.191224.003"
            },
            {
                "model": "SM-G9980",
                "id": "SP1A.210812.016"
            },
            {
                "model": "vivo X20Plus A",
                "id": "OPM1.171019.011"
            },
            {
                "model": "TCL 750",
                "id": "MRA58K"
            },
            {
                "model": "V2166A",
                "id": "SP1A.210812.003_NONFC"
            },
            {
                "model": "D1",
                "id": "MMB29M"
            },
            {
                "model": "ANA-NX9",
                "id": "HUAWEIANA-N29"
            },
            {
                "model": "Galaxy S10e",
                "id": "9IRP0FO4I0YV48D9LL"
            },
            {
                "model": "MLD-AL00",
                "id": "HUAWEIMLD-AL00"
            },
            {
                "model": "PECM20",
                "id": "RP1A.200720.011"
            },
            {
                "model": "PFFM10",
                "id": "RKQ1.211103.002"
            },
            {
                "model": "OPPO A79",
                "id": "N6F26Q"
            },
            {
                "model": "V2190A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "V2170A",
                "id": "SP1A.210812.003"
            },
            {
                "model": "OPPO A83",
                "id": "N6F26Q"
            },
            {
                "model": "V2045A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "dpos",
                "id": "KOT49H"
            },
            {
                "model": "ABR-AL60",
                "id": "HUAWEIABR-AL60"
            },
            {
                "model": "FNE-AN00",
                "id": "HONORFNE-AN00"
            },
            {
                "model": "SP100",
                "id": "CMDCSP100"
            },
            {
                "model": "OPPO R9s Plus",
                "id": "MMB29M"
            },
            {
                "model": "Lenovo TB-8705N",
                "id": "QP1A.190711.020"
            },
            {
                "model": "MOA-AL00",
                "id": "HONORMOA-AL00"
            },
            {
                "model": "t1host",
                "id": "MMB29M"
            },
            {
                "model": "AECR C9",
                "id": "N2G47H"
            },
            {
                "model": "SM-G9550",
                "id": "PPR1.180610.011"
            },
            {
                "model": "V2065A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "PGAM10",
                "id": "SKQ1.220303.001"
            },
            {
                "model": "EML-TL00",
                "id": "HUAWEIEML-TL00"
            },
            {
                "model": "V1924A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "SHARK PAR-A0",
                "id": "PTRT2202162CN00MP0"
            },
            {
                "model": "X3V",
                "id": "LMY47I"
            },
            {
                "model": "V1913T",
                "id": "P00610"
            },
            {
                "model": "MP1801",
                "id": "PKQ1.181016.001"
            },
            {
                "model": "vivo Y66",
                "id": "MMB29M"
            },
            {
                "model": "ANA-TN00",
                "id": "HUAWEIANA-TN00"
            },
            {
                "model": "vivo Y71A",
                "id": "OPM1.171019.011"
            },
            {
                "model": "LYA-TL00",
                "id": "HUAWEILYA-TL00L"
            },
            {
                "model": "SM-G6200",
                "id": "OPM1.171019.026"
            },
            {
                "model": "F810",
                "id": "JRDF810"
            },
            {
                "model": "V2141A",
                "id": "SP1A.210812.003"
            },
            {
                "model": "RNE-AL00",
                "id": "HUAWEIRNE-AL00"
            },
            {
                "model": "SM-N9700",
                "id": "QP1A.190711.020"
            },
            {
                "model": "OPPO R9st",
                "id": "MMB29M"
            },
            {
                "model": "V1930A",
                "id": "PKQ1.190616.001"
            },
            {
                "model": "MGI-AN00",
                "id": "HONORMGI-AN00"
            },
            {
                "model": "V1832T",
                "id": "QP1A.190711.020"
            },
            {
                "model": "FRL-TN00",
                "id": "HUAWEIFRL-TN00"
            },
            {
                "model": "HUAWEI NXT-AL10",
                "id": "HUAWEINXT-AL10"
            },
            {
                "model": "vivo X20Plus",
                "id": "OPM1.171019.011"
            },
            {
                "model": "CND-AN00",
                "id": "HUAWEICND-AN00"
            },
            {
                "model": "V1824BA",
                "id": "RP1A.200720.012"
            },
            {
                "model": "OPPO A73t",
                "id": "N6F26Q"
            },
            {
                "model": "SM-G9650",
                "id": "R16NW"
            },
            {
                "model": "CHL-AL00",
                "id": "HONORCHL-AL00"
            },
            {
                "model": "vivo X9Plus",
                "id": "N2G47H"
            },
            {
                "model": "NX667J",
                "id": "RKQ1.210503.001"
            },
            {
                "model": "MNT-BD00",
                "id": "PTACMNT-BD00"
            },
            {
                "model": "PCT-TL10",
                "id": "HUAWEIPCT-TL10"
            },
            {
                "model": "LP129B",
                "id": "LMY47D"
            },
            {
                "model": "BND-AL10",
                "id": "HONORBND-AL10"
            },
            {
                "model": "SM-G991B",
                "id": "RP1A.200720.012"
            },
            {
                "model": "PADM00",
                "id": "QP1A.190711.020"
            },
            {
                "model": "NZA-AL00",
                "id": "HONORNZA-AL00"
            },
            {
                "model": "PEFM00",
                "id": "QP1A.190711.020"
            },
            {
                "model": "vivo X20",
                "id": "OPM1.171019.011"
            },
            {
                "model": "TNY-TL00",
                "id": "HUAWEITNY-TL00"
            },
            {
                "model": "vivo X9L",
                "id": "N2G47H"
            },
            {
                "model": "VP003",
                "id": "LiantongVP003"
            },
            {
                "model": "Jelly2",
                "id": "RP1A.200720.011"
            },
            {
                "model": "Meizu S6",
                "id": "NRD90M"
            },
            {
                "model": "SM-G9730",
                "id": "RP1A.200720.012"
            },
            {
                "model": "vivo X21i A",
                "id": "P00610"
            },
            {
                "model": "KRJ-AN00",
                "id": "HUAWEIKRJ-AN00"
            },
            {
                "model": "TDT-MA01",
                "id": "TDTECHTDT-MA01"
            },
            {
                "model": "OPPO A79t",
                "id": "N6F26Q"
            },
            {
                "model": "PCLM10",
                "id": "RKQ1.200928.002"
            },
            {
                "model": "SM-G9738",
                "id": "SP1A.210812.016"
            },
            {
                "model": "LGM-V300K",
                "id": "PKQ1.190414.001"
            },
            {
                "model": "PAFM00",
                "id": "QKQ1.191008.001"
            },
            {
                "model": "M1852",
                "id": "OPM1.171019.026"
            },
            {
                "model": "XT2201-2",
                "id": "S1SC32.52-27-2"
            },
            {
                "model": "OPPO R9",
                "id": "KTU84P"
            },
            {
                "model": "PGJM10",
                "id": "SP1A.210812.016"
            },
            {
                "model": "PFCM00",
                "id": "RP1A.200720.011"
            },
            {
                "model": "RMX2111",
                "id": "RP1A.200720.011"
            },
            {
                "model": "vivo Y75A",
                "id": "N6F26Q"
            },
            {
                "model": "OPPO R11 Pluskt",
                "id": "OPM1.171019.011"
            },
            {
                "model": "ZTE 9040N",
                "id": "RP1A.200720.011"
            },
            {
                "model": "畅享 7 Plus",
                "id": "HonorCHM-TL00"
            },
            {
                "model": "PEGT10",
                "id": "RKQ1.201217.002"
            },
            {
                "model": "红辣椒9X",
                "id": "1F175TVPWP2XRPN6ZN"
            },
            {
                "model": "Pixel 2",
                "id": "QP1A.190711.019"
            },
            {
                "model": "LP119",
                "id": "NHG47K"
            },
            {
                "model": "PCET00",
                "id": "RP1A.200720.011"
            },
            {
                "model": "SM-F7110",
                "id": "SP1A.210812.016"
            },
            {
                "model": "Y81s",
                "id": "LMY47I"
            },
            {
                "model": "BLN-TL10",
                "id": "HONORBLN-TL10"
            },
            {
                "model": "RMX3300",
                "id": "SKQ1.211019.001"
            },
            {
                "model": "ZTE 7530N",
                "id": "RP1A.200720.011"
            },
            {
                "model": "V2066A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "JLN-AL00",
                "id": "HUAWEIJLN-AL00"
            },
            {
                "model": "BKK-AL10",
                "id": "HONORBKK-AL10"
            },
            {
                "model": "20190620G",
                "id": "O11019"
            },
            {
                "model": "AGS3-AL00",
                "id": "HUAWEIAGS3-AL00"
            },
            {
                "model": "RMX3041",
                "id": "RP1A.200720.011"
            },
            {
                "model": "nova 2",
                "id": "HUAWEITAG-AL00"
            },
            {
                "model": "DUB-AL20",
                "id": "HUAWEIDUB-AL20"
            },
            {
                "model": "vivo Y75s",
                "id": "OPM1.171019.026"
            },
            {
                "model": "SM-S9010",
                "id": "SP1A.210812.016"
            },
            {
                "model": "ONEPLUS A6010",
                "id": "QKQ1.190716.003"
            },
            {
                "model": "DT1901A",
                "id": "QKQ1.191222.002"
            },
            {
                "model": "V2",
                "id": "N6F26Q"
            },
            {
                "model": "SHARK KTUS-A0",
                "id": "KTUS2205250CN00MP3"
            },
            {
                "model": "VNE-AN00",
                "id": "HONORVNE-AN00"
            },
            {
                "model": "OPPO R9sk",
                "id": "MMB29M"
            },
            {
                "model": "OPPO R11 Plusk",
                "id": "OPM1.171019.011"
            },
            {
                "model": "PBCT10",
                "id": "QKQ1.191224.003"
            },
            {
                "model": "RMX3125",
                "id": "RP1A.200720.011"
            },
            {
                "model": "EVA-AL10",
                "id": "HUAWEIEVA-AL10"
            },
            {
                "model": "Lenovo L58091",
                "id": "OPM1.171019.026"
            },
            {
                "model": "V1818T",
                "id": "OPM1.171019.026"
            },
            {
                "model": "X23",
                "id": "OO6QP5O5C9JVHHLIA9"
            },
            {
                "model": "SM-G9960",
                "id": "SP1A.210812.016"
            },
            {
                "model": "vivo Y83",
                "id": "O11019"
            },
            {
                "model": "NE2210",
                "id": "SKQ1.211019.001"
            },
            {
                "model": "BRQ-AL00",
                "id": "HUAWEIBRQ-AL00"
            },
            {
                "model": "VTR-AL00",
                "id": "HUAWEIVTR-AL00"
            },
            {
                "model": "V2066BA",
                "id": "RP1A.200720.012"
            },
            {
                "model": "RMX3461",
                "id": "RKQ1.210503.001"
            },
            {
                "model": "WKG-TN00",
                "id": "HUAWEIWKG-TN00"
            },
            {
                "model": "EVR-AN00",
                "id": "HUAWEIEVR-AN00"
            },
            {
                "model": "V1950A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "vivo Y67",
                "id": "MRA58K"
            },
            {
                "model": "HD1900",
                "id": "RKQ1.201022.002"
            },
            {
                "model": "A602",
                "id": "LMY47O"
            },
            {
                "model": "RMX2117",
                "id": "RP1A.200720.011"
            },
            {
                "model": "VIE-AL10",
                "id": "HUAWEIVIE-AL10"
            },
            {
                "model": "Z6 5G",
                "id": "BJOV50KDNSSWBCOAGQ"
            },
            {
                "model": "SM-N9600",
                "id": "QP1A.190711.020"
            },
            {
                "model": "Lenovo L38111",
                "id": "QKQ1.191014.001"
            },
            {
                "model": "SM-S9060",
                "id": "SP1A.210812.016"
            },
            {
                "model": "GLK-TL00",
                "id": "HUAWEIGLK-TL00"
            },
            {
                "model": "SM-A3050",
                "id": "QP1A.190711.020"
            },
            {
                "model": "SM-A5260",
                "id": "SP1A.210812.016"
            },
            {
                "model": "XT2137-2",
                "id": "RRO31.Q2-12-20"
            },
            {
                "model": "Lenovo TB-X606F",
                "id": "QP1A.190711.020"
            },
            {
                "model": "V2158A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "BLN-AL10",
                "id": "HONORBLN-AL10"
            },
            {
                "model": "PFEM10",
                "id": "SKQ1.211019.001"
            },
            {
                "model": "SM-A9200",
                "id": "QP1A.190711.020"
            },
            {
                "model": "CDY-TN90",
                "id": "HUAWEICDY-TN90"
            },
            {
                "model": "OPPO R11st",
                "id": "PKQ1.190414.001"
            },
            {
                "model": "PAHM00",
                "id": "QKQ1.191008.001"
            },
            {
                "model": "LM-G850",
                "id": "QKQ1.200216.002"
            },
            {
                "model": "Y5s",
                "id": "ZOQ28UBF8L893HRYD2"
            },
            {
                "model": "红米Note 10 Pro 5G",
                "id": "6BVZDU9W3829MMFLZ7"
            },
            {
                "model": "BND-TL10",
                "id": "HONORBND-TL10"
            },
            {
                "model": "16 X",
                "id": "OPM1.171019.026"
            },
            {
                "model": "MP1718",
                "id": "OPM1.171019.026"
            },
            {
                "model": "vivo V3Max A",
                "id": "LMY47V"
            },
            {
                "model": "vivo X9i",
                "id": "N2G47H"
            },
            {
                "model": "SHARK KSR-A0",
                "id": "KASE2205120CN00MR4"
            },
            {
                "model": "V1813BA",
                "id": "PKQ1.181030.001"
            },
            {
                "model": "MED-TL00",
                "id": "HUAWEIMED-TL00"
            },
            {
                "model": "P30 Pro",
                "id": "QXHECIWTCCE6UK5XPT"
            },
            {
                "model": "OPPO A59m",
                "id": "LMY47I"
            },
            {
                "model": "V2099A",
                "id": "QP1A.190711.020"
            },
            {
                "model": "SM-A7000",
                "id": "MMB29M"
            },
            {
                "model": "HWI-TL00",
                "id": "HUAWEIHWI-TL00"
            },
            {
                "model": "SM-G975U",
                "id": "RP1A.200720.012"
            },
            {
                "model": "荣耀畅玩5",
                "id": "HUAWEIEDISON-AL10"
            },
            {
                "model": "SM-F926N",
                "id": "RP1A.200720.012"
            },
            {
                "model": "PGKM10",
                "id": "SP1A.210812.016"
            },
            {
                "model": "ELE-TL00",
                "id": "HUAWEIELE-TL00"
            },
            {
                "model": "SM-G977U",
                "id": "QP1A.190711.020"
            },
            {
                "model": "BKK-AL00",
                "id": "HONORBKK-AL00"
            },
            {
                "model": "XQ-AT72",
                "id": "58.1.A.5.530"
            },
            {
                "model": "JNY-LX1",
                "id": "HUAWEIJNY-L21"
            },
            {
                "model": "PESM10",
                "id": "RKQ1.211019.001"
            },
            {
                "model": "AGS2-W09HN",
                "id": "HUAWEIAGS2-W09HN"
            },
            {
                "model": "OPPO A73",
                "id": "N6F26Q"
            },
            {
                "model": "ELS-NX9",
                "id": "HUAWEIELS-N29"
            },
            {
                "model": "ALP-TL00",
                "id": "HUAWEIALP-TL00"
            },
            {
                "model": "MGA-AL00",
                "id": "HUAWEIMGA-AL00"
            },
            {
                "model": "JSN-TL00",
                "id": "HONORJSN-TL00"
            },
            {
                "model": "vivo Y51",
                "id": "LRX22G"
            },
            {
                "model": "OPPO R7s",
                "id": "KTU84P"
            },
            {
                "model": "V2168A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "SM-G7810",
                "id": "SP1A.210812.016"
            },
            {
                "model": "vivo Y75",
                "id": "N6F26Q"
            },
            {
                "model": "GALAXY SIII Neo",
                "id": "LMY47X"
            },
            {
                "model": "VOG-L04",
                "id": "HUAWEIVOG-L04"
            },
            {
                "model": "vivo X9s",
                "id": "OPM1.171019.019"
            },
            {
                "model": "RMX2072",
                "id": "RKQ1.200710.002"
            },
            {
                "model": "TYH211U",
                "id": "QP1A.190711.020"
            },
            {
                "model": "OPPO A57",
                "id": "MMB29M"
            },
            {
                "model": "SM-G9500",
                "id": "PPR1.180610.011"
            },
            {
                "model": "POT-AL10",
                "id": "HUAWEIPOT-AL10"
            },
            {
                "model": "RMX2176",
                "id": "RP1A.200720.011"
            },
            {
                "model": "SM-N900V",
                "id": "KTU84P"
            },
            {
                "model": "ARE-AL10",
                "id": "HONORARE-AL10"
            },
            {
                "model": "VCE-TL00",
                "id": "HUAWEIVCE-TL00"
            },
            {
                "model": "SM-W2021",
                "id": "SP1A.210812.016"
            },
            {
                "model": "V2061",
                "id": "SP1A.210812.003"
            },
            {
                "model": "Galaxy A8+",
                "id": "HTJ85B"
            },
            {
                "model": "XT2071-4",
                "id": "RCS31.Q1-34-29"
            },
            {
                "model": "TRT-AL00A",
                "id": "HUAWEITRT-AL00A"
            },
            {
                "model": "conquest-S16",
                "id": "QP1A.190711.020"
            },
            {
                "model": "HTC U12 life",
                "id": "OPM1.171019.026"
            },
            {
                "model": "SM-G973U1",
                "id": "SP1A.210812.016"
            },
            {
                "model": "RMX1931",
                "id": "RKQ1.200928.002"
            },
            {
                "model": "SM-F700F",
                "id": "SP1A.210812.016"
            },
            {
                "model": "V1816T",
                "id": "PKQ1.180819.001"
            },
            {
                "model": "LDN-AL20",
                "id": "HUAWEILDN-AL20"
            },
            {
                "model": "MP1611",
                "id": "NMF26O"
            },
            {
                "model": "MRX-AL09",
                "id": "HUAWEIMRX-AL09"
            },
            {
                "model": "M6S Plus",
                "id": "MRA58K"
            },
            {
                "model": "JER-TN20",
                "id": "HUAWEIJER-TN20"
            },
            {
                "model": "TYH601M",
                "id": "TianyiTYH601M"
            },
            {
                "model": "荣耀3C",
                "id": "HUAWEICUN-AL00"
            },
            {
                "model": "XT2125-4",
                "id": "RRN31.Q3-1-27-1"
            },
            {
                "model": "V2165A",
                "id": "SP1A.210812.003"
            },
            {
                "model": "L2K",
                "id": "N2G47H"
            },
            {
                "model": "HRY-TL00",
                "id": "HONORHRY-TL00"
            },
            {
                "model": "XQ-AS72",
                "id": "58.1.A.5.530"
            },
            {
                "model": "畅享10s",
                "id": "BER93JSUOXEIPTBY2H"
            },
            {
                "model": "ASUS_I005DA",
                "id": "SKQ1.210821.001"
            },
            {
                "model": "V2023EA",
                "id": "QP1A.190711.020"
            },
            {
                "model": "1801-A01",
                "id": "OPM1"
            },
            {
                "model": "CLT-TL00",
                "id": "HUAWEICLT-TL00"
            },
            {
                "model": "LLD-AL20",
                "id": "HONORLLD-AL20"
            },
            {
                "model": "WGR-W09",
                "id": "HUAWEIWGR-W09"
            },
            {
                "model": "XT2175-2",
                "id": "S1RXC32.50-37-2"
            },
            {
                "model": "V2178A",
                "id": "SP1A.210812.003"
            },
            {
                "model": "Note2",
                "id": "MMB29M"
            },
            {
                "model": "NEW-AN90",
                "id": "HONORNEW-AN90"
            },
            {
                "model": "L1531",
                "id": "NMF26F"
            },
            {
                "model": "CLT-L29",
                "id": "HUAWEICLT-L29"
            },
            {
                "model": "OPPO A79k",
                "id": "N6F26Q"
            },
            {
                "model": "V2135A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "MX3",
                "id": "KTU84P"
            },
            {
                "model": "SCMR-W09",
                "id": "HUAWEISCMR-W09"
            },
            {
                "model": "J9110",
                "id": "55.2.A.4.154"
            },
            {
                "model": "VRD-W09",
                "id": "HUAWEIVRD-W09"
            },
            {
                "model": "V2207A",
                "id": "SP1A.210812.003"
            },
            {
                "model": "RMX2051",
                "id": "RKQ1.201217.002"
            },
            {
                "model": "AUTOID Q7",
                "id": "V2.0.30"
            },
            {
                "model": "V2143A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "DUA-AL00",
                "id": "HONORDUA-AL00"
            },
            {
                "model": "V1836T",
                "id": "QP1A.190711.020"
            },
            {
                "model": "畅享8",
                "id": "DCXJB4XUDWGHS4I61P"
            },
            {
                "model": "MRX-W19",
                "id": "HUAWEIMRX-W19"
            },
            {
                "model": "OPPO A59s",
                "id": "LMY47I"
            },
            {
                "model": "tp2",
                "id": "KTU84Q"
            },
            {
                "model": "V2180GA",
                "id": "RP1A.200720.012"
            },
            {
                "model": "SM-N971N",
                "id": "SP1A.210812.016"
            },
            {
                "model": "SM-G9350",
                "id": "R16NW"
            },
            {
                "model": "KSA-AL10",
                "id": "HONORKSA-AL10"
            },
            {
                "model": "HUAWEI CAZ-TL10",
                "id": "HUAWEICAZ-TL10"
            },
            {
                "model": "VOG-TL00",
                "id": "HUAWEIVOG-TL00"
            },
            {
                "model": "OPPO R9 Plusm A",
                "id": "LMY47V"
            },
            {
                "model": "RMX3115",
                "id": "SP1A.210812.016"
            },
            {
                "model": "vivo X9s L",
                "id": "OPM1.171019.019"
            },
            {
                "model": "V2009A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "SM-T725C",
                "id": "PPR1.180610.011"
            },
            {
                "model": "INE-TL00",
                "id": "HUAWEIINE-TL00"
            },
            {
                "model": "TCL 580（全网通）",
                "id": "LRX22G"
            },
            {
                "model": "vivo Y79A",
                "id": "N2G47H"
            },
            {
                "model": "LM-V409N",
                "id": "QKQ1.191222.002"
            },
            {
                "model": "vivo V3",
                "id": "LMY47V"
            },
            {
                "model": "OE106",
                "id": "OPM1.171019.026"
            },
            {
                "model": "HTC M8St",
                "id": "LRX22G"
            },
            {
                "model": "OD103",
                "id": "NMF26F"
            },
            {
                "model": "SM-F9260",
                "id": "RP1A.200720.012"
            },
            {
                "model": "vivo NEX",
                "id": "QP1A.190711.020"
            },
            {
                "model": "CPH1877",
                "id": "QKQ1.190918.001"
            },
            {
                "model": "NAT-TN70",
                "id": "TDTechNAT-TN70"
            },
            {
                "model": "SM-A7100",
                "id": "MMB29M"
            },
            {
                "model": "Coolpad V1-C",
                "id": "KTU84P"
            },
            {
                "model": "H9493",
                "id": "52.0.A.8.83"
            },
            {
                "model": "T1.2",
                "id": "NRD90M"
            },
            {
                "model": "SM-N9810",
                "id": "SP1A.210812.016"
            },
            {
                "model": "SM-N9500",
                "id": "PPR1.180610.011"
            },
            {
                "model": "HPB-AN00",
                "id": "HONORHPB-AN00"
            },
            {
                "model": "ARS-TL00",
                "id": "HUAWEIARS-TL00"
            },
            {
                "model": "SM-C7010",
                "id": "R16NW"
            },
            {
                "model": "NX666J",
                "id": "RKQ1.201221.002"
            },
            {
                "model": "SM-G9880",
                "id": "RP1A.200720.012"
            },
            {
                "model": "VRD-AL10",
                "id": "HUAWEIVRD-AL10"
            },
            {
                "model": "HMA-L29",
                "id": "HUAWEIHMA-L29"
            },
            {
                "model": "SM-G977N",
                "id": "RP1A.200720.012"
            },
            {
                "model": "PAR-TL00",
                "id": "HUAWEIPAR-TL00"
            },
            {
                "model": "Qin 2 Pro",
                "id": "PPR1.180610.011"
            },
            {
                "model": "VOG-L29",
                "id": "HUAWEIVOG-L29"
            },
            {
                "model": "TNNH-AN00",
                "id": "HONORTNNH-AN00"
            },
            {
                "model": "K5",
                "id": "IO02JO6LHVVFD1UQLV"
            },
            {
                "model": "RMX2071",
                "id": "RKQ1.211103.002"
            },
            {
                "model": "5380CA",
                "id": "KTU84P"
            },
            {
                "model": "SM-G981U1",
                "id": "SP1A.210812.016"
            },
            {
                "model": "AUM-AL20",
                "id": "HONORAUM-AL20"
            },
            {
                "model": "GM1915",
                "id": "RKQ1.201022.002"
            },
            {
                "model": "RMX1821",
                "id": "QP1A.190711.020"
            },
            {
                "model": "NX619J",
                "id": "PKQ1.180929.001"
            },
            {
                "model": "JDN2-W09HN",
                "id": "HUAWEIJDN2-W09HN"
            },
            {
                "model": "OPPO R9s Plust",
                "id": "MMB29M"
            },
            {
                "model": "vivo Y79",
                "id": "N2G47H"
            },
            {
                "model": "KNT-AL20",
                "id": "HUAWEIKNT-AL20"
            },
            {
                "model": "VKY-TL00",
                "id": "HUAWEIVKY-TL00"
            },
            {
                "model": "LGE-AN20",
                "id": "HONORLGE-AN20"
            },
            {
                "model": "Lenovo TB-J606F",
                "id": "QKQ1.200730.002"
            },
            {
                "model": "SM-C7000",
                "id": "R16NW"
            },
            {
                "model": "NEM-AL10",
                "id": "HONORNEM-AL10"
            },
            {
                "model": "OPPO R9skt",
                "id": "MMB29M"
            },
            {
                "model": "Lenovo L78011",
                "id": "PKQ1.190127.001"
            },
            {
                "model": "AECR C5 PRO",
                "id": "N2G47H"
            },
            {
                "model": "KNT-AL10",
                "id": "HUAWEIKNT-AL10"
            },
            {
                "model": "WPOS-3",
                "id": "KTU84P"
            },
            {
                "model": "meizu 16Xs",
                "id": "PKQ1.190302.001"
            },
            {
                "model": "GIONEE M50Pro",
                "id": "N6F26Q"
            },
            {
                "model": "DLI-TL20",
                "id": "HONORDLI-TL20"
            },
            {
                "model": "COR-AL00",
                "id": "HUAWEICOR-AL00"
            },
            {
                "model": "V1732T",
                "id": "O11019"
            },
            {
                "model": "BAH4-W19",
                "id": "HUAWEIBAH4-W19"
            },
            {
                "model": "MHA-TL00",
                "id": "HUAWEIMHA-TL00"
            },
            {
                "model": "SM-C9000",
                "id": "MMB29M"
            },
            {
                "model": "RMX1851",
                "id": "RKQ1.201217.002"
            },
            {
                "model": "IWRIST i7",
                "id": "PPR1.180610.011"
            },
            {
                "model": "PIC-AL00",
                "id": "HUAWEIPIC-AL00"
            },
            {
                "model": "PRA-AL00",
                "id": "HONORPRA-AL00"
            },
            {
                "model": "V1s",
                "id": "MRA58K"
            },
            {
                "model": "DCS-W21",
                "id": "NHG47K"
            },
            {
                "model": "vivo X20Plus UD",
                "id": "OPM1.171019.011"
            },
            {
                "model": "BKL-AL00",
                "id": "HUAWEIBKL-AL00"
            },
            {
                "model": "LLD-AL00",
                "id": "HONORLLD-AL00"
            },
            {
                "model": "V1730EA",
                "id": "OPM1.171019.011"
            },
            {
                "model": "vivo X9Plus L",
                "id": "N2G47H"
            },
            {
                "model": "MT-N2p",
                "id": "RQ1D.210105.003"
            },
            {
                "model": "OXF",
                "id": "HUAWEIOXF"
            },
            {
                "model": "EVR-L29",
                "id": "HUAWEIEVR-L29"
            },
            {
                "model": "FIG-AL00",
                "id": "HUAWEIFIG-AL00"
            },
            {
                "model": "FIO-BD00",
                "id": "PTACFIO-BD00"
            },
            {
                "model": "eagle-pos",
                "id": "KOT49H"
            },
            {
                "model": "unknown",
                "id": "QP1A.190711.020"
            },
            {
                "model": "OPPO A83t",
                "id": "N6F26Q"
            },
            {
                "model": "RMX3475",
                "id": "RKQ1.211119.001"
            },
            {
                "model": "OPPO R9m",
                "id": "LMY47I"
            },
            {
                "model": "ONEPLUS A5000",
                "id": "QKQ1.191014.012"
            },
            {
                "model": "HLTE217T",
                "id": "PPR1.180610.011"
            },
            {
                "model": "PBFT00",
                "id": "OPM1.171019.026"
            },
            {
                "model": "LND-TL40",
                "id": "HONORLND-TL40"
            },
            {
                "model": "OPPO A57t",
                "id": "MMB29M"
            },
            {
                "model": "BLN-AL20",
                "id": "HONORBLN-AL20"
            },
            {
                "model": "8848 M6",
                "id": "QKQ1.200127.002"
            },
            {
                "model": "RMX3093",
                "id": "RP1A.200720.011"
            },
            {
                "model": "K9",
                "id": "LMY47V"
            },
            {
                "model": "LIO-L29",
                "id": "HUAWEILIO-L29"
            },
            {
                "model": "GIONEE S10L",
                "id": "NRD90M"
            },
            {
                "model": "S9",
                "id": "KVT49L"
            },
            {
                "model": "RMX2025",
                "id": "RKQ1.201217.002"
            },
            {
                "model": "PGIM10",
                "id": "RKQ1.211119.001"
            },
            {
                "model": "EVR-TL00",
                "id": "HUAWEIEVR-TL00"
            },
            {
                "model": "ASK-AL20",
                "id": "HONORASK-AL20"
            },
            {
                "model": "FLA-TL10",
                "id": "HUAWEIFLA-TL10"
            },
            {
                "model": "CHL-AL60",
                "id": "HUAWEICHL-AL60"
            },
            {
                "model": "TRT-AL00",
                "id": "HUAWEITRT-AL00"
            },
            {
                "model": "RMX2052",
                "id": "RKQ1.201217.002"
            },
            {
                "model": "EML-L29",
                "id": "HUAWEIEML-L29"
            },
            {
                "model": "HUAWEI NXT-TL00",
                "id": "HUAWEINXT-TL00"
            },
            {
                "model": "NX627J",
                "id": "RKQ1.200826.002"
            },
            {
                "model": "COL-TL10",
                "id": "HUAWEICOL-TL10"
            },
            {
                "model": "SM-F9000",
                "id": "SP1A.210812.016"
            },
            {
                "model": "NTS-AL00",
                "id": "HUAWEINTS-AL00"
            },
            {
                "model": "FRD-AL10",
                "id": "HUAWEIFRD-AL10"
            },
            {
                "model": "ZTE 8030N",
                "id": "RP1A.200720.011"
            },
            {
                "model": "KULIAO K10",
                "id": "077"
            },
            {
                "model": "OPPO R9tm",
                "id": "LMY47I"
            },
            {
                "model": "GN5001S",
                "id": "LMY47D"
            },
            {
                "model": "MXW-TN00",
                "id": "HONORMXW-TN00"
            },
            {
                "model": "DE106",
                "id": "OPM1.171019.026"
            },
            {
                "model": "DLT-A0",
                "id": "N2G47O"
            },
            {
                "model": "DP782",
                "id": "NHG47K"
            },
            {
                "model": "SM-N9750",
                "id": "RP1A.200720.012"
            },
            {
                "model": "CMA-AN40",
                "id": "HONORCMA-AN40"
            },
            {
                "model": "MRX-W09",
                "id": "HUAWEIMRX-W09"
            },
            {
                "model": "M1 E",
                "id": "NRD90M"
            },
            {
                "model": "BAH3-W09",
                "id": "HUAWEIBAH3-W09"
            },
            {
                "model": "OS105",
                "id": "NGI77B"
            },
            {
                "model": "vivo Y35A",
                "id": "LRX22G"
            },
            {
                "model": "Lenovo L78121",
                "id": "PKQ1.190319.001"
            },
            {
                "model": "SM-A6060",
                "id": "QP1A.190711.020"
            },
            {
                "model": "TET-AN10",
                "id": "HUAWEITET-AN10"
            },
            {
                "model": "NX651J",
                "id": "RKQ1.200826.002"
            },
            {
                "model": "OPD2101",
                "id": "RKQ1.211019.001"
            },
            {
                "model": "V2188A",
                "id": "SP1A.210812.003"
            },
            {
                "model": "P2",
                "id": "N6F26Q"
            },
            {
                "model": "ZTE BA602",
                "id": "MRA58K"
            },
            {
                "model": "JEF-TN20",
                "id": "HUAWEIJEF-TN20"
            },
            {
                "model": "vivo Z3x",
                "id": "QP1A.190711.020"
            },
            {
                "model": "SCG06",
                "id": "SP1A.210812.016"
            },
            {
                "model": "N900",
                "id": "NewLand_N900"
            },
            {
                "model": "SM-A8050",
                "id": "RP1A.200720.012"
            },
            {
                "model": "Lenovo L70081",
                "id": "RKQ1.201112.002"
            },
            {
                "model": "MAR-TL00",
                "id": "HUAWEIMAR-TL00"
            },
            {
                "model": "RMX3043",
                "id": "RP1A.200720.011"
            },
            {
                "model": "V2_PRO",
                "id": "N2G47H"
            },
            {
                "model": "Nokia 7 plus",
                "id": "OPM1.171019.011"
            },
            {
                "model": "ANE-TL00",
                "id": "HUAWEIANE-TL00"
            },
            {
                "model": "PBDT00",
                "id": "QKQ1.190918.001"
            },
            {
                "model": "ZTE A2322",
                "id": "RKQ1.210907.001"
            },
            {
                "model": "JEF-NX9",
                "id": "HUAWEIJEF-N29"
            },
            {
                "model": "DP792",
                "id": "RQ2A.210505.003"
            },
            {
                "model": "NX616J",
                "id": "OPM1.171019.026"
            },
            {
                "model": "HLTE510T",
                "id": "OPM1.171019.026"
            },
            {
                "model": "V2186A",
                "id": "SP1A.210812.003"
            },
            {
                "model": "vivo X21i",
                "id": "P00610"
            },
            {
                "model": "MP1603",
                "id": "NMF26O"
            },
            {
                "model": "DT1902A",
                "id": "QKQ1.191222.002"
            },
            {
                "model": "Pixel 4",
                "id": "SP2A.220505.002"
            },
            {
                "model": "Royole FlexPai 2",
                "id": "QKQ1.200920.002"
            },
            {
                "model": "OPPO A33m",
                "id": "LMY47V"
            },
            {
                "model": "TFY-AN40",
                "id": "HONORTFY-AN40"
            },
            {
                "model": "RMX3562",
                "id": "SP1A.210812.016"
            },
            {
                "model": "SM-F7070",
                "id": "SP1A.210812.016"
            },
            {
                "model": "GA2020Y5_R30",
                "id": "PPR1.180610.011"
            },
            {
                "model": "SLA-AL00",
                "id": "HUAWEISLA-AL00"
            },
            {
                "model": "H8296",
                "id": "52.0.A.3.84"
            },
            {
                "model": "AGS2-AL00HN",
                "id": "HUAWEIAGS2-AL00HN"
            },
            {
                "model": "OPPO R9km",
                "id": "LMY47I"
            },
            {
                "model": "AGM3-W09HN",
                "id": "HONORAGM3-W09HN"
            },
            {
                "model": "SM-A7050",
                "id": "RP1A.200720.012"
            },
            {
                "model": "SM-G8850",
                "id": "QP1A.190711.020"
            },
            {
                "model": "LON-L29",
                "id": "HUAWEILON-L29"
            },
            {
                "model": "EDI-AL10",
                "id": "HUAWEIEDISON-AL10"
            },
            {
                "model": "1803-A01",
                "id": "OPM1"
            },
            {
                "model": "vivo Y55",
                "id": "MMB29M"
            },
            {
                "model": "20190718Q",
                "id": "PPR1.180610.011"
            },
            {
                "model": "vivo Y53",
                "id": "MMB29M"
            },
            {
                "model": "SM-A6050",
                "id": "PPR1.180610.011"
            },
            {
                "model": "FIG-TL10",
                "id": "HUAWEIFIG-TL10"
            },
            {
                "model": "CUN-TL00",
                "id": "HUAWEICUN-TL00"
            },
            {
                "model": "S7",
                "id": "KVT49L"
            },
            {
                "model": "M6 Note",
                "id": "N2G47H"
            },
            {
                "model": "Titan",
                "id": "QP1A.190711.020"
            },
            {
                "model": "S12pro",
                "id": "PPR1.180610.011"
            },
            {
                "model": "CPH1821",
                "id": "QP1A.190711.020"
            },
            {
                "model": "SCM-AL09",
                "id": "HUAWEISCM-AL09"
            },
            {
                "model": "T1",
                "id": "NRD90M"
            },
            {
                "model": "S1804",
                "id": "KTU84Q"
            },
            {
                "model": "MRD-TL00",
                "id": "HUAWEIMRD-TL00"
            },
            {
                "model": "VTR-TL00",
                "id": "HUAWEIVTR-TL00"
            },
            {
                "model": "Lenovo L78071",
                "id": "QKQ1.191014.001"
            },
            {
                "model": "V2102A",
                "id": "RP1A.200720.012"
            },
            {
                "model": "20210605",
                "id": "PPR1.180610.011"
            },
            {
                "model": "HUAWEI RIO-UL00",
                "id": "HUAWEIRIO-UL00"
            },
            {
                "model": "KNT-TL10",
                "id": "HUAWEIKNT-TL10"
            },
            {
                "model": "NX611J",
                "id": "OPM1.171019.011"
            },
            {
                "model": "ZTE A2022",
                "id": "RKQ1.210503.001"
            },
            {
                "model": "SM-W2019",
                "id": "QP1A.190711.020"
            },
            {
                "model": "FDR-A01w",
                "id": "HuaweiMediaPad"
            },
            {
                "model": "K350t",
                "id": "K350t"
            },
            {
                "model": "NCE-TL10",
                "id": "HUAWEINCE-TL10"
            },
            {
                "model": "MP1710",
                "id": "OPM1.171019.026"
            },
            {
                "model": "PRO 7 Plus",
                "id": "NRD90M"
            },
            {
                "model": "VRD-W10",
                "id": "HUAWEIVRD-W10"
            },
            {
                "model": "TZH-L3",
                "id": "NHG47K"
            },
            {
                "model": "Pixel 3 XL",
                "id": "PPRL.190801.002"
            },
            {
                "model": "ZTE 9000N",
                "id": "QP1A.190711.020"
            },
            {
                "model": "CPH2067",
                "id": "RKQ1.200903.002"
            },
            {
                "model": "AGS2-AL00",
                "id": "HUAWEIAGS2-AL00"
            },
            {
                "model": "SM-G975U1",
                "id": "SP1A.210812.016"
            },
            {
                "model": "SM-M3070",
                "id": "RP1A.200720.012"
            },
            {
                "model": "ANE-LX2",
                "id": "HUAWEIANE-L22"
            },
            {
                "model": "BLA-TL00",
                "id": "HUAWEIBLA-TL00"
            },
            {
                "model": "RMX2142",
                "id": "RKQ1.201217.002"
            },
            {
                "model": "AGS3-W09HN",
                "id": "HUAWEIAGS3-W09HN"
            },
            {
                "model": "vivo V3M A",
                "id": "LMY47I"
            },
            {
                "model": "Pixel 6 Pro",
                "id": "SQ3A.220605.009.B1"
            },
            {
                "model": "CMR-W09",
                "id": "HUAWEICMR-W09"
            },
            {
                "model": "EVA-AL00",
                "id": "HUAWEIEVA-AL00"
            },
            {
                "model": "SM-G970F",
                "id": "SP1A.210812.016"
            },
            {
                "model": "vivo Y55A",
                "id": "MMB29M"
            },
            {
                "model": "MT-A4P",
                "id": "RQ3A.210705.001"
            },
            {
                "model": "HDL-W09",
                "id": "HUAWEIHDL-W09"
            },
            {
                "model": "L2",
                "id": "N2G47H"
            },
            {
                "model": "MRX-W29",
                "id": "HUAWEIMRX-W29"
            },
            {
                "model": "BMH-TN10",
                "id": "HUAWEIBMH-TN10"
            },
            {
                "model": "RMX1921",
                "id": "RKQ1.201217.002"
            },
            {
                "model": "SM-A8000",
                "id": "LMY47X"
            },
            {
                "model": "SM-C5000",
                "id": "NRD90M"
            },
            {
                "model": "SM-T500",
                "id": "RP1A.200720.012"
            },
            {
                "model": "BZT3-AL00",
                "id": "HUAWEIBZT3-AL00"
            }
        ]

        # from https://www.wandoujia.com/apps/36557/history
        self.uc_version_list = ["15.1.5.1205", "15.1.4.1204", "15.1.2.1202", "15.1.1.1201", "15.0.9.1199",
                                "15.0.7.1197", "15.0.6.1196", "15.0.5.1195", "15.0.4.1194", "15.0.3.1193",
                                "15.0.2.1192", "15.0.1.1191", "15.0.0.1190", "14.1.0.1185", "14.0.0.1181",
                                "13.9.9.1180", "13.9.8.1179", "13.9.7.1178", "13.9.6.1177", "13.9.5.1176",
                                "13.9.4.1175", "13.9.3.1174", "13.9.2.1173", "13.9.1.1172", "13.9.0.1171",
                                "13.8.9.1170", "13.8.8.1169", "13.8.7.1168", "13.8.6.1167", "13.8.5.1166",
                                "13.8.4.1165", "13.8.3.1164", "13.8.2.1163", "13.8.1.1162", "13.8.0.1161",
                                "13.7.9.1160", "13.7.8.1159", "13.7.7.1158", "13.7.6.1157", "13.7.4.1155",
                                "13.7.3.1154", "13.7.1.1152", "13.7.0.1151", "13.6.9.1150", "13.6.8.1149",
                                "13.6.7.1148", "13.6.6.1146", "13.6.5.1145", "13.6.3.1143", "13.6.2.1142",
                                "13.6.1.1141", "13.6.0.1140", "13.5.9.1139", "13.5.8.1138", "13.5.7.1137",
                                "13.5.6.1136", "13.5.5.1135", "13.5.4.1134", "13.5.3.1133", "13.5.2.1132",
                                "13.5.1.1131", "13.5.0.1130", "13.4.9.1129", "13.4.8.1128", "13.4.7.1127",
                                "13.4.5.1125", "13.4.4.1124", "13.4.2.1122", "13.4.1.1121", "13.4.0.1120",
                                "13.3.9.1119", "13.3.8.1118", "13.3.7.1117", "13.3.6.1116", "13.3.5.1115",
                                "13.3.4.1114", "13.3.3.1113", "13.3.2.1112", "13.3.1.1111", "13.2.9.1109",
                                "13.2.8.1108", "13.2.7.1107", "13.2.6.1106", "13.2.5.1105", "13.2.3.1103",
                                "13.2.2.1102", "13.2.1.1101", "13.2.0.1100", "13.1.9.1099", "13.1.8.1098",
                                "13.1.7.1097", "13.1.6.1096", "13.1.5.1095", "13.1.4.1094", "13.1.3.1093",
                                "13.1.2.1092", "13.1.0.1090", "13.0.8.1088", "13.0.7.1087", "13.0.6.1086",
                                "13.0.5.1085", "13.0.4.1084", "13.0.3.1083", "13.0.2.1082", "13.0.1.1081",
                                "13.0.0.1080", "12.9.9.1079", "12.9.8.1078", "12.9.7.1077", "12.9.6.1076",
                                "12.9.5.1075", "12.9.4.1074", "12.9.2.1072", "12.9.1.1071", "12.9.0.1070",
                                "12.8.9.1069", "12.8.8.1068", "12.8.7.1067", "12.8.6.1066", "12.8.5.1065",
                                "12.8.4.1064", "12.8.2.1062", "12.8.0.1060", "12.7.9.1059", "12.7.8.1058",
                                "12.7.6.1056", "12.7.4.1054", "12.7.2.1052", "12.7.0.1050", "12.6.8.1048",
                                "12.6.6.1046", "12.6.2.1042", "12.6.1.1041", "12.6.0.1040", "12.5.9.1039",
                                "12.5.6.1036", "12.5.5.1035", "12.5.4.1034", "12.5.2.1032", "12.5.0.1030",
                                "12.4.8.1028", "12.4.6.1026", "12.4.4.1024", "12.4.3.1023", "12.4.2.1022",
                                "12.4.0.1020", "12.3.8.1018", "12.3.6.1016", "12.3.0.1010", "12.2.8.1008",
                                "12.2.6.1006", "12.2.4.1004", "12.2.2.1002"]

        # from https://www.wandoujia.com/apps/44621/history
        self.qqbrowser_version_list = ["13.3", "13.2", "13.1", "13.0", "12.9",
                                       "12.8", "12.7", "12.6", "12.5", "12.4", "12.3", "12.2", "12.1"]

        # from https://www.wandoujia.com/apps/280151/history
        self.baidu_browser_version_list = ["5.26.0.30", "5.22.0.30", "5.13.0.30", "5.10.0.30", "5.9.0.31", "5.7.5.30",
                                           "5.2.0.30", "4.21.5.31", "4.21.5.30", "4.20.4.31", "4.19.5.30", "4.19.0.30",
                                           "4.18.0.32", "4.18.0.31", "4.16.0.30", "4.15.0.30", "4.14.5.31", "4.14.5.30",
                                           "4.14.0.30", "4.13.5.31", "4.9.5.36", "4.9.5.34", "7.20.11.0", "7.19.13.0",
                                           "7.19.11.0", "7.19.10.0", "7.18.21.0", "7.18.20.0", "7.18.11.0", "7.17.12.0",
                                           "7.16.12.0", "7.15.15.0",
                                           "7.14.14.0", "7.14.13.0", "7.13.13.0", "7.12.12.0", "7.11.13.0", "7.11.12.0",
                                           "7.10.12.0", "7.9.12.0", "7.8.12.0", "7.7.13.0", "7.6.12.0", "7.6.11.0",
                                           "7.5.22.0", "7.4.14.0", "7.3.14.0", "7.2.14.0", "7.1.12.0", "7.0.33.0",
                                           "7.0.15.0", "6.4.14.0", "6.3.20.0", "6.3.13.0", "6.2.20.0", "6.2.18.0",
                                           "6.2.16.0", "6.1.13.0", "6.0.23.0", "6.0.21.0", "6.0.15.0", "5.7.5.0",
                                           "5.7.3.0", "5.6.4.0", "5.6.3.0", "5.5.3.0", "5.4.5.0", "5.3.4.0", "5.2.3.0",
                                           "5.1.0.0"]

        # from https://www.wandoujia.com/apps/596157/history
        self.wechat_version_list = [f"8.0.{s_version}" for s_version in range(0, 50)]

    @staticmethod
    def generate_android_version() -> str:
        # from ro.build.version.release 
        l = ["14", "13", "12", "11"]
        return random.choice(l)

    def generate_android_model(self) -> str:
        # ro.product.model + ro.build.id
        # e.g. "Pixel 3 XL Build/PPRL.190801.002"
        model = random.choice(self.android_model)
        return model["model"] + " Build/" + model["id"]

    def generate_android_webview_ua(self) -> str:
        # generate webview useragent
        # in android is `WebView.getSettings().getUserAgentString()`
        # eg. "Mozilla/5.0 (Linux; Android 10; MI 8 Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.101 Mobile Safari/537.36"
        android_version = self.generate_android_version()
        android_model = self.generate_android_model()
        chrome_version = self.generate_chrome_version()
        ua = f"Mozilla/5.0 (Linux; Android {android_version}; {android_model}; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/{chrome_version} Mobile Safari/537.36"
        return ua

    def generate_android_app_ua(self) -> str:
        # generate app useragent
        # in android is `System.getProperty("http.agent");`
        # eg. "Dalvik/2.1.0 (Linux; U; Android 10; Pixel 3a Build/QQ2A.200305.002)"
        android_version = self.generate_android_version()
        android_model = self.generate_android_model()
        ua = f"Dalvik/2.1.0 (Linux; U; Android {android_version}; {android_model})"
        return ua

    def generate_android_uc_ua(self) -> str:
        # generate ucbrowser useragent
        # Mozilla/5.0 (Linux; U; Android 9; zh-CN; LON-AL00 Build/HUAWEILON-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.9.0.1070 Mobile Safari/537.36
        android_version = self.generate_android_version()
        android_model = self.generate_android_model()
        chrome_version = self.generate_chrome_version()
        uc_version = random.choice(self.uc_version_list)
        ua = f"Mozilla/5.0 (Linux; Android {android_version}; zh-CN; {android_model}) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/{chrome_version} UCBrowser/{uc_version} Mobile Safari/537.36"
        return ua

    def generate_android_qq_ua(self) -> str:
        # generate qq browser useragent
        # Mozilla/5.0 (Linux; U; Android 10; zh-cn; M2004J19C Build/QP1A.190711.020) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.101 MQQBrowser/13.3 Mobile Safari/537.36
        android_version = self.generate_android_version()
        android_model = self.generate_android_model()
        chrome_version = self.generate_chrome_version()
        mqq_version = random.choice(self.qqbrowser_version_list)
        ua = f"Mozilla/5.0 (Linux; Android {android_version}; zh-cn; {android_model}) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/{chrome_version} MQQBrowser/{mqq_version} Mobile Safari/537.36"
        return ua

    def generate_android_baidu_ua(self) -> str:
        # generate baidu browser useragent
        # Mozilla/5.0 (Linux; Android 10; M2004J19C Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.101 Mobile Safari/537.36 SP-engine/2.38.0 matrixstyle/0 flyflow/5.39.5.30 lite baiduboxapp/5.39.5.30 (Baidu; P1 10) NABar/1.0
        baidu_browser_version = random.choice(self.baidu_browser_version_list)
        baidu_engine_version = f"2.{random.randint(20, 60)}.0"
        ua = f"{self.generate_android_webview_ua()} SP-engine/{baidu_engine_version} matrixstyle/0 flyflow/{baidu_browser_version} lite baiduboxapp/{baidu_browser_version} (Baidu; P1 10) NABar/1.0"
        return ua

    def generate_android_wechat_ua(self) -> str:
        # generate android wechat useragent
        # Mozilla/5.0 (Linux; Android 10; M2004J19C Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3263 MMWEBSDK/20210601 Mobile Safari/537.36 MMWEBID/2319 MicroMessenger/8.0.7.1920(0x28000737) Process/toolsmp WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64
        android_version = self.generate_android_version()
        android_model = self.generate_android_model()
        chrome_version = self.generate_chrome_version()
        MMWEBSDK_version = (datetime.datetime.now(
        ) - datetime.timedelta(days=random.randint(100, 500))).strftime('%Y%m%d')
        XWEB_version = random.choice(
            ["4313", "4309", "3262", "3263", "4308", "4312", "3179", "4297"])
        MMWEBID_version = random.randint(1000, 9999)
        net_type = random.choice(["4G", "5G", "WIFI"])
        wechat_version = random.choice(
            self.wechat_version_list) + "." + str(random.randint(100, 500) * 10)
        ua = f"Mozilla/5.0 (Linux; Android {android_version}; {android_model}; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/{chrome_version} XWEB/{XWEB_version} MMWEBSDK/{MMWEBSDK_version} Mobile Safari/537.36 MMWEBID/{MMWEBID_version} MicroMessenger/{wechat_version}(0x28000737) Process/toolsmp WeChat/arm64 Weixin NetType/{net_type} Language/zh_CN ABI/arm64"
        return ua

    def generate_android_ua(self) -> str:
        d = random.choice(
            [self.generate_android_wechat_ua, self.generate_android_baidu_ua, self.generate_android_qq_ua,
             self.generate_android_uc_ua, self.generate_android_webview_ua])
        return d()


if __name__ == "__main__":
    a = Android()
    print(a.generate_android_wechat_ua())

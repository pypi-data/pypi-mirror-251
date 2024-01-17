import numbers
from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Optional

from dataclass_wizard import JSONWizard
from type_checker.decorators import enforce_strict_types

from .Data import Data

OTDRTypes = (
    "SR",
    "OTH",
    "DR",
    "HD",
    "MM_AsGa",
    "MM_Si",
    "MM_Lc",
    "VHD",
    "CD",
    "UHD",
    "VLR",
    "LR",
    "MR",
    "LMR",
    "SRL",
    "PCT",
    "UHR",
    "LM",
    "MA_MP",
    "Fttx_4_SM",
    "Fttx_MM",
    "Gen60_D",
    "Gen60_C",
    "Gen60_B",
    "Eotdr_C",
    "Eotdr_B",
    "LA",
    "CWDM",
    "PCT_MM",
    "8kv2_Reglage",
    "Nelumbo",
    "Lotus",
    "Zebra_SM",
    "Zebra_MM",
    "M45",
    "M40",
    "Puma_Av_SM",
    "Puma_UHR",
    "Dwdm_1",
    "Dwdm_8k",
    "Dwdm_x",
    "tbd_Free",
    "Eotdr_V2_A",
    "Eotdr_V2_B",
    "Eotdr_V2_C",
    "Eotdr_N1",
    "Eotdr_N2",
    "Das_SM",
    "DTS_SM",
)


class LibelleEvt(Enum):
    eEvtLibelle_NonApplicable = -1
    eEvtLibelle_NonMesure = 0
    eEvtLibelle_Marqueur = 1
    eEvtLibelle_Pent = 2
    eEvtLibelle_Epissure = 3
    eEvtLibelle_Orl = 4
    eEvtLibelle_Reflectance = 5
    eEvtLibelle_FinFibre = 6
    eEvtLibelle_Coupleur = 7
    eEvtLibelle_ConnecteurOtdr = 8
    eEvtLibelle_Fantome = 9
    eEvtLibelle_Connecteur = 10
    eEvtLibelle_Demux = 11
    eEvtLibelle_Coupleur_X_L = 12
    eEvtLibelle_Coupleur_X_N = 13
    eEvtLibelle_Coupleur_1_2_L = 14
    eEvtLibelle_Coupleur_1_2_N = 15
    eEvtLibelle_Coupleur_2_2_L = 16
    eEvtLibelle_Coupleur_2_2_N = 17
    eEvtLibelle_Coupleur_1_4_L = 18
    eEvtLibelle_Coupleur_1_4_N = 19
    eEvtLibelle_Coupleur_2_4_L = 20
    eEvtLibelle_Coupleur_2_4_N = 21
    eEvtLibelle_Coupleur_1_8_L = 22
    eEvtLibelle_Coupleur_1_8_N = 23
    eEvtLibelle_Coupleur_2_8_L = 24
    eEvtLibelle_Coupleur_2_8_N = 25
    eEvtLibelle_Coupleur_1_16_L = 26
    eEvtLibelle_Coupleur_1_16_N = 27
    eEvtLibelle_Coupleur_2_16_L = 28
    eEvtLibelle_Coupleur_2_16_N = 29
    eEvtLibelle_Coupleur_1_32_L = 30
    eEvtLibelle_Coupleur_1_32_N = 31
    eEvtLibelle_Coupleur_2_32_L = 32
    eEvtLibelle_Coupleur_2_32_N = 33
    eEvtLibelle_Coupleur_1_64_L = 34
    eEvtLibelle_Coupleur_1_64_N = 35
    eEvtLibelle_Coupleur_2_64_L = 36
    eEvtLibelle_Coupleur_2_64_N = 37
    eEvtLibelle_Coupleur_1_128_L = 38
    eEvtLibelle_Coupleur_1_128_N = 39
    eEvtLibelle_Coupleur_2_128_L = 40
    eEvtLibelle_Coupleur_2_128_N = 41
    eEvtLibelle_Semi_Coupleur_X_L = 42
    eEvtLibelle_Semi_Coupleur_X_N = 43
    eEvtLibelle_Semi_Coupleur_1_2_L = 44
    eEvtLibelle_Semi_Coupleur_1_2_N = 45
    eEvtLibelle_Semi_Coupleur_2_2_L = 46
    eEvtLibelle_Semi_Coupleur_2_2_N = 47
    eEvtLibelle_Semi_Coupleur_1_4_L = 48
    eEvtLibelle_Semi_Coupleur_1_4_N = 49
    eEvtLibelle_Semi_Coupleur_2_4_L = 50
    eEvtLibelle_Semi_Coupleur_2_4_N = 51
    eEvtLibelle_Semi_Coupleur_1_8_L = 52
    eEvtLibelle_Semi_Coupleur_1_8_N = 53
    eEvtLibelle_Semi_Coupleur_2_8_L = 54
    eEvtLibelle_Semi_Coupleur_2_8_N = 55
    eEvtLibelle_Semi_Coupleur_1_16_L = 56
    eEvtLibelle_Semi_Coupleur_1_16_N = 57
    eEvtLibelle_Semi_Coupleur_2_16_L = 58
    eEvtLibelle_Semi_Coupleur_2_16_N = 59
    eEvtLibelle_Semi_Coupleur_1_32_L = 60
    eEvtLibelle_Semi_Coupleur_1_32_N = 61
    eEvtLibelle_Semi_Coupleur_2_32_L = 62
    eEvtLibelle_Semi_Coupleur_2_32_N = 63
    eEvtLibelle_Semi_Coupleur_1_64_L = 64
    eEvtLibelle_Semi_Coupleur_1_64_N = 65
    eEvtLibelle_Semi_Coupleur_2_64_L = 66
    eEvtLibelle_Semi_Coupleur_2_64_N = 67
    eEvtLibelle_Semi_Coupleur_1_128_L = 68
    eEvtLibelle_Semi_Coupleur_1_128_N = 69
    eEvtLibelle_Semi_Coupleur_2_128_L = 70
    eEvtLibelle_Semi_Coupleur_2_128_N = 71
    eEvtLibelle_Merged_Event = 72
    eEvtLibelle_Amorce = 73
    eEvtLibelle_Amorce_End = 74
    eEvtLibelle_First_Merged_Event = 75
    eEvtLibelle_Medium_Merged_Event = 76
    eEvtLibelle_Last_Merged_Event = 77
    eEvtLibelle_Fin_Fibre_Splitter_2_N = 78
    eEvtLibelle_Expended_Beam_MM = 79
    eEvtLibelle_Bend = 80
    eEvtLibelle_Refl_Bend = 81
    eEvtLibelle_Jumper = 82
    eEvtLibelle_Coupleur_UB_N_1_99 = 83
    eEvtLibelle_Coupleur_UB_L_1_99 = 84
    eEvtLibelle_Coupleur_UB_N_2_98 = 85
    eEvtLibelle_Coupleur_UB_L_2_98 = 86
    eEvtLibelle_Coupleur_UB_N_5_95 = 87
    eEvtLibelle_Coupleur_UB_L_5_95 = 88
    eEvtLibelle_Coupleur_UB_N_10_90 = 89
    eEvtLibelle_Coupleur_UB_L_10_90 = 90
    eEvtLibelle_Coupleur_UB_N_15_85 = 91
    eEvtLibelle_Coupleur_UB_L_15_85 = 92
    eEvtLibelle_Coupleur_UB_N_20_80 = 93
    eEvtLibelle_Coupleur_UB_L_20_80 = 94
    eEvtLibelle_Coupleur_UB_N_25_75 = 95
    eEvtLibelle_Coupleur_UB_L_25_75 = 96
    eEvtLibelle_Coupleur_UB_N_30_70 = 97
    eEvtLibelle_Coupleur_UB_L_30_70 = 98
    eEvtLibelle_Coupleur_UB_N_35_65 = 99
    eEvtLibelle_Coupleur_UB_L_35_65 = 100
    eEvtLibelle_Coupleur_UB_N_40_60 = 101
    eEvtLibelle_Coupleur_UB_L_40_60 = 102
    eEvtLibelle_Coupleur_UB_N_45_55 = 103
    eEvtLibelle_Coupleur_UB_L_45_55 = 104
    eEvtLibelle_Cascaded_UB_Coupleur = 105
    eEvtLibelle_Cascaded_Std_Coupleur = 106
    eEvtLibelle_Merged_Event_Coupleur = 107
    eEvtLibelle_Coupleur_UB_N_50_50 = 108
    eEvtLibelle_Coupleur_UB_L_50_50 = 109
    eEvtLibelle_Splitter_Uncertain_N = 110
    eEvtLibelle_Splitter_Absent_N = 111
    eEvtLibelle_Cascaded_Std_Coupleur_L = 112
    eEvtLibelle_Connect_Absent = 113
    eEvtLibelle_Splitter_Last_Event = 114
    eEvtLibelle_Coupleur_UB_N_3_97 = 115
    eEvtLibelle_Coupleur_UB_L_3_97 = 116
    eEvtLibelle_Coupleur_UB_N_7_93 = 117
    eEvtLibelle_Coupleur_UB_L_7_93 = 118
    eEvtLibelle_ONT_Detected = 119
    eEvtLibelle_ONT_Failed = 120
    eEvtLibelle_Wall_Jack = 121
    eEvtLibelle_Splitter_Last_Event_Wrong_Position = 122


class NatureEventType(IntEnum):
    cEMPTY = 0
    cMARKER = 1
    cSPLICE = 2
    cREFLECTION = 3
    cSLOPE = 4
    cORL = 5


"""_summary_
TypeMesure is equivalent to teEvtTypeMesure from FO fiber-optic/Fiber_Optic_Qt/Otdr/otdr_bloc.h
Returns:
    _type_: Type of Measurement. A manually added Marker is eEvtType_SemiAuto, 
        it is too the case for eEvtLibelle_Amorce and eEvtLibelle_Amorce_End.
"""


class TypeMesure(Enum):
    eEvtType_NonApplicable = -1
    eEvtType_NonMesure = 0  # cUNDEFINED,
    eEvtType_Auto = 1  # cAUTO_MARKER,   /* Marker pose par la detection automatique           */
    eEvtType_SemiAuto = 2  # cPLACED_MARKER, /* Pose d'un marker utilisateur pour mesure semi-auto */
    eEvtType_Manuelle = 3  # cMANU_MARKER    /* Mesures manuelles

    @classmethod
    def _missing_(cls, value):
        print(
            f"Received value {value} for type measure, we do not know what it is, defaulting to eEvtType_NonApplicable"
        )
        return cls.eEvtType_NonApplicable


class MethodeMesure(Enum):
    eEvtMethode_NonApplicable = -1
    eEvtMethode_Inconnu = 0
    eEvtMethode_NonMesure = 1

    # EPISSURES
    eEvtMethode_2Curseurs = 2  # cTWO_CURSOR,
    eEvtMethode_3CurseursPenteAGauche = 3  # cTHREE_CURSOR,
    eEvtMethode_3CurseursPenteADroite = 4  # cTHREE_CURSOR,
    eEvtMethode_5Curseurs = 5  # cFIVE_CURSOR
    # } tSplice_Method;
    # PENTES
    eEvtMethode_2Points = 6  # cSlope_Two_Points ,
    eEvtMethode_Regression = 7  # cSlope_Linear_Reg
    # } tSlope_Method;
    # REFLECTANCES                       #
    # ML
    eEvtMethode_ML = 8

    @classmethod
    def _missing_(cls, value):
        print(
            f"Received value {value} for method measure, we do not know what it is, defaulting to eEvtMethode_NonApplicable"
        )
        return cls.eEvtMethode_NonApplicable


@enforce_strict_types
@dataclass(init=True, frozen=True)
class Event:
    nature_evt_type: NatureEventType
    libelle_evt_type: LibelleEvt
    type_mesure: TypeMesure
    methode_mesure: MethodeMesure
    index_debut_evt: int
    index_fin_evt: int
    loss_db: Optional[float]
    reflectance_db: Optional[float]
    bilan_db: Optional[float]
    amplitude_fresnel_db: Optional[float] = None


@dataclass(init=True, frozen=True)
class SORData(Data, JSONWizard):
    """Class for storing an OTDR capture"""

    data_points: list
    events: list[Event]
    lambda_nm: float
    pulse_ns: int
    resolution_m: float
    module_name: str
    fo_version_acquisition: str
    otdr_type: str
    refractive_index: float
    filename: str
    acquisition_time_sec: int
    acquisition_range_km: int
    k: int
    noise_floor_db: float
    time_spacing_unit: float

    def get_pulse_index(self):
        pulse_sec = self.pulse_ns / 1000000000.0
        pulse_index = int(pulse_sec / (self.resolution * self.refractive_index / 299792458))
        return pulse_index

    def check_valid_SORData(self):
        if len(self.data_points) <= 0:
            return "Invalid data_points:" + str(len(self.data_points))
        if len(self.events) <= 0:
            return "Invalid events:" + str(len(self.events))
        if self.lambda_nm < 500 or self.lambda_nm > 2000:
            return "Invalid lambda_nm:" + str(self.lambda_nm)

        for event in self.events:
            reason = SORData.check_valid_Event(event)
            if len(reason) > 0:
                return reason
        return ""

    def check_valid_Event(event):
        if not isinstance(event.start_pos, numbers.Number):
            return "Invalid start_pos:" + str(event.start_pos)
        if not isinstance(event.end_pos, numbers.Number):
            return "Invalid end_pos:" + str(event.end_pos)
        if event.start_pos > event.end_pos:
            return "Invalid start/end pos:" + str(event.start_pos) + ", " + str(event.end_pos)
        if (not isinstance(event.loss, numbers.Number)) and (event.loss is not None):
            return "Invalid loss:" + str(event.loss)
        return ""

    def __str__(self):
        res = (
            "Event data_points:"
            + str(len(self.data_points))
            + ", events: "
            + str(len(self.events))
            + ", lambda_nm:"
            + str(self.lambda_nm)
            + ", pulse_ns:"
            + str(self.pulse_ns)
            + ", resolution:"
            + str(self.resolution_cm)
            + ", module_name:"
            + str(self.module_name)
            + ", otdr_type:"
            + str(self.otdr_type)
            + ", acquisition_time:"
            + str(self.acquisition_time_sec)
            + ", acquisition_range_km:"
            + str(self.acquisition_range_km)
            + ", backscatter_coefficient:"
            + str(self.k)
            + ", noise floor",
            +str(self.noise_floor_db),
            +", time spacing unit",
            +str(self.time_spacing_unit),
        )
        return res

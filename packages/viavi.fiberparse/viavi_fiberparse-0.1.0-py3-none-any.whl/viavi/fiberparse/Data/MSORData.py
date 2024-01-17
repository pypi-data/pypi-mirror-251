from dataclasses import dataclass
from enum import Enum
from typing import Optional

from type_checker.decorators import enforce_strict_types

from viavi.fiberparse.Data.SORData import LibelleEvt, SORData


class TableIcon(Enum):
    cTable_No_Icon = 0
    cTable_Icon_Marker = 1
    cTable_Icon_Slope = 2
    cTable_Icon_Splice = 3
    cTable_Icon_Refl = 4
    cTable_Icon_Ghost = 5
    cTable_Icon_Fin_Fibre = 6
    cTable_Icon_Orl = 7
    cTable_Icon_Orl_Global = 8
    cTable_Icon_Amorce = 9
    cTable_Icon_Amorce_End = 10
    cTable_Icon_Splitter = 11
    cTable_Icon_Bend = 12
    cIcon_Up_Arrow = 13
    cIcon_Down_Arrow = 14
    cIcon_Small_Up_Arrow = 15
    cIcon_Small_Down_Arrow = 16
    cIcon_Pass = 17
    cIcon_Fail = 18
    cIcon_Warning = 19
    cIcon_Lock_Events = 20
    cIcon_Bargraph_0_16 = 21
    cIcon_Bargraph_1_16 = 22
    cIcon_Bargraph_2_16 = 23
    cIcon_Bargraph_3_16 = 24
    cIcon_Bargraph_4_16 = 25
    cIcon_Bargraph_5_16 = 26
    cIcon_Bargraph_6_16 = 27
    cIcon_Bargraph_7_16 = 28
    cIcon_Bargraph_8_16 = 29
    cIcon_Bargraph_9_16 = 30
    cIcon_Bargraph_10_16 = 31
    cIcon_Bargraph_11_16 = 32
    cIcon_Bargraph_12_16 = 33
    cIcon_Bargraph_13_16 = 34
    cIcon_Bargraph_14_16 = 35
    cIcon_Bargraph_15_16 = 36
    cIcon_Bargraph_16_16 = 37
    cIcon_Pointer_Zoom = 38
    cIcon_Carac_Lambda = 39
    cIcon_Carac_Lambda_Ref = 40
    cIcon_Carac_Delta = 41
    cIcon_Origine = 42
    cIcon_Extremite = 43
    cIcon_Small_Ok = 44
    cIcon_Small_Ko = 45
    cIcon_Small_Warning = 46
    cUpper_Table_Icon_Amorce = 47
    cTable_Icon_Fin_Fibre_Sco = 48
    cTable_Icon_Amorce_Sco_Debut_Fibre = 49
    cTable_Icon_Amorce_Sco_Fin_Fibre = 50
    cTable_Icon_Manual_Splice = 51
    cTable_Icon_Manual_Refl = 52
    cTable_Icon_Manual_Demux = 53
    cTable_Icon_Manual_Splitter = 54
    cTable_Icon_Manual_Ghost = 55
    cTable_Icon_Manual_Fin_Fibre = 56
    cTable_Icon_Curve_Warning = 57
    cTable_Icon_Curve_Warning_Under_Cursor = 58
    cTable_Icon_Alarm_OK = 59
    cTable_Icon_Alarm_KO = 60
    cTable_Icon_Alarm_Warning = 61
    cIcon_LFD_OK_On = 62
    cIcon_LFD_OK_Off = 63
    cIcon_Laser_CW = 64
    cIcon_Laser_270Hz = 65
    cIcon_Laser_330Hz = 66
    cIcon_Laser_1KHz = 67
    cIcon_Laser_2KHz = 68
    cTable_Icon_First_Connect = 69
    cIcone_file_fo_cfg = 70
    cSchematic_Cursor_Bg = 71
    cSchematic_Cursor_On = 72
    cBack_Event_Not_Tested = 73
    cBack_Event_Green = 74
    cBack_Event_Orange = 75
    cBack_Event_Red = 76
    cSchematic_Fiber_xpm = 77
    cSchematic_Right_Arrow = 78
    cSchematic_Left_Arrow = 79
    cSchematic_Mts_2K = 80
    cSchematic_Mts_Small = 81
    cTable_Icon_Auto_Splitter_X_L = 82
    cTable_Icon_Auto_Splitter_X_N = 83
    cTable_Icon_Auto_Splitter_1_2_L = 84
    cTable_Icon_Auto_Splitter_1_2_N = 85
    cTable_Icon_Auto_Splitter_2_2_L = 86
    cTable_Icon_Auto_Splitter_2_2_N = 87
    cTable_Icon_Auto_Splitter_1_4_L = 88
    cTable_Icon_Auto_Splitter_1_4_N = 89
    cTable_Icon_Auto_Splitter_2_4_L = 90
    cTable_Icon_Auto_Splitter_2_4_N = 91
    cTable_Icon_Auto_Splitter_1_8_L = 92
    cTable_Icon_Auto_Splitter_1_8_N = 93
    cTable_Icon_Auto_Splitter_2_8_L = 94
    cTable_Icon_Auto_Splitter_2_8_N = 95
    cTable_Icon_Auto_Splitter_1_16_L = 96
    cTable_Icon_Auto_Splitter_1_16_N = 97
    cTable_Icon_Auto_Splitter_2_16_L = 98
    cTable_Icon_Auto_Splitter_2_16_N = 99
    cTable_Icon_Auto_Splitter_1_32_L = 100
    cTable_Icon_Auto_Splitter_1_32_N = 101
    cTable_Icon_Auto_Splitter_2_32_L = 102
    cTable_Icon_Auto_Splitter_2_32_N = 103
    cTable_Icon_Auto_Splitter_1_64_L = 104
    cTable_Icon_Auto_Splitter_1_64_N = 105
    cTable_Icon_Auto_Splitter_2_64_L = 106
    cTable_Icon_Auto_Splitter_2_64_N = 107
    cTable_Icon_Auto_Splitter_1_128_L = 108
    cTable_Icon_Auto_Splitter_1_128_N = 109
    cTable_Icon_Auto_Splitter_2_128_L = 110
    cTable_Icon_Auto_Splitter_2_128_N = 111
    cTable_Icon_Manu_Splitter_X_L = 112
    cTable_Icon_Manu_Splitter_X_N = 113
    cTable_Icon_Manu_Splitter_1_2_L = 114
    cTable_Icon_Manu_Splitter_1_2_N = 115
    cTable_Icon_Manu_Splitter_2_2_L = 116
    cTable_Icon_Manu_Splitter_2_2_N = 117
    cTable_Icon_Manu_Splitter_1_4_L = 118
    cTable_Icon_Manu_Splitter_1_4_N = 119
    cTable_Icon_Manu_Splitter_2_4_L = 120
    cTable_Icon_Manu_Splitter_2_4_N = 121
    cTable_Icon_Manu_Splitter_1_8_L = 122
    cTable_Icon_Manu_Splitter_1_8_N = 123
    cTable_Icon_Manu_Splitter_2_8_L = 124
    cTable_Icon_Manu_Splitter_2_8_N = 125
    cTable_Icon_Manu_Splitter_1_16_L = 126
    cTable_Icon_Manu_Splitter_1_16_N = 127
    cTable_Icon_Manu_Splitter_2_16_L = 128
    cTable_Icon_Manu_Splitter_2_16_N = 129
    cTable_Icon_Manu_Splitter_1_32_L = 130
    cTable_Icon_Manu_Splitter_1_32_N = 131
    cTable_Icon_Manu_Splitter_2_32_L = 132
    cTable_Icon_Manu_Splitter_2_32_N = 133
    cTable_Icon_Manu_Splitter_1_64_L = 134
    cTable_Icon_Manu_Splitter_1_64_N = 135
    cTable_Icon_Manu_Splitter_2_64_L = 136
    cTable_Icon_Manu_Splitter_2_64_N = 137
    cTable_Icon_Manu_Splitter_1_128_L = 138
    cTable_Icon_Manu_Splitter_1_128_N = 139
    cTable_Icon_Manu_Splitter_2_128_L = 140
    cTable_Icon_Manu_Splitter_2_128_N = 141
    cTable_Icon_Semi_Splitter_X_L = 142
    cTable_Icon_Semi_Splitter_X_N = 143
    cTable_Icon_Semi_Splitter_1_2_L = 144
    cTable_Icon_Semi_Splitter_1_2_N = 145
    cTable_Icon_Semi_Splitter_2_2_L = 146
    cTable_Icon_Semi_Splitter_2_2_N = 147
    cTable_Icon_Semi_Splitter_1_4_L = 148
    cTable_Icon_Semi_Splitter_1_4_N = 149
    cTable_Icon_Semi_Splitter_2_4_L = 150
    cTable_Icon_Semi_Splitter_2_4_N = 151
    cTable_Icon_Semi_Splitter_1_8_L = 152
    cTable_Icon_Semi_Splitter_1_8_N = 153
    cTable_Icon_Semi_Splitter_2_8_L = 154
    cTable_Icon_Semi_Splitter_2_8_N = 155
    cTable_Icon_Semi_Splitter_1_16_L = 156
    cTable_Icon_Semi_Splitter_1_16_N = 157
    cTable_Icon_Semi_Splitter_2_16_L = 158
    cTable_Icon_Semi_Splitter_2_16_N = 159
    cTable_Icon_Semi_Splitter_1_32_L = 160
    cTable_Icon_Semi_Splitter_1_32_N = 161
    cTable_Icon_Semi_Splitter_2_32_L = 162
    cTable_Icon_Semi_Splitter_2_32_N = 163
    cTable_Icon_Semi_Splitter_1_64_L = 164
    cTable_Icon_Semi_Splitter_1_64_N = 165
    cTable_Icon_Semi_Splitter_2_64_L = 166
    cTable_Icon_Semi_Splitter_2_64_N = 167
    cTable_Icon_Semi_Splitter_1_128_L = 168
    cTable_Icon_Semi_Splitter_1_128_N = 169
    cTable_Icon_Semi_Splitter_2_128_L = 170
    cTable_Icon_Semi_Splitter_2_128_N = 171
    cTable_Icon_Merged_Event = 172
    cTable_Icon_First_Merged_Event = 173
    cTable_Icon_Medium_Merged_Event = 174
    cTable_Icon_Last_Merged_Event = 175
    cTable_Icon_Fin_Fibre_Splitter_2_N = 176
    cTable_Icon_EB_MM = 177
    cTable_Icon_Refl_Bend = 178
    cTable_Icon_Splitter_Bend_L = 179
    cTable_Icon_Splitter_Bend_N = 180
    cTable_Icon_Jumper = 181
    cTable_Icon_Sco_Jumper = 182
    cTable_Icon_Manu_UB_Splitter_1_99_L = 183
    cTable_Icon_Manu_UB_Splitter_1_99_N = 184
    cTable_Icon_Manu_UB_Splitter_2_98_L = 185
    cTable_Icon_Manu_UB_Splitter_2_98_N = 186
    cTable_Icon_Manu_UB_Splitter_5_95_L = 187
    cTable_Icon_Manu_UB_Splitter_5_95_N = 188
    cTable_Icon_Manu_UB_Splitter_10_90_L = 189
    cTable_Icon_Manu_UB_Splitter_10_90_N = 190
    cTable_Icon_Manu_UB_Splitter_15_85_L = 191
    cTable_Icon_Manu_UB_Splitter_15_85_N = 192
    cTable_Icon_Manu_UB_Splitter_20_80_L = 193
    cTable_Icon_Manu_UB_Splitter_20_80_N = 194
    cTable_Icon_Manu_UB_Splitter_25_75_L = 195
    cTable_Icon_Manu_UB_Splitter_25_75_N = 196
    cTable_Icon_Manu_UB_Splitter_30_70_L = 197
    cTable_Icon_Manu_UB_Splitter_30_70_N = 198
    cTable_Icon_Manu_UB_Splitter_35_65_L = 199
    cTable_Icon_Manu_UB_Splitter_35_65_N = 200
    cTable_Icon_Manu_UB_Splitter_40_60_L = 201
    cTable_Icon_Manu_UB_Splitter_40_60_N = 202
    cTable_Icon_Manu_UB_Splitter_45_55_L = 203
    cTable_Icon_Manu_UB_Splitter_45_55_N = 204
    cTable_Icon_Semi_UB_Splitter_1_99_L = 205
    cTable_Icon_Semi_UB_Splitter_1_99_N = 206
    cTable_Icon_Semi_UB_Splitter_2_98_L = 207
    cTable_Icon_Semi_UB_Splitter_2_98_N = 208
    cTable_Icon_Semi_UB_Splitter_5_95_L = 209
    cTable_Icon_Semi_UB_Splitter_5_95_N = 210
    cTable_Icon_Semi_UB_Splitter_10_90_L = 211
    cTable_Icon_Semi_UB_Splitter_10_90_N = 212
    cTable_Icon_Semi_UB_Splitter_15_85_L = 213
    cTable_Icon_Semi_UB_Splitter_15_85_N = 214
    cTable_Icon_Semi_UB_Splitter_20_80_L = 215
    cTable_Icon_Semi_UB_Splitter_20_80_N = 216
    cTable_Icon_Semi_UB_Splitter_25_75_L = 217
    cTable_Icon_Semi_UB_Splitter_25_75_N = 218
    cTable_Icon_Semi_UB_Splitter_30_70_L = 219
    cTable_Icon_Semi_UB_Splitter_30_70_N = 220
    cTable_Icon_Semi_UB_Splitter_35_65_L = 221
    cTable_Icon_Semi_UB_Splitter_35_65_N = 222
    cTable_Icon_Semi_UB_Splitter_40_60_L = 223
    cTable_Icon_Semi_UB_Splitter_40_60_N = 224
    cTable_Icon_Semi_UB_Splitter_45_55_L = 225
    cTable_Icon_Semi_UB_Splitter_45_55_N = 226
    cTable_Icon_Auto_Cascaded_UB_Splitter_N = 227
    cTable_Icon_Manu_Cascaded_UB_Splitter_N = 228
    cTable_Icon_Auto_Cascaded_Std_Splitter_N = 229
    cTable_Icon_Manu_Cascaded_Std_Splitter_N = 230
    cTable_Icon_Auto_Merged_Event_Splitter_N = 231
    cTable_Icon_Manu_Merged_Event_Splitter_N = 232
    cTable_Icon_Mux_Demux = 233
    cTable_Icon_Manu_UB_Splitter_50_50_L = 234
    cTable_Icon_Manu_UB_Splitter_50_50_N = 235
    cTable_Icon_Semi_UB_Splitter_50_50_L = 236
    cTable_Icon_Semi_UB_Splitter_50_50_N = 237
    cTable_Icon_Auto_Splitter_Uncertain_N = 238
    cTable_Icon_Auto_Splitter_Absent_N = 239
    cTable_Icon_Auto_Cascaded_Std_Splitter_L = 240
    cTable_Icon_Manu_Cascaded_Std_Splitter_L = 241
    cTable_Icon_Connect_Absent = 242
    cTable_Icon_Splitter_Last_Event = 243
    cTable_Icon_Manu_UB_Splitter_3_97_L = 244
    cTable_Icon_Manu_UB_Splitter_3_97_N = 245
    cTable_Icon_Semi_UB_Splitter_3_97_L = 246
    cTable_Icon_Semi_UB_Splitter_3_97_N = 247
    cTable_Icon_Manu_UB_Splitter_7_93_L = 248
    cTable_Icon_Manu_UB_Splitter_7_93_N = 249
    cTable_Icon_Semi_UB_Splitter_7_93_L = 250
    cTable_Icon_Semi_UB_Splitter_7_93_N = 251
    cTable_Icon_ONT_Detected = 252
    cTable_Icon_ONT_Failed = 253
    cTable_Icon_Wall_Jack = 254
    cTable_Icon_Splitter_Last_Event_Wrong_Position = 255
    cRectangle_SLM_Left = 256
    cRectangle_SLM_Right = 257
    cUpper_arrow = 258
    cDown_arrow = 259
    cTable_Icon_Event_Absent = 260
    cTable_Icon_Event_Uncertain = 261
    cTable_Icon_Event_Demux_Colored = 262
    cTable_Last_Icon = 263
    cIcon_Running = 264


@enforce_strict_types
@dataclass(init=True, frozen=True)
class MultipulseEvent:
    table_icon: TableIcon
    pos_meters: float  # We cannot take index_debut_evt cause events comes from different .sor with different resolutions.
    loss_db: Optional[float]
    reflectance_db: Optional[float]
    bilan_db: Optional[float]


@enforce_strict_types
@dataclass(unsafe_hash=True)
class LaserIdentifier:
    lambda_nm: float


@dataclass
class MSORData:
    """
    Represents MSOR data containing SORData and MultipulseEvent information.

    Attributes:
        sor_data_list (list[SORData]): List of SORData objects (for each belcore/sor).
        multipulse_events (Optional[Dict[LaserIdentifier, MultipulseEvent]]):
            Dictionary mapping LaserIdentifier to MultipulseEvent. In a single Laser Multipulse file,
            we have only one list of MultipulseEvent (length one dictionary). In multiple lasers files, if there are multiple
            pulses per laser, we have one list per laser. In Multiple Laser but single pulse .msor,
            this field is None.
    """

    sor_data_list: list[SORData]
    multipulse_events: Optional[dict[LaserIdentifier, MultipulseEvent]]


@enforce_strict_types
@dataclass
class SmartAcqEventData:
    number: int
    idxcurve: int
    icon: int
    distance: float
    loss: Optional[float]
    reflectance: Optional[float]
    slope: Optional[float]
    section: Optional[float]
    sectionLoss: Optional[float]
    budget: Optional[float]


def mapTableIconToLibelleEvt(table_icon: TableIcon) -> LibelleEvt:
    if table_icon == TableIcon.cTable_No_Icon:
        return LibelleEvt.eEvtLibelle_NonApplicable
    elif table_icon == TableIcon.cTable_Icon_Marker:
        return LibelleEvt.eEvtLibelle_Marqueur
    elif table_icon == TableIcon.cTable_Icon_Slope:
        return LibelleEvt.eEvtLibelle_Pent
    elif table_icon in [TableIcon.cTable_Icon_Splice, TableIcon.cTable_Icon_Manual_Splice]:
        return LibelleEvt.eEvtLibelle_Epissure
    elif table_icon in [TableIcon.cTable_Icon_Refl, TableIcon.cTable_Icon_Manual_Refl]:
        return LibelleEvt.eEvtLibelle_Reflectance
    elif table_icon in [TableIcon.cTable_Icon_Ghost, TableIcon.cTable_Icon_Manual_Ghost]:
        return LibelleEvt.eEvtLibelle_Fantome
    elif table_icon in [TableIcon.cTable_Icon_Fin_Fibre, TableIcon.cTable_Icon_Manual_Fin_Fibre]:
        return LibelleEvt.eEvtLibelle_FinFibre
    elif table_icon in [TableIcon.cTable_Icon_Orl, TableIcon.cTable_Icon_Orl_Global]:
        return LibelleEvt.eEvtLibelle_Orl
    elif table_icon in [TableIcon.cTable_Icon_Splitter, TableIcon.cTable_Icon_Manual_Splitter]:
        return LibelleEvt.eEvtLibelle_Coupleur
    elif table_icon in [TableIcon.cTable_Icon_Auto_Splitter_X_L, TableIcon.cTable_Icon_Manu_Splitter_X_L]:
        return LibelleEvt.eEvtLibelle_Coupleur_X_L
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_X_L:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_X_L
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_X_N,
        TableIcon.cTable_Icon_Manu_Splitter_X_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_X_N
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_X_N:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_X_N
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_1_2_L,
        TableIcon.cTable_Icon_Manu_Splitter_1_2_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_1_2_L
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_1_2_L:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_1_2_L
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_1_2_N,
        TableIcon.cTable_Icon_Manu_Splitter_1_2_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_1_2_N
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_1_2_N:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_1_2_N
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_2_2_L,
        TableIcon.cTable_Icon_Manu_Splitter_2_2_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_2_2_L
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_2_2_L:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_2_2_L
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_2_2_N,
        TableIcon.cTable_Icon_Manu_Splitter_2_2_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_2_2_N
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_2_2_N:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_2_2_N
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_1_4_L,
        TableIcon.cTable_Icon_Manu_Splitter_1_4_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_1_4_L
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_1_4_L:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_1_4_L
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_1_4_N,
        TableIcon.cTable_Icon_Manu_Splitter_1_4_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_1_4_N
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_1_4_N:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_1_4_N
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_2_4_L,
        TableIcon.cTable_Icon_Manu_Splitter_2_4_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_2_4_L
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_2_4_L:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_2_4_L
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_2_4_N,
        TableIcon.cTable_Icon_Manu_Splitter_2_4_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_2_4_N
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_2_4_N:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_2_4_N
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_1_8_L,
        TableIcon.cTable_Icon_Manu_Splitter_1_8_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_1_8_L
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_1_8_L:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_1_8_L
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_1_8_N,
        TableIcon.cTable_Icon_Manu_Splitter_1_8_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_1_8_N
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_1_8_N:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_1_8_N
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_2_8_L,
        TableIcon.cTable_Icon_Manu_Splitter_2_8_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_2_8_L
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_2_8_L:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_2_8_L
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_2_8_N,
        TableIcon.cTable_Icon_Manu_Splitter_2_8_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_2_8_N
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_2_8_N:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_2_8_N
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_1_16_L,
        TableIcon.cTable_Icon_Manu_Splitter_1_16_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_1_16_L
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_1_16_L:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_1_16_L
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_1_16_N,
        TableIcon.cTable_Icon_Manu_Splitter_1_16_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_1_16_N
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_1_16_N:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_1_16_N
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_2_16_L,
        TableIcon.cTable_Icon_Manu_Splitter_2_16_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_2_16_L
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_2_16_L:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_2_16_L
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_2_16_N,
        TableIcon.cTable_Icon_Manu_Splitter_2_16_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_2_16_N
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_2_16_N:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_2_16_N
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_1_32_L,
        TableIcon.cTable_Icon_Manu_Splitter_1_32_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_1_32_L
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_1_32_L:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_1_32_L
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_1_32_N,
        TableIcon.cTable_Icon_Manu_Splitter_1_32_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_1_32_N
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_1_32_N:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_1_32_N

    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_2_32_L,
        TableIcon.cTable_Icon_Manu_Splitter_2_32_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_2_32_L
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_2_32_L:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_2_32_L
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_2_32_N,
        TableIcon.cTable_Icon_Manu_Splitter_2_32_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_2_32_N
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_2_32_N:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_2_32_N

    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_1_64_L,
        TableIcon.cTable_Icon_Manu_Splitter_1_64_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_1_64_L
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_1_64_L:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_1_64_L
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_1_64_N,
        TableIcon.cTable_Icon_Manu_Splitter_1_64_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_1_64_N
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_1_64_N:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_1_64_N

    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_2_64_L,
        TableIcon.cTable_Icon_Manu_Splitter_2_64_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_2_64_L
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_2_64_L:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_2_64_L
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_2_64_N,
        TableIcon.cTable_Icon_Manu_Splitter_2_64_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_2_64_N
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_2_64_N:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_2_64_N
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_1_128_L,
        TableIcon.cTable_Icon_Manu_Splitter_1_128_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_1_128_L
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_1_128_L:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_1_128_L
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_1_128_N,
        TableIcon.cTable_Icon_Manu_Splitter_1_128_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_1_128_N
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_1_128_N:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_1_128_N

    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_2_128_L,
        TableIcon.cTable_Icon_Manu_Splitter_2_128_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_2_128_L
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_2_128_L:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_2_128_L
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Splitter_2_128_N,
        TableIcon.cTable_Icon_Manu_Splitter_2_128_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_2_128_N
    elif table_icon == TableIcon.cTable_Icon_Semi_Splitter_2_128_N:
        return LibelleEvt.eEvtLibelle_Semi_Coupleur_2_128_N
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_1_99_L,
        TableIcon.cTable_Icon_Semi_UB_Splitter_1_99_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_L_1_99
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_1_99_N,
        TableIcon.cTable_Icon_Semi_UB_Splitter_1_99_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_N_1_99
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_2_98_L,
        TableIcon.cTable_Icon_Semi_UB_Splitter_2_98_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_L_2_98
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_2_98_N,
        TableIcon.cTable_Icon_Semi_UB_Splitter_2_98_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_N_2_98
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_3_97_L,
        TableIcon.cTable_Icon_Semi_UB_Splitter_3_97_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_L_3_97
    elif table_icon in [
        TableIcon.cTable_Icon_Semi_UB_Splitter_3_97_N,
        TableIcon.cTable_Icon_Manu_UB_Splitter_3_97_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_N_3_97
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_5_95_L,
        TableIcon.cTable_Icon_Semi_UB_Splitter_5_95_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_L_5_95
    elif table_icon in [
        TableIcon.cTable_Icon_Semi_UB_Splitter_5_95_N,
        TableIcon.cTable_Icon_Manu_UB_Splitter_5_95_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_N_5_95
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_7_93_L,
        TableIcon.cTable_Icon_Semi_UB_Splitter_7_93_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_L_7_93
    elif table_icon in [
        TableIcon.cTable_Icon_Semi_UB_Splitter_7_93_N,
        TableIcon.cTable_Icon_Manu_UB_Splitter_7_93_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_N_7_93
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_10_90_L,
        TableIcon.cTable_Icon_Semi_UB_Splitter_10_90_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_L_10_90
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_10_90_N,
        TableIcon.cTable_Icon_Semi_UB_Splitter_10_90_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_N_10_90
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_15_85_L,
        TableIcon.cTable_Icon_Semi_UB_Splitter_15_85_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_L_15_85
    elif table_icon in [
        TableIcon.cTable_Icon_Semi_UB_Splitter_15_85_N,
        TableIcon.cTable_Icon_Manu_UB_Splitter_15_85_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_N_15_85
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_20_80_L,
        TableIcon.cTable_Icon_Semi_UB_Splitter_20_80_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_L_20_80
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_20_80_N,
        TableIcon.cTable_Icon_Semi_UB_Splitter_20_80_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_N_20_80
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_25_75_L,
        TableIcon.cTable_Icon_Semi_UB_Splitter_25_75_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_L_25_75
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_25_75_N,
        TableIcon.cTable_Icon_Semi_UB_Splitter_25_75_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_N_25_75
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_30_70_L,
        TableIcon.cTable_Icon_Semi_UB_Splitter_30_70_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_L_30_70
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_30_70_N,
        TableIcon.cTable_Icon_Semi_UB_Splitter_30_70_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_N_30_70
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_35_65_L,
        TableIcon.cTable_Icon_Semi_UB_Splitter_35_65_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_L_35_65
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_35_65_N,
        TableIcon.cTable_Icon_Semi_UB_Splitter_35_65_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_N_35_65
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_40_60_L,
        TableIcon.cTable_Icon_Semi_UB_Splitter_40_60_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_L_40_60
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_40_60_N,
        TableIcon.cTable_Icon_Semi_UB_Splitter_40_60_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_N_40_60
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_45_55_L,
        TableIcon.cTable_Icon_Semi_UB_Splitter_45_55_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_L_45_55
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_45_55_N,
        TableIcon.cTable_Icon_Semi_UB_Splitter_45_55_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_N_45_55
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_50_50_L,
        TableIcon.cTable_Icon_Semi_UB_Splitter_50_50_L,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_L_50_50
    elif table_icon in [
        TableIcon.cTable_Icon_Manu_UB_Splitter_50_50_N,
        TableIcon.cTable_Icon_Semi_UB_Splitter_50_50_N,
    ]:
        return LibelleEvt.eEvtLibelle_Coupleur_UB_N_50_50

    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Cascaded_UB_Splitter_N,
        TableIcon.cTable_Icon_Manu_Cascaded_UB_Splitter_N,
    ]:
        return LibelleEvt.eEvtLibelle_Cascaded_UB_Coupleur
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Cascaded_Std_Splitter_N,
        TableIcon.cTable_Icon_Manu_Cascaded_Std_Splitter_N,
    ]:
        return LibelleEvt.eEvtLibelle_Cascaded_Std_Coupleur
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Cascaded_Std_Splitter_L,
        TableIcon.cTable_Icon_Manu_Cascaded_Std_Splitter_L,
    ]:
        return LibelleEvt.eEvtLibelle_Cascaded_Std_Coupleur_L
    elif table_icon in [
        TableIcon.cTable_Icon_Auto_Merged_Event_Splitter_N,
        TableIcon.cTable_Icon_Manu_Merged_Event_Splitter_N,
    ]:
        return LibelleEvt.eEvtLibelle_Merged_Event_Coupleur
    elif table_icon == TableIcon.cTable_Icon_Auto_Splitter_Uncertain_N:
        return LibelleEvt.eEvtLibelle_Splitter_Uncertain_N
    elif table_icon == TableIcon.cTable_Icon_Auto_Splitter_Absent_N:
        return LibelleEvt.eEvtLibelle_Splitter_Absent_N
    elif table_icon == TableIcon.cTable_Icon_Connect_Absent:
        return LibelleEvt.eEvtLibelle_Connect_Absent
    elif table_icon == TableIcon.cTable_Icon_Splitter_Last_Event:
        return LibelleEvt.eEvtLibelle_Splitter_Last_Event
    elif table_icon == TableIcon.cTable_Icon_Splitter_Last_Event_Wrong_Position:
        return LibelleEvt.eEvtLibelle_Splitter_Last_Event_Wrong_Position
    elif table_icon == TableIcon.cTable_Icon_ONT_Detected:
        return LibelleEvt.eEvtLibelle_ONT_Detected
    elif table_icon == TableIcon.cTable_Icon_ONT_Failed:
        return LibelleEvt.eEvtLibelle_ONT_Failed
    elif table_icon == TableIcon.cTable_Icon_First_Connect:
        return LibelleEvt.eEvtLibelle_ConnecteurOtdr
    elif table_icon in [
        TableIcon.cTable_Icon_Manual_Demux,
        TableIcon.cTable_Icon_Mux_Demux,
    ]:
        return LibelleEvt.eEvtLibelle_Demux
    elif table_icon == TableIcon.cTable_Icon_Merged_Event:
        return LibelleEvt.eEvtLibelle_Merged_Event
    elif table_icon == TableIcon.cTable_Icon_Wall_Jack:
        return LibelleEvt.eEvtLibelle_Wall_Jack
    elif table_icon == TableIcon.cTable_Icon_Amorce:
        return LibelleEvt.eEvtLibelle_Amorce
    elif table_icon == TableIcon.cTable_Icon_Amorce_End:
        return LibelleEvt.eEvtLibelle_Amorce_End
    elif table_icon == TableIcon.cTable_Icon_First_Merged_Event:
        return LibelleEvt.eEvtLibelle_First_Merged_Event
    elif table_icon == TableIcon.cTable_Icon_Medium_Merged_Event:
        return LibelleEvt.eEvtLibelle_Medium_Merged_Event
    elif table_icon == TableIcon.cTable_Icon_Last_Merged_Event:
        return LibelleEvt.eEvtLibelle_Last_Merged_Event
    elif table_icon == TableIcon.cTable_Icon_Fin_Fibre_Splitter_2_N:
        return LibelleEvt.eEvtLibelle_Fin_Fibre_Splitter_2_N
    elif table_icon == TableIcon.cTable_Icon_EB_MM:
        return LibelleEvt.eEvtLibelle_Expended_Beam_MM
    elif table_icon == TableIcon.cTable_Icon_Bend:
        return LibelleEvt.eEvtLibelle_Bend
    elif table_icon == TableIcon.cTable_Icon_Refl_Bend:
        return LibelleEvt.eEvtLibelle_Refl_Bend
    elif table_icon == TableIcon.cTable_Icon_Jumper:
        return LibelleEvt.eEvtLibelle_Jumper
    else:
        return LibelleEvt.eEvtLibelle_NonApplicable

import base64
import os
import struct
import subprocess
from pathlib import Path

from lxml import etree
from type_checker.decorators import enforce_strict_types

from viavi.fiberparse.Data.SORData import (
    Event,
    LibelleEvt,
    MethodeMesure,
    NatureEventType,
    OTDRTypes,
    SORData,
    TypeMesure,
)
from viavi.fiberparse.FileParser.FileParser import FileParser
from viavi.fiberparse.Utils.HelpersXMLParsing import convert_xml_string_to_float_or_null


class SORParser(FileParser):
    def __init__(self, sor2xmlPath="/usr/bin/sor2xml"):
        if os.name == "nt":
            raise EnvironmentError("SORParser does not work on windows, please use it on debian")
        elif not os.path.exists(sor2xmlPath):
            raise EnvironmentError("sor2xml not installed, please add it using apt install viavi-libbellcore")
        else:
            self._sor2xmlPath = sor2xmlPath

    def getXML(self, filePath):
        args = [self._sor2xmlPath, filePath]
        bXML = b""
        rc = None
        with subprocess.Popen(args, stdout=subprocess.PIPE) as proc:
            while rc is None:
                bXML += proc.stdout.read()
                rc = proc.poll()
        return bXML

    def _getDataPoints(self, xmlSOR):
        points = xmlSOR.xpath("DataPts/points/text()")[0]
        rawpts = base64.b64decode(points)

        data_points_lin = struct.unpack("<" + ("H" * int(len(rawpts) / 2)), rawpts)

        db_value_unit = float(xmlSOR.xpath("WaveMTSParams/dbValueUnit/text()")[0])

        db_value_offsetUTS = float(xmlSOR.xpath("WaveMTSParams/dBValueOffsetUTS/text()")[0])
        db_value_offset = float(xmlSOR.xpath("WaveMTSParams/dbValueOffset/text()")[0])

        powerOffsetFirstPoint = int(xmlSOR.xpath("FxdParams/powerOffsetFirstPoint/text()")[0])
        powerOffsetFirstPoint_dB = float(powerOffsetFirstPoint) / 1000.0

        res = [
            (float(x) * db_value_unit + powerOffsetFirstPoint_dB + (db_value_offset - db_value_offsetUTS))
            for x in data_points_lin
        ]
        return res

    def _getNoiseFloor(self, xmlSOR):
        db_value_unit = float(xmlSOR.xpath("WaveMTSParams/dbValueUnit/text()")[0])
        db_value_offsetUTS = float(xmlSOR.xpath("WaveMTSParams/dBValueOffsetUTS/text()")[0])
        noise_floor = (
            -(float(xmlSOR.xpath("/belcore/sor/WaveMTSParams/noiseFloor/text()")[0]) * db_value_unit)
            - db_value_offsetUTS
        )
        return noise_floor

    def _getOTDRType(self, xmlSOR):
        otdrType = int(xmlSOR.xpath("/belcore/sor/WaveMTSParams/otdrType/text()")[0])
        if otdrType > len(OTDRTypes):
            return "Unknown OTDR type"
        return OTDRTypes[otdrType]

    def _getModuleName(self, xmlSOR):
        return str(xmlSOR.xpath("SupParams/opticalModuleID/text()")[0])

    def _getAcquisitionFOVersion(self, xmlSOR):
        return str(xmlSOR.xpath("SupParams/softwareRevision/text()")[0])

    def _getPulseData(self, xmlSOR):
        for child in xmlSOR.xpath("FxdParams/pulse"):
            pulseWidth = "".join(child.xpath("./@pulseWidthsUsed"))
            dataSpacing = "".join(child.xpath("./@dataSpacing"))
            nbPoints = "".join(child.xpath("./@numberOfDataPoints"))

        res = (int(pulseWidth), int(dataSpacing), int(nbPoints))
        return res

    def _getRefractiveIndex(self, xmlSOR):
        refractive_index = int(xmlSOR.xpath("FxdParams/groupIndex/text()")[0])
        return float(refractive_index / 100000.0)

    def _getSpatialResolutionMeters(self, xmlSOR):
        time_spacing = float(xmlSOR.xpath("/belcore/sor/WaveMTSParams/timeSpacingUnit/text()")[0])
        spatial_resolution = ((299792458.0 * time_spacing) / self._getRefractiveIndex(xmlSOR)) / 2.0
        spatial_resolution = round(spatial_resolution, 2)
        return spatial_resolution

    def _getLambda(self, xmlSOR):
        return float(xmlSOR.xpath("FxdParams/actualWavelenght/text()")[0])

    def _getAcquisitionTime(self, xmlSOR):
        return int(xmlSOR.xpath("FxdParams/averagingTime/text()")[0])

    def _getAcquisitionRange(self, xmlSOR):
        return int(xmlSOR.xpath("FxdParams/acquisitionRangeDistance/text()")[0])

    def _getBackscatterCoefficient(self, xmlSOR):
        return int(xmlSOR.xpath("FxdParams/backscatterCoefficient/text()")[0]) / -10

    def _getTimeSpacingUnit(self, xmlSOR):
        return float(xmlSOR.xpath("/belcore/sor/WaveMTSParams/timeSpacingUnit/text()")[0])

    def _getEvents(self, xmlSOR) -> list[Event]:
        xml_evt_type = xmlSOR.xpath("JDSUEvenementsMTS/block/block/natureEvt/text()")
        xml_evt_libelle = xmlSOR.xpath("JDSUEvenementsMTS/block/block/libelleEvt/text()")
        xml_type_mesure = xmlSOR.xpath("JDSUEvenementsMTS/block/block/typeMesure/text()")
        xml_methode_mesure = xmlSOR.xpath("JDSUEvenementsMTS/block/block/methodeMesure/text()")
        xml_evt_debut = xmlSOR.xpath("JDSUEvenementsMTS/block/block/posDebutEvt/text()")
        xml_evt_fin = xmlSOR.xpath("JDSUEvenementsMTS/block/block/posFinEvt/text()")
        xml_evt_loss_db = xmlSOR.xpath("JDSUEvenementsMTS/block/block/valeurDb/text()")
        xml_evt_refl_db = xmlSOR.xpath("JDSUEvenementsMTS/block/block/reflectanceDb/text()")
        xml_evt_bilan_db = xmlSOR.xpath("JDSUEvenementsMTS/block/block/bilanDb/text()")
        xml_evt_index = xmlSOR.xpath("JDSUEvenementsMTS/block/block/index/text()")
        xml_evt_amplitude_pic_fresnel_db = xmlSOR.xpath("JDSUEvenementsMTS/block/block/amplitudePicDb/text()")
        try:
            events = []
            for i in range(len(xml_evt_index)):
                nature_evt_type = NatureEventType(int(xml_evt_type[i]))
                libelle_evt_type = LibelleEvt(int(xml_evt_libelle[i]))
                type_mesure = TypeMesure(int(xml_type_mesure[i]))
                methode_mesure = MethodeMesure(int(xml_methode_mesure[i]))
                index_debut_evt = int(xml_evt_debut[i])
                index_fin_evt = int(xml_evt_fin[i])
                loss_db = convert_xml_string_to_float_or_null(xml_evt_loss_db[i])
                reflectance_db = convert_xml_string_to_float_or_null(xml_evt_refl_db[i])
                bilan_db = convert_xml_string_to_float_or_null(xml_evt_bilan_db[i])
                amplitude_pic_fresnel_db = convert_xml_string_to_float_or_null(xml_evt_amplitude_pic_fresnel_db[i])
                events.append(
                    Event(
                        nature_evt_type,
                        libelle_evt_type,
                        type_mesure,
                        methode_mesure,
                        index_debut_evt,
                        index_fin_evt,
                        loss_db,
                        reflectance_db,
                        bilan_db,
                        amplitude_pic_fresnel_db,
                    )
                )
        except Exception as e:
            raise LookupError(f"Could not find events due to {e}")
        return events

    def getXmlTree(self, filePath: str) -> list[etree._Element]:
        if not os.path.exists(filePath):
            raise FileExistsError(f"{filePath} does not exist")
        bXML = self.getXML(filePath)
        try:
            xml = etree.fromstring(bXML)
            sorListElems = xml.xpath("/belcore/sor")
        except Exception as e:
            raise RuntimeError(f"Failed parsing XML, due to {e}")
        return sorListElems

    @enforce_strict_types
    def retrieveOneSorInfo(self, filePath: str, crtSOR: etree._Element) -> SORData:
        data_points = self._getDataPoints(crtSOR)
        otdrType = self._getOTDRType(crtSOR)
        module_name = self._getModuleName(crtSOR)
        fo_version_acquisition = self._getAcquisitionFOVersion(crtSOR)
        pulse = self._getPulseData(crtSOR)[0]
        resolution = self._getSpatialResolutionMeters(crtSOR)
        lambda_nm = self._getLambda(crtSOR)
        events = self._getEvents(crtSOR)
        refractive_index = self._getRefractiveIndex(crtSOR)
        acquisition_time = self._getAcquisitionTime(crtSOR)
        acquisition_range = self._getAcquisitionRange(crtSOR)
        k = self._getBackscatterCoefficient(crtSOR)
        noise_floor = self._getNoiseFloor(crtSOR)
        time_spacing_unit = self._getTimeSpacingUnit(crtSOR)

        sorData = SORData(
            data_points,
            events,
            lambda_nm,
            pulse,
            resolution,
            module_name,
            fo_version_acquisition,
            otdrType,
            refractive_index,
            filePath,
            acquisition_time,
            acquisition_range,
            k,
            noise_floor,
            time_spacing_unit,
        )
        return sorData

    def getData(self, filePath: str) -> SORData:
        file_extension = Path(filePath).suffix
        if file_extension != ".sor":
            raise RuntimeError(
                f"SORParser is made to parse .sor. I received {file_extension}, please use adequate Parser"
            )
        sorList = self.getXmlTree(filePath)
        assert (
            len(sorList) == 1
        ), "File is .sor but contains multiple sor data concatenated (multiple belcore/sor elements from xml tree). This should not occur"
        crtSOR = sorList[0]  # Only one Sor for ".sor" files
        try:
            sorData = self.retrieveOneSorInfo(filePath, crtSOR)
        except Exception as e:
            raise RuntimeError(f"Failed parsing {filePath} due to {e}")
        return sorData

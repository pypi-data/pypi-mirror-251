from pathlib import Path

from lxml import etree

from viavi.fiberparse.Data.MSORData import (
    LaserIdentifier,
    MSORData,
    MultipulseEvent,
    SmartAcqEventData,
    TableIcon,
)
from viavi.fiberparse.FileParser.SORParser import SORParser
from viavi.fiberparse.Utils.HelpersXMLParsing import float_if_exist


class MSORParser(SORParser):
    def _getMultipulseCombinedEvents(self, crtSOR: etree._Element) -> list[MultipulseEvent]:
        # If we enter here, all lambdas in SorList are the same. Thus smart_acq/event_table is the same in all Sors
        smart_acq_event_data_list: list[SmartAcqEventData] = []
        smart_acq_event_table = crtSOR.findall("BlocOtdrPrivate/block/block/smart_acq/event_table/event")
        for smart_acq_event_element in smart_acq_event_table[1:]:
            event = SmartAcqEventData(
                number=int(smart_acq_event_element.get("no")),
                idxcurve=int(smart_acq_event_element.get("idxcurve")) if smart_acq_event_element.get("idxcurve") is not None else 0,
                icon=int(smart_acq_event_element.find("icon").text),
                distance=float_if_exist(smart_acq_event_element.find("distance").text),
                loss=float_if_exist(smart_acq_event_element.find("loss").text),
                reflectance=float_if_exist(smart_acq_event_element.find("reflectance").text),
                slope=float_if_exist(smart_acq_event_element.find("slope").text),
                section=float_if_exist(smart_acq_event_element.find("section").text),
                sectionLoss=float_if_exist(smart_acq_event_element.find("sectionLoss").text),
                budget=float_if_exist(smart_acq_event_element.find("budget").text),
            )
            smart_acq_event_data_list.append(event)

        list_multipulse_events: list[MultipulseEvent] = []
        for smart_acq_event in smart_acq_event_data_list:
            list_multipulse_events.append(
                MultipulseEvent(
                    TableIcon(smart_acq_event.icon),
                    smart_acq_event.distance,
                    smart_acq_event.loss,
                    smart_acq_event.reflectance,
                    smart_acq_event.budget,
                )
            )
        return list_multipulse_events

    def getData(self, filePath: str) -> MSORData:
        file_extension = Path(filePath).suffix
        if file_extension not in [".msor", ".csor"]:  # .csor is just encrypted msor
            raise RuntimeError(
                f"SORParser is made to parse .sor. I received {file_extension}, please use adequate Parser"
            )
        sorList = self.getXmlTree(filePath)
        assert (
            len(sorList) > 1
        ), f"File is {file_extension} but does not contain multiple sor data concatenated (multiple belcore/sor elements from xml tree). This should not occur"

        sorDataList = []
        multipulse_events = None

        list_lambda_nm = [self._getLambda(crtSOR) for crtSOR in sorList]
        list_pulse_ns = [self._getPulseData(crtSOR)[0] for crtSOR in sorList]
        is_multilambda = not all(lambda_nm == list_lambda_nm[0] for lambda_nm in list_lambda_nm)
        is_multipulse = not all(pulse_ns == list_pulse_ns[0] for pulse_ns in list_pulse_ns)
        if is_multilambda and is_multipulse:
            raise RuntimeError(
                f"This is a {file_extension} with multiple lambdas: {list_lambda_nm} and multiple pulses {list_pulse_ns} parser implementation not yet complete, Not parsing"
            )
        else:
            # If we enter here, file is multipulse xor multilambda
            for crtSOR in sorList:
                try:
                    sorData = self.retrieveOneSorInfo(filePath, crtSOR)
                    sorDataList.append(sorData)
                except Exception as e:
                    raise RuntimeError(f"Failed parsing {filePath} due to {e}")
            if is_multipulse:  # Multipulse only file
                lambda_all_sors = list_lambda_nm[0]
                multipulse_combined_events = self._getMultipulseCombinedEvents(
                    sorList[0]
                )  # Multipulse combined events are all the same in all SOR in Multipulse only .msor
                multipulse_events: dict[LaserIdentifier, list[MultipulseEvent]] = {
                    LaserIdentifier(lambda_all_sors): multipulse_combined_events,
                }
        return MSORData(sorDataList, multipulse_events)

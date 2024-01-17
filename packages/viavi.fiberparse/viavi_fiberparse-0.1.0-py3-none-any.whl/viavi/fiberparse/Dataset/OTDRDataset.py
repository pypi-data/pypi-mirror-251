from dataclasses import dataclass
from typing import List

from viavi.fiberparse.Data.SORData import SORData
from viavi.fiberparse.Dataset.Dataset import Dataset


@dataclass(init=True, frozen=True)
class OTDRDataset(Dataset):
    data: List[SORData]

    def summary(self):
        module_names = {}
        otdr_types = {}
        lambda_nms = {}
        pulse_nss = {}
        resolution = {}
        data_points = 0
        events = 0

        for crt in self.data:
            key = crt.module_name
            if key in module_names:
                module_names[key] += 1
            else:
                module_names[key] = 1

            key = crt.otdr_type
            if key in otdr_types:
                otdr_types[key] += 1
            else:
                otdr_types[key] = 1

            key = crt.lambda_nm
            if key in lambda_nms:
                lambda_nms[key] += 1
            else:
                lambda_nms[key] = 1

            key = crt.pulse_ns
            if key in pulse_nss:
                pulse_nss[key] += 1
            else:
                pulse_nss[key] = 1

            key = crt.resolution
            if key in resolution:
                resolution[key] += 1
            else:
                resolution[key] = 1

            data_points += len(crt.data_points)
            events += len(crt.events)

        return (
            "records:"
            + str(len(self.data))
            + "\n"
            + "module_names:"
            + str(module_names)
            + "\n"
            + "otdr_types:"
            + str(otdr_types)
            + "\n"
            + "lambda_nms:"
            + str(lambda_nms)
            + "\n"
            + "pulse_nss:"
            + str(pulse_nss)
            + "\n"
            + "data_points:"
            + str(data_points)
            + "\n"
            + "events:"
            + str(events)
        )

    def getListOfResolutions(self):
        resolutionList = []
        for crt in self.data:
            rounded_resolution = round(crt.resolution, 2)
            if rounded_resolution not in resolutionList:
                resolutionList.append(rounded_resolution)
        return resolutionList

    def getListOfPulses(self):
        pulsesList = []
        for crt in self.data:
            if crt.pulse_ns not in pulsesList:
                pulsesList.append(crt.pulse_ns)
        return pulsesList

    def getListOfModulesNames(self):
        modulesNamesList = []
        for crt in self.data:
            if crt.module_name not in modulesNamesList:
                modulesNamesList.append(crt.module_name)
        return modulesNamesList

    def getListOfOtdrTypes(self):
        OtdrTypesList = []
        for crt in self.data:
            if crt.otdr_type not in OtdrTypesList:
                OtdrTypesList.append(crt.otdr_type)
        return OtdrTypesList

    def getListOfLambdas(self):
        LambdasList = []
        for crt in self.data:
            if crt.lambda_nm not in LambdasList:
                LambdasList.append(crt.lambda_nm)
        return LambdasList

    def getListOfFilename(self):
        filenameList = []
        for crt in self.data:
            if crt.filename not in filenameList:
                filenameList.append(crt.filename)
        return filenameList

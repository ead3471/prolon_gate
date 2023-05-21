from src.prolon_modbus_registers import ProlonRegister


def get_m2000_boiler_modbus_map():
    return {
        "HOLDING": {
            0: ProlonRegister(name="DeviceType", register_number=0, mult=1),
            1: ProlonRegister(name="DeviceSoftVer", register_number=1, mult=100),
            2: ProlonRegister(name="DeviceHardVer", register_number=2, mult=10),
            3: ProlonRegister(name="SupplyTempScaleMin", register_number=3, mult=100),
            4: ProlonRegister(name="SupplyTempScaleMax", register_number=4, mult=100),
            5: ProlonRegister(name="OutsideTempScaleMin", register_number=5, mult=100),
            6: ProlonRegister(name="OutsideTempScaleMax", register_number=6, mult=100),
            7: ProlonRegister(name="DemandOffsetMathSource", register_number=7, mult=1),
            8: ProlonRegister(name="OccupiedOffset", register_number=8, mult=100),
            9: ProlonRegister(
                name="NumberofStagesperBoiler", register_number=9, mult=1
            ),
            10: ProlonRegister(name="BoilerMinOffTime", register_number=10, mult=1),
            11: ProlonRegister(
                name="BoilerTargetDifferential", register_number=11, mult=100
            ),
            12: ProlonRegister(name="EnableValveSequence", register_number=12, mult=1),
            13: ProlonRegister(
                name="ModulatingProportionnal", register_number=13, mult=100
            ),
            14: ProlonRegister(name="ModulatingIntegral", register_number=14, mult=1),
            15: ProlonRegister(name="ValveDerivative", register_number=15, mult=100),
            16: ProlonRegister(
                name="ModulatingActivationPoint", register_number=16, mult=1
            ),
            17: ProlonRegister(name="HighReturmLimit", register_number=17, mult=100),
            18: ProlonRegister(
                name="AnalogOutputReverseActing", register_number=18, mult=1
            ),
            19: ProlonRegister(name="AnalogOutputRange", register_number=19, mult=1),
            20: ProlonRegister(name="MaxReceiveTime", register_number=20, mult=1),
            21: ProlonRegister(name="NetBaud", register_number=21, mult=1),
            22: ProlonRegister(name="NetParity", register_number=22, mult=1),
            23: ProlonRegister(name="NetStopBits", register_number=23, mult=1),
            24: ProlonRegister(name="RJ45Baud", register_number=24, mult=1),
            25: ProlonRegister(name="RJ45Parity", register_number=25, mult=1),
            26: ProlonRegister(name="RJ45StopBits", register_number=26, mult=1),
            27: ProlonRegister(
                name="SupplyWaterTempCalibration", register_number=27, mult=100
            ),
            28: ProlonRegister(
                name="OutsideAirTempCalibration", register_number=28, mult=100
            ),
            29: ProlonRegister(
                name="ReturnWaterTempCalibration", register_number=29, mult=100
            ),
            30: ProlonRegister(name="Location", register_number=30, mult=1),
            38: ProlonRegister(name="BoilerMinOnTime", register_number=38, mult=1),
            39: ProlonRegister(
                name="PumpWarmWeatherShutdown", register_number=39, mult=100
            ),
            40: ProlonRegister(name="LeadPumpMode", register_number=40, mult=1),
            41: ProlonRegister(name="UseDualPumps", register_number=41, mult=1),
            42: ProlonRegister(name="LagPumpMode", register_number=42, mult=1),
            43: ProlonRegister(name="PumpLeadLagSequence", register_number=43, mult=1),
            44: ProlonRegister(
                name="PumpFixedRunTimeMinutes", register_number=44, mult=1
            ),
            45: ProlonRegister(name="PumpNoProofTime", register_number=45, mult=1),
            46: ProlonRegister(
                name="BoilerWarmWeatherShutDown", register_number=46, mult=100
            ),
            47: ProlonRegister(name="UseOffsetSequence", register_number=47, mult=1),
            48: ProlonRegister(
                name="UseFixedTargetSetpoint", register_number=48, mult=1
            ),
            49: ProlonRegister(
                name="FixedTargetSetpoint", register_number=49, mult=100
            ),
            50: ProlonRegister(name="UseModulatingBoiler", register_number=50, mult=1),
            51: ProlonRegister(
                name="BoilerLeadLagSequence", register_number=51, mult=1
            ),
            52: ProlonRegister(
                name="BoilerFixedRunTimeMinutes", register_number=52, mult=1
            ),
            53: ProlonRegister(name="PumpMinOnTime", register_number=53, mult=1),
            54: ProlonRegister(name="PumpMinOffTime", register_number=54, mult=1),
            55: ProlonRegister(name="PumpExerciseInterval", register_number=55, mult=1),
            56: ProlonRegister(name="PumpExerciseTime", register_number=56, mult=1),
            57: ProlonRegister(name="MorningWarmUpTime", register_number=57, mult=1),
            58: ProlonRegister(name="NumberofBoilers", register_number=58, mult=1),
            59: ProlonRegister(name="UseReturnSensor", register_number=59, mult=1),
            60: ProlonRegister(name="LowReturnLimit", register_number=60, mult=100),
            61: ProlonRegister(name="BoilerPostOffTime", register_number=61, mult=1),
            62: ProlonRegister(name="UseBackupBoiler", register_number=62, mult=1),
            63: ProlonRegister(
                name="Inter-StageActivationDelay", register_number=63, mult=1
            ),
            64: ProlonRegister(
                name="Inter-StageDeactivationDelay", register_number=64, mult=1
            ),
            65: ProlonRegister(
                name="ModulatingDeactivationPoint", register_number=65, mult=1
            ),
            66: ProlonRegister(
                name="AlarmHighSupplyLimit", register_number=66, mult=100
            ),
            67: ProlonRegister(
                name="AlarmLowSupplyLimit", register_number=67, mult=100
            ),
            68: ProlonRegister(
                name="UseSameProofforBothPumps", register_number=68, mult=1
            ),
            74: ProlonRegister(name="DO5PumpOverride", register_number=74, mult=1),
            75: ProlonRegister(name="AO1PumpOverride", register_number=75, mult=1),
            76: ProlonRegister(name="Boiler1Override", register_number=76, mult=1),
            77: ProlonRegister(name="Boiler2Override", register_number=77, mult=1),
            78: ProlonRegister(
                name="ModulatingBoiler1Override", register_number=78, mult=1
            ),
            79: ProlonRegister(name="ScheduleOverride", register_number=79, mult=1),
            80: ProlonRegister(name="Boiler3Override", register_number=80, mult=1),
            81: ProlonRegister(name="Boiler4Override", register_number=81, mult=1),
            82: ProlonRegister(name="ModulatingBoiler2", register_number=82, mult=1),
            89: ProlonRegister(name="ClearLeadPumpTimers", register_number=89, mult=1),
            90: ProlonRegister(name="ClearPumpDO5Timers", register_number=90, mult=1),
            91: ProlonRegister(name="ClearPumpAO1Timers", register_number=91, mult=1),
            92: ProlonRegister(
                name="ClearLeadBoilerTimers", register_number=92, mult=1
            ),
            93: ProlonRegister(name="ClearBoilerDO1Timers", register_number=93, mult=1),
            94: ProlonRegister(name="ClearBoilerDO2Timers", register_number=94, mult=1),
            95: ProlonRegister(name="ClearBoilerDO3Timers", register_number=95, mult=1),
            96: ProlonRegister(name="ClearBoilerDO4Timers", register_number=96, mult=1),
            99: ProlonRegister(name="Reset", register_number=99, mult=1),
            100: ProlonRegister(name="Reprogram", register_number=100, mult=1),
            124: ProlonRegister(name="TimeZone", register_number=124, mult=1),
            125: ProlonRegister(
                name="UseDaylightSavingsTime", register_number=125, mult=1
            ),
            126: ProlonRegister(name="DSTActiveMonth", register_number=126, mult=1),
            127: ProlonRegister(name="DSTActiveWeek", register_number=127, mult=1),
            128: ProlonRegister(name="DSTDeactiveMonth", register_number=128, mult=1),
            129: ProlonRegister(name="DSTDeactiveWeek", register_number=129, mult=1),
            139: ProlonRegister(name="LockedAddress", register_number=139, mult=1),
            174: ProlonRegister(name="Time-SetYear", register_number=174, mult=1),
            175: ProlonRegister(name="Time-SetMonth", register_number=175, mult=1),
            176: ProlonRegister(name="Time-SetWeekday", register_number=176, mult=1),
            177: ProlonRegister(name="Time-SetDay", register_number=177, mult=1),
            178: ProlonRegister(name="Time-SetHours", register_number=178, mult=1),
            179: ProlonRegister(name="Time-SetMinutes", register_number=179, mult=1),
            180: ProlonRegister(name="Time-SetSeconds", register_number=180, mult=1),
            199: ProlonRegister(name="WeeklySchedule", register_number=199, mult=1),
            327: ProlonRegister(name="Calendar", register_number=327, mult=1),
            134: ProlonRegister(name="Math1Value", register_number=134, mult=1),
            135: ProlonRegister(name="OccupancyInput", register_number=135, mult=1),
            138: ProlonRegister(name="OutsideTempInput", register_number=138, mult=100),
            141: ProlonRegister(
                name="SupplyWaterTempInput", register_number=141, mult=1
            ),
        },
        "INPUT": {
            0: ProlonRegister(name="SupplyWaterTemp", register_number=0, mult=100),
            1: ProlonRegister(name="OutsideAirTemp", register_number=1, mult=100),
            2: ProlonRegister(name="ReturnWaterTemp", register_number=2, mult=100),
            3: ProlonRegister(name="BoilerDO1Action", register_number=3, mult=1),
            4: ProlonRegister(
                name="ModulatingBoiler1Value/ValvePos", register_number=4, mult=1
            ),
            5: ProlonRegister(name="BoilerCalculatedProof", register_number=5, mult=1),
            6: ProlonRegister(name="BoilerDO2Action", register_number=6, mult=1),
            7: ProlonRegister(name="SupplyWaterTargetSP", register_number=7, mult=100),
            8: ProlonRegister(name="PumpDO5Action", register_number=8, mult=1),
            9: ProlonRegister(name="ProofPumpDO5", register_number=9, mult=1),
            10: ProlonRegister(name="PumpAO1Action", register_number=10, mult=1),
            11: ProlonRegister(name="ProofPumpAO1", register_number=11, mult=1),
            12: ProlonRegister(name="Occupancy", register_number=12, mult=1),
            13: ProlonRegister(name="BoilerDO3Action", register_number=13, mult=1),
            14: ProlonRegister(
                name="BoilerDO4Action(BackupStageinModulatingSeq)",
                register_number=14,
                mult=1,
            ),
            15: ProlonRegister(name="LeadPumpID", register_number=15, mult=1),
            16: ProlonRegister(name="LeadBoilerStageID", register_number=16, mult=1),
            17: ProlonRegister(
                name="ModulatingBoiler2Value", register_number=17, mult=1
            ),
            18: ProlonRegister(name="MaxSpRequest", register_number=18, mult=1),
            19: ProlonRegister(name="BoilerDisable", register_number=19, mult=1),
            20: ProlonRegister(name="AlertStatus", register_number=20, mult=1),
            29: ProlonRegister(name="LeadPumpRunTime", register_number=29, mult=1),
            30: ProlonRegister(name="LeadPumpInactiveTime", register_number=30, mult=1),
            31: ProlonRegister(name="DO5RunTime-Days", register_number=31, mult=1),
            32: ProlonRegister(name="DO5RunTime-Minutes", register_number=32, mult=1),
            33: ProlonRegister(name="AO1RunTime-Days", register_number=33, mult=1),
            34: ProlonRegister(name="AO1RunTime-Minutes", register_number=34, mult=1),
            35: ProlonRegister(name="LeadBoilerRunTime", register_number=35, mult=1),
            36: ProlonRegister(name="DO1RunTime-Days", register_number=36, mult=1),
            37: ProlonRegister(name="DO1RunTime-Minutes", register_number=37, mult=1),
            38: ProlonRegister(name="DO2RunTime-Days", register_number=38, mult=1),
            39: ProlonRegister(name="DO2RunTime-Minutes", register_number=39, mult=1),
            40: ProlonRegister(name="DO3RunTime-Days", register_number=40, mult=1),
            41: ProlonRegister(name="DO3RunTime-Minutes", register_number=41, mult=1),
            42: ProlonRegister(name="DO4RunTime-Days", register_number=42, mult=1),
            43: ProlonRegister(name="DO4RunTime-Minutes", register_number=43, mult=1),
        },
    }


def get_network_controller_map():
    return {
        "HOLDING": {
            0: ProlonRegister(name="DeviceType", register_number=0, mult=1),
            1: ProlonRegister(name="DeviceSoftVer", register_number=1, mult=1),
            2: ProlonRegister(name="DeviceHardVer", register_number=2, mult=1),
            3: ProlonRegister(name="Address", register_number=3, mult=1),
            4: ProlonRegister(name="Baudrate", register_number=4, mult=1),
            5: ProlonRegister(name="Timezone", register_number=5, mult=1),
            6: ProlonRegister(
                name="UseDST(DaylightSavingsTime)", register_number=6, mult=1
            ),
            7: ProlonRegister(name="MACAddress1", register_number=7, mult=1),
            8: ProlonRegister(name="MACAddress2", register_number=8, mult=1),
            9: ProlonRegister(name="MACAddress3", register_number=9, mult=1),
            10: ProlonRegister(name="MACAddress4", register_number=10, mult=1),
            11: ProlonRegister(name="MACAddress5", register_number=11, mult=1),
            12: ProlonRegister(name="MACAddress6", register_number=12, mult=1),
            13: ProlonRegister(name="IPMode", register_number=13, mult=1),
            14: ProlonRegister(name="IPAddress1", register_number=14, mult=1),
            15: ProlonRegister(name="IPAddress2", register_number=15, mult=1),
            16: ProlonRegister(name="IPAddress3", register_number=16, mult=1),
            17: ProlonRegister(name="IPAddress4", register_number=17, mult=1),
            18: ProlonRegister(name="SubnetMask1", register_number=18, mult=1),
            19: ProlonRegister(name="SubnetMask2", register_number=19, mult=1),
            20: ProlonRegister(name="SubnetMask3", register_number=20, mult=1),
            21: ProlonRegister(name="SubnetMask4", register_number=21, mult=1),
            22: ProlonRegister(name="DefaultGateway1", register_number=22, mult=1),
            23: ProlonRegister(name="DefaultGateway2", register_number=23, mult=1),
            24: ProlonRegister(name="DefaultGateway3", register_number=24, mult=1),
            25: ProlonRegister(name="DefaultGateway4", register_number=25, mult=1),
            26: ProlonRegister(name="DSTActiveMonth", register_number=26, mult=1),
            27: ProlonRegister(name="DSTActiveWeek", register_number=27, mult=1),
            28: ProlonRegister(name="DSTDeactiveMonth", register_number=28, mult=1),
            29: ProlonRegister(name="DSTDeactiveWeek", register_number=29, mult=1),
            30: ProlonRegister(name="DeviceName1", register_number=30, mult=1),
            31: ProlonRegister(name="DeviceName2", register_number=31, mult=1),
            32: ProlonRegister(name="DeviceName3", register_number=32, mult=1),
            33: ProlonRegister(name="DeviceName4", register_number=33, mult=1),
            34: ProlonRegister(name="DeviceName5", register_number=34, mult=1),
            35: ProlonRegister(name="DeviceName6", register_number=35, mult=1),
            36: ProlonRegister(name="DeviceName7", register_number=36, mult=1),
            37: ProlonRegister(name="DeviceName8", register_number=37, mult=1),
            38: ProlonRegister(name="DeviceName9", register_number=38, mult=1),
            39: ProlonRegister(name="DeviceName10", register_number=39, mult=1),
            40: ProlonRegister(name="DeviceName11", register_number=40, mult=1),
            41: ProlonRegister(name="DeviceName12", register_number=41, mult=1),
            42: ProlonRegister(name="DeviceName13", register_number=42, mult=1),
            43: ProlonRegister(name="DeviceName14", register_number=43, mult=1),
            44: ProlonRegister(name="DeviceName15", register_number=44, mult=1),
            45: ProlonRegister(name="DeviceName16", register_number=45, mult=1),
            46: ProlonRegister(
                name="OutsideTemperatureSource", register_number=46, mult=1
            ),
            47: ProlonRegister(
                name="OutsideTemperatureDistribution1", register_number=47, mult=1
            ),
            48: ProlonRegister(
                name="OutsideTemperatureDistribution2", register_number=48, mult=1
            ),
            49: ProlonRegister(
                name="OutsideTemperatureDistribution3", register_number=49, mult=1
            ),
            50: ProlonRegister(
                name="OutsideTemperatureDistribution4", register_number=50, mult=1
            ),
            51: ProlonRegister(
                name="OutsideTemperatureDistribution5", register_number=51, mult=1
            ),
            52: ProlonRegister(
                name="OutsideTemperatureDistribution6", register_number=52, mult=1
            ),
            53: ProlonRegister(
                name="OutsideTemperatureDistribution7", register_number=53, mult=1
            ),
            54: ProlonRegister(
                name="OutsideTemperatureDistribution8", register_number=54, mult=1
            ),
            55: ProlonRegister(
                name="Alerts/DatalogLanguage", register_number=55, mult=1
            ),
            56: ProlonRegister(
                name="Alerts/DatalogTemperatureUnits", register_number=56, mult=1
            ),
            57: ProlonRegister(name="DNSAddress1", register_number=57, mult=1),
            58: ProlonRegister(name="DNSAddress2", register_number=58, mult=1),
            59: ProlonRegister(name="DNSAddress3", register_number=59, mult=1),
            60: ProlonRegister(name="DNSAddress4", register_number=60, mult=1),
            61: ProlonRegister(
                name="QuantityofValidWeeklyRoutines", register_number=61, mult=1
            ),
            62: ProlonRegister(
                name="QuantityofValidAnnualRoutines", register_number=62, mult=1
            ),
            63: ProlonRegister(
                name="AllowCloudCommunication", register_number=63, mult=1
            ),
            64: ProlonRegister(name="AlertType", register_number=64, mult=1),
            65: ProlonRegister(
                name="QtyofValidAlerts(Read-Only)", register_number=65, mult=1
            ),
            66: ProlonRegister(
                name="QtyofValidLogs(Read-Only)", register_number=66, mult=1
            ),
            67: ProlonRegister(
                name="QtyofValidDevices(Read-Only)", register_number=67, mult=1
            ),
            68: ProlonRegister(
                name="DataDistributionPeriod", register_number=68, mult=1
            ),
            69: ProlonRegister(name="SupplyWaterSource", register_number=69, mult=1),
            81: ProlonRegister(name="DataloggingStatus", register_number=81, mult=1),
            82: ProlonRegister(name="DataLogMaxSize1", register_number=82, mult=1),
            83: ProlonRegister(name="DataLogMaxSize2", register_number=83, mult=1),
            84: ProlonRegister(name="DataLogTotalSectors1", register_number=84, mult=1),
            85: ProlonRegister(name="DataLogTotalSectors2", register_number=85, mult=1),
            86: ProlonRegister(name="DataLogUsedSectors1", register_number=86, mult=1),
            87: ProlonRegister(name="DataLogUsedSectors2", register_number=87, mult=1),
            88: ProlonRegister(name="DatalogFileSize1", register_number=88, mult=1),
            89: ProlonRegister(name="DatalogFileSize2", register_number=89, mult=1),
            97: ProlonRegister(
                name="LaunchGetListFunction", register_number=97, mult=1
            ),
            99: ProlonRegister(name="Reset", register_number=99, mult=1),
            100: ProlonRegister(name="CurrentTime-Year", register_number=100, mult=1),
            101: ProlonRegister(name="CurrentTime-Month", register_number=101, mult=1),
            102: ProlonRegister(
                name="CurrentTime-DayofWeek", register_number=102, mult=1
            ),
            103: ProlonRegister(name="CurrentTime-Day", register_number=103, mult=1),
            104: ProlonRegister(name="CurrentTime-Hours", register_number=104, mult=1),
            105: ProlonRegister(name="CurrentTime-Minute", register_number=105, mult=1),
            106: ProlonRegister(
                name="CurrentTime-Seconds", register_number=106, mult=1
            ),
            107: ProlonRegister(
                name="WeeklyRoutines-Identification", register_number=107, mult=1
            ),
            395: ProlonRegister(
                name="AnnualRoutines-Identification", register_number=395, mult=1
            ),
            651: ProlonRegister(
                name="AnnualRoutines-Dates", register_number=651, mult=1
            ),
            1419: ProlonRegister(
                name="WeeklyRoutine-Schedules", register_number=1419, mult=1
            ),
            3723: ProlonRegister(
                name="ScheduleDistribution", register_number=3723, mult=1
            ),
            4227: ProlonRegister(
                name="WeeklyRoutines-Status", register_number=4227, mult=1
            ),
            4451: ProlonRegister(name="EmailList", register_number=4451, mult=1),
            4643: ProlonRegister(
                name="AlertEntriesBlock1(1-100)", register_number=4643, mult=1
            ),
            7043: ProlonRegister(
                name="DataLogEntriesBlock1(1-50)", register_number=7043, mult=1
            ),
            8143: ProlonRegister(
                name="ScheduleDestinationRegs", register_number=8143, mult=1
            ),
            8269: ProlonRegister(name="FoundList", register_number=8269, mult=1),
            8277: ProlonRegister(
                name="AlertEntriesBlock2(101-200)", register_number=8277, mult=1
            ),
            10677: ProlonRegister(
                name="DataLogEntriesBlock2(51-100)", register_number=10677, mult=1
            ),
            11777: ProlonRegister(
                name="SupplyWaterDistribution1", register_number=11777, mult=1
            ),
            11778: ProlonRegister(
                name="SupplyWaterDistribution2", register_number=11778, mult=1
            ),
            11779: ProlonRegister(
                name="SupplyWaterDistribution3", register_number=11779, mult=1
            ),
            11780: ProlonRegister(
                name="SupplyWaterDistribution4", register_number=11780, mult=1
            ),
            11781: ProlonRegister(
                name="SupplyWaterDistribution5", register_number=11781, mult=1
            ),
            11782: ProlonRegister(
                name="SupplyWaterDistribution6", register_number=11782, mult=1
            ),
            11783: ProlonRegister(
                name="SupplyWaterDistribution7", register_number=11783, mult=1
            ),
            11784: ProlonRegister(
                name="SupplyWaterDistribution8", register_number=11784, mult=1
            ),
        },
        "INPUT": {},
    }


def get_m2000_MUA_map():
    return {
        "HOLDING": {
            0: ProlonRegister(name="DeviceType", register_number=0, mult=1),
            1: ProlonRegister(name="DeviceSoftVer", register_number=1, mult=100),
            2: ProlonRegister(name="DeviceHardVer", register_number=2, mult=10),
            3: ProlonRegister(name="NetBaud", register_number=3, mult=1),
            4: ProlonRegister(name="RJ45Baud", register_number=4, mult=1),
            5: ProlonRegister(name="NetParity", register_number=5, mult=1),
            6: ProlonRegister(name="RJ45Parity", register_number=6, mult=1),
            7: ProlonRegister(name="NetStopBits", register_number=7, mult=1),
            8: ProlonRegister(name="RJ45StopBits", register_number=8, mult=1),
            9: ProlonRegister(name="Location", register_number=9, mult=1),
            17: ProlonRegister(name="ZoneProportionnal", register_number=17, mult=100),
            18: ProlonRegister(name="ZoneHeatIntegral", register_number=18, mult=1),
            19: ProlonRegister(name="ZoneCoolIntegral", register_number=19, mult=1),
            20: ProlonRegister(name="DefaultZoneHeatSP", register_number=20, mult=100),
            21: ProlonRegister(name="DefaultZoneCoolSP", register_number=21, mult=100),
            22: ProlonRegister(name="MinimumZoneHeatSP", register_number=22, mult=100),
            23: ProlonRegister(name="MaximumZoneHeatSP", register_number=23, mult=100),
            24: ProlonRegister(name="MinimumZoneCoolSP", register_number=24, mult=100),
            25: ProlonRegister(name="MaximumZoneCoolSP", register_number=25, mult=100),
            26: ProlonRegister(
                name="UnoccupiedModeOverrrideTime", register_number=26, mult=1
            ),
            27: ProlonRegister(
                name="OutsideAirTempCalibration", register_number=27, mult=100
            ),
            28: ProlonRegister(
                name="DischargeAirTempCalibration", register_number=28, mult=100
            ),
            29: ProlonRegister(name="ZoneAirTempOffset", register_number=29, mult=100),
            30: ProlonRegister(name="PressureOffset", register_number=30, mult=10),
            31: ProlonRegister(name="CO2Offset", register_number=31, mult=1),
            32: ProlonRegister(name="MechCoolingSetup", register_number=32, mult=1),
            33: ProlonRegister(name="AnalogOut1Range", register_number=33, mult=1),
            34: ProlonRegister(
                name="AnalogOut1ReverseActing", register_number=34, mult=1
            ),
            35: ProlonRegister(name="AnalogOut3Range", register_number=35, mult=1),
            36: ProlonRegister(
                name="AnalogOut3ReverseActing", register_number=36, mult=1
            ),
            37: ProlonRegister(name="PressureInputMode", register_number=37, mult=1),
            38: ProlonRegister(name="PressureInputVoltage", register_number=38, mult=1),
            39: ProlonRegister(
                name="NetworkSupplyTempSource", register_number=39, mult=1
            ),
            40: ProlonRegister(name="MathRefreshRate", register_number=40, mult=1),
            41: ProlonRegister(name="GroupCode1", register_number=41, mult=1),
            42: ProlonRegister(name="GroupCode2", register_number=42, mult=1),
            43: ProlonRegister(name="GroupCode3", register_number=43, mult=1),
            44: ProlonRegister(name="GroupWeight1", register_number=44, mult=1),
            45: ProlonRegister(name="GroupWeight2", register_number=45, mult=1),
            46: ProlonRegister(name="GroupWeight3", register_number=46, mult=1),
            47: ProlonRegister(name="GlobalWeight", register_number=47, mult=1),
            48: ProlonRegister(name="ListRefreshRate", register_number=48, mult=1),
            49: ProlonRegister(name="Math1Source", register_number=49, mult=1),
            50: ProlonRegister(name="Math2Source", register_number=50, mult=1),
            51: ProlonRegister(name="Math3Source", register_number=51, mult=1),
            52: ProlonRegister(name="Math4Source", register_number=52, mult=1),
            53: ProlonRegister(name="Math5Source", register_number=53, mult=1),
            54: ProlonRegister(name="Math1Group", register_number=54, mult=1),
            55: ProlonRegister(name="Math2Group", register_number=55, mult=1),
            56: ProlonRegister(name="Math3Group", register_number=56, mult=1),
            57: ProlonRegister(name="Math4Group", register_number=57, mult=1),
            58: ProlonRegister(name="Math5Group", register_number=58, mult=1),
            59: ProlonRegister(name="DemandFilter", register_number=59, mult=1),
            60: ProlonRegister(name="MathUnoccupiedMode", register_number=60, mult=1),
            61: ProlonRegister(
                name="DischargeTempLowLimit", register_number=61, mult=100
            ),
            62: ProlonRegister(
                name="DischargeTempReenable", register_number=62, mult=100
            ),
            63: ProlonRegister(
                name="DamperRunTimewhilebelowDischargeLim", register_number=63, mult=1
            ),
            64: ProlonRegister(
                name="DischargeLowLimitrepeattime", register_number=64, mult=1
            ),
            65: ProlonRegister(
                name="DamperopenTimewithoutproof", register_number=65, mult=1
            ),
            66: ProlonRegister(
                name="Fanruntimewithoutproof", register_number=66, mult=1
            ),
            67: ProlonRegister(name="VolumeSequenceType", register_number=67, mult=1),
            68: ProlonRegister(name="VFDcontrolledbyCO2", register_number=68, mult=1),
            69: ProlonRegister(name="VFDMinVolts", register_number=69, mult=10),
            70: ProlonRegister(name="VFDMaxVolts", register_number=70, mult=10),
            71: ProlonRegister(name="CO2Setpoint", register_number=71, mult=1),
            72: ProlonRegister(name="CO2Proportionnal", register_number=72, mult=1),
            73: ProlonRegister(name="PressureSetpoint", register_number=73, mult=1),
            74: ProlonRegister(
                name="PressureProportionnal", register_number=74, mult=1
            ),
            75: ProlonRegister(name="PressureIntegral", register_number=75, mult=1),
            76: ProlonRegister(name="SummerSeqEnOutTemp", register_number=76, mult=100),
            77: ProlonRegister(
                name="Controlcoolingbasedondemand", register_number=77, mult=1
            ),
            78: ProlonRegister(name="CompressorMinONTime", register_number=78, mult=1),
            79: ProlonRegister(name="CompressorMinOFFTime", register_number=79, mult=1),
            80: ProlonRegister(
                name="CoolStage1OutEnableTemp", register_number=80, mult=100
            ),
            81: ProlonRegister(
                name="CoolStage2OutEnableTemp", register_number=81, mult=100
            ),
            82: ProlonRegister(name="CoolStage1Setpoint", register_number=82, mult=1),
            83: ProlonRegister(name="CoolStage2Setpoint", register_number=83, mult=1),
            84: ProlonRegister(
                name="CoolStage1Differential", register_number=84, mult=1
            ),
            85: ProlonRegister(
                name="CoolStage2Differential", register_number=85, mult=1
            ),
            86: ProlonRegister(name="WinterSeqEnOutTemp", register_number=86, mult=100),
            87: ProlonRegister(
                name="HeatDischargeTempScaleMin", register_number=87, mult=100
            ),
            88: ProlonRegister(
                name="HeatDischargeTempScaleMid", register_number=88, mult=100
            ),
            89: ProlonRegister(
                name="HeatDischargeTempScaleMax", register_number=89, mult=100
            ),
            90: ProlonRegister(
                name="Controlheatingbasedondemand", register_number=90, mult=1
            ),
            91: ProlonRegister(name="HeatDemandScaleMin", register_number=91, mult=1),
            92: ProlonRegister(name="HeatDemandScaleMid", register_number=92, mult=1),
            93: ProlonRegister(name="HeatDemandScaleMax", register_number=93, mult=1),
            94: ProlonRegister(
                name="HeatOutsideTempScaleMax", register_number=94, mult=100
            ),
            95: ProlonRegister(
                name="HeatOutsideTempScaleMin", register_number=95, mult=100
            ),
            96: ProlonRegister(
                name="ModulatingHeatPropBand", register_number=96, mult=100
            ),
            97: ProlonRegister(
                name="ModulatingHeatIntegral", register_number=97, mult=1
            ),
            98: ProlonRegister(name="SlaveList", register_number=98, mult=1),
            106: ProlonRegister(
                name="EnableAbsoluteOverrides", register_number=106, mult=1
            ),
            107: ProlonRegister(name="TimeZone", register_number=107, mult=1),
            108: ProlonRegister(
                name="UseDaylightSavingsTime", register_number=108, mult=1
            ),
            109: ProlonRegister(name="DSTActiveMonth", register_number=109, mult=1),
            110: ProlonRegister(name="DSTActiveWeek", register_number=110, mult=1),
            111: ProlonRegister(name="DSTDeactiveMonth", register_number=111, mult=1),
            112: ProlonRegister(name="DSTDeactiveWeek", register_number=112, mult=1),
            113: ProlonRegister(
                name="DischargeTempHighLimit", register_number=113, mult=100
            ),
            114: ProlonRegister(name="DO1DisplayMode", register_number=114, mult=1),
            115: ProlonRegister(name="CoolDemandScaleMin", register_number=115, mult=1),
            116: ProlonRegister(name="CoolDemandScaleMid", register_number=116, mult=1),
            117: ProlonRegister(name="CoolDemandScaleMax", register_number=117, mult=1),
            118: ProlonRegister(
                name="CoolDischargeTempScaleMin", register_number=118, mult=100
            ),
            119: ProlonRegister(
                name="CoolDischargeTempScaleMid", register_number=119, mult=100
            ),
            120: ProlonRegister(
                name="CoolDischargeTempScaleMax", register_number=120, mult=100
            ),
            121: ProlonRegister(
                name="CoolOutsideTempScaleMin", register_number=121, mult=100
            ),
            122: ProlonRegister(
                name="CoolOutsideTempScaleMax", register_number=122, mult=100
            ),
            123: ProlonRegister(
                name="ModulatingCoolPropBand", register_number=123, mult=100
            ),
            124: ProlonRegister(
                name="ModulatingCoolIntegral", register_number=124, mult=1
            ),
            125: ProlonRegister(name="AnalogOut2Range", register_number=125, mult=1),
            126: ProlonRegister(
                name="AnalogOut2ReverseActing", register_number=126, mult=1
            ),
            127: ProlonRegister(
                name="IntegralDropoffRate", register_number=127, mult=1
            ),
            139: ProlonRegister(name="LockedAddress", register_number=139, mult=1),
            149: ProlonRegister(name="Reset", register_number=149, mult=1),
            150: ProlonRegister(
                name="GetSlaveListCommand", register_number=150, mult=1
            ),
            151: ProlonRegister(name="Reprogram", register_number=151, mult=1),
            199: ProlonRegister(name="AlarmOverride", register_number=199, mult=1),
            200: ProlonRegister(name="DamperOverride", register_number=200, mult=1),
            201: ProlonRegister(name="FanOverride", register_number=201, mult=1),
            202: ProlonRegister(name="VFDOverride", register_number=202, mult=10),
            203: ProlonRegister(name="CoolingOverride", register_number=203, mult=1),
            204: ProlonRegister(
                name="HeatAuthorizationOverride", register_number=204, mult=1
            ),
            205: ProlonRegister(
                name="ModulatingHeatOverride", register_number=205, mult=1
            ),
            206: ProlonRegister(name="ScheduleOverride", register_number=206, mult=1),
            249: ProlonRegister(name="Time-SetYear", register_number=249, mult=1),
            250: ProlonRegister(name="Time-SetMonth", register_number=250, mult=1),
            251: ProlonRegister(name="Time-SetWeekday", register_number=251, mult=1),
            252: ProlonRegister(name="Time-SetDay", register_number=252, mult=1),
            253: ProlonRegister(name="Time-SetHours", register_number=253, mult=1),
            254: ProlonRegister(name="Time-SetMinutes", register_number=254, mult=1),
            255: ProlonRegister(name="Time-SetSeconds", register_number=255, mult=1),
            259: ProlonRegister(name="Password", register_number=259, mult=1),
            299: ProlonRegister(name="WeeklySchedule", register_number=299, mult=1),
            427: ProlonRegister(name="Calendar", register_number=427, mult=1),
        },
        "INPUT": {
            0: ProlonRegister(name="OutsideAirTemp", register_number=0, mult=100),
            1: ProlonRegister(name="DischargeAirTemp", register_number=1, mult=100),
            2: ProlonRegister(name="Occupancy", register_number=2, mult=1),
            3: ProlonRegister(name="DigitalInput1State", register_number=3, mult=1),
            4: ProlonRegister(name="DigitalInput2State", register_number=4, mult=1),
            5: ProlonRegister(name="DamperOpenProof", register_number=5, mult=1),
            6: ProlonRegister(name="FanProof", register_number=6, mult=1),
            7: ProlonRegister(name="ZoneAirTemp", register_number=7, mult=100),
            8: ProlonRegister(name="ActiveZoneHeatSP", register_number=8, mult=100),
            9: ProlonRegister(name="ActiveZoneCoolSP", register_number=9, mult=100),
            10: ProlonRegister(name="Pressure", register_number=10, mult=10),
            11: ProlonRegister(name="CO2Reading", register_number=11, mult=1),
            12: ProlonRegister(name="ActiveSeason", register_number=12, mult=1),
            13: ProlonRegister(name="DischargeSetpoint", register_number=13, mult=100),
            14: ProlonRegister(name="ReasonForLockoutMode", register_number=14, mult=1),
            15: ProlonRegister(
                name="DischargeAirLimitTriggered", register_number=15, mult=1
            ),
            16: ProlonRegister(name="DamperDemand", register_number=16, mult=1),
            17: ProlonRegister(name="FanDemand", register_number=17, mult=1),
            18: ProlonRegister(name="HeatAuthorization", register_number=18, mult=1),
            19: ProlonRegister(name="AlarmState", register_number=19, mult=1),
            20: ProlonRegister(name="ModulatingHeatValue", register_number=20, mult=1),
            21: ProlonRegister(name="CoolingStatus", register_number=21, mult=1),
            22: ProlonRegister(
                name="VariableFreqDriveValue", register_number=22, mult=10
            ),
            23: ProlonRegister(name="Math1", register_number=23, mult=1),
            24: ProlonRegister(name="Math2", register_number=24, mult=1),
            25: ProlonRegister(name="Math3", register_number=25, mult=1),
            26: ProlonRegister(name="Math4", register_number=26, mult=1),
            27: ProlonRegister(name="Math5", register_number=27, mult=1),
            28: ProlonRegister(
                name="UnoccupiedOverrStatus", register_number=28, mult=1
            ),
        },
    }


def get_Flexio_map():
    return {
        "HOLDING": {
            0: ProlonRegister(name="DeviceType", register_number=0, mult=1),
            1: ProlonRegister(name="DeviceSoftVer", register_number=1, mult=100),
            2: ProlonRegister(name="DeviceHardVer", register_number=2, mult=10),
            3: ProlonRegister(name="NetBaud", register_number=3, mult=1),
            4: ProlonRegister(name="NetParity", register_number=4, mult=1),
            5: ProlonRegister(name="NetStopBits", register_number=5, mult=1),
            6: ProlonRegister(name="RJ45Baud", register_number=6, mult=1),
            7: ProlonRegister(name="RJ45Parity", register_number=7, mult=1),
            8: ProlonRegister(name="RJ45StopBits", register_number=8, mult=1),
            9: ProlonRegister(name="Location", register_number=9, mult=1),
            10: ProlonRegister(name="InputMode1", register_number=10, mult=1),
            11: ProlonRegister(name="InputMode2", register_number=11, mult=1),
            12: ProlonRegister(name="InputMode3", register_number=12, mult=1),
            13: ProlonRegister(name="InputMode4", register_number=13, mult=1),
            14: ProlonRegister(name="InputMode5", register_number=14, mult=1),
            15: ProlonRegister(name="InputMode6", register_number=15, mult=1),
            16: ProlonRegister(name="InputMode7", register_number=16, mult=1),
            17: ProlonRegister(name="InputMode8", register_number=17, mult=1),
            18: ProlonRegister(name="InputMode9", register_number=18, mult=1),
        },
        "INPUT": {
            0: ProlonRegister(name="InputValue1", register_number=0, mult=100),
            1: ProlonRegister(name="InputValue2", register_number=1, mult=100),
            2: ProlonRegister(name="InputValue3", register_number=2, mult=100),
            3: ProlonRegister(name="InputValue4", register_number=3, mult=100),
            4: ProlonRegister(name="InputValue5", register_number=4, mult=100),
            5: ProlonRegister(name="InputValue6", register_number=5, mult=100),
            6: ProlonRegister(name="InputValue7", register_number=6, mult=100),
            7: ProlonRegister(name="InputValue8", register_number=7, mult=100),
            8: ProlonRegister(name="InputValue9", register_number=8, mult=100),
            9: ProlonRegister(name="OutputValue1", register_number=9, mult=1),
            10: ProlonRegister(name="OutputValue2", register_number=10, mult=1),
            11: ProlonRegister(name="OutputValue3", register_number=11, mult=1),
            12: ProlonRegister(name="OutputValue4", register_number=12, mult=1),
            13: ProlonRegister(name="OutputValue5", register_number=13, mult=1),
            14: ProlonRegister(name="OutputValue6", register_number=14, mult=1),
            15: ProlonRegister(name="OutputValue7", register_number=15, mult=1),
            16: ProlonRegister(name="OutputValue8", register_number=16, mult=1),
            17: ProlonRegister(name="ActiveOccupancy", register_number=17, mult=1),
            18: ProlonRegister(name="Net-OutsideTemp", register_number=18, mult=100),
        },
    }
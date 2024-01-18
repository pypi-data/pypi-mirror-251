"""
  Simple Wrapper on the Job class to handle EvnDisp Analysis
  for the Prod5b 2020 analysis from container
  https://forge.in2p3.fr/issues/42322
"""

__RCSID__ = "$Id$"

# generic imports
import json
import collections

# DIRAC imports
from DIRAC.Interfaces.API.Job import Job


class EvnDispSingJob(Job):
    """Job extension class for EvnDisp Analysis,
    takes care of running converter and evndisp.
    """

    def __init__(self, cpuTime=432000):
        """Constructor

        Keyword arguments:
        cpuTime -- max cpu time allowed for the job
        """
        Job.__init__(self)
        self.setCPUTime(cpuTime)
        # defaults
        self.setName("Evndisplay_CalibReco")
        self.setType("EvnDispProcessing")
        self.package = "evndisplay"
        self.version = "eventdisplay-cta-dl1-prod5.v06"
        self.compiler = "gcc48_default"
        self.container = True
        self.program_category = "calibimgreco"
        self.prog_name = "evndisp"
        self.configuration_id = 8
        self.output_data_level = 1
        self.base_path = "/vo.cta.in2p3.fr/MC/PROD5b/"
        self.catalogs = json.dumps(["DIRACFileCatalog", "TSCatalog"])
        self.ts_task_id = 0
        self.output_metadata = collections.OrderedDict()
        self.output_file_metadata = collections.OrderedDict()
        self.group_size = 1

    def set_output_metadata(self, tel_sim_md):
        """Set EventDisplay meta data

        Parameters:
        tel_sim_md -- metadata dictionary from the telescope simulation
        """
        # # Set evndisp directory meta data
        self.output_metadata["array_layout"] = tel_sim_md["array_layout"]
        self.output_metadata["site"] = tel_sim_md["site"]
        self.output_metadata["particle"] = tel_sim_md["particle"]
        try:
            phiP = tel_sim_md["phiP"]["="]
        except BaseException:
            phiP = tel_sim_md["phiP"]
        self.output_metadata["phiP"] = phiP
        try:
            thetaP = tel_sim_md["thetaP"]["="]
        except BaseException:
            thetaP = tel_sim_md["thetaP"]
        self.output_metadata["thetaP"] = thetaP
        self.output_metadata["sct"] = tel_sim_md["sct"]
        self.output_metadata[self.program_category + "_prog"] = self.prog_name
        self.output_metadata[self.program_category + "_prog_version"] = self.version
        self.output_metadata["data_level"] = self.output_data_level
        self.output_metadata["configuration_id"] = self.configuration_id
        self.output_metadata["merged"] = 0
        self.output_metadata["MCCampaign"] = self.MCCampaign

    def set_executable_sequence(self, debug=False):
        """Setup job workflow by defining the sequence of all executables
        All parameters shall have been defined before that method is called.
        """
        i_step = 0
        # step 1 -- debug
        if debug:
            ls_step = self.setExecutable("/bin/ls -alhtr", logFile="LS_Init_Log.txt")
            ls_step["Value"]["name"] = "Step%i_LS_Init" % i_step
            ls_step["Value"]["descr_short"] = "list files in working directory"
            i_step += 1

            env_step = self.setExecutable("/bin/env", logFile="Env_Log.txt")
            env_step["Value"]["name"] = "Step%i_Env" % i_step
            env_step["Value"]["descr_short"] = "Dump environment"
            i_step += 1

        # step 2
        sw_step = self.setExecutable(
            "cta-prod-setup-software",
            arguments="-p %s -v %s -a simulations -g %s"
            % (self.package, self.version, self.compiler),
            logFile="SetupSoftware_Log.txt",
        )
        sw_step["Value"]["name"] = "Step%i_SetupSoftware" % i_step
        sw_step["Value"]["descr_short"] = "Setup software"
        i_step += 1

        # step 3 run EventDisplay
        ev_step = self.setExecutable(
            "./dirac_sing_evndisp.sh", logFile="EvnDisp_Log.txt"
        )
        ev_step["Value"]["name"] = "Step%i_EvnDisplay" % i_step
        ev_step["Value"]["descr_short"] = "Run EvnDisplay"
        i_step += 1

        # step 4 set meta data and register Data
        meta_data_json = json.dumps(self.output_metadata)
        file_meta_data_json = json.dumps(self.output_file_metadata)

        # register Data
        # to be used with job.version = 'eventdisplay-cta-dl1-prod5.v04'
        # data_output_pattern = './Data/*.simtel.DL1.root'
        # to be used with job.version = 'eventdisplay-cta-dl1-prod5.v06'
        data_output_pattern = "./Data/*.simtel.DL1.tar.gz"
        dm_step = self.setExecutable(
            "cta-prod-managedata",
            arguments="'%s' '%s' %s '%s' %s %s '%s' Data"
            % (
                meta_data_json,
                file_meta_data_json,
                self.base_path,
                data_output_pattern,
                self.package,
                self.program_category,
                self.catalogs,
            ),
            logFile="DataManagement_Log.txt",
        )
        dm_step["Value"]["name"] = f"Step{i_step}_DataManagement"
        dm_step["Value"][
            "descr_short"
        ] = "Save data files to SE and register them in DFC"
        i_step += 1

        # step 5 failover step
        if not debug:
            failover_step = self.setExecutable(
                "/bin/ls -l", modulesList=["Script", "FailoverRequest"]
            )
            failover_step["Value"]["name"] = f"Step{i_step}_Failover"
            failover_step["Value"]["descr_short"] = "Tag files as unused if job failed"
            i_step += 1

        # step 6 - debug only
        if debug:
            ls_step = self.setExecutable("/bin/ls -Ralhtr", logFile="LS_End_Log.txt")
            ls_step["Value"]["name"] = f"Step{i_step}_LSHOME_End"
            ls_step["Value"]["descr_short"] = "list files in Home directory"
            i_step += 1

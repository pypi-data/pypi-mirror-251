""" Simtel Script to create a Transformation with Corsika Input Data

    https://forge.in2p3.fr/issues/33932
                        July 13th 2018 - J. Bregeon, C. Bigongiari, L. Arrabito
"""

__RCSID__ = "$Id$"

from DIRAC.Core.Base import Script

Script.setUsageMessage(
    "\n".join(
        [
            __doc__.split("\n")[1],
            "Usage:",
            f"  {Script.scriptName} mode file_path (trans_name) group_size",
            "Arguments:",
            "  mode: WMS for testing, TS for production",
            "  file_path: path to the input file with the list of LFNs to process",
            "  trans_name: name of the transformation for TS mode only",
            "  group_size: n files to process",
            f"\ne.g: python {Script.scriptName}.py WMS p20.txt simtel_astri_p20 10",
        ]
    )
)

Script.parseCommandLine()

import DIRAC
from DIRAC.TransformationSystem.Client.TransformationClient import TransformationClient
from DIRAC.TransformationSystem.Client.Transformation import Transformation
from CTADIRAC.Interfaces.API.SimtelTSJob import SimtelTSJob
from DIRAC.Interfaces.API.Dirac import Dirac
from DIRAC.Core.Workflow.Parameter import Parameter
from CTADIRAC.Core.Utilities.tool_box import read_inputs_from_file


def submit_trans(job, infileList, trans_name, group_size):
    """Create a transformation executing the job workflow"""
    DIRAC.gLogger.notice(f"submit_trans : {trans_name}")

    # Initialize JOB_ID
    job.workflow.addParameter(
        Parameter("JOB_ID", "000000", "string", "", "", True, False, "Temporary fix")
    )

    trans = Transformation()
    trans.setTransformationName(trans_name)  # this must be unique
    trans.setType("DataReprocessing")
    trans.setDescription("Simtel TS example")
    trans.setLongDescription("Simtel tel_sim")  # mandatory
    trans.setBody(job.workflow.toXML())
    trans.setGroupSize(group_size)
    res = trans.addTransformation()  # transformation is created here
    if not res["OK"]:
        return res
    trans.setStatus("Active")
    trans.setAgentType("Automatic")
    # add 10*group_size files to transformation (to have the first 10 jobs)
    trans_id = trans.getTransformationID()
    trans_client = TransformationClient()
    res = trans_client.addFilesToTransformation(
        trans_id["Value"], infileList[: 10 * group_size]
    )
    return res


def submit_WMS(job, infileList):
    """Submit the job locally or to the WMS"""
    dirac = Dirac()
    job.setInputData(infileList)
    job.setJobGroup("SimtelJob")
    res = dirac.submitJob(job)
    if res["OK"]:
        Script.gLogger.info("Submission Result: ", res["Value"])
    return res


def run_simtel_ts(args=None):
    """Simple wrapper to create a SimtelTSJob and setup parameters
    from positional arguments given on the command line.

    Parameters:
    args -- mode file_path (trans_name) group_size
    """
    DIRAC.gLogger.notice("run_simtel_ts")
    # get arguments
    mode = args[0]
    if mode == "WMS":
        file_path = args[1]
        group_size = int(args[2])
    elif mode == "TS":
        file_path = args[1]
        trans_name = args[2]
        group_size = int(args[3])
    else:
        DIRAC.gLogger.error(
            "1st argument should be the job mode: WMS or TS,\n\
                             not %s"
            % args[0]
        )
        DIRAC.exit(-1)

    # read list of input file names
    input_file_list = read_inputs_from_file(file_path)

    ################################
    job = SimtelTSJob(cpuTime=43200)  # to be adjusted!!

    ### Main Script ###
    # override for testing
    job.setName("Simtel")
    # Allow job meshing with ByJobType plugin
    job.setType("SimtelProcessing")

    # Defaults to override
    # job.version = '2018-06-12'
    # job.simtel_config_file = 'ASTRI_MiniArray15_Paranal_ACDC_2018_06_12.cfg'
    # job.thetaP = 20.0
    # job.phiP = 0.0

    # output
    job.setOutputSandbox(["*Log.txt"])
    # Customize this path to point to your user area
    job.base_path = "/vo.cta.in2p3.fr/user/a/arrabito/Miniarray15"

    # specific configuration
    if mode == "WMS":
        # set meta data
        # job.set_metadata(input_file_list[0])
        job.ts_task_id = "0"
        job.setupWorkflow(debug=True)
        # subtmit to the WMS for debug
        job.setDestination("LCG.IN2P3-CC.fr")
        res = submit_WMS(job, input_file_list[:group_size])
    elif mode == "TS":
        job.ts_task_id = "@{JOB_ID}"  # dynamic
        job.setupWorkflow(debug=True)
        res = submit_trans(job, input_file_list, trans_name, group_size)
    else:
        DIRAC.gLogger.error("Unknown mode")
        return None

    return res


#########################################################
if __name__ == "__main__":
    args = Script.getPositionalArgs()
    if len(args) not in [3, 4]:
        Script.showHelp()
    try:
        res = run_simtel_ts(args)
        if not res["OK"]:
            DIRAC.gLogger.error(res["Message"])
            DIRAC.exit(-1)
        else:
            DIRAC.gLogger.notice("Done")
    except Exception:
        DIRAC.gLogger.exception()
        DIRAC.exit(-1)

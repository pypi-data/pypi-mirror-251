"""
    Launcher script to launch a Prod5MCPipeAlphaDivergentJob
    on the WMS or create a Transformation.
        adapted fy FDP, from prod5b_mcpipe_alpha_ssts_fullmoon_nsb_launcher.py by OG, January 2022
"""

from DIRAC.Core.Base import Script

Script.setUsageMessage(
    "\n".join(
        [
            __doc__.split("\n")[1],
            "Usage:",
            "python %s.py <mode> <site> <particle> <pointing> <zenith> <n showers>"
            % Script.scriptName,
            "Arguments:",
            "  mode: WMS for testing, TS for production",
            "  site: must be Paranal",
            "  particle: in gamma, gamma-diffuse, electron, proton",
            "  pointing: North or South",
            "  zenith: 20, 40 or 60",
            "  n shower: 100 for testing",
            f"\ne.g: python {Script.scriptName}.py WMS Paranal gamma North 20 100",
        ]
    )
)

Script.parseCommandLine()

import DIRAC
from DIRAC.TransformationSystem.Client.Transformation import Transformation
from CTADIRAC.Interfaces.API.Prod5bMCPipeAlphaDivergentJob import (
    Prod5bMCPipeAlphaDivergentJob,
)
from DIRAC.Core.Workflow.Parameter import Parameter
from DIRAC.Interfaces.API.Dirac import Dirac


def submit_transformation(job, trans_name):
    """Create a transformation executing the job workflow"""
    DIRAC.gLogger.notice(f"submit_trans : {trans_name}")

    # Initialize JOB_ID
    job.workflow.addParameter(
        Parameter("JOB_ID", "000000", "string", "", "", True, False, "Temporary fix")
    )

    trans = Transformation()
    trans.setTransformationName(trans_name)  # this must be unique
    trans.setType("MCSimulation")
    trans.setDescription("Prod5 Alpha divergent")
    trans.setLongDescription("Prod5 simulation pipeline Alpha divergent")  # mandatory
    trans.setBody(job.workflow.toXML())
    result = trans.addTransformation()  # transformation is created here
    if not result["OK"]:
        return result
    trans.setStatus("Active")
    trans.setAgentType("Automatic")
    trans_id = trans.getTransformationID()
    return trans_id


def submit_wms(job):
    """Submit the job to the WMS
    @todo launch job locally
    """
    dirac = Dirac()
    job.setJobGroup("Prod5bAlphaDivergentJob")
    result = dirac.submitJob(job)
    if result["OK"]:
        Script.gLogger.notice("Submitted job: ", result["Value"])
    return result


def run_simulation(args):
    """Simple wrapper to create a Prod5MCPipeNSBJob and setup parameters
    from positional arguments given on the command line.

    Parameters:
    args -- mode (trans_name)
    """
    DIRAC.gLogger.notice("run_mc_pipeline")
    # get arguments
    mode = args[0]

    # job setup
    job = Prod5bMCPipeAlphaDivergentJob()
    job.version = "2020-06-29b"
    job.compiler = "gcc83_matchcpu"
    # override for testing
    job.setName("Prod5_Divergent")
    # parameters from command line
    job.set_site(args[1])
    job.set_particle(args[2])
    job.set_pointing_dir(args[3])
    job.zenith_angle = args[4]
    job.n_shower = args[5]

    # output
    job.setOutputSandbox(["*Log.txt"])

    # input
    # job.setInputSandbox( ['dirac_prod5_alpha_divergent_run'] ) #if not yet present in the cvmfs directory should be uploaded from local via ISB

    # specific configuration
    if mode == "WMS":
        # put here your user directory under the Dirac File Catalog
        job.base_path = "/vo.cta.in2p3.fr/user/f/fdipierro/Divergent-test6"
        # adjust start_run_number and run_number for testing, both can be 0
        job.start_run_number = "0"
        job.run_number = "1"
        job.setupWorkflow(debug=True)
        # submit to the WMS for debug, choose a destination site
        job.setDestination("LCG.IN2P3-CC.fr")
        # job.setDestination('LCG.DESY-ZEUTHEN.de')
        result = submit_wms(job)
    elif mode == "TS":
        # put here your user directory under the Dirac File Catalog
        job.base_path = "/vo.cta.in2p3.fr/MC/PROD5b"
        job.start_run_number = "0"
        job.run_number = "@{JOB_ID}"  # dynamic
        job.setupWorkflow(debug=False)
        # extra tag in case you have to run different tests, can be empty
        tag = ""
        # Change below the name of transformation, in particular the user name
        # this name must be unique accross the whole system
        trans_name = "Prod5b_divergent_{}_{}_{}_{}_{}{}".format(
            job.cta_site,
            job.particle,
            job.pointing_dir,
            job.zenith_angle,
            job.n_shower,
            tag,
        )
        result = submit_transformation(job, trans_name)
    else:
        DIRAC.gLogger.error(
            "1st argument should be the job mode: WMS or TS,\n\
                             not %s"
            % mode
        )
        return None

    return result


#########################################################
if __name__ == "__main__":
    arguments = Script.getPositionalArgs()
    if len(arguments) != 6:
        Script.showHelp()
    try:
        result = run_simulation(arguments)
        if not result["OK"]:
            DIRAC.gLogger.error(result["Message"])
            DIRAC.exit(-1)
        else:
            DIRAC.gLogger.notice("Done")
    except Exception:
        DIRAC.gLogger.exception()
        DIRAC.exit(-1)

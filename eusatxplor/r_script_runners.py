import subprocess
from logging_config import logger
import utils.constants as constants
import utils.utils as utils

def run_pca_script(alignment):

    logger.info(f"Running PCA umap for {alignment}")
    command = ['Rscript', './eusatxplor/r/pca_umap_plots.R',
                    "-a", alignment,
                    "-d", constants.DIMENSION_RED_MODE,
                    "-o", constants.PCA_UMAP_SAVE_ROOT]
    
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        logger.info(f"R script executed successfully for {alignment}.")
    else:
        logger.warning(f"Error executing R script for {alignment}. Return code:", result.returncode)
        logger.warning("STDERR:\n", result.stderr)
        quit()


    
def run_networks_script(distance_matrix):

    logger.info(f"Running networks {distance_matrix}")
    command = ['Rscript', './eusatxplor/r/network_plots.R',
                    "-a", constants.ARRAYS_OUT_PATH,
                    "-m", distance_matrix,
                    "-k", "5",
                    "-o", constants.NETWORKS_SAVE_ROOT]
    
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        logger.info(f"R script executed successfully for {distance_matrix}.")
    else:
        logger.info(f"Error executing R script for {distance_matrix}. Return code:", result.returncode)
        logger.info("STDERR:\n", result.stderr)

        
def run_flank_distances(flank_alignment):

    logger.info(f"Running flank alignment {flank_alignment}")
    command = ['Rscript', './eusatxplor/r/distance_maps.R',
                    "-a", flank_alignment,
                    "-o", constants.DISTANCE_SAVE_ROOT]
    
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"R script executed successfully for {flank_alignment}.")
    else:
        print(f"Error executing R script for {flank_alignment}. Return code:", result.returncode)
        print("STDERR:\n", result.stderr)


 
def run_microhomology():
    search_string = 'microhomology_aligned'
    matching_files = utils.get_files_containing_string(constants.FLANKS_SAVE_ROOT, search_string)
    print(matching_files)
    for mhl in matching_files:
        logger.info(f"Running flank alignment {mhl}")
        command = ['Rscript', './eusatxplor/r/microhomology_analysis.R',
                    "-a", mhl,
                    "-o", constants.MICROHOMOLOGY_SAVE_ROOT]
    
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"R script executed successfully for {mhl}.")
        else:
            logger.info(f"Error executing R script for {mhl}. Return code:", result.returncode)
            logger.info("STDERR:\n", result.stderr)
    

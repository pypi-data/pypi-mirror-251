import os
import sys
import subprocess
import platform

from cdh_dav_python.cdc_admin_service.environment_logging import LoggerSingleton

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class NpmClient:
    """
    A class representing a client for interacting with NPM.
    """

    @classmethod
    def install_node(cls, data_product_id, environment):
        """
        Install Node by running the npm install command.

        Returns:
            A subprocess.CompletedProcess object representing the result of the installation command.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("install_node"):
            try:
                if platform.system() == "Windows":
                    cls.install_node_windows()
                else:
                    print("This is not a Windows operating system.")

            except subprocess.CalledProcessError as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def install_node_windows():
        # Deactivate virtual environment if necessary
        # subprocess.call(["deactivate"], shell=True)

        # Change to the home directory
        os.chdir(os.path.expanduser("~"))

        # Uninstall nodeenv
        subprocess.call(["pip", "uninstall", "-y", "nodeenv"], shell=True)

        # Install Node.js (Requires manual download or a separate script to download and run the installer)

        # Install a specific version of npm if necessary
        # subprocess.call(["npm", "install", "npm@9.1.1", "-g"], shell=True)

        # Install nodeenv
        subprocess.call(["pip", "install", "nodeenv"], shell=True)

        # Install Mermaid CLI
        subprocess.call(["npm", "install", "@mermaid-js/mermaid-cli"], shell=True)

        # Test installations
        subprocess.call(["node", "-v"], shell=True)
        subprocess.call(["npm", "-v"], shell=True)
        subprocess.call(["mmdc", "-h"], shell=True)

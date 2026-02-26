import os
from composio_phidata import Action, ComposioToolSet
from utils import setup_logger

logger = setup_logger(__name__)

class StorageEngine:
    """
    Handles Google Docs and Composio initialization.
    """
    def __init__(self, composio_api_key: str):
        self.composio_api_key = composio_api_key
        try:
            self.toolset = ComposioToolSet(api_key=composio_api_key)
            self.google_docs_create = self.toolset.get_tools(actions=[Action.GOOGLEDOCS_CREATE_DOCUMENT])[0]
            self.google_docs_update = self.toolset.get_tools(actions=[Action.GOOGLEDOCS_UPDATE_EXISTING_DOCUMENT])[0]
            logger.info("StorageEngine initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize StorageEngine: {e}")
            raise e

    def get_create_tool(self):
        return self.google_docs_create

    def get_update_tool(self):
        return self.google_docs_update

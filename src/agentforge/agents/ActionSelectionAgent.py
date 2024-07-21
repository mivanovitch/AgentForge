from agentforge.agent import Agent


class StopExecution(Exception):
    """
    Custom exception to signal a stop in the agent's execution flow, particularly when no relevant action is found.
    """
    pass


class ActionSelectionAgent(Agent):
    def __init__(self, threshold: float = 0.6, num_results: int = 0) -> None:
        super().__init__()
        self.data: dict = {}
        self.threshold = threshold  # Threshold value for action selection.
        self.num_results = num_results  # Number of results to be considered in the action selection process.

    def run(self, **kwargs):
        """
        Executes the agent's run cycle with enhanced error handling to catch a StopExecution exception.

        Parameters:
            **kwargs: Arbitrary keyword arguments passed to the base run method.

        Returns: The output generated by the agent or None if a StopExecution exception is caught, indicating no
        relevant action was found.
        """
        try:
            return super().run(**kwargs)
        except StopExecution:
            self.logger.log('Stopped Action Selection', 'Info')
            return None

    def load_from_storage(self):
        """
        Loads actions based on the current object and specified criteria from the storage system.
        """
        action_list = {}
        try:
            action_list = self.agent_data['storage'].search_storage_by_threshold(collection_name='Actions',
                                                                                 query=self.data['objective'],
                                                                                 threshold=self.threshold,
                                                                                 num_results=self.num_results)
        except Exception as e:
            self.logger.log(f"Error loading actions: {e}", 'error')

        if not action_list:
            raise StopExecution("No actions found, stopping execution.")

        self.data['action_list'] = self.format_actions(action_list)
        # print(f'\nAction List:\n{self.data["action_list"]}\n')

    def format_actions(self, action_list):
        """
        Formats the actions into a human-readable string and stores it in the agent's data for later use.
        """
        try:
            formatted_actions = []
            parsed_actions = self.parse_actions(action_list)
            for action_name, metadata in parsed_actions.items():
                action_desc = metadata.get("Description", "No Description")
                formatted_action = f"Action: {action_name}\nDescription: {action_desc}\n"
                formatted_actions.append(formatted_action)
            return "\n".join(formatted_actions)
        except Exception as e:
            self.logger.log(f"Error Formatting Actions:\n{action_list}\n\nError: {e}", 'error')
            raise StopExecution("Error Formatting Actions, stopping execution.")

    def parse_actions(self, action_list):
        """
        Parses and structures the actions fetched from storage for easier handling and processing.
        """
        parsed_actions = {}
        try:
            for metadata in action_list.get("metadatas", []):
                action_name = metadata.get("Name")
                if action_name:
                    metadata.pop('timestamp', None)  # Remove any non-relevant metadata, such as timestamps
                    parsed_actions[action_name] = metadata
            return parsed_actions
        except Exception as e:
            self.logger.log(f"Error Parsing Actions:\n{action_list}\n\nError: {e}", 'error')
            raise StopExecution("Error Parsing Actions, stopping execution.")

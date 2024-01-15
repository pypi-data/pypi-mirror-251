import logging
from typing import Dict, List

from apna_python_experiment_sdk.defaults.sinks.mixpanel_sink import MixpanelExperimentSink
from .base.tracker import Tracker, Sink, Configuration
from .constants import ExperimentClients, Sinks
from .defaults import DefaultUnleashConf
from UnleashClient import UnleashClient
import logging
import atexit
# logging.getLogger().setLevel(logging.INFO)


class ApnaExperimentTracker(Tracker):
    """This class is the implmentation of the Tracker interface.
    This is used to fetch variants from the experiment_client (unleash).
    This class also internally tracks the variant information and the UserId
    to mixpanel and Bigquery via Rudderstack (one of the sinks).
    """
    client = None

    def __init__(self,
                 experiment_client_name: str = ExperimentClients.UNLEASH,
                 experiment_client_conf: 'Configuration' = DefaultUnleashConf,
                 sinks: List[Sink] = []):
        # 1. Initialize experiment_client:
        if self.client is None:
            self.exp_conf = experiment_client_conf()
            # TODO: Replace this with ExperimentClientFactory
            # Skipping for now as we are only using unleash as of now.
            self.client = UnleashClient(**self.exp_conf.get_conf())
            self.client.initialize_client()
            atexit.register(self.__close)
            logging.info(
                f'ApnaExperimentTracker and UnleashClient initialized!')

        # 2. Initialize Sinks:
        self.sinks = [sink() for sink in sinks]

    def __close(self):
        logging.info(
            f'ApnaExperimentTracker Object is being destroyed, flushing the sinks.')
        self._flush()

    def is_enabled(self, feature_name: str, context: Dict[str, str], track: bool = False) -> bool:
        """This method returns by calling `is_enabled` of the unleash client.

        Args:
            feature_name (str): Name of the feature (experiment).
            context (Dict[str, str]): Context to pass in the experimentation client.
            track (bool, optional): [description]. Defaults to False.

        Returns:
            bool: Returns true if the feature is enabled.
        """
        enabled: bool = self.client.is_enabled(
            feature_name=feature_name, context=context)

        # Track:
        if enabled and track is True:
            self._track({'feature': feature_name, 'context': context})

        return enabled

    def get_variant(self, feature_name: str, context: Dict[str, str], track: bool = True, **kwargs) -> bool:
        """This method calls `get_variant` method of unleash and returns it.
        NOTE: Call this method only if the is_enabled has returned true otherwise NotFoundException will
        be raised.

        Args:
            feature_name (str): Name of the feature (experiment).
            context (Dict[str, str]): Context to pass in the experimentation client.
            track (bool, optional): This flags determine whether to push to sink or not. Defaults to True.            

        Returns:
            bool: Returns true if the feature is enabled else false.
        """
        variant = self.client.get_variant(
            feature_name=feature_name, context=context)

        if track:
            self._track({'feature': feature_name, 'context': context,
                        'variant': variant, 'extra': kwargs})

        return variant

    def _track(self, data: dict, **kwargs) -> None:
        return super()._track(data, **kwargs)

    def _flush(self):
        """This method is used to flush all the buffers of all the sinks."""
        logging.info(
            f'Flushing all the sinks from ApnaPythonExperimentTracker.')
        for sink in self.sinks:
            logging.info(f'Flushing {sink} sink.')
            sink.flush()
            logging.info(f'{sink} sink - flushed successfully.')
        logging.info(f'All the sinks flushed successfully.')

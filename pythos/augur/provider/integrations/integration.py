

from abc import ABC, abstractmethod


#circular import
def get_interactive_providers():
    from provider.integrations.internal.market.market import InteractiveMarket

    return {
        'oracle': InteractiveMarket
    }

class InteractiveProvider(ABC):

    def __init__(self, provider_integration) -> None:
        self.provider_integration = provider_integration


    @property
    def capabilities(self):
        return self.provider_integration.capabilityoptions_set.all().values_list('value',flat=True)    


    @property
    def config_options(self):
        return self.provider_integration.config_options.all()   


    @abstractmethod
    def feasibility_search():
        pass

    @abstractmethod
    def archive_search():
        pass

    @abstractmethod
    def task_order():
        pass

    @abstractmethod
    def task_order_status():
        pass

    @abstractmethod
    def task_download():
        pass


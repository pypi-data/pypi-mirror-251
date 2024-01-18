# Class watchdog
class watchdog:
    # Initialize a watchdog instance
    def __init__(self, config: dict):
        self.config = config

    # A constructor-like function to init a watchdog instance
    @classmethod
    def init(cls, config: dict) -> 'watchdog':
        return cls(config)

# # Test block
# if __name__ == "__main__":
#     # Example dictionary as config
#     dictionary = {"key1": "value1", "key2": "value2"}
#
#     # Create a watchdog instance using the init method
#     model = watchdog.init(dictionary)
#
#     # Access and print the config attribute to verify it's working
#     print("model config:", model.config)

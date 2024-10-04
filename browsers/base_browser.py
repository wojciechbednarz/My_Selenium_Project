class BaseBrowser:
    def __init__(self, driver_path, base_url, service_class, options):
        self.driver = None
        self.driver_path = driver_path
        self.base_url = base_url
        self.service = service_class(executable_path=driver_path)
        self.options = options

    def __repr__(self):
        return f"{type(self).__name__} {self.base_url}"

    def _compare_service(self, other_service):
        # Since `executable_path` doesn't exist, compare relevant info (e.g., driver_path)
        return self.driver_path == other_service.path

    def _compare_options(self, other_options):
        # Assuming options is a class with some attributes like arguments
        return self.options.arguments == other_options.arguments

    def __eq__(self, other):
        if isinstance(other, BaseBrowser):
            return (
                    self.driver_path == other.driver_path and
                    self.base_url == other.base_url and
                    self._compare_service(other.service) and
                    self._compare_options(other.options)
            )
        return False

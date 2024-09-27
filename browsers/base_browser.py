class BaseBrowser:
    def __init__(self, driver_path, base_url, service_class, options):
        self.driver = None
        self.driver_path = driver_path
        self.base_url = base_url
        self.service = service_class(executable_path=driver_path)
        self.options = options

    def __repr__(self):
        return f"{type(self).__name__} {self.base_url}"

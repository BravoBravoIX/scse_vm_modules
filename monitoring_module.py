import psutil
import logging
import time

class MonitoringModule:
    def __init__(self, interval=60):
        """
        Initialize the monitoring module with the specified interval in seconds.
        """
        self.interval = interval
        self.setup_logging()
    
    def setup_logging(self):
        """
        Set up the logging configuration for the module.
        """
        logging.basicConfig(filename='monitoring_module.log', level=logging.INFO,
                            format='%(asctime)s %(levelname)s: %(message)s')
    
    def log_system_metrics(self):
        """
        Log system metrics such as CPU, memory, and disk usage.
        """
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')
        
        logging.info(f'CPU Usage: {cpu_usage}%')
        logging.info(f'Memory Usage: {memory_info.percent}%')
        logging.info(f'Disk Usage: {disk_usage.percent}%')

    def start_monitoring(self):
        """
        Start the monitoring process.
        """
        while True:
            self.log_system_metrics()
            time.sleep(self.interval)

# Example usage:
if __name__ == "__main__":
    monitor = MonitoringModule(interval=10)
    monitor.start_monitoring()

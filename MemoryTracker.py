from plyer import notification
import psutil
import time

CHECK_INTERVAL = 15


class MemoryTracker:
    def __init__(self):
        self.previous_state = {
            'high_memory': False,
            'critical_memory': False,
        }
        self.high_memory_percent = 80
        self.critical_memory_percent = 90
        self.notification_icon = None
        self.notification_timeout = 10
        pass

    def tick(self):
        # calculate current memory percentage
        memory_stats = psutil.virtual_memory()
        swap_stats = psutil.swap_memory()
        total_memory = memory_stats.total + swap_stats.total
        used_memory = memory_stats.used + swap_stats.used
        percentage = used_memory / total_memory * 100
        print(f"Memory usage: {round(percentage, 4)}%", flush=True)

        # check critical memory first
        if percentage >= self.critical_memory_percent:
            if not self.previous_state['critical_memory']:
                self.previous_state['critical_memory'] = True
                self.previous_state['high_memory'] = True
                self.alert_critical_memory()
        elif percentage >= self.high_memory_percent:
            if not self.previous_state['high_memory']:
                self.previous_state['critical_memory'] = False
                self.previous_state['high_memory'] = True
                self.alert_high_memory()

        return

    def alert_high_memory(self):
        notification.notify(
            title='High Memory Alert',
            message=f'Memory usage exceeded {self.high_memory_percent}%!',
            app_icon=self.notification_icon,
            timeout=self.notification_timeout,
        )
        return

    def alert_critical_memory(self):
        notification.notify(
            title='Critical Memory Alert',
            message=f'Memory usage exceeded {self.critical_memory_percent}%!',
            app_icon=self.notification_icon,
            timeout=self.notification_timeout,
        )


if __name__ == '__main__':
    print("This is WIP, it will hold onto the cmd instance until you abort this script.")
    tracker = MemoryTracker()
    while True:
        tracker.tick()
        time.sleep(CHECK_INTERVAL)

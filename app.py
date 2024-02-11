"""
An application to help optimize your workout efficiency.
"""
import time
from threading import Timer
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class MagCoIntervalTimer(toga.App):
    def startup(self):
        # Create the main box to hold UI elements
        self.main_box = toga.Box(style=Pack(direction=COLUMN))

        # Create the start button
        self.start_button = toga.Button('Start', on_press=self.start_timer)

        # Create the stop button
        self.stop_button = toga.Button('Stop', on_press=self.stop_timer)

        # Create the label to display elapsed time
        self.timer_label = toga.Label('00:00:00')  # Initial label includes centiseconds

        # Create a box to hold the buttons
        button_box = toga.Box(style=Pack(direction=ROW))
        button_box.add(self.start_button)
        button_box.add(self.stop_button)

        # Add the buttons and label to the main box
        self.main_box.add(button_box)
        self.main_box.add(self.timer_label)

        # Create the main window and set its content
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()

        # Initialize timer variables
        self.interval = 0.01  # Timer interval in seconds (1 centisecond)
        self.running = False
        self.elapsed_time = 0

    def start_timer(self, widget):
        # Set running flag to True
        self.running = True
        # Get the current time in centiseconds
        self.start_time = time.time()
        # Start the timer loop
        self.timer_loop()

    def stop_timer(self, widget):
        # Set running flag to False
        self.running = False

    def timer_loop(self):
        if self.running:
            # Calculate elapsed time in centiseconds
            current_time = time.time()
            elapsed_time_cs = int((current_time - self.start_time) * 100)
            # Convert centiseconds to minutes, seconds, and centiseconds
            minutes = elapsed_time_cs // 6000
            seconds = (elapsed_time_cs // 100) % 60
            centiseconds = elapsed_time_cs % 100
            # Update the label text with formatted time
            self.timer_label.text = f'{minutes:02}:{seconds:02}:{centiseconds:02}'
            # Schedule the next timer loop iteration
            Timer(self.interval, self.timer_loop).start()

def main():
    return MagCoIntervalTimer()

if __name__ == '__main__':
    app = main()
    app.main_loop()

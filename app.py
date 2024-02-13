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

        # Create the start button for regular timer
        self.start_button = toga.Button('Start Timer', on_press=self.start_timer)

        # Create the stop button for regular timer
        self.stop_button = toga.Button('Stop Timer', on_press=self.stop_timer)

        # Create the label to display elapsed time for regular timer
        self.timer_label = toga.Label('00:00:00', style=Pack(font_size=48))  # Initial label includes centiseconds

        # Create the start button for countdown timer
        self.start_countdown_button = toga.Button('Start Countdown', on_press=self.start_countdown)

        # Create the stop button for countdown timer
        self.stop_countdown_button = toga.Button('Stop Countdown', on_press=self.stop_countdown)

        # Create the label to display remaining time for countdown timer
        self.countdown_label = toga.Label('00:00:00', style=Pack(font_size=72))  # Larger font size for countdown timer

        # Create buttons for adjusting countdown duration for minutes
        self.up_minutes_button = toga.Button('↑', on_press=self.increase_minutes)
        self.down_minutes_button = toga.Button('↓', on_press=self.decrease_minutes)

        # Create buttons for adjusting countdown duration for seconds
        self.up_seconds_button = toga.Button('↑', on_press=self.increase_seconds)
        self.down_seconds_button = toga.Button('↓', on_press=self.decrease_seconds)

        # Create boxes to hold the buttons and labels for countdown timer controls
        minutes_control_box = toga.Box(style=Pack(direction=ROW, padding_top=10, padding_bottom=10))
        minutes_control_box.add(self.up_minutes_button)
        minutes_control_box.add(self.countdown_label)
        minutes_control_box.add(self.down_minutes_button)

        seconds_control_box = toga.Box(style=Pack(direction=ROW, padding_top=10, padding_bottom=10))
        seconds_control_box.add(self.up_seconds_button)
        seconds_control_box.add(self.countdown_label)
        seconds_control_box.add(self.down_seconds_button)

        # Create a box to hold the buttons and label for regular timer
        timer_box = toga.Box(style=Pack(direction=ROW))
        timer_box.add(self.start_button)
        timer_box.add(self.stop_button)

        # Add the buttons, labels, and input for both regular timer and countdown timer to the main box
        self.main_box.add(timer_box)
        self.main_box.add(self.timer_label)

        # Create a box to hold the buttons and label for countdown timer
        countdown_box = toga.Box(style=Pack(direction=ROW))
        countdown_box.add(self.start_countdown_button)
        countdown_box.add(self.stop_countdown_button)

        # Add the buttons and label for countdown timer to the main box
        self.main_box.add(countdown_box)
        self.main_box.add(minutes_control_box)
        self.main_box.add(seconds_control_box)

        # Create the main window and set its content
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()

        # Initialize timer variables for regular timer
        self.interval = 0.01  # Timer interval in seconds (1 centisecond)
        self.running = False
        self.elapsed_time = 0

        # Initialize timer variables for countdown timer
        self.countdown_running = False
        self.countdown_duration = 0
        self.countdown_start_time = 0

    def start_timer(self, widget):
        # Set running flag to True
        self.running = True
        # Get the current time in centiseconds
        self.start_time = time.time()
        # Start the regular timer loop
        self.timer_loop()

    def stop_timer(self, widget):
        # Set running flag to False
        self.running = False

    def start_countdown(self, widget):
        # Set countdown running flag to True
        self.countdown_running = True
        # Get the current time
        self.countdown_start_time = time.time()
        # Start the countdown timer loop
        self.countdown_loop()

    def stop_countdown(self, widget):
        # Set countdown running flag to False
        self.countdown_running = False

    def timer_loop(self):
        if self.running:
            # Calculate elapsed time in centiseconds
            current_time = time.time()
            elapsed_time_cs = int((current_time - self.start_time) * 100)
            # Convert centiseconds to minutes, seconds, and centiseconds
            minutes = elapsed_time_cs // 6000
            seconds = (elapsed_time_cs // 100) % 60
            centiseconds = elapsed_time_cs % 100
            # Update the label text with formatted time for regular timer
            self.timer_label.text = f'{minutes:02}:{seconds:02}:{centiseconds:02}'
            # Schedule the next timer loop iteration
            Timer(self.interval, self.timer_loop).start()

    def countdown_loop(self):
        if self.countdown_running:
            # Calculate remaining time in countdown
            current_time = time.time()
            remaining_time = max(0, self.countdown_duration - (current_time - self.countdown_start_time))
            # Convert remaining time to minutes and seconds
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            # Update the label text with formatted time for countdown timer
            self.countdown_label.text = f'{minutes:02}:{seconds:02}'
            if remaining_time > 0:
                # Schedule the next countdown loop iteration
                Timer(1, self.countdown_loop).start()
            else:
                # Countdown finished
                self.countdown_label.text = "Countdown Finished"

    def increase_minutes(self, widget):
        # Increase the countdown duration by 60 seconds (1 minute)
        self.countdown_duration += 60
        # Update the countdown label with the new duration
        self.update_countdown_label()

    def decrease_minutes(self, widget):
        # Decrease the countdown duration by 60 seconds (1 minute), ensuring it does not go below 0
        if self.countdown_duration >= 60:
            self.countdown_duration -= 60
            # Update the countdown label with the new duration
            self.update_countdown_label()

    def increase_seconds(self, widget):
        # Increase the countdown duration by 1 second
        self.countdown_duration += 1
        # Update the countdown label with the new duration
        self.update_countdown_label()

    def decrease_seconds(self, widget):
        # Decrease the countdown duration by 1 second, ensuring it does not go below 0
        if self.countdown_duration > 0:
            self.countdown_duration -= 1
            # Update the countdown label with the new duration
            self.update_countdown_label()

    def update_countdown_label(self):
        # Convert countdown duration to minutes and seconds
        minutes = self.countdown_duration // 60
        seconds = self.countdown_duration % 60
        # Update the countdown label text with formatted time
        self.countdown_label.text = f'{minutes:02}:{seconds:02}'

def main():
    return MagCoIntervalTimer()

if __name__ == '__main__':
    app = main()
    app.main_loop()






#NEXT STEPS

# Center the timer on the screen
# Add functions for sets/reps
# Add a count down timer function (most important part)
# Add another timer for rest time
# Connect these 3 with conditons, etc
# 

import wpilib

from robotpy_rev_digit import RevDigitBoard

I2C_DEV_ADDR = 0x70
TEST_PATTERN = "   ABCDEFGHIJKLMNOPQRSTUVWXYZ*?@#   "


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.rev_digit = RevDigitBoard()
        self.timer = wpilib.Timer()
        self.robot = wpilib.RobotController

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        pass

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        pass

    def teleopInit(self):
        """This function is called periodically during operator control."""
        self.timer.start()

    def teleopPeriodic(self):
        """This function is called periodically during autonomous."""
        time = self.timer.get()
        idx = int(time // 1) % len(TEST_PATTERN)
        text = TEST_PATTERN[idx:]
        voltage = self.rev_digit.potentiometer

        # If neither button is pressed, show the timer
        if self.rev_digit.button_a and self.rev_digit.button_b:
            self.rev_digit.display_message(time)
        # If Button A is pressed, display the battery voltage
        elif not self.rev_digit.button_a:
            self.rev_digit.display_message(voltage)
        # If Button B is pressed, display the test pattern
        elif not self.rev_digit.button_b:
            self.rev_digit.display_message(text)

    def teleopExit(self):
        """This function is called when teleop ends."""
        self.timer.stop()

    def disabledPeriodic(self):
        """This function is called periodically when the robot is disabled"""
        voltage = self.robot.getBatteryVoltage()
        self.rev_digit.display_message(voltage)


if __name__ == "__main__":
    wpilib.run(MyRobot)

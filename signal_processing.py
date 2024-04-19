from numpy import angle
import math
import asyncio

# S11 phase throttle parameters
UPPER_PHASE_LIM = 0.8 * math.pi
LOWER_PHASE_LIM = 0.1 * math.pi
K = 1 / (LOWER_PHASE_LIM - UPPER_PHASE_LIM)
M = 1 - (LOWER_PHASE_LIM) / (LOWER_PHASE_LIM - UPPER_PHASE_LIM)
UPPER_VAL_LIM = 2.0  # Needs to be calibrated
# Direction parameters


class SignalProcessing:
    def __init__(self, data_queue, verbose=False):
        self.data_queue = data_queue  # The queue from which to consume data
        self.verbose = verbose

    async def process_data_continuously(self):
        while True:
            s11_data, s21_data = await self.data_queue.get()
            # Process the data using existing 
            phase = self.process_throttle_phase(s11_data)
            direction = self.process_direction(s11_data, s21_data)
            if self.verbose:
                print(f"Processed phase: {phase}, direction: {direction}")
            self.data_queue.task_done()
            await asyncio.sleep(2)

    @staticmethod
    def process_throttle_phase(s11_data):
        # TODO: Handle faulty input and output data. 
        # Calculates the the S11 phase and uses that to determine the throttle. 
        phase = angle(s11_data)
        output = K * phase + M
        val = abs(s11_data)

        if phase < LOWER_PHASE_LIM:
            output = 1
        elif (phase > UPPER_PHASE_LIM) or (val < UPPER_VAL_LIM):
            output = 0

        return output

    @staticmethod
    def process_direction(s11_data, s21_data):
        # TODO: Handle faulty input and output data. 
        # S11 and S21 added.
        s11_val = abs(s11_data)
        s21_val = abs(s21_data)

        output = s11_val / s21_val
        # Need to look at data to do more.

        return output
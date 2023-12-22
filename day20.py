from abc import ABC, abstractmethod
from enum import Enum
from collections import deque, defaultdict
from dataclasses import dataclass


class PulseStrength(Enum):
    HIGH = 1
    LOW = 0

    def __repr__(self):
        return self.name


@dataclass
class Pulse():
    source: str
    dest: str
    strength: PulseStrength


class Module:
    def __init__(self, destinations):
        self.destinations = destinations

    def send_pulse(self, pulse: Pulse, pulse_queue: deque[Pulse]):
        pulse_queue.appendleft(pulse)

    @abstractmethod
    def receive_pulse(self, pulse: Pulse, pulse_queue: deque[Pulse]):
        pass

    def __repr__(self):
        return type(self).__name__ + self.destinations.__repr__()


class Broadcast(Module):
    def receive_pulse(self, pulse: Pulse, pulse_queue: deque[Pulse]):
        for d in self.destinations:
            self.send_pulse(Pulse('broadcaster', d, pulse.strength),
                            pulse_queue)


class FlipFlop(Module):
    def __init__(self, destinations):
        super().__init__(destinations)
        self.state = False

    def receive_pulse(self, pulse: Pulse, pulse_queue: deque[Pulse]):
        if pulse.strength == PulseStrength.LOW:
            self.state = not self.state
            out_strength = PulseStrength.HIGH if self.state else PulseStrength.LOW
            for d in self.destinations:
                self.send_pulse(
                    Pulse(pulse.dest, d, out_strength), pulse_queue)


class Conjunction(Module):
    def __init__(self, destinations):
        super().__init__(destinations)
        self.state = {}

    def init_state(self, source):
        self.state[source] = PulseStrength.LOW

    def receive_pulse(self, pulse: Pulse, pulse_queue: deque[Pulse]):
        self.state[pulse.source] = pulse.strength
        all_high = True
        for s in self.state:
            if self.state[s] == PulseStrength.LOW:
                all_high = False
                break
        if part2 == True and pulse.dest == 'zh':
            for s in self.state:
                if self.state[s] == PulseStrength.HIGH:
                    print(s, 'is high at', ps, 'in press', presses)
        out_strength = PulseStrength.LOW if all_high else PulseStrength.HIGH
        for d in self.destinations:
            self.send_pulse(Pulse(pulse.dest, d, out_strength), pulse_queue)


presses = 0
ps = 0


class System():
    button_queue = deque()
    pulse_queue = deque()
    modules = defaultdict(Module)
    output = []
    low_pulses, high_pulses = 0, 0

    def __init__(self, input_str: str):
        for line in input_str.splitlines():
            m_type, d_str = line.split(' -> ')
            d_list = d_str.split(', ')
            if m_type == 'broadcaster':
                self.modules['broadcaster'] = Broadcast(d_list)
            elif m_type[0] == '%':
                self.modules[m_type[1:]] = FlipFlop(d_list)
            else:
                self.modules[m_type[1:]] = Conjunction(d_list)
        self.init_conjunctions_()

    def __call__(self):
        while self.button_queue:
            self.press_button()
            while self.pulse_queue:
                self.process_pulse()

    def init_conjunctions_(self):
        for m in self.modules:
            for d in self.modules[m].destinations:
                if d in self.modules and isinstance(self.modules[d], Conjunction):
                    self.modules[d].init_state(m)

    def press_button(self):
        if part2:
            global presses
            presses += 1
            global ps
            ps = 0
        pulse = self.button_queue.pop()
        self.track_pulse(pulse)
        self.modules['broadcaster'].receive_pulse(pulse, self.pulse_queue)

    def process_pulse(self):
        pulse = self.pulse_queue.pop()
        self.track_pulse(pulse)
        if pulse.dest in self.modules:
            self.modules[pulse.dest].receive_pulse(pulse, self.pulse_queue)
        else:
            self.output.append(pulse)

    def queue_button_press(self, n: int):
        for _ in range(n):
            self.button_queue.appendleft(
                Pulse('button', 'broadcaster', PulseStrength.LOW))

    def track_pulse(self, pulse: Pulse):
        print_pulses = False
        if part2:
            global ps
            ps += 1
        if pulse.strength == PulseStrength.LOW:
            self.low_pulses += 1
        else:
            self.high_pulses += 1
        if print_pulses:
            print(pulse)

    def __repr__(self):
        out_s = ""
        for m in self.modules:
            out_s += m + ': ' + self.modules[m].__repr__() + '\n'
        return out_s


part2 = False

with open('inputs/day20', 'r') as f:
    s = f.read()
    system = System(s)
    print(system)
    system.queue_button_press(1000)
    system()
    print(system.low_pulses)
    print(system.high_pulses)

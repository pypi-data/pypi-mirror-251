# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring
# pylint: disable=fixme

import signal
import blessed


UL_CORNER = "\u2554"
UR_CORNER = "\u2557"
LL_CORNER = "\u255A"
LR_CORNER = "\u255D"
UPPER = "\u2550"
LOWER = "\u2550"
LEFT = "\u2551"
RIGHT = "\u2551"
HORIZONTAL_SEPARATOR = "\u2500"

ONLINE_ANIMATION_TRIANGLE_1 = "▲"
ONLINE_ANIMATION_TRIANGLE_2 = "▶"
ONLINE_ANIMATION_TRIANGLE_3 = "▼"
ONLINE_ANIMATION_TRIANGLE_4 = "◀"
ONLINE_ANIMATION_HEXAGON_1 = "⎔"
ONLINE_ANIMATION_HEXAGON_2 = "⌬"
ONLINE_ANIMATION_HEXAGON_3 = "⏣"
ONLINE_ANIMATION_WHALE_1 = "🐋"
ONLINE_ANIMATION_WHALE_2 = "🐳"


# TODO: docstrings
class Window:
    def __init__(
        self,
        terminal,
        percent_x,
        percent_y,
        percent_width,
        percent_height,
        title="",
        color=None,
        indent=2,
        top_margin=1,
        bottom_margin=1,
    ):
        self._t = terminal
        self.percent_x = percent_x
        self.percent_y = percent_y
        self.percent_width = percent_width
        self.percent_height = percent_height
        self.indent = indent
        self.top_margin = top_margin
        self.bottom_margin = bottom_margin
        self.title = title
        # calculate absolute values, needs to be recalled if window size or above values change
        self._calculate_dimensions()

        self._text = []
        self.next_line = 1
        if color is None:
            self._color = ""
        else:
            self._color = getattr(terminal, color)

    def _calculate_dimensions(self):
        """(Re-)calculate all absolute geometry values from the percenteages."""
        # cache the terminal's dimension to make sure they do not change during execution of this function
        width = self._t.width
        height = self._t.height
        # transform the percentage values in integer coordinates. int() will always round down here
        self._pos_x = int(width * self.percent_x)
        self._pos_y = int(height * self.percent_y)
        # the following calculation of the extent values (lower left corner of the window) makes sure that bordering
        # windows will neither overlap, nor have a gap - and that we use the full screen if x+width=100%
        self._extent_x = int(width * (self.percent_x + self.percent_width)) - 1
        self._extent_y = int(height * (self.percent_y + self.percent_height)) - 1
        self._width = self._extent_x - self._pos_x + 1
        self._height = self._extent_y - self._pos_y + 1
        # boundaries for text inside the window
        self._print_min_x = self._pos_x + 1 + self.indent
        self._print_min_y = self._pos_y + 1 + self.top_margin
        self._print_width = self._width - 2 - 2 * self.indent
        self._print_max_x = self._extent_x - 1 - self.indent
        self._print_max_y = self._extent_y - 1 - self.bottom_margin
        self._max_lines = self._print_max_y - self._print_min_y + 1

    def resize(self):
        """Update and redraw the window after the terminal's or the window's dimensions have changed."""
        self._calculate_dimensions()
        self.draw()

    @property
    def terminal(self):
        return self._t

    @property
    def pos_x(self):
        return self._pos_x

    @property
    def pos_y(self):
        return self._pos_y

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def extent_x(self):
        return self._extent_x

    @property
    def extent_y(self):
        return self._extent_y

    @property
    def max_lines(self):
        return self._max_lines

    @property
    def print_width(self):
        return self._print_width

    @property
    def color(self):
        return self._color

    def _draw_border(self):
        print(self._color)
        print(self._t.move_xy(self._pos_x, self._pos_y) + UL_CORNER, end="")
        print((self._width - 2) * UPPER, end="")  # upper border
        print(UR_CORNER, end="")
        for _ in range(self._height - 2):  # left border
            print(self._t.move_x(self._pos_x) + self._t.move_down(1) + LEFT, end="")
        print(self._t.move_x(self._pos_x) + self._t.move_down(1) + LL_CORNER, end="")
        print((self._width - 2) * LOWER, end="")  # lower border
        print(LR_CORNER, end="")
        for _ in range(self._height - 2):  # right border
            print(self._t.move_x(self._extent_x) + self._t.move_up(1) + RIGHT, end="")
        print(self._t.normal, end="")

    def _print_title(self):
        title_ident = 1
        max_title_length = self._width - 2 - title_ident
        if max_title_length > 0:
            print(self._t.move_xy(self._pos_x + 2, self._pos_y) + " ", end="")
            print(self._color + self._t.bold, end="")
            print(self._t.truncate(self.title, width=max_title_length - 2), end="")
            print(" ", end="")
            print(self._t.normal, end="")

    def clear_text(self):
        self._text = []
        self.next_line = 1

    def add_text(self, text, line="next"):
        # returns the line number in which the text was added
        if line == "next":
            self._text.append(text)
            line = len(self._text)
        else:
            if line < 1:
                raise Exception("Minimum line number is 1.")
            # Append empty lines, if line number is beyond current length
            while line > len(self._text):
                self._text.append("")
            self._text[line - 1] = text
        self.next_line = len(self._text) + 1
        return line

    def _print_line(self, line):
        if line <= len(self._text):
            line_text = self._text[line - 1]
        else:
            line_text = ""
        formatted_text = self._t.truncate(line_text, width=self._print_width)
        padding = self._print_width - self._t.length(formatted_text)
        formatted_text = formatted_text + padding * " "
        print(self._t.move_xy(self._print_min_x, self._print_min_y + line - 1), end="")
        print(self._color + formatted_text + self._t.normal, end="")

    def _print_text(self):
        for line in range(1, self._max_lines + 1):
            self._print_line(line)

    def update_text(self):
        self._print_text()

    def draw(self):
        self._draw_border()
        self._print_title()
        self._print_text()
        print(self._t.move_xy(0, 0))


# --- end of window class --------------------------------------


def _print_box_status(status, window):
    window.clear_text()
    window.add_text("Name: " + status["box"]["Name"])
    if status["network"]:
        window.add_text(
            "Network: "
            + status["network"]["Name"]
            + " ("
            + status["network"]["Short ID"]
            + "), "
            + "Gateway: "
            + status["network"]["Gateway"]
            + ", "
            + "Subnet: "
            + status["network"]["Subnet"]
        )
    window.add_text("Bind volume base path: " + status["box"]["Bind volume base path"])
    window.update_text()


def _print_container_status(container_status, window):
    window.clear_text()
    if container_status:
        key_width = 1 + max(len(k) for k, v in container_status.items() if not isinstance(v, (list, tuple)))
        for key, value in container_status.items():
            key += ":"
            if isinstance(value, (list, tuple)):  #  value is an array type and needs to be printed as a list
                window.add_text(key)
                for elem in value:
                    if isinstance(elem, (list, tuple)):
                        # print first element normally, further elements as comma-separated list in parantheses
                        window.add_text("   " + elem[0] + " (" + ", ".join(elem[1:]) + ")")
                    else:
                        window.add_text("   " + elem)
            else:
                window.add_text(f"{key:{key_width}} {value}")
    window.update_text()


def _print_mounts_status(mounts_status, window):
    term = window.terminal
    window.clear_text()
    if not mounts_status:
        window.update_text()
        return
    # get field names and maximuma length for each field
    fields = list(mounts_status[0].keys())
    field_widths = [None] * len(fields)
    for i, fieldname in enumerate(fields):
        field_widths[i] = max(len(mount[fieldname]) for mount in mounts_status)
        field_widths[i] = max(len(fields[i]), field_widths[i])
    # scale down if window is not large enough
    table_width = sum(field_widths) + len(fields) - 1  # assuming min spacing of 1 between columns
    if table_width > window.print_width:
        scaling_factor = window.print_width / table_width
    else:
        scaling_factor = 1.0
    scaled_field_widths = [round(fw * scaling_factor) for fw in field_widths]
    table_width = sum(scaled_field_widths) + len(fields) - 1
    # make sure we use the entire space, but also not more (may otherwise happen due to rounding)
    if scaling_factor < 1.0 and table_width < window.print_width:
        to_increase = scaled_field_widths.index(min(scaled_field_widths))
        scaled_field_widths[to_increase] += window.print_width - table_width
    if table_width > window.print_width:
        to_decrease = scaled_field_widths.index(max(scaled_field_widths))
        scaled_field_widths[to_decrease] -= table_width - window.print_width
    table_width = sum(scaled_field_widths) + len(fields) - 1
    # determine the spacing between the columns
    maximum_spacing = int((window.print_width - table_width) / (len(fields) - 1))
    spacing = max(1, min(4, maximum_spacing))
    spacing_str = " " * spacing
    table_width = sum(scaled_field_widths) + spacing * (len(fields) - 1)
    # create an string.format pattern wich we can use to print each table line
    # This will yield something like: '{0: <10.10} {1: <5.5} {2: <6.6} {3: <4.4}'
    table_row_format = spacing_str.join(
        "{" + str(i) + ": <" + str(w) + "." + str(w) + "}" for i, w in enumerate(scaled_field_widths)
    )

    # print header line
    header = table_row_format.format(*fields)
    header = header + " " * (window.print_width - len(header))
    window.add_text(term.underline + header + term.normal)
    # print table entries
    for mnt in mounts_status:
        window.add_text(table_row_format.format(*mnt.values()))
    # TODO: refactor table printing into a separate function
    window.update_text()


def _get_next_online_animation_char(old_char, icon):
    if icon == "triangle":
        if old_char == ONLINE_ANIMATION_TRIANGLE_1:
            return ONLINE_ANIMATION_TRIANGLE_2
        if old_char == ONLINE_ANIMATION_TRIANGLE_2:
            return ONLINE_ANIMATION_TRIANGLE_3
        if old_char == ONLINE_ANIMATION_TRIANGLE_3:
            return ONLINE_ANIMATION_TRIANGLE_4
        return ONLINE_ANIMATION_TRIANGLE_1
    if icon == "hexagon":
        if old_char == ONLINE_ANIMATION_HEXAGON_1:
            return ONLINE_ANIMATION_HEXAGON_2
        if old_char == ONLINE_ANIMATION_HEXAGON_2:
            return ONLINE_ANIMATION_HEXAGON_3
        return ONLINE_ANIMATION_HEXAGON_1
    if icon == "whale":
        if old_char == ONLINE_ANIMATION_WHALE_1:
            return ONLINE_ANIMATION_WHALE_2
        return ONLINE_ANIMATION_WHALE_1
    raise Exception("Unknown icon type for online animation.")


def _print_online_animation(term, char, pos_x=0, pos_y=0, icon="triangle"):
    char = _get_next_online_animation_char(char, icon)
    print(term.move_xy(pos_x, pos_y), end="")
    print(char + " ")
    return char


def _print_help(term, pos_x=3, pos_y="bottom"):
    if pos_y == "bottom":
        pos_y = term.height
    print(term.move_xy(pos_x, pos_y), end="")
    print(" (Q)uit ", end="")


def show_status_screen(box, main_color=None):
    term = blessed.Terminal()

    with term.fullscreen(), term.hidden_cursor(), term.cbreak():
        # TODO: title window too easily hides relevant info (network name) when not in fullscreen mode
        title_win = Window(term, 0, 0, 1, 0.15, "  DindBox", main_color)
        build_container_win = Window(term, 0, 0.15, 0.495, 0.55, "Build Container", main_color)
        service_container_win = Window(term, 0.505, 0.15, 0.495, 0.55, "Service Container", main_color)
        bottom_win = Window(term, 0, 0.7, 1, 0.3, "Mounts", main_color)
        title_win.draw()
        build_container_win.draw()
        service_container_win.draw()
        bottom_win.draw()
        _print_help(term)

        # flags that can be modified by callbacks
        flags = {"resize_requested": False}

        def _on_resize(_sig, _action):
            # Since resizing is slow and prone to messy behaviour when several resize operation overlap, we only set
            # a flag, and do the actual resizing every second only, as part of the general waiting-for-input loop.
            # Flag needs to be part of a dict, a simple boolean would not propagate changes to the outer scope.
            flags["resize_requested"] = True

        signal.signal(signal.SIGWINCH, _on_resize)

        pressed_key = ""
        online_animation_char = ""
        while pressed_key.lower() != "q":
            # TODO: more command keys (start, stop, remove)
            # TODO: make certain status checks (running containers?) not at every iteration, if they are slow
            #       (needs checking if helpful and necessary). Consider using a parallel thread.
            status = box.status()
            if flags["resize_requested"]:
                flags["resize_requested"] = False
                print(term.clear)
                title_win.resize()
                build_container_win.resize()
                service_container_win.resize()
                bottom_win.resize()
                _print_help(term)
            online_animation_char = _print_online_animation(term, online_animation_char, 3, 0)
            _print_box_status(status, title_win)
            _print_container_status(status["build_container"], build_container_win)
            _print_container_status(status["service_container"], service_container_win)
            _print_mounts_status(status["mounts"], bottom_win)
            pressed_key = term.inkey(timeout=1)


# if this module is called directly, show a status screen with dummy values in order to test its functionality
if __name__ == "__main__":

    class TestDindBox:
        # a dummy version of the DindBox class which only knows the status() method and returns static dummy data
        @staticmethod
        def status():
            test_status = {}
            test_status["box"] = {"Name": "my_DindBox", "Bind volume base path": "/foo/bar"}
            test_status["build_container"] = {
                "Name": "my_build_container",
                "Image": "alpine:test",
                "Short ID": "abcdefgh",
                "Status": "exited",
                "IP": "192.168.7.3",
                "Running Processes": ["setup.sh", "/usr/bin/apt", "run_me.exe"],
                "Environment": [
                    "HOME=/root",
                    "DEBUG=1",
                    "SERVICE_CONTAINER=my_service_container",
                ],
            }
            test_status["service_container"] = {
                "Name": "my_service_container",
                "Image": "docker:dind",
                "Short ID": "uvwxyzabc",
                "Status": "running",
                "IP": "192.168.7.2",
                # 'DinD Containers': ['adam', 'eve','johnny'],
                "DinD Containers": [
                    ["adam", "Up 2 days"],
                    ["eve", "Restarting", "'cause it's cool"],
                    "johnny",
                ],
                "Environment": ["HOME=/root", "DEBUG=1"],
            }
            test_status["network"] = {
                "Name": "my_network",
                "Short ID": "hijklmnop",
                "Subnet": "192.168.7.0/24",
                "Gateway": "192.168.7.1",
            }
            test_status["mounts"] = [
                {
                    "Source": "my_volume",
                    "Target": "/config",
                    "Type": "Docker volume",
                    "Auto-remove": "yes",
                },
                {
                    "Source": "/tmp/dindbox/foobar",
                    "Target": "/srv/foobar",
                    "Type": "Bind volume",
                    "Auto-remove": "yes",
                },
                {
                    "Source": "/home/user/workdir",
                    "Target": "/mnt",
                    "Type": "Bind mount",
                    "Auto-remove": "no",
                },
            ]
            return test_status

    testbox = TestDindBox()
    show_status_screen(testbox)

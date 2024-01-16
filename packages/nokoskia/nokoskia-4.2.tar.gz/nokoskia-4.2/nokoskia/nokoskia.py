import curses 
from curses import wrapper
import time

def get_terminal_size(stdscr):
    # Get terminal size
    height, width = stdscr.getmaxyx()
    return height, width

def knock():
    def main(stdscr):

        # Check if the terminal supports colors
        curses.start_color()
        # Define color pairs (foreground, background)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_YELLOW)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLUE)
        curses.curs_set(0)
            
        stdscr.clear();
        stdscr.refresh();
            
        # adding the co-ordinates to be the top-left corner as default.
        x = 0;
        y = 0;
        start = True;
        # splitting the dialogue into two variables making it easy to change the color of the sentences in the sameline.
        part1 = "I am the One Who ";
        part2 = "KNOCKS."
        

        # making the loop always true to give it a infinite behaviour.
        try:
            while start:
                # getting the size of the terminal window, to avoid error like "characters out of the visible area error"
                height, width = get_terminal_size(stdscr);
                center_x = int(height/2);
                center_y = int(width/2);
                width = width - len(part1+part2);
                # checking whether the line is within the visible area.
                if x < height and y < width :
                    stdscr.addstr(x, y, part1, curses.color_pair(1))
                    stdscr.addstr(x, y + len(part1), part2, curses.color_pair(2) | curses.A_BOLD)
                    x = x+1;
                    second = len(part1+part2);
                    stdscr.refresh();
                    # if the line is going to outside the visible area, then:
                elif y < width :
                    # erase the screen and start from the beginning.
                    stdscr.erase();
                    x = 0;
                    y = (y + second); # Loop horizontally=second
                else:
                    stdscr.erase();
                    stdscr.addstr(center_x,center_y, "NoW sAy My NaMe", curses.color_pair(3) | curses.A_BOLD);
                    stdscr.refresh();
                    time.sleep(2);
                    start = False
                time.sleep(0.06);
        except KeyboardInterrupt:
            pass

    wrapper(main);


import curses


def centerstr(wnd, y, txt):
    h,w = wnd.getmaxyx()
    wc = int(w/2)
    wnd.addstr(y, wc-int(len(txt)/2), txt)

def dialog(title, parent, height, width, lines):
    ph,pw = parent.getmaxyx()
    pch = int(ph/2)
    pcw = int(pw/2)

    w = parent.derwin(height,width, int(pch-height/2),int(pcw-width/2))
    w.clear()
    centerstr(w, 1, title)
    w.hline(2,0, curses.ACS_HLINE, w.getmaxyx()[1])
    y = 3
    for line in lines:
        w.move(y,1)
        if isinstance(line, str):
            w.addstr(line)
        else:
            i = 0
            while i < len(line):
                txt = line[i]
                if len(line) > i+1 and not isinstance(line[i+1], str):
                    color = line[i+1]
                    w.addstr(txt, color)
                    i += 2
                else:
                    w.addstr(txt)
                    i += 1
        y += 1
        if y >= height:
            break
    w.border()
    return w

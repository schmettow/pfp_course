# Programming for Psychologists 2026 — Six-day lesson plan

Find the [time table](https://cloud.timeedit.net/nl_utwente/web/staff/ri15567y6Z0255Q097QQY201Z567047Q367W55.html) with times and rooms.

> **Every day has the same four elements:**
>
> 1. **Learning goal** — a general programming technique.
> 2. **Lecture** — agenda, subgoals, key formulations, and development steps in the two
>    running examples: **Stroop task** and **traffic light**.
> 3. **Workshop** — the eye-experiment assignment as **M** and **M+**, addressed to students.
> 4. **Checkpoint** — a commented standard solution and a quick checklist.
>
> **Lecture examples are Stroop and traffic light only.** The eye is strictly the workshop
> assignment; no eye code belongs in the lecture.
>
> **Daily rhythm:** a day is **90 min lecture + 180 min workshop**. The checkpoint is the
> final 20 min of the workshop; it is not additional time. The workshop includes a short
> break; if the lecture needs a stretch, take 5 min from the pair/predict exercise.

## The six days at a glance

| Day | Learning goal (general technique) | Lecture: Stroop + traffic light | Workshop: M / M+ | Checkpoint |
|---|---|---|---|---|
| **1** | Problem decomposition and composition | Strip the Stroop to its skeleton; compose the traffic light from shapes; extract a function | **M0** draw the eye; **M0+** make it nicer | Commented M0/M0+ solution + checklist |
| **2** | Time-to-event and animation | Traffic light: automatic cycle with timestamps; Stroop: timed cross → word → blank | **M1** random fixations; **M1+** blink | Commented M1/M1+ solution + checklist |
| **3** | Interaction flow and state | Traffic light: manual state cycle; Stroop: response keys and feedback | **M2** event-controlled gaze; **M2+** optional extension | Checklist + commented solution (next pass) |
| **4** | Mixed-initiative control | Traffic light: operator + timer; Stroop: prepare → show → response → feedback | **M3** mixed-initiative eye flow; **M3+** optional extension | Checklist + commented solution (next pass) |
| **5** | Data collection and logging | Stroop: RT capture and CSV; traffic light: transition log | **M4** eye trial data to CSV; **M4+** optional extension | Checklist + commented solution (next pass) |
| **6** | Testing, debugging, integration | Test and review both examples; reproduce from a clean start | **M5** complete/test the eye program; **M5+** optional extension | Checklist + commented solution (next pass) |

**Milestone note.** M0+ and M1+ are the stretch milestones you defined. For Days 3–6,
**M2+–M5+ are proposed optional extensions**; confirm or replace them.

## Course frame

- **Audience:** psychology students, no programming experience assumed.
- **Software:** Python 3, Pygame, the course editor.
- **Running examples:** the working Stroop task and the traffic light. The book’s
  `pfp_book/Programs/PIP_stroop_interaction.py` is Python 2-era; use your modernized course
  copy for execution and the book file as a reading reference.
- **Assignment:** the eye experiment, one core milestone per day, with an optional M+.
- **Assessment (suggested):** each day ends with a 20-minute checkpoint on the milestone,
  inside the workshop; the final assessment is the M5 program plus a short code walkthrough.
- **AI policy:** AI tools are forbidden for assessed work. The exam asks students to
  predict, debug, and modify code live; a generated program they cannot explain will fail.
  The book, official documentation, and notes are allowed. Adjust the wording to your exam
  regulations.
- **Live-coding rule:** students type along. Keep a known-good version of each lecture
  example and each milestone open in a second tab as the break-glass reference.

---

# Day 1 — Problem decomposition and composition (M0)

## 1. Learning goal

**Problem decomposition and composition.** Given a working program, identify the invariant
skeleton, strip away the content, and rebuild a new stimulus by composing primitives and
extracting a parameterized function.

The general technique is not “draw a specific picture.” It is:

- separate **skeleton** from **content**;
- separate **structure** from **appearance**;
- turn a repeated drawing into a **function with parameters**.

## 2. Lecture (90 min)

### Agenda

| Min | Block |
|---|---|
| 0–10 | Learning goal and hook |
| 10–15 | Pair exercise: find the skeleton in the Stroop |
| 15–40 | Stroop: rip out the loop; freeze; restore the event pump |
| 40–50 | Stroop: compare `draw_stimulus` with a parameterized function |
| 50–65 | Traffic light: compose the housing and lamps |
| 65–80 | Traffic light: extract `draw_lamp` and `draw_traffic_light` |
| 80–90 | Compare both examples; key formulations; workshop brief |

**Pair exercise (10–15).** In pairs, find the skeleton in the Stroop file and point to the
event loop, `screen.fill`, and `display.update`. Compare with the class.

### Subgoals

By the end of the lecture, students can:

1. identify the invariant parts of an interactive Pygame program;
2. strip a program to its skeleton and restore the minimal event pump;
3. explain why the event loop is the interface;
4. draw a figure by stacking primitives in the right order;
5. extract a repeated drawing into a parameterized function;
6. explain why the same skeleton can host different experiments.

### Key formulations

> “A program is a **skeleton plus content**. Keep the skeleton; replace the content.”
>
> “The event loop is the interface. Without it, `while True` is a busy loop.”
>
> “Pygame is **wet paint**: the last shape wins.”
>
> “A function is a **named recipe with parameters**. It turns a picture into a reusable
> stimulus.”
>
> “One shape is a drawing; a stack of shapes is a stimulus.”

### Running example A: Stroop task — strip to the skeleton

The Stroop program is the template. We are not going to read all of it; we are going to
steal its skeleton.

#### Development steps

1. Run the working Stroop; play one trial.
2. Find the skeleton together:
   - imports and config;
   - `pygame.init()`, `pygame.display.set_mode(...)`, `screen`;
   - `def main():`;
   - `while True:`;
   - `for event in pygame.event.get():`;
   - `screen.fill(...)`;
   - `pygame.display.update()`.
3. Ask: “What happens if we delete everything inside `while True`?”
4. Do it. Leave only:
   ```python
   while True:
       pass
   ```
   Run it. The window freezes; you cannot close it. Warn students: close it with Ctrl+C in
   the console or force-quit.
5. Explain: the loop body pumps events and updates the display. Without it, the program is
   a busy loop with no interface.
6. Restore the minimal event pump:
   ```python
   while True:
       for event in pygame.event.get():
           if event.type == QUIT:
               pygame.quit()
               sys.exit()
   ```
   Run: the window opens and closes.
7. Restore the frame:
   ```python
   screen.fill(BACKGR_COL)
   ...
   pygame.display.update()
   ```
   Run: a blank canvas that closes cleanly.
8. Delete the Stroop-specific content:
   - delete `STATE`, `trial_number`, `WORDS`, `KEYS`; keep `COLORS` for the comparison;
   - delete `pick_color`, `draw_welcome`, `draw_feedback`, `draw_goodbye`, `draw_button`;
   - keep `SCREEN_SIZE`, `BACKGR_COL`, the Pygame startup, `screen`, the event pump,
     `screen.fill`, and `display.update`;
   - change the caption to `"Demo"`.
9. Show the existing `draw_stimulus` function as the first drawing function:
   ```python
   def draw_stimulus(color, word):
       text_surface = font.render(word, True, COLORS[color], BACKGR_COL)
       text_rectangle = text_surface.get_rect()
       text_rectangle.center = (SCREEN_SIZE[0] / 2.0, 150)
       screen.blit(text_surface, text_rectangle)
   ```
   Ask: “What are the inputs? What is hidden as a global? What would you parameterize?”
   After the comparison, delete `draw_stimulus` and `COLORS`; they have served their purpose.
10. Add a clean drawing function to the blank canvas:
    ```python
    def draw_cross(surface, screen_size):
        cx, cy = screen_size[0] // 2, screen_size[1] // 2
        pygame.draw.line(surface, (20, 20, 20),
                         (cx - 20, cy), (cx + 20, cy), 2)
        pygame.draw.line(surface, (20, 20, 20),
                         (cx, cy - 20), (cx, cy + 20), 2)
    ```
    Call it from the loop:
    ```python
    draw_cross(screen, SCREEN_SIZE)
    ```
11. Run it. The skeleton now hosts a new stimulus. That is the whole move.

> **Key insight:** `draw_stimulus` works because it is a function, but it depends on globals.
> `draw_cross` is cleaner: the surface and the screen size are parameters. That is the
> progression we will use for the assignment.

### Running example B: Traffic light — composition and function extraction

#### Development steps

1. Start from the same blank skeleton.
2. Draw the housing:
   ```python
   pygame.draw.rect(
       screen, (35, 35, 35),
       (330, 90, 140, 420), border_radius=20)
   ```
3. Draw three lamps:
   ```python
   pygame.draw.circle(screen, (220, 40, 40), (400, 200), 45)
   pygame.draw.circle(screen, (240, 200, 40), (400, 300), 45)
   pygame.draw.circle(screen, (40, 200, 80), (400, 400), 45)
   ```
4. Run it. Discuss the stack: the housing is behind the lamps; the lamps are later in the
   code. Draw one lamp first and then the housing; the lamp disappears.
5. Refactor one lamp into a function:
   ```python
   def draw_lamp(surface, center, radius, color, on):
       if on:
           pygame.draw.circle(surface, color, center, radius)
       else:
           pygame.draw.circle(surface, (45, 45, 45), center, radius)
       pygame.draw.circle(surface, (20, 20, 20), center, radius, 2)
   ```
6. Call it three times; change the `on` flags; run:
   ```python
   draw_lamp(screen, (400, 200), 45, (220, 40, 40), True)
   draw_lamp(screen, (400, 300), 45, (240, 200, 40), False)
   draw_lamp(screen, (400, 400), 45, (40, 200, 80), False)
   ```
7. Group the housing and the lamps into one function with a `state` parameter:
   ```python
   def draw_traffic_light(surface, center, state):
       cx, cy = center
       pygame.draw.rect(
           surface, (35, 35, 35),
           (cx - 70, cy - 210, 140, 420), border_radius=20)
       draw_lamp(surface, (cx, cy - 100), 45, (220, 40, 40),
                 state == "stop")
       draw_lamp(surface, (cx, cy), 45, (240, 200, 40),
                 state == "prep" or state == "att")
       draw_lamp(surface, (cx, cy + 100), 45, (40, 200, 80),
                 state == "go")
   ```
8. Call it from the loop:
   ```python
   draw_traffic_light(
       screen, (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2), "stop")
   ```
9. Change the string to `"prep"`, `"go"`, `"att"`; run each time. The picture changes without
   rewriting the drawing code.

> **Key insight:** `state` is just a label today. On Day 3 it becomes a real state machine.
> The important step today is that the drawing function takes the state as a parameter
> instead of reading a global.

### Close: transfer to the assignment

Both examples use the same skeleton:

```text
setup → while True → event pump → fill → presentationals → update
```

The Stroop draws text; the traffic light draws lamps. The assignment draws your stimulus.
The technique is identical: compose primitives, draw back to front, extract a function, and
parameterize it.

---

## 3. Workshop (180 min, including the checkpoint)

### Workshop run of show

| Min | Block |
|---|---|
| 0–10 | Stand-up and setup |
| 10–75 | M0 build: eye + function |
| 75–90 | Break |
| 90–140 | M0 finish + M0+ stretch |
| 140–160 | Peer test / show-and-tell |
| 160–180 | Checkpoint: standard solution + checklist |

### M0 — Build the eye

**Your task.** Build a recognizable human eye on the blank canvas you inherited from the
Stroop skeleton. Do not copy the instructor’s file; type your own version.

Your program must:

- open a window and close cleanly;
- draw a sclera with `pygame.draw.ellipse`;
- draw an iris, a pupil, and a highlight with `pygame.draw.circle`;
- draw in the order **sclera → iris → pupil → highlight**;
- use named color constants, not repeated RGB tuples;
- put the drawing into a function:
  ```python
  draw_eye(surface, center, width, height, iris_radius)
  ```
- call the function from the loop with the eye at the centre of the screen;
- have no hard-coded eye centre inside the function.

**Definition of done:** the eye is recognizable at a glance, the function has the signature
above, and you can explain why the drawing order matters.

### M0+ — Make it nicer (optional)

Keep the `draw_eye` signature and choose **at least two**:

- layered iris (outer ring, inner ring, pupil);
- eyelid or lid shadow;
- brow, lashes, or outline;
- asymmetric highlight;
- soft shadow with an alpha surface;
- a second eye with coordinated gaze.

**Simple lid trick:** after the iris, pupil, and highlight, paint the background back over
the top and bottom quarters:

```python
pygame.draw.ellipse(
    surface, BACKGR_COL,
    (cx - width // 2, cy - height // 2 - height // 4,
     width, height // 2))
pygame.draw.ellipse(
    surface, BACKGR_COL,
    (cx - width // 2, cy + height // 4,
     width, height // 2))
```

If the iris looks too clipped, reduce `iris_radius` from 55 to about 45. This trick assumes
a solid background; for a gradient or photo, draw the eye to a separate surface and mask it.

**M0+ is not a blocker.** A correct M0 is enough; M0+ is for students who finish early.

### Acceptance checklist (workshop)

- [ ] the window opens and closes;
- [ ] the eye has sclera, iris, pupil, highlight;
- [ ] `draw_eye` is defined and called;
- [ ] the function takes `surface, center, width, height, iris_radius`;
- [ ] the function can draw a second eye at a different centre;
- [ ] drawing order is correct;
- [ ] no `time.sleep`;
- [ ] M0+ keeps the same signature.

---

## 4. Checkpoint (last 20 min of the workshop)

### Standard solution M0 (commented)

```python
# M0 standard solution.
# Assumes the M0 file's imports.
# Requires SCLERA, IRIS, PUPIL, HIGHLIGHT, and BACKGR_COL at the top of the file.
# The eye is a stack of four primitives, drawn back to front.
def draw_eye(surface, center, width, height, iris_radius):
    cx, cy = center

    # The pupil is a fixed fraction of the iris.
    pupil_radius = int(iris_radius * 0.45)

    # 1. Sclera: an ellipse inscribed in the bounding box.
    pygame.draw.ellipse(
        surface, SCLERA,
        (cx - width // 2, cy - height // 2, width, height))

    # 2. Iris: a circle at the eye centre.
    pygame.draw.circle(surface, IRIS, (cx, cy), iris_radius)

    # 3. Pupil: a smaller circle.
    pygame.draw.circle(surface, PUPIL, (cx, cy), pupil_radius)

    # 4. Highlight: a small circle in the upper-left of the pupil.
    pygame.draw.circle(
        surface, HIGHLIGHT,
        (cx - pupil_radius // 3, cy - pupil_radius // 3),
        max(2, pupil_radius // 4))
```

Call it from the loop:

```python
draw_eye(
    screen,
    (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2),
    240, 120, 55)
```

### Standard solution M0+ (commented, one possible enhancement)

```python
# M0+ standard solution: simple lids by painting the background back.
# Place this inside draw_eye, after the iris, pupil, and highlight.
# The upper lid covers the top quarter; the lower lid covers the bottom quarter.
pygame.draw.ellipse(
    surface, BACKGR_COL,
    (cx - width // 2,
     cy - height // 2 - height // 4,
     width, height // 2))
pygame.draw.ellipse(
    surface, BACKGR_COL,
    (cx - width // 2,
     cy + height // 4,
     width, height // 2))
```

Other M0+ solutions are accepted if they keep the signature and meet the acceptance
checklist.

### Quick checklist

```text
[ ] grep -n "sleep" eye.py        -> no output
[ ] grep -n "def draw_eye" eye.py -> exactly one definition
[ ] grep -n "draw_eye(" eye.py    -> at least one call
[ ] grep -n "QUIT" eye.py         -> present
[ ] the eye reads as an eye
[ ] the drawing order is sclera -> iris -> pupil -> highlight
[ ] draw_eye has the required signature
[ ] no hard-coded eye centre inside draw_eye
[ ] M0+ keeps the same signature
```

---

# Day 2 — Time-to-event and animation (M1)

## 1. Learning goal

**Time-to-event and animation.** Schedule events with timestamps instead of sleeping;
animate by redrawing state in a fast loop. The general technique is to separate the
**clock** from the **frame**.

## 2. Lecture (90 min)

### Agenda

| Min | Block |
|---|---|
| 0–10 | Recap Day 1; learning goal |
| 10–15 | Predict: what happens with `sleep`? |
| 15–45 | Traffic light: automatic cycle with timestamps |
| 45–50 | Predict/check: break the timer |
| 50–75 | Stroop: timed cross → word → blank |
| 75–85 | Compare both examples; key formulations |
| 85–90 | Workshop brief |

**Predict/check (10–15 and 45–50).** Ask students to predict what `sleep(1)` does to the
window, then run it. Use the second slot to break the traffic-light timer and let students
find the fix.

### Subgoals

By the end of the lecture, students can:

1. explain why `sleep` blocks the event loop;
2. use `time()` and `t_next` to schedule a transition;
3. implement a cyclic automatic state machine;
4. implement a timed stimulus sequence;
5. explain why frame counting is not experiment timing;
6. transfer the timestamp pattern to a new stimulus.

### Key formulations

> “`sleep` stops the world; a timestamp lets the world keep running.”
>
> “Set the timestamp before the loop, check it every frame, reset it after the event.”
>
> “Frames are the projector; timestamps are the truth.”
>
> “A stimulus event is an event, not a wait.”
>
> “Never count frames for experiment timing.”

### Running example A: Traffic light — automatic cycle with timestamps

#### Development steps

1. Start from the Day 1 traffic light drawing.
2. Add `from time import time`.
3. Add a clock:
   ```python
   clock = pygame.time.Clock()
   ```
4. Add the state and the first timestamp before the loop:
   ```python
   STATE = "stop"
   t_next = time() + 3.0
   ```
5. At the top of the loop, read the clock once:
   ```python
   now = time()
   ```
6. Add the automatic transitions:
   ```python
   if STATE == "stop" and now >= t_next:
       STATE = "prep"
       t_next = now + 1.0
   elif STATE == "prep" and now >= t_next:
       STATE = "go"
       t_next = now + 3.0
   elif STATE == "go" and now >= t_next:
       STATE = "att"
       t_next = now + 1.0
   elif STATE == "att" and now >= t_next:
       STATE = "stop"
       t_next = now + 3.0
   ```
7. Present the state:
   ```python
   screen.fill(BACKGR_COL)
   draw_traffic_light(
       screen, (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2), STATE)
   pygame.display.update()
   clock.tick(60)
   ```
8. Run it. The light cycles automatically.
9. Deliberate bugs:
   - add `sleep(1)`; the window freezes; remove it;
   - reset `t_next` at the top of every frame; the cycle stops;
   - forget to reset `t_next`; the light strobes;
   - count frames; the timing changes with the machine.

#### Reference code: the traffic light loop

```python
from time import time

# ...

def main():
    pygame.init()
    pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Traffic light")
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    STATE = "stop"
    t_next = time() + 3.0

    while True:
        now = time()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if STATE == "stop" and now >= t_next:
            STATE = "prep"
            t_next = now + 1.0
        elif STATE == "prep" and now >= t_next:
            STATE = "go"
            t_next = now + 3.0
        elif STATE == "go" and now >= t_next:
            STATE = "att"
            t_next = now + 1.0
        elif STATE == "att" and now >= t_next:
            STATE = "stop"
            t_next = now + 3.0

        screen.fill(BACKGR_COL)
        draw_traffic_light(
            screen, (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2), STATE)
        pygame.display.update()
        clock.tick(60)
```

> **Key insight:** the traffic light is a pure automatic state machine. There are no user
> events except `QUIT`. The timestamp is the event trigger.

### Running example B: Stroop — timed cross → word → blank

#### Development steps

1. Start from the Day 1 Stroop skeleton. Keep the font:
   ```python
   font = pygame.font.Font(None, 80)
   ```
2. Add two drawing functions:
   ```python
   def draw_cross(surface, screen_size):
       cx, cy = screen_size[0] // 2, screen_size[1] // 2
       pygame.draw.line(surface, (20, 20, 20),
                        (cx - 20, cy), (cx + 20, cy), 2)
       pygame.draw.line(surface, (20, 20, 20),
                        (cx, cy - 20), (cx, cy + 20), 2)


   def draw_word(surface, text, color, font, screen_size):
       text_surface = font.render(text, True, color)
       rect = text_surface.get_rect(
           center=(screen_size[0] // 2, screen_size[1] // 2))
       surface.blit(text_surface, rect)
   ```
3. Add the state and the first timestamp before the loop:
   ```python
   STATE = "cross"
   t_next = time() + 0.5
   ```
4. Add the timed transitions:
   ```python
   if STATE == "cross" and now >= t_next:
       STATE = "stimulus"
       t_next = now + 1.0
       time_when_presented = now
   elif STATE == "stimulus" and now >= t_next:
       STATE = "blank"
       t_next = now + 0.5
   elif STATE == "blank" and now >= t_next:
       STATE = "cross"
       t_next = now + 0.5
   ```
5. Present the state:
   ```python
   screen.fill(BACKGR_COL)
   if STATE == "cross":
       draw_cross(screen, SCREEN_SIZE)
   elif STATE == "stimulus":
       draw_word(screen, "RED", (250, 0, 0), font, SCREEN_SIZE)
   pygame.display.update()
   clock.tick(60)
   ```
6. Run it. Observe: cross 500 ms → word 1000 ms → blank 500 ms → repeat.
7. Note that `time_when_presented` is recorded now; Day 5 will use it to compute a response
   time.
8. Deliberate bugs: `sleep`, resetting `t_next`, and frame counting.

#### Reference code: the Stroop timing loop

```python
from time import time

# ...

def main():
    pygame.init()
    pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Stroop timing")
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 80)

    STATE = "cross"
    t_next = time() + 0.5

    while True:
        now = time()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if STATE == "cross" and now >= t_next:
            STATE = "stimulus"
            t_next = now + 1.0
            time_when_presented = now
        elif STATE == "stimulus" and now >= t_next:
            STATE = "blank"
            t_next = now + 0.5
        elif STATE == "blank" and now >= t_next:
            STATE = "cross"
            t_next = now + 0.5

        screen.fill(BACKGR_COL)
        if STATE == "cross":
            draw_cross(screen, SCREEN_SIZE)
        elif STATE == "stimulus":
            draw_word(screen, "RED", (250, 0, 0), font, SCREEN_SIZE)
        pygame.display.update()
        clock.tick(60)
```

> **Key insight:** the timing pattern is identical to the traffic light. The difference is
> the content: lamps versus a cross and a word. The assignment transfers the pattern to its
> own stimulus events.

### Close: transfer to the assignment

The traffic light cycles automatically; the Stroop sequence is a timed stimulus train. Both
use the same three-part timestamp rule:

1. set `t_next` before the loop;
2. compare `now >= t_next` every frame;
3. reset `t_next` after the transition.

The assignment uses the same pattern to schedule its stimulus events.

---

## 3. Workshop (180 min, including the checkpoint)

### Workshop run of show

| Min | Block |
|---|---|
| 0–10 | Stand-up and setup |
| 10–75 | M1 build: `look_at`, clamp, timer |
| 75–90 | Break |
| 90–140 | M1 finish + M1+ blink |
| 140–160 | Peer test / show-and-tell |
| 160–180 | Checkpoint: standard solution + checklist |

### M1 — Make the eye move

**Your task.** Turn your M0 eye into an animated eye with random fixations.

Your program must:

- keep the `draw_eye` function, but add a `look_at` parameter:
  ```python
  draw_eye(surface, center, width, height, iris_radius, look_at)
  ```
- compute the iris offset from `look_at` and clamp it so the iris stays inside the eye;
- generate a new random target every 0.5–2 s;
- use `time()` and `next_saccade`; no `sleep`;
- keep the window responsive and close it with `QUIT`;
- use `clock.tick(60)` to cap the frame rate.

**Tuning note:** with a 120 px-high eye and an iris radius of 55, the iris has only 5 px of
vertical travel. Use an iris radius of 45 or a taller eye if you want visible vertical
movement.

**Definition of done:** the eye changes gaze at irregular intervals, the iris does not leave
the eye, and you can explain where `next_saccade` is set and reset.

### M1+ — Add blinking (optional)

Add a blink timer:

- blink every 2–6 s;
- close the eye for 100–150 ms;
- let saccades continue afterwards;
- do not use `sleep`.

The simplest version is a background-colored overlay plus a closed-lid line. Keep the M1
code intact; add the blink as a separate timer and a presentational overlay.

**M1+ is not a blocker.** A correct M1 is enough; M1+ is for students who finish early.

### Acceptance checklist (workshop)

- [ ] the eye moves at irregular intervals;
- [ ] `look_at` is a parameter, not a global;
- [ ] the iris is clamped inside the eye;
- [ ] `next_saccade` is set before the loop;
- [ ] `next_saccade` is reset after each saccade;
- [ ] no `time.sleep`;
- [ ] `QUIT` works;
- [ ] M1+ blinks for 100–150 ms and does not block saccades.

---

## 4. Checkpoint (last 20 min of the workshop)

### Standard solution M1 (commented)

```python
# Standard solution M1.
# Assumes the M0 file's imports and constants.
# The sclera stays put; the iris, pupil, and highlight follow look_at.
import math
import random
from time import time

# ...


def clamp(value, low, high):
    return max(low, min(high, value))


def draw_eye(surface, center, width, height, iris_radius, look_at):
    cx, cy = center

    # The iris can move this far before it leaves the sclera.
    max_dx = width // 2 - iris_radius
    max_dy = height // 2 - iris_radius

    # Clamp the target to the eye's bounding box.
    dx = clamp(look_at[0] - cx, -max_dx, max_dx)
    dy = clamp(look_at[1] - cy, -max_dy, max_dy)
    ix, iy = int(cx + dx), int(cy + dy)

    pupil_radius = int(iris_radius * 0.45)

    # Sclera stays at the eye centre.
    pygame.draw.ellipse(
        surface, SCLERA,
        (cx - width // 2, cy - height // 2, width, height))

    # Iris, pupil, and highlight follow the gaze target.
    pygame.draw.circle(surface, IRIS, (ix, iy), iris_radius)
    pygame.draw.circle(surface, PUPIL, (ix, iy), pupil_radius)
    pygame.draw.circle(
        surface, HIGHLIGHT,
        (ix - pupil_radius // 3, iy - pupil_radius // 3),
        max(2, pupil_radius // 4))


def random_target():
    angle = random.uniform(0, 2 * math.pi)
    distance = random.uniform(0, 1)
    max_dx = EYE_W // 2 - IRIS_R
    max_dy = EYE_H // 2 - IRIS_R
    return (EYE_CENTER[0] + math.cos(angle) * distance * max_dx,
            EYE_CENTER[1] + math.sin(angle) * distance * max_dy)
```

In `main()`, before the loop:

```python
look_at = EYE_CENTER
next_saccade = time() + random.uniform(0.5, 2.0)
```

Inside the loop, after the event pump:

```python
now = time()
if now >= next_saccade:
    look_at = random_target()
    next_saccade = now + random.uniform(0.5, 2.0)
```

Presentational:

```python
screen.fill(BACKGR_COL)
draw_eye(screen, EYE_CENTER, EYE_W, EYE_H, IRIS_R, look_at)
pygame.display.update()
clock.tick(60)
```

### Standard solution M1+ (commented)

```python
# Before the loop:
blink_until = 0.0
next_blink = time() + random.uniform(2.0, 6.0)

# Inside the loop, after the saccade block:
if now >= next_blink:
    blink_until = now + 0.15          # 150 ms closure
    next_blink = now + random.uniform(2.0, 6.0)

# Presentational, after draw_eye:
if now < blink_until:
    # Cover the eye with the background ...
    pygame.draw.rect(
        screen, BACKGR_COL,
        (EYE_CENTER[0] - EYE_W // 2, EYE_CENTER[1] - EYE_H // 2,
         EYE_W, EYE_H))
    # ... and draw the closed lid.
    pygame.draw.line(
        screen, (18, 18, 22),
        (EYE_CENTER[0] - EYE_W // 2, EYE_CENTER[1]),
        (EYE_CENTER[0] + EYE_W // 2, EYE_CENTER[1]), 3)
```

### Quick checklist

```text
[ ] grep -n "sleep" eye.py          -> no output
[ ] grep -n "next_saccade" eye.py   -> set before the loop, reset after the saccade
[ ] grep -n "look_at" eye.py        -> parameter and clamp present
[ ] grep -n "QUIT" eye.py           -> present
[ ] the eye moves at irregular intervals
[ ] the iris stays inside the eye
[ ] draw_eye still has the required signature plus look_at
[ ] M1+ blink duration is 100-150 ms
[ ] M1+ does not block saccades
```

---

# Day 3 — Interaction flow and state (M2)

## 1. Learning goal

**Interaction flow.** Turn a transition table into conditionals, events, state variables,
transitionals, and presentationals. The general technique is: **one event, one transition;
state is memory; the screen is a projection.**

## 2. Lecture (90 min)

**Agenda.** Recap Day 2; traffic light manual control; Stroop response state machine;
compare both; workshop brief.

**Suggested split:** 10 min recap; 35 min traffic light manual control; 30 min Stroop
response flow; 15 min compare and workshop brief.

**Subgoals.**

- read `KEYDOWN` and `MOUSEMOTION` events;
- write one-way, two-way, and multi-way conditionals;
- separate external transitionals from presentationals;
- use `elif`/`continue` correctly;
- print the state on every transition.

**Key formulations.**

> “One event, one transition.”
>
> “Transitionals write state; presentationals read state.”
>
> “The state is the memory; the screen is a projection.”
>
> “If you can draw the transition table, you can code the program.”

**Stroop development steps (to be detailed).** Welcome screen → trial on SPACE; response keys
→ feedback; state printed on every transition; `elif` branches; no drawing inside the event
loop.

**Traffic light development steps (to be detailed).** Manual one-button cycle
`stop → prep → go → att`; event conditional; presentational reads `STATE`.

## 3. Workshop (180 min, including the checkpoint)

**Workshop rhythm:** 10 min stand-up; 70 min M2 build; 15 min break; 45 min M2+ / finish;
20 min peer test; 20 min checkpoint.

**Your task.** **M2 — Control the eye with events.** Give the eye at least three states: `wander`,
`follow`, `at_user`. Keys switch states; the mouse controls gaze in `follow`; `at_user`
looks straight at the viewer. Keep `QUIT` global, print state transitions, and keep drawing
out of the event loop.

**M2+ (proposed).** Add one of: gaze aversion on a key, two eyes with coordinated gaze, or
smooth pursuit.

## 4. Checkpoint (last 20 min of the workshop)

**Commented standard solution:** to be written in the Day 1–2 format.

**Quick checklist.**

```text
[ ] transitionals present; no drawing inside the event loop
[ ] global QUIT handled first
[ ] state printed on every transition
[ ] elif used for mutually exclusive transitions
[ ] three named states: wander, follow, at_user
[ ] presentationals only read state
[ ] no time.sleep
```

---

# Day 4 — Mixed-initiative flow (M3)

## 1. Learning goal

**Mixed-initiative control.** Combine internal timers and external events in one state
machine, with branching trial flow. The general technique is: **the program can act, and the
participant can act; both change the same state.**

## 2. Lecture (90 min)

**Agenda.** Recap Day 3; semi-automatic traffic light; Stroop trial flow; compare both;
workshop brief.

**Suggested split:** 10 min recap; 35 min semi-automatic traffic light; 30 min Stroop trial
flow; 15 min compare and workshop brief.

**Subgoals.**

- combine automatic and interactive transitionals;
- design a branching transition table;
- use a ghost state to prepare data;
- keep trial flow and presentation separate.

**Key formulations.**

> “Internal and external events share one state machine.”
>
> “A ghost state prepares data without showing anything.”
>
> “Branching is a transition table with more than one way out.”

**Stroop development steps (to be detailed).** Prepare trial → show trial → wait for
response → feedback → next trial; ghost state; trial counter.

**Traffic light development steps (to be detailed).** Semi-automatic light: operator
requests Stop/Go; the light runs through `prep` and `att` automatically.

## 3. Workshop (180 min, including the checkpoint)

**Workshop rhythm:** 10 min stand-up; 70 min M3 build; 15 min break; 45 min M3+ / finish;
20 min peer test; 20 min checkpoint.

**Your task.** **M3 — Mixed-initiative eye flow.** Build a trial flow: welcome → fixation → stimulus →
response → feedback → next trial. Internal timers drive the stimulus; external keys record
the response. Keep the state visible for debugging.

**M3+ (proposed).** Add practice trials, an experimenter override, or counterbalanced
conditions.

## 4. Checkpoint (last 20 min of the workshop)

**Commented standard solution:** to be written in the Day 1–2 format.

**Quick checklist.**

```text
[ ] both internal and external transitions present
[ ] transition table covers every state
[ ] trial counter present
[ ] no time.sleep
[ ] QUIT works from every state
[ ] feedback state exists
```

---

# Day 5 — Data collection and logging (M4)

## 1. Learning goal

**Event logging.** Record trial-based events and response times and write them to CSV. The
general technique is: **record at the event, not at the frame; one row per trial.**

## 2. Lecture (90 min)

**Agenda.** Recap Day 4; Stroop RT capture; traffic light transition log; CSV writer;
compare both; workshop brief.

**Suggested split:** 10 min recap; 35 min Stroop RT/CSV; 30 min traffic light log; 15 min
compare and workshop brief.

**Subgoals.**

- record `time_when_presented` and `time_when_reacted`;
- compute RT at the response event;
- append one row per trial;
- write a CSV with a header and close the file.

**Key formulations.**

> “Record the event timestamp, not the drawing time.”
>
> “One trial, one row.”
>
> “The CSV is the experiment’s memory.”

**Stroop development steps (to be detailed).** Capture RT in the response transitional;
append `[trial, condition, response, correct, rt]`; write with `csv.writer`; close the file.

**Traffic light development steps (to be detailed).** Log `[time, state]` on every
transition; write the log to CSV; use it to verify the cycle.

## 3. Workshop (180 min, including the checkpoint)

**Workshop rhythm:** 10 min stand-up; 70 min M4 build; 15 min break; 45 min M4+ / finish;
20 min peer test; 20 min checkpoint.

**Your task.** **M4 — Eye trial data to CSV.** Record one row per trial: trial number, condition, gaze
target, response key, correctness, and RT. Write a CSV with a header. Keep the data in
memory and write it at the end, or append safely after each trial.

**M4+ (proposed).** Add an event log for state transitions or summary statistics per
condition.

## 4. Checkpoint (last 20 min of the workshop)

**Commented standard solution:** to be written in the Day 1–2 format.

**Quick checklist.**

```text
[ ] CSV header present
[ ] one row per trial
[ ] no missing RT
[ ] file closed
[ ] data not only printed to the console
[ ] trial number and condition included
```

---

# Day 6 — Testing, debugging, integration (M5)

## 1. Learning goal

**Testing and integration.** Verify the experiment end to end, handle edge cases, document
the program, and demonstrate it. The general technique is: **test the skeleton, the
transitionals, and the data; change one thing at a time.**

## 2. Lecture (90 min)

**Agenda.** Recap Day 5; review the Stroop task; review the traffic light; build a shared
test checklist; workshop brief.

**Suggested split:** 10 min recap; 35 min Stroop review; 30 min traffic light review; 15 min
shared test checklist and workshop brief.

**Subgoals.**

- test from a clean start;
- test every state and branch;
- test the data file;
- test the quit path;
- review code structure and naming.

**Key formulations.**

> “A program is finished when it runs from a clean start and can be explained.”
>
> “Test the skeleton, then the transitions, then the data.”
>
> “The demo is part of the program.”

**Stroop development steps (to be detailed).** Walk through the full trial loop; check
response keys, feedback, RT, trial count, and quit.

**Traffic light development steps (to be detailed).** Walk through the full cycle; check
timing, state labels, and edge cases.

## 3. Workshop (180 min, including the checkpoint)

**Workshop rhythm:** 10 min stand-up; 60 min M5 finish; 15 min break; 50 min test/demo
prep; 25 min peer test; 20 min checkpoint.

**Your task.** **M5 — Complete and test the eye experiment.** The program must run from a clean start,
complete the full trial flow, write a complete CSV, close cleanly, and include a short
README with run instructions and a description of the conditions.

**M5+ (proposed).** Add counterbalancing, practice trials, or a demo mode that runs without
saving data.

## 4. Checkpoint (last 20 min of the workshop)

**Commented standard solution:** to be written in the Day 1–2 format.

**Quick checklist.**

```text
[ ] runs from a clean start
[ ] no time.sleep
[ ] QUIT works from every state
[ ] CSV header and one row per trial
[ ] no missing RT
[ ] README with run instructions
[ ] code walkthrough: model, view, controller
```

---

# Open decisions

- Confirm the daily split: 90 min lecture + 180 min workshop, with the checkpoint as the
  final 20 min of the workshop.
- Confirm the lecture rule: Stroop and traffic light only; no eye code in the lecture.
- Confirm M0+ and M1+ as the defined stretch milestones; confirm or replace the proposed
  M2+–M5+ extensions.
- Confirm the working Stroop copy used for the lecture (modernized course copy vs. the
  Python 2-era book file).
- Confirm whether the checkpoint standard solutions are shared with students after the
  workshop or kept as instructor reference.

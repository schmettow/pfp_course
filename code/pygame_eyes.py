import math

import pygame

WIDTH, HEIGHT = 800, 600

BG         = pygame.Color(24, 26, 32)
SCLERA     = pygame.Color(245, 243, 238)
IRIS_OUTER = pygame.Color(70, 130, 180)
IRIS_INNER = pygame.Color(28, 56, 104)
PUPIL      = pygame.Color(10, 10, 14)
HIGHLIGHT  = pygame.Color(255, 255, 255)
LID        = pygame.Color(18, 18, 22)

LID_STEPS = 40
IRIS_STEPS = 64


def quad_bezier(p0, p1, p2, t):
    u = 1.0 - t
    return (
        u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
        u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1],
    )


def clamp_to_ellipse(dx, dy, ax, ay):
    """Clamp an offset to an ellipse. Total: accepts ANY real (dx, dy)."""
    if ax <= 0.0 or ay <= 0.0:
        return 0.0, 0.0
    k = (dx / ax) ** 2 + (dy / ay) ** 2
    if k <= 1.0:
        return dx, dy
    s = 1.0 / math.sqrt(k)
    return dx * s, dy * s


def lid_curves(cx, cy, w, h, steps=LID_STEPS):
    """Upper and lower lid as quadratic beziers, both running left to right."""
    left, right = (cx - w, cy), (cx + w, cy)
    top, bottom = (cx, cy - h), (cx, cy + h)
    upper = [quad_bezier(left, top, right, i / steps) for i in range(steps + 1)]
    lower = [quad_bezier(right, bottom, left, i / steps) for i in range(steps + 1)]
    return upper, lower


def ellipse_points(cx, cy, major, minor, ux, uy, steps=IRIS_STEPS):
    """Ellipse whose minor radius lies along the unit vector (ux, uy)."""
    vx, vy = -uy, ux
    points = []
    for i in range(steps):
        a = math.tau * i / steps
        c, s = math.cos(a), math.sin(a)
        points.append((
            cx + c * major * vx + s * minor * ux,
            cy + c * major * vy + s * minor * uy,
        ))
    return points


def draw_eye(surface, center, w: float, h:float, iris_r: float, look_at):
    cx, cy = center

    # 1. look offset, clamped inside the eyeball
    ax, ay = w * 0.65, h * 0.45
    ox, oy = clamp_to_ellipse(look_at[0] - cx, look_at[1] - cy, ax, ay)
    gx = ox / ax if ax > 0.0 else 0.0
    gy = oy / ay if ay > 0.0 else 0.0

    # 2. sclera: static almond, the lids do not follow the gaze
    upper, lower = lid_curves(cx, cy, w, h)
    almond = upper + lower[1:]
    pygame.draw.polygon(surface, SCLERA, almond)

    # 3. iris on a sphere: foreshorten along the gaze by 1 - k * d^2,
    #    where d is the normalized distance of the iris from the centre
    d2 = gx * gx + gy * gy
    d = math.sqrt(d2)
    ux, uy = (gx / d, gy / d) if d > 0.0 else (1.0, 0.0)
    squash = 1.0 - 0.22 * d2
    ix, iy = cx + ox, cy + oy
    for radius, color in (
        (iris_r, IRIS_OUTER),
        (iris_r * 0.6, IRIS_INNER),
        (iris_r * 0.38, PUPIL),
    ):
        pygame.draw.polygon(
            surface, color,
            ellipse_points(ix, iy, radius, radius * squash, ux, uy))

    # 4. small reflection in the pupil; it drifts opposite to the gaze.
    #    Clamping to the pupil's minor radius minus the highlight radius keeps
    #    the whole highlight inside the pupil, even when the pupil is squashed.
    pupil_r = iris_r * 0.38
    hr = max(2, int(iris_r * 0.14))
    room = max(0.0, pupil_r * squash - hr)
    base = -0.35 * pupil_r  # rest position: upper-left of the pupil
    hdx, hdy = clamp_to_ellipse(
        base - 0.5 * ox, base - 0.5 * oy, room, room)
    pygame.draw.circle(
        surface, HIGHLIGHT, (int(ix + hdx), int(iy + hdy)), hr)

    # 5. paint the background back over everything the lids hide
    cap = w + iris_r + 20
    pygame.draw.polygon(
        surface, BG,
        [(cx - w - cap, cy - h - cap)] + upper + [(cx + w + cap, cy - h - cap)])
    pygame.draw.polygon(
        surface, BG,
        [(cx + w + cap, cy + h + cap)] + lower + [(cx - w - cap, cy + h + cap)])
    pygame.draw.rect(surface, BG, (cx + w, cy - cap, cap, 2 * cap))
    pygame.draw.rect(surface, BG, (cx - w - cap, cy - cap, cap, 2 * cap))

    # 6. lid outline
    pygame.draw.lines(surface, LID, True, almond, 3)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BG)
        draw_eye(screen, (WIDTH // 2, HEIGHT // 2), 220, 110, 70,
                 pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()

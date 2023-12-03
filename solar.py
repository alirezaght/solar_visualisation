import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulation")

# Colors
YELLOW = (255, 255, 0)  # Sun color
WHITE = (255, 255, 255)  # Line color
PLANET_COLORS = {  # Simplified colors for each planet
    "Mercury": (169, 169, 169),
    "Venus": (255, 215, 0),
    "Earth": (0, 191, 255),
    "Mars": (255, 0, 0),
    "Jupiter": (255, 140, 0),
    "Saturn": (218, 165, 32),
    "Uranus": (173, 216, 230),
    "Neptune": (65, 105, 225)
}
FPS = 180
SUN_RADIUS = 40
PLANET_RADIUS = 10
LINE_DRAW_RATE = 5
ORBIT_RATIOS = {
    "Mercury": 0.39,
    "Venus": 0.72,
    "Earth": 1.0,
    "Mars": 1.52,
    "Jupiter": 5.2,
    "Saturn": 9.58,
    "Uranus": 19.22,
    "Neptune": 30.05
}
ORBITAL_PERIODS = {
    "Mercury": 0.24,
    "Venus": 0.62,
    "Earth": 1.0,
    "Mars": 1.88,
    "Jupiter": 11.86,
    "Saturn": 29.46,
    "Uranus": 84.01,
    "Neptune": 164.8
}

# Add a dictionary for the rotational periods (length of a day) in Earth days
ROTATIONAL_PERIODS = {
    "Mercury": 58.6,   # Example values
    "Venus": 243,
    "Earth": 1.0,
    "Mars": 1.03,
    "Jupiter": 0.41,
    "Saturn": 0.45,
    "Uranus": 0.72,
    "Neptune": 0.67
}

# Clock
clock = pygame.time.Clock()

# Font
FONT = pygame.font.SysFont('Arial', 20)


def draw_simulation(planet1_pos, planet2_pos, planet1_color, planet2_color,
                    lines, planet1, planet2, scaling_factor):
    WIN.fill((0, 0, 0))  # Clear screen

    # Draw all lines
    for line in lines:
        pygame.draw.line(WIN, WHITE, line[0], line[1])
    pygame.draw.line(WIN, WHITE, planet1_pos, planet2_pos)
    # Draw Sun
    pygame.draw.circle(WIN, YELLOW, (WIDTH // 2, HEIGHT // 2), SUN_RADIUS * scaling_factor)

    # Draw planets
    pygame.draw.circle(WIN, planet1_color, planet1_pos, PLANET_RADIUS * scaling_factor)
    pygame.draw.circle(WIN, planet2_color, planet2_pos, PLANET_RADIUS * scaling_factor)

    # Render and draw planet names
    planet1_text = FONT.render(planet1, True, WHITE)
    planet2_text = FONT.render(planet2, True, WHITE)
    WIN.blit(planet1_text, (10, 10))
    WIN.blit(planet2_text, (10, 35))

    pygame.display.update()


def main(planet1, planet2):
    run = True
    angle1 = 0
    angle2 = 0
    frame_counter = 0
    lines = []

    # Find the larger of the two orbital ratios
    larger_orbit_ratio = max(ORBIT_RATIOS[planet1], ORBIT_RATIOS[planet2])

    # Calculate max orbit radius to fit the larger orbit within the screen
    MAX_ORBIT_RADIUS = (min(WIDTH, HEIGHT) / 2) / larger_orbit_ratio

    # Scaling factor for the planet sizes
    scaling_factor = MAX_ORBIT_RADIUS / (min(WIDTH, HEIGHT) / 2)


    planet1_orbit_radius = ORBIT_RATIOS[planet1] * MAX_ORBIT_RADIUS
    planet2_orbit_radius = ORBIT_RATIOS[planet2] * MAX_ORBIT_RADIUS

    # Ensure orbits are distinct
    if planet1_orbit_radius == planet2_orbit_radius:
        planet1_orbit_radius *= 0.9

        # Calculate angle increments based on orbital periods
    angle_increment1 = ORBITAL_PERIODS["Earth"] / ORBITAL_PERIODS[planet1]
    angle_increment2 = ORBITAL_PERIODS["Earth"] / ORBITAL_PERIODS[planet2]

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Update planet positions
        planet1_x = int(WIDTH / 2 + planet1_orbit_radius * math.cos(angle1))
        planet1_y = int(HEIGHT / 2 + planet1_orbit_radius * math.sin(angle1))
        planet2_x = int(WIDTH / 2 + planet2_orbit_radius * math.cos(angle2))
        planet2_y = int(HEIGHT / 2 + planet2_orbit_radius * math.sin(angle2))

        # Draw line based on the rate
        if frame_counter % LINE_DRAW_RATE == 0:
            lines.append(((planet1_x, planet1_y), (planet2_x, planet2_y)))

        # Draw simulation
        draw_simulation((planet1_x, planet1_y), (planet2_x, planet2_y),
                        PLANET_COLORS[planet1], PLANET_COLORS[planet2], lines,
                        planet1, planet2, scaling_factor)

        # Update angles and frame counter
        angle1 += angle_increment1 * 0.01 / scaling_factor
        angle2 += angle_increment2 * 0.01 / scaling_factor
        frame_counter += 1

    pygame.quit()


def print_planet_names():
    print("Available planets:")
    for planet in PLANET_COLORS.keys():
        print(planet)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_planet_names()
        print("Usage: python script.py planet1 planet2")
        sys.exit(1)
    planet1 = sys.argv[1]
    planet2 = sys.argv[2]
    if planet1 in PLANET_COLORS and planet2 in PLANET_COLORS:
        main(planet1, planet2)
    else:
        print("Invalid planet names entered.")
        print_planet_names()
        sys.exit(1)

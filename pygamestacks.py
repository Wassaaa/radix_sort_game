import pygame
import sys
import random

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.insert(0, item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def swap(self):
        if self.size() > 1:
            self.items[0], self.items[1] = self.items[1], self.items[0]

    def rotate(self):
        if not self.is_empty():
            self.items.append(self.items.pop(0))

    def reverse_rotate(self):
        if not self.is_empty():
            self.items.insert(0, self.items.pop())

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def __str__(self, max_bits):
        return ' '.join(f"{item} ({item:0{max_bits}b})" for item in self.items)

def sa(stack_a):
    stack_a.swap()

def sb(stack_b):
    stack_b.swap()

def ss(stack_a, stack_b):
    sa(stack_a)
    sb(stack_b)

def pa(stack_a, stack_b):
    if not stack_b.is_empty():
        stack_a.push(stack_b.pop())

def pb(stack_a, stack_b):
    if not stack_a.is_empty():
        stack_b.push(stack_a.pop())

def ra(stack_a):
    stack_a.rotate()

def rb(stack_b):
    stack_b.rotate()

def rr(stack_a, stack_b):
    ra(stack_a)
    rb(stack_b)

def rra(stack_a):
    stack_a.reverse_rotate()

def rrb(stack_b):
    stack_b.reverse_rotate()

def rrr(stack_a, stack_b):
    rra(stack_a)
    rrb(stack_b)

def get_max_bits(numbers):
    return max(numbers).bit_length()

def draw_stacks(screen, font, stack_a, stack_b, max_bits, tracked_number):
    global a_rects, b_rects
    a_rects, b_rects = [], []
    a_y, b_y = 50, 50
    decimal_x, binary_x = 50, 125

    for i, item in enumerate(stack_a.items):
        color = (255, 0, 0) if item == tracked_number else (255, 255, 255)
        decimal_text = font.render(f"{item}", True, color)
        binary_text = font.render(f"({item:0{max_bits}b})", True, color)

        screen.blit(decimal_text, (decimal_x, a_y))
        screen.blit(binary_text, (binary_x, a_y))

        rect = pygame.Rect(decimal_x, a_y, binary_text.get_width() + binary_x - decimal_x, binary_text.get_height())
        a_rects.append((rect, item))
        a_y += 30

    for item in stack_b.items:
        decimal_text = font.render(f"{item}", True, (255, 255, 255))
        binary_text = font.render(f"({item:0{max_bits}b})", True, (255, 255, 255))

        screen.blit(decimal_text, (500 + decimal_x, b_y))
        screen.blit(binary_text, (500 + binary_x, b_y))

        rect = pygame.Rect(500 + decimal_x, b_y, binary_text.get_width() + binary_x - decimal_x, binary_text.get_height())
        b_rects.append((rect, item))
        b_y += 30

def check_click(pos, tracked_number):
    for rect, item in a_rects + b_rects:
        if rect.collidepoint(pos):
            return item
    return tracked_number

def main_pygame():
    global stack_a, stack_b, max_bits, a_rects, b_rects
    pygame.init()

    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Stack Sorting Simulator")
    font = pygame.font.SysFont("Courier", 36)  # Using a monospaced font

    stack_a = Stack()
    stack_b = Stack()

    num_count = 8 #int(input("Enter the number of random numbers to generate (up to 10): "))
    numbers = [random.randint(1, 99) for _ in range(min(num_count, 10))]
    max_bits = get_max_bits(numbers)
    for num in numbers:
        stack_a.push(num)

    tracked_number = stack_a.items[0] if stack_a.items else None
    a_rects, b_rects = [], []

    clock = pygame.time.Clock()
    while True:
        screen.fill((0, 0, 0))
        draw_stacks(screen, font, stack_a, stack_b, max_bits, tracked_number)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                tracked_number = check_click(event.pos, tracked_number)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RIGHT:
                    if stack_a.items:
                        if stack_a.items[0] == tracked_number:
                            tracked_number = stack_a.items[1] if len(stack_a.items) > 1 else None
                        pb(stack_a, stack_b)
                elif event.key == pygame.K_LEFT:
                    pa(stack_a, stack_b)
                    if tracked_number and not stack_b.items:
                        tracked_number = stack_a.items[0]
                elif event.key == pygame.K_UP:
                    ra(stack_a)
                elif event.key == pygame.K_DOWN:
                    rra(stack_a)
                elif event.key == pygame.K_PAGEUP:
                    rb(stack_b)
                elif event.key == pygame.K_PAGEDOWN:
                    rrb(stack_b)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_pygame()
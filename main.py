import pygame
from collections import deque
import random
import time
import math 
from maze_data import MAZE, GRID_SIZE, START, END, DIRECTIONS, CELL_SIZE, SCREEN_SIZE


DASHBOARD_WIDTH = 220 
WINDOW_WIDTH = SCREEN_SIZE + DASHBOARD_WIDTH
WINDOW_HEIGHT = SCREEN_SIZE

TITLE = "The Maze Explorer"
FPS = 60 


PATH_BG_COLOR = (245, 245, 245)
WALL_COLOR = (40, 40, 40)        
START_COLOR = (100, 200, 100)    
END_COLOR = (100, 150, 255)      
PLAYER_COLOR = (255, 100, 100)   


DASHBOARD_BG = (60, 60, 60)
PANEL_COLOR = (90, 90, 90)
DASHBOARD_TEXT_COLOR = (255, 255, 255)
DASHBOARD_HEADER_COLOR = (255, 180, 0) 


PLAYER_PATH_COLOR = (255, 180, 0)
OPTIMAL_PATH_COLOR = (255, 0, 0) 
DFS_PATH_COLOR = (150, 50, 150)   


PLAYER_MOVE_SPEED = 7


pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
large_font = pygame.font.Font(None, 36)
score_font = pygame.font.Font(None, 28)
player_history = []
bfs_path_coords = []
dfs_path_coords = []
shortest_path_length = 0
dfs_path_length = 0
WIN_TIME = 0


class Player:
    def __init__(self, start_pos):
        self.r, self.c = start_pos
        self.color = PLAYER_COLOR
        self.goal_reached = False
        self.move_timer = 0
        self.move_delay = FPS // PLAYER_MOVE_SPEED
        global player_history
        player_history = [start_pos]

    def move(self, dr, dc):
        global WIN_TIME
        new_r, new_c = self.r + dr, self.c + dc
        
        if self.goal_reached: 
            return

        if (0 <= new_r < GRID_SIZE and 
            0 <= new_c < GRID_SIZE and 
            MAZE[new_r][new_c] == 0):
            
            self.r, self.c = new_r, new_c
            
            if not player_history or player_history[-1] != (self.r, self.c):
                player_history.append((self.r, self.c))
            
            if (self.r, self.c) == END:
                self.goal_reached = True
                WIN_TIME = pygame.time.get_ticks() 
                calculate_bfs_path()
                calculate_dfs_path()

    def draw(self):
        center_x = self.c * CELL_SIZE + CELL_SIZE // 2
        center_y = self.r * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, self.color, (center_x, center_y), CELL_SIZE // 2 - 2)


def run_solver(mode='BFS'):
    queue_or_stack = deque([START])
    visited = {START}
    parent = {START: None}
    path_found = False
    
    while queue_or_stack:
        if mode == 'BFS':
            current_r, current_c = queue_or_stack.popleft()
        else:
            current_r, current_c = queue_or_stack.pop()

        if (current_r, current_c) == END:
            path_found = True
            break

        for dr, dc in DIRECTIONS:
            next_pos = (current_r + dr, current_c + dc)
            next_r, next_c = next_pos
            
            if (0 <= next_r < GRID_SIZE and 
                0 <= next_c < GRID_SIZE and 
                MAZE[next_r][next_c] == 0 and 
                next_pos not in visited):
                
                visited.add(next_pos)
                parent[next_pos] = (current_r, current_c)
                queue_or_stack.append(next_pos)

    path_coords = []
    if path_found:
        curr = END
        while curr is not None:
            path_coords.append(curr)
            curr = parent.get(curr)
        path_coords.reverse()
        
    return path_coords

def calculate_bfs_path():
    global bfs_path_coords, shortest_path_length
    bfs_path_coords = run_solver(mode='BFS')
    shortest_path_length = len(bfs_path_coords) - 1 if bfs_path_coords else 0

def calculate_dfs_path():
    global dfs_path_coords, dfs_path_length
    dfs_path_coords = run_solver(mode='DFS')
    dfs_path_length = len(dfs_path_coords) - 1 if dfs_path_coords else 0

def draw_text(surface, text, position, font_obj, color):
    text_surface = font_obj.render(text, True, color)
    surface.blit(text_surface, position)
    return text_surface.get_width()

def draw_grid():
    maze_rect = pygame.Rect(0, 0, SCREEN_SIZE, SCREEN_SIZE)
    if player.goal_reached:
        t = (pygame.time.get_ticks() - WIN_TIME) / 500.0
        raw_color = 245 + 10 * (1 + math.sin(t * 3))
        clamped_color = int(max(0, min(255, raw_color)))
        
        r = g = b = clamped_color
        pygame.draw.rect(screen, (r, g, b), maze_rect)
    else:
        pygame.draw.rect(screen, PATH_BG_COLOR, maze_rect)
        
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            if MAZE[r][c] == 1:
                 pygame.draw.rect(screen, WALL_COLOR, rect)
            else:
                inner_rect = rect.inflate(-1, -1)
                pygame.draw.rect(screen, PATH_BG_COLOR, inner_rect)

            if (r, c) == START:
                 pygame.draw.rect(screen, START_COLOR, rect)
            if (r, c) == END:
                 pygame.draw.rect(screen, END_COLOR, rect)

def draw_path_line(path_coords, color, thickness):
    if not path_coords or len(path_coords) < 2:
        return
    
    pixel_coords = []
    for r, c in path_coords:
        x = c * CELL_SIZE + CELL_SIZE // 2
        y = r * CELL_SIZE + CELL_SIZE // 2
        pixel_coords.append((x, y))
        
    pygame.draw.lines(screen, color, False, pixel_coords, thickness)

def draw_all_paths_on_win():
    if not player.goal_reached:
        return
    
    draw_path_line(dfs_path_coords, DFS_PATH_COLOR, 2)
    draw_path_line(player_history, PLAYER_PATH_COLOR, 4)
    draw_path_line(bfs_path_coords, OPTIMAL_PATH_COLOR, 6)

def draw_dashboard():
    """Draws the fixed score/info dashboard on the right side."""
    
    DASHBOARD_START_X = SCREEN_SIZE
    DASHBOARD_HEIGHT = WINDOW_HEIGHT
    PANEL_PADDING = 15
    PANEL_HEIGHT = 100
    
    pygame.draw.rect(screen, DASHBOARD_BG, (DASHBOARD_START_X, 0, DASHBOARD_WIDTH, DASHBOARD_HEIGHT))
    
    panel_y = PANEL_PADDING
    panel_rect = pygame.Rect(DASHBOARD_START_X + PANEL_PADDING, panel_y, 
                             DASHBOARD_WIDTH - 2 * PANEL_PADDING, PANEL_HEIGHT)
    
    pygame.draw.rect(screen, PANEL_COLOR, panel_rect, 0, 5)
    
    status_text = "STATUS" if not player.goal_reached else "GOAL REACHED!"
    draw_text(screen, status_text, (panel_rect.x + 10, panel_rect.y + 10), large_font, DASHBOARD_HEADER_COLOR)
    
    if not player.goal_reached:
        draw_text(screen, "Controls: ARROW keys", (panel_rect.x + 10, panel_rect.y + 40), font, DASHBOARD_TEXT_COLOR)
        draw_text(screen, "Goal: Blue Square", (panel_rect.x + 10, panel_rect.y + 60), font, DASHBOARD_TEXT_COLOR)
    else:
        draw_text(screen, "Press SPACE to exit", (panel_rect.x + 10, panel_rect.y + 40), font, DASHBOARD_TEXT_COLOR)
    if player.goal_reached:
        player_len = len(player_history) - 1
        difference = player_len - shortest_path_length
        
        if difference == 0:
            verdict = "PERFECT!"
            verdict_color = START_COLOR
        else:
            verdict = f"{difference} EXTRA MOVES"
            verdict_color = PLAYER_PATH_COLOR
            
        
        panel_y += PANEL_HEIGHT + PANEL_PADDING
        panel_rect_2 = pygame.Rect(DASHBOARD_START_X + PANEL_PADDING, panel_y, 
                                 DASHBOARD_WIDTH - 2 * PANEL_PADDING, 80)
        pygame.draw.rect(screen, PANEL_COLOR, panel_rect_2, 0, 5)
        
        draw_text(screen, "VERDICT:", (panel_rect_2.x + 10, panel_rect_2.y + 10), large_font, DASHBOARD_TEXT_COLOR)
        draw_text(screen, verdict, (panel_rect_2.x + 10, panel_rect_2.y + 45), score_font, verdict_color)
        
        panel_y += 80 + PANEL_PADDING
        panel_rect_3 = pygame.Rect(DASHBOARD_START_X + PANEL_PADDING, panel_y, 
                                 DASHBOARD_WIDTH - 2 * PANEL_PADDING, 180)
        pygame.draw.rect(screen, PANEL_COLOR, panel_rect_3, 0, 5)
        
        draw_text(screen, "SCORE BREAKDOWN", (panel_rect_3.x + 10, panel_rect_3.y + 10), score_font, DASHBOARD_HEADER_COLOR)
        
        SCORE_RIGHT_ALIGN_X = panel_rect_3.x + DASHBOARD_WIDTH - 2 * PANEL_PADDING - 10 
        
        draw_text(screen, "Optimal (BFS):", (panel_rect_3.x + 10, panel_rect_3.y + 45), font, DASHBOARD_TEXT_COLOR)
        score_width = score_font.size(str(shortest_path_length))[0]
        draw_text(screen, str(shortest_path_length), (SCORE_RIGHT_ALIGN_X - score_width, panel_rect_3.y + 45), score_font, OPTIMAL_PATH_COLOR)

        draw_text(screen, "Your Path:", (panel_rect_3.x + 10, panel_rect_3.y + 75), font, DASHBOARD_TEXT_COLOR)
        score_width = score_font.size(str(player_len))[0]
        draw_text(screen, str(player_len), (SCORE_RIGHT_ALIGN_X - score_width, panel_rect_3.y + 75), score_font, PLAYER_PATH_COLOR)
  
        draw_text(screen, "DFS Path:", (panel_rect_3.x + 10, panel_rect_3.y + 105), font, DASHBOARD_TEXT_COLOR)
        score_width = score_font.size(str(dfs_path_length))[0]
        draw_text(screen, str(dfs_path_length), (SCORE_RIGHT_ALIGN_X - score_width, panel_rect_3.y + 105), score_font, DFS_PATH_COLOR)
        

        draw_text(screen, "MIND GAME COMPLETE", (panel_rect_3.x + 10, panel_rect_3.y + 140), score_font, DASHBOARD_TEXT_COLOR)


player = Player(START)
running = True

keys_pressed = {
    pygame.K_UP: False,
    pygame.K_DOWN: False,
    pygame.K_LEFT: False,
    pygame.K_RIGHT: False
}

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key in keys_pressed:
                keys_pressed[event.key] = True
            
            if player.goal_reached and event.key == pygame.K_SPACE:
                running = False 
        
        if event.type == pygame.KEYUP:
            if event.key in keys_pressed:
                keys_pressed[event.key] = False

    
    if not player.goal_reached:
        player.move_timer += 1
        
        if player.move_timer >= player.move_delay:
            player.move_timer = 0
            
            if keys_pressed[pygame.K_UP]:
                player.move(-1, 0)
            elif keys_pressed[pygame.K_DOWN]:
                player.move(1, 0)
            elif keys_pressed[pygame.K_LEFT]:
                player.move(0, -1)
            elif keys_pressed[pygame.K_RIGHT]:
                player.move(0, 1)

    
    draw_grid()
    draw_all_paths_on_win() 
    player.draw()
    draw_dashboard()

   
    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()

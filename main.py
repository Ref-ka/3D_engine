import pygame
import numpy as np
from math import sqrt, fabs
pygame.init()


class Line:
    def __init__(self, vector, length, start_point):
        self.vector = np.matrix(vector)
        self.length = length
        self.start_point = start_point
        self.end_point = length * self.vector
        self.end_point = self.end_point.tolist()[0]
        print(self.end_point)

    def calc_endpoint(self):
        pass
        # self.end_point.append(round(self.vector[2] * self.length / sqrt(self.vector[0] ** 2 + self.vector[1] ** 2 + self.vector[2] ** 2), 1))
        # self.end_point.append(round(self.vector[1] * sqrt(self.length ** 2 - self.end_point[0] ** 2) /
        #                             sqrt(self.vector[0] ** 2 + self.vector[1] ** 2), 1))
        # self.end_point.append(round(self.vector[0] * sqrt(self.length ** 2 - self.end_point[0] ** 2) /
        #                             sqrt(self.vector[0] ** 2 + self.vector[1] ** 2), 1))
        # self.end_point = self.end_point[::-1]


class Engine:
    def __init__(self):
        self.figures = [Line([1, 1, -1], 5, [0, 0, 0])]
        # Some lines
        # Line([-1, -1, -1], 30, [0, 0, 0]), Line([1, 1, 0], 30, [0, 0, 0]), Line([-1, -1, 0], 30, [0, 0, 0])
        self.surface = pygame.display.set_mode((600, 600))
        self.line_color = (255, 255, 255)
        self.line_color_start = (255, 0, 0)
        self.line_color_end = (0, 0, 255)
        self.clock = pygame.time.Clock()
        self.view_point = [-20, 0, 0]
        self.view_vector = [1, 0, 0]
        self.view_length = 20
        self.screen_point = [0, 0, 0]
        self.font = pygame.font.SysFont('arial', 15)

    def draw_info(self, figure, start_point, end_point, x_start, x_end,
                  y_start, y_end, fac_draw, view_point):
        self.surface.blit(self.font.render(f'pos_start: {figure.start_point}', True, self.line_color), (90, 50))
        self.surface.blit(self.font.render(f'pos_end: {figure.end_point}', True, self.line_color), (250, 50))
        self.surface.blit(self.font.render(f'pos_start_proj: {start_point}', True, self.line_color), (90, 70))
        self.surface.blit(self.font.render(f'pos_end_proj: {end_point}', True, self.line_color), (250, 70))
        self.surface.blit(self.font.render(f'pos_start_scrn: {x_start, y_start}', True, self.line_color), (250, 90))
        self.surface.blit(self.font.render(f'pos_end_scrn: {x_end, y_end}', True, self.line_color), (250, 110))
        self.surface.blit(self.font.render(f'fac_fl: {fac_draw}', True, self.line_color), (90, 130))
        self.surface.blit(self.font.render(f'view_point: {view_point}', True, self.line_color), (90, 150))
        # print('    start_old', figure.start_point, 'start_new', start_point, 'start_full', x_start, y_start)
        # print('    end_old', figure.end_point, 'end_new', end_point, 'end_full', x_end, y_end)
        # print('    view_vector', self.view_vector)

    def draw_cycle(self, view_fl):
        self.surface.blit(self.font.render(f'view_fl: {view_fl}', True, self.line_color), (90, 150))

    def screen_point_calc(self):
        view_vector_xy_diagonal = sqrt(self.view_vector[0] ** 2 + self.view_vector[1] ** 2)
        view_vector_full_diagonal = sqrt(self.view_vector[0] ** 2 + self.view_vector[1] ** 2 + self.view_vector[2] ** 2)
        screen_xy_diagonal = view_vector_xy_diagonal * self.view_length / view_vector_full_diagonal

        self.screen_point[2] = self.view_vector[2] * self.view_length / view_vector_full_diagonal
        self.screen_point[1] = self.view_vector[1] * screen_xy_diagonal / view_vector_xy_diagonal
        self.screen_point[0] = self.view_vector[0] * screen_xy_diagonal / view_vector_xy_diagonal

        self.screen_point[2] = round(self.screen_point[2], 1)
        self.screen_point[1] = round(self.screen_point[1], 1)
        self.screen_point[0] = round(self.screen_point[0], 1)

    def make_projection(self, x, y, z, figure_vector):
        a = ([[self.view_vector[1], -self.view_vector[0], 0],
             [self.view_vector[2], self.view_vector[2], -(self.view_vector[0] + self.view_vector[1])],
             [self.view_vector[0], self.view_vector[1], self.view_vector[2]]])
        # print('    xyz', x, y, z)
        b = [x * self.view_vector[1] - y * self.view_vector[0], self.view_vector[2]*(x + y) - z * (self.view_vector[0] + self.view_vector[1]), 0]
        # print('a')
        # for line in a:
        #     print('    ', line)
        # print('b')
        # print('    ', b)
        # print(list(fabs(i) for i in self.view_vector))
        # print(list(fabs(i) for i in figure_vector))
        if np.linalg.det(a) == 0:
            ans = [x, y, z]
        else:
            ans = np.linalg.solve(a, b)
        # print('ans')
        # print('    ', ans)
        # print('------------')
        return ans

    def make_projection_new(self, point_x, point_y, point_z):  # x1 = point_x, x2 = self.view_point[0]
        a = [[self.view_point[1] - point_y, point_x - self.view_point[0], 0],
             [self.view_point[2] - point_z,
              self.view_point[2] - point_z,
              point_y - self.view_point[1] + point_x - self.view_point[0]],
             [self.view_vector[0], self.view_vector[1], self.view_vector[2]]]
        b = [(self.view_point[1] - point_y) * point_y,
             (self.view_point[2] - point_z) * (point_y + point_x) -
             point_z * (self.view_point[1] - point_y + self.view_point[0] - point_x),
             0]
        if np.linalg.det(a) == 0:
            ans = [point_x, point_y, point_z]
        else:
            ans = np.linalg.solve(a, b)
        return ans

    def draw(self):
        print('    draw!--------------')
        for figure in self.figures:
            pos_start_proj = self.make_projection_new(figure.start_point[0],
                                                      figure.start_point[1],
                                                      figure.start_point[2])
            pos_end_proj = self.make_projection_new(figure.end_point[0],
                                                    figure.end_point[1],
                                                    figure.end_point[2])

            fac = 1
            fac_draw = 0
            if pos_end_proj[0] > 0 and self.view_vector[1] * -1 > 0:
                if pos_end_proj[1] >= 0 and self.view_vector[0] >= 0:
                    fac = -1
                    fac_draw = 1
            if pos_end_proj[0] < 0 and self.view_vector[1] * -1 < 0:
                if pos_end_proj[1] >= 0 and self.view_vector[0] >= 0:
                    fac = -1
                    fac_draw = 2
            if pos_end_proj[0] > 0 and self.view_vector[1] * -1 > 0:
                if pos_end_proj[1] <= 0 and self.view_vector[0] <= 0:
                    fac = -1
                    fac_draw = 3
            if pos_end_proj[0] < 0 and self.view_vector[1] * -1 < 0:
                if pos_end_proj[1] <= 0 and self.view_vector[0] <= 0:
                    fac = -1
                    fac_draw = 4

            #  You need to add another checks like << >< <>
            pos_start_screen = [round(sqrt(pos_start_proj[0] ** 2 + pos_start_proj[1] ** 2), 1),
                                round(pos_start_proj[2], 1)]
            pos_end_screen = [round(sqrt(pos_end_proj[0] ** 2 + pos_end_proj[1] ** 2), 1) * fac,
                              round(pos_end_proj[2], 1)]

            # view_point = list()
            # view_point.append(round(-self.view_vector[2] * self.view_length /
            #                         sqrt(fabs(-self.view_vector[0] ** 2 - self.view_vector[1] ** 2 - self.view_vector[2] ** 2)), 1))
            # view_point.append(round(-self.view_vector[1] * sqrt(self.view_length ** 2 - view_point[0] ** 2) /
            #                         sqrt(fabs(-self.view_vector[0] ** 2 + -self.view_vector[1] ** 2)), 1))
            # view_point.append(round(-self.view_vector[0] * sqrt(self.view_length ** 2 - view_point[0] ** 2) /
            #                         sqrt(fabs(-self.view_vector[0] ** 2 + -self.view_vector[1] ** 2)), 1))
            # view_point = view_point[::-1]

            d_start = round(sqrt((self.view_point[0] - pos_start_proj[0]) ** 2 + (self.view_point[1] - pos_start_proj[1]) ** 2
                                 + (self.view_point[2] - pos_start_proj[2]) ** 2), 1)
            d_end = round(sqrt((self.view_point[0] - pos_end_proj[0]) ** 2 + (self.view_point[1] - pos_end_proj[1]) ** 2
                               + (self.view_point[2] - pos_end_proj[2]) ** 2), 1)

            if d_start < d_end:
                first_point = pos_end_screen
                last_point = pos_start_screen
            else:
                first_point = pos_start_screen
                last_point = pos_end_screen

            pygame.draw.circle(self.surface,
                               center=[pos_start_screen[0] * 10 + 300, pos_start_screen[1] * 10 + 400],
                               color=self.line_color_start,
                               radius=d_start)  # d_start / 8
            pygame.draw.circle(self.surface,
                               center=[pos_end_screen[0] * 10 + 300, pos_end_screen[1] * 10 + 400],
                               color=self.line_color_end,
                               radius=d_end)

            self.draw_info(figure, pos_start_proj, pos_end_proj, pos_start_screen[0], pos_end_screen[0],
                           pos_start_screen[1], pos_end_screen[1], fac_draw, self.view_point)

            # d_diff = fabs(d_end - d_start)
            last_j = 0
            d = d_start
            color = [251, 3, 3]
            # d = 1
            if pos_start_screen[0] != pos_end_screen[0]:
                k = (pos_end_screen[1] - pos_start_screen[1]) / (pos_end_screen[0] - pos_start_screen[0])
                c = k * pos_start_screen[0] - pos_start_screen[1]
                print(f'        k: {k}, c: {c}')
                print(f'        p_s_scr: {pos_start_screen}')
                print(f'        p_e_scr: {pos_end_screen}')

                for i in range(int(pos_start_screen[0] * 10),
                               int(pos_end_screen[0] * 10) + 1,
                               1 if pos_start_screen[0] < pos_end_screen[0] else -1):
                    j = round(k * (i / 10) + c, 1)
                    # z = figure.start_point[2] - ((i - figure.start_point[0]) * figure.vector[2] / figure.vector[0])
                    # print('    i, j', i, j)
                    # d = round(d, 1)
                    # print(type(tuple(color)))
                    pygame.draw.circle(self.surface,
                                       center=[i + 300, j * 10 + 400],
                                       color=tuple(color),
                                       radius=int(d / 10 if d > 1 else 1))
                    if i != (pos_start_screen[0] if pos_start_screen[0] < pos_end_screen[0] else pos_end_screen[0]) \
                            and fabs(last_j - j) * 10 > 1:
                        pygame.draw.circle(self.surface,
                                           center=[i + 300, j * 10 + 400],
                                           color=self.line_color,
                                           radius=int(d / 10 if d > 1 else 1))
                    last_j = j
                    # d += d_diff
                    if color[0] < 252 and color[1] < 252 and color[2] < 252:
                        color[0] -= 2
                        color[1] += 2
                        color[2] += 2
            else:
                for m in range(int(pos_start_screen[1] * 10),
                               int(pos_end_screen[1] * 10) + 1,
                               1 if pos_start_screen[1] < pos_end_screen[1] else -1):
                    pygame.draw.circle(self.surface, center=[pos_start_screen[0] + 300, m + 400], color=tuple(color),
                                       radius=int(d / 10 if d > 1 else 1))

    def cycle(self):
        while True:
            print('another cycle!')
            self.surface.fill((0, 0, 0))
            self.draw()
            self.surface.blit(self.font.render(f'i: {self.view_vector[0]}', True, self.line_color), (50, 50))
            self.surface.blit(self.font.render(f'j: {self.view_vector[1]}', True, self.line_color), (50, 70))
            self.surface.blit(self.font.render(f'k: {self.view_vector[2]}', True, self.line_color), (50, 90))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            keys = pygame.key.get_pressed()

            # view_vector change
            if keys[pygame.K_LEFT]:
                print('left')
                if self.view_vector[0] > 0.01:
                    self.view_vector[0] -= 0.01
                    self.view_vector[0] = round(self.view_vector[0], 2)
            if keys[pygame.K_RIGHT]:
                print('right')
                if self.view_vector[0] < 1:
                    self.view_vector[0] += 0.01
                    self.view_vector[0] = round(self.view_vector[0], 2)
            if keys[pygame.K_UP]:
                print('up')
                if 0 <= self.view_vector[1] < 1 and self.view_vector[0] > 0:
                    self.view_vector[1] += 0.01
                    self.view_vector[0] -= 0.01
                    self.view_vector[1] = round(self.view_vector[1], 2)
                    self.view_vector[0] = round(self.view_vector[0], 2)
                elif self.view_vector[1] > 0 and self.view_vector[0] > -1:
                    self.view_vector[1] -= 0.01
                    self.view_vector[0] -= 0.01
                    self.view_vector[1] = round(self.view_vector[1], 2)
                    self.view_vector[0] = round(self.view_vector[0], 2)
                elif self.view_vector[1] > -1 and self.view_vector[0] < 0:
                    self.view_vector[1] -= 0.01
                    self.view_vector[0] += 0.01
                    self.view_vector[1] = round(self.view_vector[1], 2)
                    self.view_vector[0] = round(self.view_vector[0], 2)
                elif self.view_vector[1] < 0 and self.view_vector[0] < 1:
                    self.view_vector[1] += 0.01
                    self.view_vector[0] += 0.01
                    self.view_vector[1] = round(self.view_vector[1], 2)
                    self.view_vector[0] = round(self.view_vector[0], 2)
            if keys[pygame.K_DOWN]:
                print('down')
                if self.view_vector[1] > -25:
                    self.view_vector[1] -= 0.1
                    self.view_vector[1] = round(self.view_vector[1], 1)
                elif self.view_vector[1] == -25:
                    self.view_vector[1] = 25
                elif self.view_vector[1] < 0.1:
                    self.view_vector[1] -= 0.1
                    self.view_vector[1] = round(self.view_vector[1], 1)
                elif self.view_vector[1] == 0.1:
                    self.view_vector[1] = -0.1
            if keys[pygame.K_1]:
                print('one')
                if self.view_vector[2] > -50:
                    self.view_vector[2] -= 0.1
                    self.view_vector[2] = round(self.view_vector[2], 1)
                elif self.view_vector[2] == -50:
                    self.view_vector[2] = 50
                elif self.view_vector[2] < 0.1:
                    self.view_vector[2] -= 0.1
                    self.view_vector[2] = round(self.view_vector[2], 1)
                elif self.view_vector[2] == 0.1:
                    self.view_vector[2] = -0.1
            if keys[pygame.K_2]:
                print('two')
                if self.view_vector[2] < 50:
                    self.view_vector[2] += 0.1
                    self.view_vector[2] = round(self.view_vector[2], 1)
                elif self.view_vector[2] == 50:
                    self.view_vector[2] = -50
                elif self.view_vector[2] > -0.1:
                    self.view_vector[2] += 0.1
                    self.view_vector[2] = round(self.view_vector[2], 1)
                elif self.view_vector[2] == -0.1:
                    self.view_vector[2] = 0.1

            # view_point change
            if keys[pygame.K_w]:
                self.view_point[0] += 1
            if keys[pygame.K_s]:
                self.view_point[0] -= 1
            if keys[pygame.K_a]:
                self.view_point[1] += 1
            if keys[pygame.K_d]:
                self.view_point[1] -= 1
            if keys[pygame.K_SPACE]:
                self.view_point[2] += 1
            if keys[pygame.K_LCTRL]:
                self.view_point[2] -= 1
            self.clock.tick(60)


engine = Engine()
engine.cycle()

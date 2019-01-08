#使用pygame编写的游戏的基本结构

#import sys  #退出游戏时会用到(代码重构后，在gamefunction中调用，所以主函数可以省略
import pygame
from ship import Ship
from settings import Settings
from game_stats import GameStats
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from button import Button
from score_board import ScoreBoard

def run_game():
    #初始化pygame、设置和屏幕对象
    pygame.init()   #初始化背景设置
    ai_settings = Settings()    #创建窗口设置的实例，下方再调用它
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))#显示窗口，名为screen
    pygame.display.set_caption("Alien Invasion")
    play_button = Button(ai_settings,screen,"play")
    stats = GameStats(ai_settings)  #创建一个统计游戏信息的stats实例
    sb = ScoreBoard(ai_settings,screen,stats)   #创建记分牌实例

    #创建一艘飞船
    ship = Ship(ai_settings,screen) #提供screen实参，表示将在screen上绘制飞船

    #创建一个用于存储子弹的编组
    bullets = Group()

    #创建一个外星人空的编组
    aliens = Group()

    #创建外星人群
    gf.creat_fleet(ai_settings,stats,screen,ship,aliens)


    #开始游戏的主循环
    while True:
        #开始监视鼠标和键盘事件
        gf.check_event(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)

        if stats.game_active:
            #调用飞船移动位置坐标更新的方法
            ship.update()
            bullets.update()

            #删除已消失的子弹
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)

            #更新外星人的坐标位置
            gf.update_alien(ai_settings,stats,screen,sb,ship,aliens,bullets)

        #更新屏幕，包括screen和ship
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)

run_game()


import sys
from time import sleep
import  pygame
from bullet import Bullet
from alien import Alien
from game_stats import GameStats

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        # 向左向右移动飞船
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings,screen,ship,bullets):
    """ 创建一颗子弹，并将其加入到编组bullets中,屏幕中的子弹数量未达到上限时，可发射一颗子弹"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event,ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_event(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
            check_keydown_events(event,ai_settings,screen,ship,bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,mouse_x,mouse_y,ship,aliens,bullets)

def check_play_button(ai_settings,screen,stats,sb,play_button,mouse_x,mouse_y,ship,aliens,bullets):
    """玩家在单机play按钮时，开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.increase_speed()
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        #重置记分牌图像
        sb.prep_high_score()
        sb.prep_score()
        sb.prep_level()
        sb.prep_ships()

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并将飞船放到屏幕低端中央
        creat_fleet(ai_settings,stats,screen,ship,aliens)
        ship.center_ship()


def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都会重绘屏幕
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()

    #在飞船后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    #如果游戏处于飞活动状态，就绘制play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见，刷新
    pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """更新子弹位置，并删除已经消失的子弹"""
    #更新子弹位置
    bullets.update()

    #remonve the bullet whoes rect.bottom<0
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #print(len(bullets))

    check_alien_bullet_collisons(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_alien_bullet_collisons(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """响应检查是否有子弹与外星人发生了碰撞"""
    #若发生了碰撞，则删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points
            sb.prep_score()
        check_high_score(stats,sb)

    if len(aliens) == 0:
        #删除现有的子弹并创建一群新的外星人
        bullets.empty()
        ai_settings.increase_speed()
        #提升等级
        stats.level += 1
        sb.prep_level()

        creat_fleet(ai_settings,stats,screen,ship,aliens)

def get_number_aliens_x(ai_settings,alien_width):
    """计算一行能够容纳多少个外星人，获得数量"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_alein_x = int(available_space_x/(alien_width + 20))
    return number_alein_x

def creat_alien(ai_settings,stats,screen,aliens,alien_number,row_number):
    """创建一个外星人并将其放在当前行"""
    #外星人间距为20
    alien = Alien(ai_settings,stats,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + (20 + alien_width) * alien_number   #每个外星人在x上的坐标
    alien.rect.x = alien.x
    alien.y = alien.rect.height + (alien.rect.height + 20) * row_number
    alien.rect.y = alien.y
    aliens.add(alien)

def creat_fleet(ai_settings,stats,screen,ship,aliens):
    """创建外星人群"""
    #创建第一行外星人并计算一行能够容纳多少个外星人
    alien = Alien(ai_settings,stats,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,alien.rect.height,ship.rect.height)

    #创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            creat_alien(ai_settings,stats,screen,aliens,alien_number,row_number)

def get_number_rows(ai_settings,alien_height,ship_height):
    """计算屏幕可以容纳多少行外星人"""
    available_space_y = ai_settings.screen_width - 25*alien_height - ship_height   #飞船+间距   乘以n的可用空间
    number_rows = int(available_space_y / (alien_height + 20))   #外星人行数
    return number_rows

def check_fleet_edges(ai_settings,aliens):
    """当有外星人到达边缘时，采取的相应措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    """将正群外星人下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets):
    """响应被外星人撞到的飞船"""
    #将ships_left减1
    if stats.ships_left > 0:
        stats.ships_left -= 1

        #更新记分牌
        sb.prep_ships()

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并将飞船放到屏幕低端中央
        creat_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        #暂停
        sleep(1)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,stats,screen,sb,ship,aliens,bullets):
    """检查是否有外星人到达屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞一样进行处理
            ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)
            break


def update_alien(ai_settings,stats,screen,sb,ship,aliens,bullets):
    """检查是否有外星人位于屏幕边缘，并更新正群外星人的位置，这两个动作"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #监测外星人与飞船质检的碰撞（包括碰撞后的处理吗？？？不包括
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)
        print("Ship het!!!")

    check_aliens_bottom(ai_settings,stats,screen,sb,ship,aliens,bullets)

def check_high_score(stats,sb):
    """检查是否产生了新的最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()





#ship模块，包含ship类，它将负责飞船的大部分行为
import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self,ai_settings,screen):  #指定要将飞船绘制到什么地方
        """初始化飞船并设置它的初始位置"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')   #加载图像，并返回一个surface
        self.rect = self.image.get_rect()   #获取飞船surface的rect属性
        self.screen_rect = screen.get_rect()    #获取窗口surface的rect属性

        #将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #在飞船属性中存储小数值
        self.center = float(self.rect.centerx)

        #移动标志初始化
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志调整飞船位置（显示上），其余的计算和动作响应在gamefunction"""
        #更新飞船的center值，而不是rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= self.ai_settings.ship_speed_factor

        #根据self.center更新rect对象
        self.rect.centerx = self.center

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        """让飞船在屏幕上居中的方法"""
        self.center = self.screen_rect.centerx
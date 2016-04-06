import pygame
 
 
def img_list(self, source_sheet, x, y, size):
    '''
    a generic image list creator
 
    it creates a list of images such as an animation
    and returns the list
 
    it needs the spritesheet that is to be animated from
    and the number of pieces it's to be chopped up in
    vertical then horisontal
    '''
    self.image = pygame.image.load(source_sheet).convert_alpha()
    w, h = self.image.get_size()
    w /= size[0]
    h /= size[1]
    results = []
    for i in range(y):
        for j in range(x):
            results.append(self.image.subsurface(j*w, i*h, w, h))
    return results
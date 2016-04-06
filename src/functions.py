import pygame
 
 
def img_list(source_sheet, x, y):
    '''
    a generic image list creator
 
    it creates a list of images such as an animation
    and returns the list
 
    it needs the spritesheet that is to be animated from
    and the number of pieces it's to be chopped up in
    vertical then horisontal
    '''
    w, h = source_sheet.get_size()
    w /= x
    h /= y
    results = []
    for i in range(y):
        for j in range(x):
            results.append(source_sheet.subsurface(j*w, i*h, w, h))
    return results
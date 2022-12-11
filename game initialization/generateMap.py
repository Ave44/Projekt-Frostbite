def generateMap():
    width, height = 101, 101
    a, b = 50, 50
    r = 51

    mapAreaArray = [['.' for x in range(width)] for y in range(height)]

    # draw the circle
    for y in range(height):
        for x in range(width):
            # see if we're close to (x-a)**2 + (y-b)**2 == r**2
            if abs((x - a) ** 2 + (y - b) ** 2) < r ** 2:
                mapAreaArray[y][x] = '#'

    # print the map
    # for line in mapAreaArray:
    #    print( ' '.join(line))

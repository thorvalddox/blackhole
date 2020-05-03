from subprocess import run

tiles = [0,1,2,3,4,5,10,11,12,13,14,20,21,22,23,30,31,32,40,41,50]
def gen_polygon(index):
    x = index % 10
    y = index // 10
    sz = 10
    sx = x * 4 + y*2
    sy = y*3 
    for xx,yy in [(2,2),(2,0),(4,1),(4,3),(2,4),(0,3),(0,1)]:
        yield sz*(xx+sx),sz*(yy+sy)
        
def gen_polygon_2(index):
    poly = list(gen_polygon(index))
    coords = ' '.join(f'{x},{y}' for x,y in poly[1:])
    x,y = poly[0]
    yield """<polygon points="{}" style="fill:white;stroke:black;stroke-width:1" id="tile_{}"/>"""\
        .format(coords,index)
    yield f"""<text x="{x}" y="{y}" fill="black" text-anchor="middle" dominant-baseline="central" id="text_{index}"></text>"""
    
def gen_svg_struct():
    for x in tiles:
        yield from gen_polygon_2(x)
    
def create_svg():
    run(('transcrypt','core.py','-n'))
    run(('cp','-a','./__target__/.','.'))
    run(('rm','-rf','./__target__'))
    with open('./index.html','w') as file:
        file.write("<html><svg height=\"300\" width=\"300\" id=\"blackholeroot\">\n")
        for x in gen_svg_struct():
            file.write(x+"\n")
        file.write("</svg>")
        file.write("<script type=\"module\" src=\"core.js\"></script>\n</html>")
    run(('git','add','-A'))
    run(('git','commit','-m',input('message')))
            
create_svg()


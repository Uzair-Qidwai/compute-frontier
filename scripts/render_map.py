"""Render a fixed, self-contained North America basemap for the dashboard."""
from pathlib import Path
import sys
DARK = "--dark" in sys.argv
def tone(light, dark): return dark if DARK else light
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

WEST, EAST, SOUTH, NORTH = -129, -62, 14, 58
W, H = 3840, 2400
fig = plt.figure(figsize=(W/240, H/240), dpi=240, facecolor=tone('#dbe9eb', '#112731'))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor(tone('#dbe9eb', '#112731'))
m = Basemap(projection='cyl', llcrnrlon=WEST, urcrnrlon=EAST,
            llcrnrlat=SOUTH, urcrnrlat=NORTH, resolution='i', ax=ax)
m.drawmapboundary(fill_color=tone('#dbe9eb', '#112731'), linewidth=0)
m.fillcontinents(color=tone('#f4f2e9', '#223d46'), lake_color=tone('#dbe9eb', '#112731'), zorder=2)
m.drawcoastlines(color=tone('#79999d', '#6b929a'), linewidth=.65, zorder=5)
m.drawcountries(color=tone('#667e80', '#8aa9ae'), linewidth=.9, zorder=6)
m.drawstates(color=tone('#b8c6bf', '#4b6871'), linewidth=.42, zorder=4)
m.drawrivers(color=tone('#bdd5d6', '#35565f'), linewidth=.35, zorder=3)
m.drawparallels(range(20, 60, 10), linewidth=.35, color=tone('#abc9cc', '#2d4955'), dashes=[1, 4], zorder=1)
m.drawmeridians(range(-120, -59, 10), linewidth=.35, color=tone('#abc9cc', '#2d4955'), dashes=[1, 4], zorder=1)
for label,x,y,size in [
    ('CANADA',-105,52,22),('UNITED STATES',-100,39,24),('MEXICO',-105,24,21),
    ('PACIFIC OCEAN',-124,28,13),('ATLANTIC OCEAN',-68,31,13),
]:
    color = tone('#859b98', '#a4bcc0') if 'OCEAN' not in label else tone('#96b7bc', '#789ca6')
    ax.text(x,y,label,ha='center',va='center',fontsize=size,color=color,
            fontfamily='DejaVu Sans',fontweight='bold' if 'OCEAN' not in label else 'normal',
            alpha=.68, zorder=7)
ax.set_xlim(WEST,EAST);ax.set_ylim(SOUTH,NORTH)
ax.set_aspect('auto');ax.axis('off')
out=Path(__file__).resolve().parents[1]/'dist'/('north-america-map-dark.png' if DARK else 'north-america-map.png')
fig.savefig(out,dpi=240,facecolor=fig.get_facecolor(),pad_inches=0)
plt.close(fig)
print(f'Wrote {out.name}: {out.stat().st_size:,} bytes, {W}×{H}')

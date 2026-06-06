import sys
sys.path.insert(0, "python")

from reel_converter.gate3_render.png_export import export_pptx_to_pngs

pngs = export_pptx_to_pngs('output/combined_reel.pptx', 'output/pngs')
print(f'Exported {len(pngs)} PNGs:')
for p in pngs:
    print(f'  {p}')

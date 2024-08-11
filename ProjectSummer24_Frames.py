import json
from PIL import Image, ImageDraw

f = open("sim.json", "r")
road_seg = []
vehicle_series = []
for line in f:
    js_obj = json.loads(line)
    if "road_segments" in js_obj:
        road_seg = js_obj["road_segments"]
    if "vehicles" in js_obj:
        vehicle_series.append(js_obj["vehicles"])
print(road_seg)
for i in vehicle_series:
    print(i)


def img_background(road_seg_list, loop_counter):
    image = Image.new("RGB", (1000, 1000), "black")
    mydraw = ImageDraw.Draw(image)
    mydraw.text((200, 5), "Traffic Simulator: Frame #" + str(loop_counter), align="center", fill="white", font_size=24)
    for seg in road_seg_list:
        mydraw.line([(seg["x1a"], seg["y1a"]), (seg["x2a"], seg["y2a"])], width=10, fill="green", joint="curve")
    return image

frames = []
print(road_seg[0])
print(vehicle_series[0][0])
loop_count = 0
for i in vehicle_series:
    frame_cur = img_background(road_seg, loop_count)
    draw = ImageDraw.Draw(frame_cur)
    for veh in i:
        draw.ellipse((veh["x"]-2, veh["y"]-2, veh["x"]+2, veh["y"]+2), outline="white", width=3, fill="yellow")
    frames.append(frame_cur)
    loop_count += 1

frame_one = frames[0]
frame_one.save("test2.gif", format="GIF", save_all=True, loop=0, append_images=frames, duration=100)

print(loop_count)
exit(0)

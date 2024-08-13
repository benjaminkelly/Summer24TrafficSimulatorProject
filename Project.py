import uuid
import math
import random
import json

int(random.expovariate(0.1))

class Vehicle:
    def __init__(self, x, y, orient):
        self.orient = orient
        self.current_vx = 0
        self.current_vy = 0
        self.current_ax = 0
        self.current_ay = 0
        self.next_vx = 0
        self.next_vy = 0
        self.next_ax = 0
        self.next_ay = 0
        self.dt = 1 / 60
        self.current_px = x
        self.current_py = y
        self.next_px = x
        self.next_py = y
        self.id = uuid.uuid4()
        return

    def update_phase1(self, road_segment, dt):
        # Update position and velocity
        if self.orient == "east":
            if self.current_vx + self.current_ax * dt < 0:
                self.next_px -= (self.current_vx * dt + self.current_ax * dt * dt / 2)
                self.next_vx = 0
            else:
                self.next_vx += self.current_ax * dt
                self.next_px += (self.current_vx * dt + self.current_ax * dt * dt / 2)
        else:
            if self.current_vx + self.current_ax * dt > 0:
                self.next_px -= (self.current_vx * dt + self.current_ax * dt * dt / 2)
                self.next_vx = 0
            else:
                self.next_vx += self.current_ax * dt
                self.next_px += (self.current_vx * dt + self.current_ax * dt * dt / 2)
        if self.orient == "north":
            if self.current_vy + self.current_ay * dt < 0:
                self.next_py -= (self.current_vy * dt + self.current_ay * dt * dt / 2)
                self.next_vy = 0
            else:
                self.next_vy += self.next_ay * dt
                self.next_py += (self.current_vy * dt + self.current_ay * dt * dt / 2)
        else:
            if self.current_vy + self.current_ay * dt > 0:
                self.next_py -= (self.current_vy * dt + self.current_ay * dt * dt / 2)
                self.next_vy = 0
            else:
                self.next_vy += self.next_ay * dt
                self.next_py += (self.current_vy * dt + self.current_ay * dt * dt / 2)
        distancefinal = math.sqrt((road_segment.x2 - self.next_px) ** 2 + (road_segment.y2 - self.next_py) ** 2)
        if road_segment.trafficcontrol == "Stop sign" and distancefinal <= 100:
            if distancefinal == 0:
                self.next_vx = 0
                self.next_vy = 0
            elif distancefinal > 0 and distancefinal < 50:
                self.set_acceleration(-2.5)
            elif distancefinal >= 50 and distancefinal < 100:
                self.set_acceleration(-1)
            else:
                pass

        else:
            speed = math.sqrt(self.next_vx**2 + self.next_vy**2)
            speedfraction = speed/road_segment.speedlimit
            if speedfraction >= 0 and speedfraction <= 0.6:
                self.set_acceleration(2)
            elif speedfraction > 0.6 and speedfraction < 0.8:
                self.set_acceleration(1)
            elif speedfraction > 0.8 and speedfraction < 1:
                self.set_acceleration(0.5)
            elif speedfraction >= 1:
                self.set_acceleration(0)
            else:
                self.set_acceleration(-2)

    def update_phase2(self, dt):
        self.current_px = self.next_px
        self.current_py = self.next_py
        self.current_vx = self.next_vx
        self.current_vy = self.next_vy
        self.current_ax = self.next_ax
        self.current_ay = self.next_ay
        self.stopped = False
        self.current_road_index = 0
        print("id: " + str(self.id) + " x: " + str(self.current_px) + " y: " + str(self.current_py) + "        vx:  "
        + str(self.current_vx) + " vy: " + str(self.current_vy) + "            ax: " + str(self.current_ax) + " ay: " + str(self.current_ay))
        return

    def set_acceleration(self, a):
        if self.orient == "east":
            self.next_ax = a
            self.next_ay = 0
        elif self.orient == "west":
            self.next_ax = -a
            self.next_ay = 0
        elif self.orient == "north":
            self.next_ax = 0
            self.next_ay = a
        else:
            self.next_ax = 0
            self.next_ay = -a
        return

    def to_dict(self):
        v = {}
        v["id"] = str(self.id)
        v["x"] = self.current_px
        v["y"] = self.current_py
        return v

class VehicleGenerator:
    def __init__(self, x, y, orient, rate):
        self.x = x
        self.y = y
        self.orient = orient
        self.rate = rate
        self.amtleft = 1
        return

    def update(self):
        self.amtleft -= 1
        if self.amtleft <= 0:
            self.amtleft = random.expovariate(1.0 / self.rate)
            print('adding vehicle' + " " + str(self.amtleft))
            a = Vehicle(self.x, self.y, self.orient)
            return a
        else:
            return None


class Simulation:
    def __init__(self):
        self.segment1 = []
        self.segment2 = []
        self.vehicles = {}
        self.t = 0.0
        self.frame_count = 0
        self.dt = 1 / 60
        self.road_seg = []
        a = Road_Segment(0, 400, 400, 400, 20, True, "east", "Stop sign")
        b = Road_Segment(400, 400, 800, 400, 20, False, "east", "No stop sign")
        c = Road_Segment(800, 405, 405, 405, 20, False, "west", "Stop sign")
        d = Road_Segment(405, 405, 0, 405, 20, False, "west", "No stop sign")
        e = Road_Segment(405, 0, 405, 400, 20, False, "north", "Stop sign")
        f = Road_Segment(405, 400, 405, 800, 20, False, "north", "No stop sign")
        g = Road_Segment(400, 800, 400, 405, 20, False, "south", "Stop sign")
        h = Road_Segment(400, 405, 400, 0, 20, False, "south", "No stop sign")
        self.road_seg.append(a)
        self.road_seg.append(b)
        self.road_seg.append(c)
        self.road_seg.append(d)
        self.road_seg.append(e)
        self.road_seg.append(f)
        self.road_seg.append(g)
        self.road_seg.append(h)
        a.roadSeg[0] = b
        a.roadSeg[1] = h
        a.roadSeg[2] = f
        a.roadSeg[3] = d
        c.roadSeg[0] = d
        c.roadSeg[1] = f
        c.roadSeg[2] = h
        c.roadSeg[3] = b
        e.roadSeg[0] = f
        e.roadSeg[1] = b
        e.roadSeg[2] = d
        e.roadSeg[3] = h
        g.roadSeg[0] = h
        g.roadSeg[1] = d
        g.roadSeg[2] = b
        g.roadSeg[3] = f

    def add_vehicle(self, veh):
        self.vehicles[veh.id] = veh

    def run(self, steps):
        outfile = open("sim.json", "w")
        new_dict = {}
        road_seg_list = []
        for ea_ch in self.road_seg:
            new_dictionary_road_seg = ea_ch.to_dict()
            road_seg_list.append(new_dictionary_road_seg)
        new_dict_2 = {}
        new_dict_2["road_segments"] = road_seg_list
        outfile.write(json.dumps(new_dict_2))
        outfile.write("\n")
        for _ in range(steps):
            vehicle_list = []
            for seg in self.road_seg:
                seg.update_phase1(self.dt)
            for seg in self.road_seg:
                seg.update_phase2(self.dt)
            for seg in self.road_seg:
                seg.update_phase3(self.dt)
            for seg in self.road_seg:
                for veh in seg.vehicles:
                    veh_dict = veh.to_dict()
                    vehicle_list.append(veh_dict)
            new_dict_3 = {}
            new_dict_3["vehicles"] = vehicle_list
            outfile.write(json.dumps(new_dict_3))
            outfile.write("\n")
            print("Ran a step.")
        return

class Road_Segment():
    def __init__(self, x1, y1, x2, y2, speedlimit, veh_gen, orient, trafficcontrol):
        self.trafficcontrol = trafficcontrol
        self.orient = orient
        self.roadSeg = [None, None, None, None]
        self.children = []
        self.occupied = False
        self.wasOccupied = False
        self.occupancyCounter = 0
        self.propOccupancyRecord = []
        self.switch = 0
        self.switchRecord = []
        if veh_gen:
            self.vgen = VehicleGenerator(x1, y1, orient, 40)
        else:
            self.vgen = None
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.speedlimit = 20
        self.vehicles = []

    def add_vehicle(self, veh):
        self.vehicles.append(veh)

    def remove_vehicle(self, veh):
        self.vehicles.remove(veh)

    def update_phase1(self, dt):
        if self.vgen is not None:
            c = self.vgen.update()
            if c is not None:
                self.add_vehicle(c)
        for veh in self.vehicles:
            veh.update_phase1(self, 1)
        return

    def update_phase3(self, dt):
        for veh in self.vehicles:
            if (self.orient == "east" and veh.current_px > self.x2) or (
                    self.orient == "west" and veh.current_px < self.x2) or (
                    self.orient == "north" and veh.current_py > self.y2) or (
                    self.orient == "south" and veh.current_py < self.y2):
                rdm = random.random()
                print("Random: " + str(rdm))
                distancefinal = math.sqrt((self.x2 - veh.current_px) ** 2 + (self.y2 - veh.current_py) ** 2)
                if rdm >= 0 and rdm < 0.75:
                    new_roadSeg = self.roadSeg[0]
                elif rdm >= 0.75 and rdm < 0.85:
                    new_roadSeg = self.roadSeg[1]
                    temp_vx = veh.current_vx
                    veh.current_vx = veh.current_vy
                    veh.current_vy = -temp_vx
                    temp_ax = veh.current_ax
                    veh.current_ax = veh.current_ay
                    veh.current_ay = -temp_ax
                elif rdm >= 0.85 and rdm < 0.95:
                    new_roadSeg = self.roadSeg[2]
                    temp_vx = veh.current_vx
                    veh.current_vx = -veh.current_vy
                    veh.current_vy = temp_vx
                    temp_ax = veh.current_ax
                    veh.current_ax = -veh.current_ay
                    veh.current_ay = temp_ax
                else:
                    new_roadSeg = self.roadSeg[3]
                    temp_vx = veh.current_vx
                    veh.current_vx = -veh.current_vy
                    veh.current_vy = -temp_vx
                    temp_ax = veh.current_ax
                    veh.current_ax = -veh.current_ay
                    veh.current_ay = -temp_ax
                if new_roadSeg is not None:
                    veh.current_px = new_roadSeg.x1
                    veh.current_py = new_roadSeg.y1
                    if new_roadSeg.orient == "east":
                        veh.current_px += distancefinal
                    elif new_roadSeg.orient == "west":
                        veh.current_px -= distancefinal
                    elif new_roadSeg.orient == "north":
                        veh.current_py += distancefinal
                    else:
                        veh.current_py -= distancefinal
                    new_roadSeg.add_vehicle(veh)
                    print("Added vehicle " + str(veh.id) + " to Road Segment " + str(new_roadSeg.x1) + " " + str(
                        new_roadSeg.y1))
                self.remove_vehicle(veh)
                print("Removed vehicle " + str(veh.id) + " from Road Segment " + str(self.x1) + " " + str(self.y1))
        return
    def update_phase2(self, dt):
        for veh in self.vehicles:
            veh.update_phase2(1)
        return

    def to_dict(self):
        v = {}
        v["id"] = ""
        v["orient"] = self.orient
        if (self.orient == "east") or (self.orient == "west"):
            v["x1a"] = self.x1
            v["x1b"] = self.x1
            v["x2a"] = self.x2
            v["x2b"] = self.x2
            v["y1a"] = self.y1 - 2
            v["y1b"] = self.y1 + 2
            v["y2a"] = self.y2 - 2
            v["y2b"] = self.y2 + 2
        else:
            v["x1a"] = self.x1 - 2
            v["x1b"] = self.x1 + 2
            v["x2a"] = self.x2 - 2
            v["x2b"] = self.x2 + 2
            v["y1a"] = self.y1
            v["y1b"] = self.y1
            v["y2a"] = self.y2
            v["y2b"] = self.y2
        return v

sim = Simulation()
sim.run(150)
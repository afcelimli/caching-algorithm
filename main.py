import numpy as np
import matplotlib.pyplot as plt
import random
import math


class Device:
    capacity = 10 ** 9;  #device capacity 1Gbits
    base_capacity = 8 * 10**8
    enhancement_capacity = 2 * 10**8
    counter = 0

    def __init__(self, coordinate_x, coordinate_y):
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.base_cache = []
        self.enhancement_cache = []
        self.capacity_used = 0
        self.base_capacity_used = 0
        self.enhancement_capacity_used = 0
        self.base_content_frequency = []
        self.enhancement_content_frequency = []
        self.id = Device.counter
        Device.counter = Device.counter + 1

    def add_cache(self, content):
        if type(content) is BaseContent:
            if self.base_capacity_used + content.size  <= self.base_capacity:
                self.base_cache.append(content)
                self.base_content_frequency.append(0)
                self.base_capacity_used = self.base_capacity_used + content.size
                return True

        elif type(content) is EnhancementContent:
            if self.enhancement_capacity_used + content.size <= self.enhancement_capacity:
                self.enhancement_cache.append(content)
                self.enhancement_content_frequency.append(0)
                self.enhancement_capacity_used = self.enhancement_capacity_used + content.size
                return True

        else:
            return False


    def cache_algorithm(self, content):
        if type(content) is BaseContent:
            content_popularity = content.popularity
            least_popular_content = self.base_cache[0]
            index_for_remove = 0
            counter = 0
            for x in self.base_cache:
                if x.popularity <= least_popular_content.popularity:
                    least_popular_content = x
                    index_for_remove = counter
                counter = counter + 1

            if content_popularity >= least_popular_content.popularity:
                if self.base_capacity >= self.base_capacity_used - least_popular_content.size + content.size:
                    self.base_cache.pop(index_for_remove)
                    self.base_capacity_used = self.base_capacity_used - least_popular_content.size
                    self.base_cache.append(content)
                    self.base_capacity_used = self.base_capacity_used + content.size
                else:
                    pass
            else:
                pass

        else:
            content_popularity = content.popularity
            least_popular_content = self.enhancement_cache[0]
            index_for_remove = 0
            counter = 0
            for x in self.enhancement_cache:
                if x.popularity <= least_popular_content.popularity:
                    least_popular_content = x
                    index_for_remove = counter
                counter = counter + 1

            if content_popularity >= least_popular_content.popularity:
                if self.enhancement_capacity >= self.enhancement_capacity_used - least_popular_content.size + content.size:
                    self.enhancement_cache.pop(index_for_remove)
                    self.enhancement_capacity_used = self.enhancement_capacity_used - least_popular_content.size
                    self.enhancement_cache.append(content)
                    self.enhancement_capacity_used = self.enhancement_capacity_used + content.size
                else:
                    #print('Context of enhancement cache wiil not change because not enough storage in the cache')
                    pass
            else:
                #print('Context of enhancement cache will not change because popularity of content is too low')
                pass

    def cache_lru(self, content):
        if type(content) is BaseContent:
            least_recently_used_content = self.base_cache[0]
            if self.base_capacity >= self.base_capacity_used - least_recently_used_content.size + content.size:
                self.base_cache.pop(0)
                self.base_capacity_used = self.base_capacity_used - least_recently_used_content.size
                self.base_cache.append(content)
                self.base_capacity_used = self.base_capacity_used + content.size
            else:
                pass
        else:
            least_recently_used_content = self.enhancement_cache[0]
            if self.enhancement_capacity >= self.enhancement_capacity_used - least_recently_used_content.size + content.size:
                self.enhancement_cache.pop(0)
                self.enhancement_capacity_used = self.enhancement_capacity_used - least_recently_used_content.size
                self.enhancement_cache.append(content)
                self.enhancement_capacity_used = self.enhancement_capacity_used + content.size
            else:
                pass


    def cache_lfu(self, content):
       if type(content) is BaseContent:
            min = 100000
            counter = 0
            index_for_remove = 0
            for x in self.base_content_frequency:
                if x < min:
                    min = x
                    index_for_remove = counter
                counter = counter + 1

            least_frequently_used_content = self.base_cache[index_for_remove]

            if self.base_capacity >= self.base_capacity_used - least_frequently_used_content.size + content.size:
                self.base_cache.pop(index_for_remove)
                self.base_content_frequency.pop(index_for_remove)
                self.base_capacity_used = self.base_capacity_used - least_frequently_used_content.size
                self.base_cache.append(content)
                self.base_content_frequency.append(1)
                self.base_capacity_used = self.base_capacity_used + content.size
            else:
                pass
       else:
           min = 100000
           counter = 0
           index_for_remove = 0
           for x in self.enhancement_content_frequency:
               if x < min:
                   min = x
                   index_for_remove = counter
               counter = counter + 1

           least_frequently_used_content = self.enhancement_cache[index_for_remove]

           if self.enhancement_capacity >= self.enhancement_capacity_used - least_frequently_used_content.size + content.size:
               self.enhancement_cache.pop(index_for_remove)
               self.enhancement_content_frequency.pop(index_for_remove)
               self.enhancement_capacity_used = self.enhancement_capacity_used - least_frequently_used_content.size
               self.enhancement_cache.append(content)
               self.enhancement_content_frequency.append(1)
               self.enhancement_capacity_used = self.enhancement_capacity_used + content.size
           else:
               #print('Context of base cache will not change because not enough storage in the cache')
                pass


    def to_string(self):
        print('x coordinate -> {} , y coordinate -> {}'.format(self.coordinate_x, self.coordinate_y))

    def print_content(self):
        print('BASE')
        for x in self.base_cache:
            print(x.serial_number)

        print('ENHANCEMENT')
        for y in self.enhancement_cache:
            print(y.serial_number)



class BaseContent:
    def __init__(self, size, popularity, serial_number):
        self.size = size
        self.popularity = popularity
        self.serial_number = serial_number
        self.counter = 0

    def to_string(self):
        print('base size -> {}, popularity -> {}, serial number -> {}'.format(self.size, self.popularity, self.serial_number))

class EnhancementContent:
    def __init__(self, size, popularity, serial_number):
        self.size = size
        self.popularity = popularity
        self.serial_number = serial_number
        self.counter = 0


    def to_string(self):
        print('enhancement size -> {}, popularity -> {}, serial number -> {}'.format(self.size, self.popularity, self.serial_number))

class Channel:
    def __init__(self, frequency):
        self.frequency = frequency
        self.release_time = 0
        self.owner = -2

    def to_string(self):
        print("{} -> {}".format(self.frequency, self.available))


class PrimaryUser:
    counter = 0
    def __init__(self, request_time, content, frequency_channel):
        self.request_time = request_time
        self.content = content
        self.frequency_channel = frequency_channel
        self.id = PrimaryUser.counter
        PrimaryUser.counter = PrimaryUser.counter + 1


class SecondaryUser:
    counter = 0
    def __init__(self, request_time, base_content, enhancement_content):
        self.request_time = request_time
        self.base_content = base_content
        self.enhancement_content = enhancement_content
        self.id = SecondaryUser.counter
        SecondaryUser.counter = SecondaryUser.counter + 1



all_devices = []
all_base_contents = []
all_enhancement_contents = []
all_content_popularities = []
popularity_boundaries = []
all_channels = []
all_primary_users = []
all_secondary_users = []
all_secondary_users_original = []


all_devices_lru = []
all_channels_lru = []
all_primary_users_lru = []
all_secondary_users_lru = []
all_secondary_users_original_lru = []


all_devices_lfu = []
all_channels_lfu = []
all_primary_users_lfu = []
all_secondary_users_lfu = []
all_secondary_users_original_lfu = []


lat_results_cache_algorithm = []
p_loc_sq_cache_algorithm = []
p_loc_hq_cache_algorithm = []
p_loc_hq_enh_loc_base_loc_cache_algorithm = []
p_loc_hq_enh_loc_base_d2d_cache_algorithm = []

lat_results_lru = []
p_loc_sq_lru = []
p_loc_hq_lru = []
p_loc_hq_enh_loc_base_loc_lru = []
p_loc_hq_enh_loc_base_d2d_lru = []

lat_results_lfu = []
p_loc_sq_lfu = []
p_loc_hq_lfu = []
p_loc_hq_enh_loc_base_loc_lfu = []
p_loc_hq_enh_loc_base_d2d_lfu = []


repeat = 1
simulation_length = 1200 * repeat


f = open("log.txt", "w")
def create_devices():
    all_devices.clear()
    all_devices_lru.clear()
    all_devices_lfu.clear()
    lamb = 0.0015 # the rate
    pi = np.pi # pi = 3.14...
    r = 300 # the radius of the circle C
    n = 500
    uniform_points = np.random.uniform(0.0, 1.0, n)
    x = np.zeros(n)
    y = np.zeros(n)
    radii = np.zeros(n)
    for i in range(n):
        radii[i] = r * (np.sqrt(uniform_points[i]))

    uniform_points = np.random.uniform(0.0, 1.0, n)
    angle = np.zeros(n) # the angular coordinate of the points
    for i in range(n):
        angle[i] = 2 * pi * uniform_points[i]

    for i in range(n):
        x[i] = radii[i] * np.cos(angle[i])
        y[i] = radii[i] * np.sin(angle[i])
        all_devices.append(Device(x[i],y[i]))
        all_devices_lru.append(Device(x[i],y[i]))
        all_devices_lfu.append(Device(x[i], y[i]))


    """ Plots """
    '''fig = plt.gcf()
    ax = fig.gca()
    plt.xlim(-300, 300)
    plt.ylim(-300, 300)
    circ = plt.Circle((0, 0), radius=300, color='r', linewidth=2, fill=False)
    plt.plot(x,y,'bo')
    ax.add_artist(circ)
    plt.show()'''

def create_contents():
    all_base_contents.clear()
    all_enhancement_contents.clear()
    s = 0.8
    zipf_denominator = 0
    for_plot = []

    for i in range(100):
        zipf_denominator = zipf_denominator + (1 / ((i+1) ** s))


    for k in range(100):
        all_content_popularities.append((1 / ((k+1) ** s)) / zipf_denominator)
        for_plot.append(k+1)

    '''plt.plot(for_plot,all_content_popularities)
    plt.show()'''

    temp = np.random.exponential(25*10**6,100)
    sum_base = 0
    counter = 0;
    content_base = []
    for x in temp:
        content_base.append(int(round(x)))
        sum_base = sum_base + content_base[counter]
        counter = counter + 1

    temp = np.random.exponential(5*10**6,100)
    sum_enhancement = 0
    counter = 0
    content_enhancement = []
    for x in temp:
        content_enhancement.append(int(round(x)))
        sum_enhancement = sum_enhancement + content_enhancement[counter]
        counter = counter + 1

    for i in range(100):
        #all_contents.append(Content(content_base[i], content_enhancement[i], all_content_popularities[i]))
        all_base_contents.append(BaseContent(content_base[i], all_content_popularities[i], i))
        all_enhancement_contents.append(EnhancementContent(content_enhancement[i], all_content_popularities[i], i))

def fill_caches():

    number_of_contents = len(all_base_contents)
    boundary = 0
    for i in range(number_of_contents):
        boundary = boundary + all_content_popularities[i]
        popularity_boundaries.append(boundary)


    for x in all_devices:
        cache_is_available = True
        while cache_is_available:
            temp_random = random.random()
            for j in range(number_of_contents):
                if temp_random <= popularity_boundaries[j]:
                    base_cache_available = x.add_cache(all_base_contents[j])
                    enhancement_cache_available = x.add_cache(all_enhancement_contents[j])
                    cache_is_available = base_cache_available or enhancement_cache_available
                    break


    for x in all_devices_lru:
        cache_is_available = True
        while cache_is_available:
            temp_random = random.random()
            for j in range(number_of_contents):
                if temp_random <= popularity_boundaries[j]:
                    base_cache_available = x.add_cache(all_base_contents[j])
                    enhancement_cache_available = x.add_cache(all_enhancement_contents[j])
                    cache_is_available = base_cache_available or enhancement_cache_available
                    break


    for x in all_devices_lfu:
        cache_is_available = True
        while cache_is_available:
            temp_random = random.random()
            for j in range(number_of_contents):
                if temp_random <= popularity_boundaries[j]:
                    base_cache_available = x.add_cache(all_base_contents[j])
                    enhancement_cache_available = x.add_cache(all_enhancement_contents[j])
                    cache_is_available = base_cache_available or enhancement_cache_available
                    break

def create_channels():
    all_channels.clear()
    all_channels_lru.clear()
    all_channels_lfu.clear()
    for i in range(10):
        frequency = (700 + 2 * i) * 10**6
        all_channels.append(Channel(frequency))
        all_channels_lru.append(Channel(frequency))
        all_channels_lfu.append(Channel(frequency))

def create_users():
    all_primary_users.clear()
    all_primary_users_lru.clear()
    all_primary_users_lfu.clear()
    all_secondary_users.clear()
    all_secondary_users_original.clear()
    all_secondary_users_lru.clear()
    all_secondary_users_original_lru.clear()
    all_secondary_users_lfu.clear()
    all_secondary_users_original_lfu.clear()

    simulation_time = 0
    counter = 0
    while simulation_time < simulation_length:
        next_request_time = np.random.exponential(1)
        simulation_time = simulation_time + next_request_time
        temp_random = random.random()
        for j in range(100): #loops through contents
            if temp_random <= popularity_boundaries[j]:
                frequency_channel = random.randint(0,9)
                all_primary_users.append(PrimaryUser(simulation_time, all_base_contents[j], all_channels[frequency_channel]))
                all_primary_users_lru.append(
                    PrimaryUser(simulation_time, all_base_contents[j], all_channels[frequency_channel]))
                all_primary_users_lfu.append(
                    PrimaryUser(simulation_time, all_base_contents[j], all_channels[frequency_channel]))
                break
        counter = counter + 1

    simulation_time = 0
    counter = 0
    counter2 = 0
    while simulation_time < simulation_length:
        next_request_time = np.random.exponential(0.67)
        simulation_time = simulation_time + next_request_time
        temp_random = random.random()
        for j in range(100):
            if temp_random <= popularity_boundaries[j]:
                is_enhancement_requested = random.random()
                if is_enhancement_requested <= 0.5:
                    temp_su = SecondaryUser(simulation_time, all_base_contents[j], all_enhancement_contents[j])
                    all_secondary_users.append(temp_su)
                    all_secondary_users_original.append(temp_su)
                    all_secondary_users_lru.append(temp_su)
                    all_secondary_users_original_lru.append(temp_su)
                    all_secondary_users_lfu.append(temp_su)
                    all_secondary_users_original_lfu.append(temp_su)
                    counter2 = counter2 + 1
                    break
                else:
                    temp_su = SecondaryUser(simulation_time, all_base_contents[j], None)
                    all_secondary_users.append(temp_su)
                    all_secondary_users_original.append(temp_su)
                    all_secondary_users_lru.append(temp_su)
                    all_secondary_users_original_lru.append(temp_su)
                    all_secondary_users_lfu.append(temp_su)
                    all_secondary_users_original_lfu.append(temp_su)
                    break
        counter = counter + 1

def calculate_distance(device1, device2):
    distance = math.sqrt( math.pow((device1.coordinate_x - device2.coordinate_x), 2) + math.pow((device1.coordinate_y - device2.coordinate_y), 2))
    return distance

def calculate_bandwidth_for_primary(frequency):
    #frequency = (700 + channel_index * 2) * 10**6
    p = (4.7 * 10**13) / ((4 * math.pi * frequency * 150)**2)
    b = 2 * 10**6
    n = 1.6 * 10**-19
    capacity = int(b * math.log2(1 + (p / (b * n))))
    return capacity

def calculate_bandwidth_for_secondary(frequency, distance):
    #frequency = (700 + channel_index * 2) * 10 ** 6
    if distance == 0:
        distance = 0.00001  # for avoiding division by 0 error

    p = (2.6 * 10 ** 13) / ((4 * math.pi * frequency * distance) ** 2)
    b = 2 * 10 ** 6
    n = 1.6 * 10 ** -19
    capacity = int(b * math.log2(1 + (p / (b * n))))
    return capacity


def start_simulation(all_devices, all_channels, all_primary_users, all_secondary_users, all_secondary_users_original):
    latency_tall = 0
    count_base = 0
    count_enh = 0
    count_sq = 0
    count_loc_sq = 0
    count_hq = 0
    count_loc_hq = 0
    count_loc_hq_enh = 0
    count_hq_base_d2d = 0
    count_loc_hq_enh_base_d2d = 0

    current_time = 0    #second
    while(current_time < simulation_length):
        if all_primary_users[0].request_time <= all_secondary_users[0].request_time:
            current_user = all_primary_users.pop(0)
            current_time = current_user.request_time
            current_channel = current_user.frequency_channel
            current_content = current_user.content

            if current_channel.owner == -1 and current_time < current_channel.release_time:
                #print('Primary user blocked')
                f.write('{} blocked SQ PU Base {} {} NON NON {}\n'.format(int(current_user.id/3) + current_user.id%3,
                                                                          current_time,
                                                                          current_time,
                                                                          int(current_channel.frequency/1000000)))

            elif current_channel.owner != -1 and current_time < current_channel.release_time:
                discarded_secondary_user_id = current_channel.owner
                discarded_base_content = all_secondary_users_original[discarded_secondary_user_id].base_content
                discarded_secondary_user_request_time = all_secondary_users_original[discarded_secondary_user_id].request_time
                discarded_device_id = discarded_secondary_user_id % 500
                discarded_device = all_devices[discarded_device_id]

                content_size = current_content.size
                bandwidth = calculate_bandwidth_for_primary(current_channel.frequency)
                duration = content_size / bandwidth
                current_channel.release_time = current_time + duration
                current_channel.owner = -1
                #print("Primary user served and cut SU operation")
                f.write('{} served SQ PU Base {} {} NON NON {}\n'.format(int(current_user.id/3) + current_user.id%3,
                                                                         current_time,
                                                                         current_time+duration,
                                                                         int(current_channel.frequency/1000000)))

                ################### IMPLEMENT FINDING A NEW FREQUENCY FOR SU ###################
                tried_channels = []
                while (True):
                    temp = random.randint(0, 9)

                    if current_time < all_channels[temp].release_time:  # channel is being used by someone else
                        if temp not in tried_channels:
                            tried_channels.append(temp)  # mark used channels
                            if len(tried_channels) == 10:  # if all channels are full end loop
                                #print('Secondary user base dropped')
                                f.write('{} dropped SQ SU Base {} {} NON NON {}\n'.format(int(current_user.id/3) + current_user.id%3,
                                                                                          discarded_secondary_user_request_time,
                                                                                          current_time,
                                                                                          int(current_channel.frequency / 1000000)))
                                count_base = count_base - 1
                                latency_tall = latency_tall - (current_time - discarded_secondary_user_request_time)
                                break

                    else:  # an idle channel is found
                        transmitter_device = None
                        break_nested_loop = False
                        for x in all_devices:
                            for y in x.base_cache:
                                if discarded_base_content.serial_number == y.serial_number:
                                    transmitter_device = x
                                    break_nested_loop = True
                                    break
                            if break_nested_loop:
                                break

                        if type(transmitter_device) is Device:
                            new_channel = all_channels[temp]
                            distance = calculate_distance(discarded_device, transmitter_device)
                            discarded_bandwidth = calculate_bandwidth_for_secondary(current_channel.frequency, distance)
                            new_content_size = discarded_base_content.size - (discarded_bandwidth * current_time - discarded_secondary_user_request_time)
                            bandwidth = calculate_bandwidth_for_secondary(new_channel.frequency, distance)
                            duration = new_content_size / bandwidth

                            new_channel.release_time = current_time + duration
                            current_channel.owner = discarded_secondary_user_id
                            discarded_device.cache_algorithm(discarded_base_content)
                            #print('Secondary user is served by D2D communication after left its place to Primary user')
                            break
                        else:
                            break

            elif current_time >= current_channel.release_time:
                content_size = current_content.size
                bandwidth = calculate_bandwidth_for_primary(current_channel.frequency)
                duration = content_size / bandwidth
                current_channel.release_time = current_time + duration
                current_channel.owner = -1
                #print("Primary user served, channel was empty")
                f.write('{} served SQ PU Base {} {} NON NON {}\n'.format(int(current_user.id/3) + current_user.id%3,
                                                                         current_time,
                                                                         current_time + duration,
                                                                         int(current_channel.frequency/1000000)))


            else:
                #print("Shouldn't come here")
                pass


        else:   # secondary user request
            current_user = all_secondary_users.pop(0)
            current_time = current_user.request_time
            if current_user.enhancement_content is None:    #Implement 3 different scenarios. Fourth will be updated in primary user section
                local_hit = False
                device_number = current_user.id % 500
                current_device = all_devices[device_number]
                current_base_content = current_user.base_content
                count_sq = count_sq + 1

                for x in current_device.base_cache:
                    if current_base_content.serial_number == x.serial_number:
                        #print('Local hit')
                        f.write('{} local hit SQ SU Base {} {} {} {} NON\n'.format(int(current_user.id),
                                                                                   current_time,
                                                                                   current_time + 0.25,
                                                                                   int(current_device.id / 3) + current_device.id % 3,
                                                                                   int(current_device.id / 3) + current_device.id % 3))
                        local_hit = True
                        count_base = count_base + 1
                        latency_tall = latency_tall + 0.25
                        count_loc_sq = count_loc_sq + 1
                        break

                if not local_hit:
                    tried_channels = []
                    while(True):
                        temp = random.randint(0,9)
                        if current_time < all_channels[temp].release_time:  # channel is being used by someone else
                            if temp not in tried_channels:
                                tried_channels.append(temp)         # mark used channels
                                if len(tried_channels) == 10:       # if all channels are full end loop
                                    #print('Secondary user base blocked')
                                    f.write('{} blocked SQ SU Base {} {} NON NON NON\n'.format(current_user.id,
                                                                                               current_time,
                                                                                               current_time))
                                    break
                        else:       # an idle channel is found
                            transmitter_device = None
                            break_nested_loop = False
                            d2d_communication = False

                            for x in all_devices:
                                for y in x.base_cache:
                                    if current_base_content.serial_number == y.serial_number:
                                        transmitter_device = x
                                        break_nested_loop = True
                                        d2d_communication = True
                                        break
                                if break_nested_loop:
                                    break

                            if d2d_communication:
                                content_size = current_base_content.size
                                current_channel = all_channels[temp]
                                distance = calculate_distance(current_device, transmitter_device)
                                bandwidth = calculate_bandwidth_for_secondary(current_channel.frequency, distance)
                                duration = content_size / bandwidth
                                current_channel.release_time = current_time + duration
                                current_channel.owner = current_user.id
                                current_device.cache_algorithm(current_base_content)
                                #print('Secondary user is served by D2D communication')
                                f.write('{} served SQ SU Base {} {} {} {} {}\n'.format(current_user.id,
                                                                                           current_time,
                                                                                           current_time+duration,
                                                                                           int(transmitter_device.id/3)+transmitter_device.id%3,
                                                                                           int(current_device.id/3)+current_device.id%3,
                                                                                       int(current_channel.frequency / 1000000)))
                                count_base = count_base + 1
                                latency_tall = latency_tall + duration

                                break
                            else:
                                #print('Secondary user is dropped because no device contain the requested content')
                                f.write('{} dropped SQ SU Base {} {} NON NON NON\n'.format(current_user.id,
                                                                                           current_time,
                                                                                           current_time))
                                break


            else:       #request contains an enhancement content
                base_local_hit = False
                enhancement_local_hit = False
                device_number = current_user.id % 500
                current_device = all_devices[device_number]
                current_base_content = current_user.base_content
                current_enhancement_content = current_user.enhancement_content
                count_hq = count_hq + 1

                for x in current_device.base_cache:
                    if current_base_content.serial_number == x.serial_number:
                        #print('Base local hit')
                        f.write('{} local hit HQ SU Base {} {} {} {} NON\n'.format(current_user.id,
                                                                                   current_time,
                                                                                   current_time+0.25,
                                                                                   int(current_device.id/3)+current_device.id%3,
                                                                                   int(current_device.id/3)+current_device.id%3))
                        base_local_hit = True
                        count_enh = count_enh + 1
                        latency_tall = latency_tall + 0.25
                        count_loc_hq = count_loc_hq + 1
                        break

                if base_local_hit:
                    for x in current_device.enhancement_cache:
                        if current_enhancement_content.serial_number == x.serial_number:
                            #print('Enhancement local hit while base local hit')
                            f.write('{} local hit HQ SU Enhancement {} {} {} {} NON\n'.format(current_user.id,
                                                                                              current_time,
                                                                                              current_time+0.05,
                                                                                              int(current_device.id/3)+current_device.id%3,
                                                                                              int(current_device.id/3)+current_device.id%3))
                            enhancement_local_hit = True
                            latency_tall = latency_tall + 0.05
                            count_loc_hq_enh = count_loc_hq_enh + 1
                            break

                    if not enhancement_local_hit:       #base found in cache, but not enhancement
                        tried_channels = []
                        while(True):
                            temp = random.randint(0,9)
                            if current_time < all_channels[temp].release_time:
                                if temp not in tried_channels:
                                    tried_channels.append(temp)
                                    if len(tried_channels) == 10:
                                        #print('Secondary user enhancement blocked while base local hit')
                                        f.write('{} blocked HQ SU Enhancement {} {} {} NON NON\n'.format(current_user.id,
                                                                                                   current_time,
                                                                                                   current_time,
                                                                                                   int(current_device.id / 3) + current_device.id % 3))

                                        break
                            else:
                                transmitter_device = None
                                break_nested_loop = False
                                d2d_communication = False
                                for x in all_devices:
                                    for y in x.enhancement_cache:
                                        if current_enhancement_content.serial_number == y.serial_number:
                                            transmitter_device = x
                                            break_nested_loop = True
                                            d2d_communication = True
                                            break
                                    if break_nested_loop:
                                        break
                                if d2d_communication:
                                    current_enhancement_content_size = current_enhancement_content.size
                                    current_channel = all_channels[temp]
                                    distance = calculate_distance(current_device, transmitter_device)
                                    bandwidth = calculate_bandwidth_for_secondary(current_channel.frequency, distance)
                                    duration = current_enhancement_content_size / bandwidth
                                    current_channel.release_time = current_time + duration
                                    current_channel.owner = current_user.id
                                    current_device.cache_algorithm(current_enhancement_content)
                                    #print('Secondary user enhancement content is served by D2D while base is local hit')
                                    f.write('{} served HQ SU Enhancement {} {} {} {} {}\n'.format(current_user.id,
                                                                                                  current_time,
                                                                                                  current_time+duration,
                                                                                                  int(current_device.id / 3) + current_device.id % 3,
                                                                                                  int(transmitter_device.id/3) + transmitter_device.id % 3,
                                                                                                  int(all_channels[temp].frequency / 1000000)))
                                    latency_tall = latency_tall + duration
                                    break
                                else:
                                    #print('Enhancement content is dropped because no device contain the requested content')
                                    f.write('{} dropped HQ SU Enhancement {} {} {} NON NON\n'.format(current_user.id,
                                                                                                     current_time,
                                                                                                     current_time,
                                                                                                     int(current_device.id / 3) + current_device.id % 3))

                                    break
                                    pass



                if not base_local_hit:
                    tried_channels = []
                    while(True):
                        temp = random.randint(0,9)
                        if current_time < all_channels[temp].release_time:
                            if temp not in tried_channels:
                                tried_channels.append(temp)
                                if len(tried_channels) == 10:
                                    #print('Both base and enhancement blocked')
                                    f.write('{} blocked HQ SU Base {} {} {} NON NON\n'.format(current_user.id,
                                                                                                    current_time,
                                                                                                    current_time,
                                                                                                    int(current_device.id / 3) + current_device.id % 3))
                                    f.write('{} blocked HQ SU Enhancement {} {} {} NON NON\n'.format(current_user.id,
                                                                                                     current_time,
                                                                                                     current_time,
                                                                                                     int(current_device.id / 3) + current_device.id % 3))

                                    break

                        else:
                            transmitter_device_for_base = None
                            transmitter_device_for_enhancement = None
                            break_nested_loop = False
                            d2d_communication_for_base = False
                            for x in all_devices:
                                for y in x.base_cache:
                                    if current_base_content.serial_number == y.serial_number:
                                        transmitter_device_for_base = x
                                        break_nested_loop = True
                                        d2d_communication_for_base = True
                                        break
                                if break_nested_loop:
                                    break_nested_loop = False
                                    break

                            if d2d_communication_for_base:
                                count_hq_base_d2d = count_hq_base_d2d + 1
                                for x in current_device.enhancement_cache:
                                    if current_enhancement_content.serial_number == x.serial_number:
                                        #print('Enhancement local hit while base served with D2D communication')
                                        f.write(
                                            '{} local hit HQ SU Enhancement {} {} {} {} NON\n'.format(current_user.id,
                                                                                                      current_time,
                                                                                                      current_time+0.05,
                                                                                                      int(
                                                                                                          current_device.id / 3) + current_device.id % 3,
                                                                                                      int(
                                                                                                         current_device.id / 3) + current_device.id % 3))
                                        break_nested_loop = True
                                        enhancement_local_hit = True
                                        count_enh = count_enh + 1
                                        latency_tall = latency_tall + 0.05
                                        count_loc_hq_enh_base_d2d  = count_loc_hq_enh_base_d2d + 1
                                        break
                                if break_nested_loop:
                                    break_nested_loop = False
                                    break

                                if not enhancement_local_hit:
                                    break_nested_loop = False
                                    d2d_communication_for_enhancement = False
                                    for x in all_devices:
                                        for y in x.enhancement_cache:
                                            if current_enhancement_content.serial_number == y.serial_number:
                                                transmitter_device_for_enhancement = x
                                                break_nested_loop = True
                                                d2d_communication_for_enhancement = True
                                                break
                                        if break_nested_loop:
                                            break_nested_loop = False
                                            break

                                    if d2d_communication_for_enhancement:
                                        current_channel = all_channels[temp]

                                        current_base_content_size = current_base_content.size
                                        distance = calculate_distance(current_device, transmitter_device_for_base)
                                        bandwidth = calculate_bandwidth_for_secondary(current_channel.frequency, distance)
                                        duration = current_base_content_size / bandwidth
                                        current_channel.release_time = current_time + duration
                                        current_channel.owner = current_user.id
                                        current_device.cache_algorithm(current_base_content)
                                        count_enh = count_enh + 1
                                        latency_tall = latency_tall + duration
                                        f.write('{} served HQ SU Base {} {} {} {} {}\n'.format(current_user.id,
                                                                                               current_time,
                                                                                               current_time+duration,
                                                                                               int(current_device.id / 3) + current_device.id % 3,
                                                                                               int(transmitter_device_for_base.id/3) + transmitter_device_for_base.id%3,
                                                                                               int(current_channel.frequency / 1000000)))

                                        current_enhancement_content_size = current_enhancement_content.size
                                        distance = calculate_distance(current_device, transmitter_device_for_enhancement)
                                        bandwidth = calculate_bandwidth_for_secondary(current_channel.frequency, distance)
                                        duration = current_enhancement_content_size / bandwidth
                                        current_channel.release_time = current_channel.release_time + duration
                                        current_device.cache_algorithm(current_enhancement_content)
                                        latency_tall = latency_tall + duration
                                        #print('Both base and enhancement content is served by D2D')
                                        f.write('{} served HQ SU Enhancement {} {} {} {} {}\n'.format(current_user.id,
                                                                                                      current_time,
                                                                                                      current_time + duration,
                                                                                                      int(current_device.id / 3) + current_device.id % 3,
                                                                                                      int(transmitter_device_for_enhancement.id / 3) + transmitter_device_for_enhancement.id % 3,
                                                                                                     int(current_channel.frequency / 1000000)))
                                        break
                                    else:
                                        #print('Enhancement is dropped because no device contains requested content while base is served by d2d')
                                        f.write(
                                            '{} dropped HQ SU Enhancement {} {} {} NON NON\n'.format(current_user.id,
                                                                                                     current_time,
                                                                                                     current_time,
                                                                                                     int(current_device.id / 3) + current_device.id % 3))
                                        break
                            else:
                                f.write('{} dropped HQ SU Base {} {} {} NON NON\n'.format(current_user.id,
                                                                                                current_time,
                                                                                                current_time,
                                                                                                int(current_device.id / 3) + current_device.id % 3))
                                f.write('{} dropped HQ SU Enhancement {} {} {} NON NON\n'.format(current_user.id,
                                                                                                 current_time,
                                                                                                 current_time,
                                                                                                 int(current_device.id / 3) + current_device.id % 3))
                                #print('Both base and enhancement is dropped because no device contains requested content')
                                break

    if current_time >= simulation_length:

        latency = latency_tall / (count_base + count_enh)
        lat_results_cache_algorithm.append(latency)
        #print('Latency: {}'.format(latency))

        p_loc_sq = count_loc_sq * 1.0 / (count_sq)
        p_loc_sq_cache_algorithm.append(p_loc_sq)
        #print('PlocSQ: {}'.format(p_loc_sq))


        p_loc_hq = count_loc_hq * 1.0 / (count_hq)
        p_loc_hq_cache_algorithm.append(p_loc_hq)
        #print('PlocHQ: {}'.format(p_loc_hq))

        p_loc_hq_enh_base = count_loc_hq_enh * 1.0 / (count_loc_hq)
        p_loc_hq_enh_loc_base_loc_cache_algorithm.append(p_loc_hq_enh_base)
        #print('PlocHQ(enh(loc)|base(loc)): {}'.format(p_loc_hq_enh_base))


        p_loc_hq_enh_base_d2d = count_loc_hq_enh_base_d2d * 1.0 / (count_hq_base_d2d)
        p_loc_hq_enh_loc_base_d2d_cache_algorithm.append(p_loc_hq_enh_base_d2d)
        #print('PlocHQ(enh(loc)|base(D2D)): {}'.format(p_loc_hq_enh_base_d2d))



def start_simulation_lru(all_devices, all_channels, all_primary_users, all_secondary_users, all_secondary_users_original):
    latency_tall = 0   ##########################################################################################
    count_base = 0     ##########################################################################################
    count_enh = 0      ##########################################################################################
    count_sq = 0       ##########################################################################################
    count_loc_sq = 0   ##########################################################################################
    count_hq = 0       ##########################################################################################
    count_loc_hq = 0   ##########################################################################################
    count_loc_hq_enh = 0    #####################################################################################
    count_hq_base_d2d = 0   #####################################################################################
    count_loc_hq_enh_base_d2d = 0  ##############################################################################


    current_time = 0    #second
    while(current_time < simulation_length):
        #print('CURRENT TIME {}'.format(current_time))
        if all_primary_users[0].request_time <= all_secondary_users[0].request_time:
            current_user = all_primary_users.pop(0)
            current_time = current_user.request_time
            current_channel = current_user.frequency_channel
            current_content = current_user.content

            if current_channel.owner == -1 and current_time < current_channel.release_time:
                #print('Primary user blocked')
                pass
            elif current_channel.owner != -1 and current_time < current_channel.release_time:
                discarded_secondary_user_id = current_channel.owner
                #print(len(all_secondary_users_original))
                #print(discarded_secondary_user_id)
                #discarded_base_content = all_secondary_users[discarded_secondary_user_id].base_content
                #discarded_secondary_user_request_time = all_secondary_users[discarded_secondary_user_id].request_time
                discarded_base_content = all_secondary_users_original[discarded_secondary_user_id].base_content
                discarded_secondary_user_request_time = all_secondary_users_original[discarded_secondary_user_id].request_time
                discarded_device_id = discarded_secondary_user_id % 500
                discarded_device = all_devices[discarded_device_id]

                #current_content = current_user.content
                content_size = current_content.size
                bandwidth = calculate_bandwidth_for_primary(current_channel.frequency)
                duration = content_size / bandwidth
                current_channel.release_time = current_time + duration
                current_channel.owner = -1
                #print("Primary user served and cut SU operation")
                ################### IMPLEMENT FINDING A NEW FREQUENCY FOR SU ###################
                tried_channels = []
                while (True):
                    temp = random.randint(0, 9)

                    if current_time < all_channels[temp].release_time:  # channel is being used by someone else
                        if temp not in tried_channels:
                            tried_channels.append(temp)  # mark used channels
                            if len(tried_channels) == 10:  # if all channels are full end loop
                                #print('Secondary user base dropped')
                                count_base = count_base - 1  ##########################################################
                                latency_tall = latency_tall - (current_time - discarded_secondary_user_request_time)
                                break

                    else:  # an idle channel is found
                        transmitter_device = None
                        break_nested_loop = False
                        for x in all_devices:
                            for y in x.base_cache:
                                if discarded_base_content.serial_number == y.serial_number:
                                    transmitter_device = x
                                    break_nested_loop = True
                                    break
                            if break_nested_loop:
                                break

                        if type(transmitter_device) is Device:
                            new_channel = all_channels[temp]
                            distance = calculate_distance(discarded_device, transmitter_device)
                            discarded_bandwidth = calculate_bandwidth_for_secondary(current_channel.frequency, distance)
                            new_content_size = discarded_base_content.size - (discarded_bandwidth * current_time - discarded_secondary_user_request_time)
                            bandwidth = calculate_bandwidth_for_secondary(new_channel.frequency, distance)
                            duration = new_content_size / bandwidth

                            new_channel.release_time = current_time + duration
                            current_channel.owner = discarded_secondary_user_id
                            #discarded_device.cache_algorithm(current_base_content)
                            discarded_device.cache_lru(discarded_base_content)
                            #discarded_device.cache_lfu(current_base_content)
                            #print('Secondary user is served by D2D communication after left its place to Primary user')
                            break
                        else:
                            break

            elif current_time >= current_channel.release_time:
                content_size = current_content.size
                bandwidth = calculate_bandwidth_for_primary(current_channel.frequency)
                duration = content_size / bandwidth
                current_channel.release_time = current_time + duration
                current_channel.owner = -1
                #print("Primary user served, channel was empty")

            else:
                #print("Shouldn't come here")
                pass


        else:   # secondary user request
            current_user = all_secondary_users.pop(0)
            current_time = current_user.request_time

            if current_user.enhancement_content is None:    #Implement 3 different scenarios. Fourth will be updated in primary user section
                local_hit = False
                device_number = current_user.id % 500
                current_device = all_devices[device_number]
                current_base_content = current_user.base_content
                count_sq = count_sq + 1     #########################################################################

                for x in current_device.base_cache:
                    if current_base_content.serial_number == x.serial_number:
                        #print('Local hit')
                        local_hit = True
                        count_base = count_base + 1  #################################################################
                        latency_tall = latency_tall + 0.25  ##########################################################
                        count_loc_sq = count_loc_sq + 1  #############################################################
                        break

                if not local_hit:
                    tried_channels = []
                    while(True):
                        temp = random.randint(0,9)
                        if current_time < all_channels[temp].release_time:  # channel is being used by someone else
                            if temp not in tried_channels:
                                tried_channels.append(temp)         # mark used channels
                                if len(tried_channels) == 10:       # if all channels are full end loop
                                    #print('Secondary user base blocked')
                                    break
                        else:       # an idle channel is found
                            transmitter_device = None
                            break_nested_loop = False
                            d2d_communication = False

                            for x in all_devices:
                                for y in x.base_cache:
                                    if current_base_content.serial_number == y.serial_number:
                                        transmitter_device = x
                                        break_nested_loop = True
                                        d2d_communication = True
                                        break
                                if break_nested_loop:
                                    break

                            if d2d_communication:
                                content_size = current_base_content.size
                                current_channel = all_channels[temp]
                                distance = calculate_distance(current_device, transmitter_device)
                                bandwidth = calculate_bandwidth_for_secondary(current_channel.frequency, distance)
                                duration = content_size / bandwidth
                                current_channel.release_time = current_time + duration
                                current_channel.owner = current_user.id
                                #current_device.cache_algorithm(current_base_content)
                                current_device.cache_lru(current_base_content)
                                #current_device.cache_lfu(current_base_content)
                                #print('Secondary user is served by D2D communication')
                                count_base = count_base + 1  ##########################################################
                                latency_tall = latency_tall + duration  ###############################################

                                break
                            else:
                                #print('Secondary user is dropped because no device contain the requested content')
                                break


            else:       #request contains an enhancement content
                base_local_hit = False
                enhancement_local_hit = False
                device_number = current_user.id % 500
                current_device = all_devices[device_number]
                current_base_content = current_user.base_content
                current_enhancement_content = current_user.enhancement_content
                count_hq = count_hq + 1

                for x in current_device.base_cache:
                    if current_base_content.serial_number == x.serial_number:
                        #print('Base local hit')
                        base_local_hit = True
                        count_enh = count_enh + 1
                        latency_tall = latency_tall + 0.25
                        count_loc_hq = count_loc_hq + 1
                        break

                if base_local_hit:
                    for x in current_device.enhancement_cache:
                        if current_enhancement_content.serial_number == x.serial_number:
                            #print('Enhancement local hit while base local hit')
                            enhancement_local_hit = True
                            latency_tall = latency_tall + 0.05
                            count_loc_hq_enh = count_loc_hq_enh + 1
                            break

                    if not enhancement_local_hit:       #base found in cache, but not enhancement
                        tried_channels = []
                        while(True):
                            temp = random.randint(0,9)
                            if current_time < all_channels[temp].release_time:
                                if temp not in tried_channels:
                                    tried_channels.append(temp)
                                    if len(tried_channels) == 10:
                                        #print('Secondary user enhancement blocked while base local hit')
                                        break
                            else:
                                transmitter_device = None
                                break_nested_loop = False
                                d2d_communication = False
                                for x in all_devices:
                                    for y in x.enhancement_cache:
                                        if current_enhancement_content.serial_number == y.serial_number:
                                            transmitter_device = x
                                            break_nested_loop = True
                                            d2d_communication = True
                                            break
                                    if break_nested_loop:
                                        break
                                if d2d_communication:
                                    current_enhancement_content_size = current_enhancement_content.size
                                    current_channel = all_channels[temp]
                                    distance = calculate_distance(current_device, transmitter_device)
                                    bandwidth = calculate_bandwidth_for_secondary(current_channel.frequency, distance)
                                    duration = current_enhancement_content_size / bandwidth
                                    current_channel.release_time = current_time + duration
                                    current_channel.owner = current_user.id
                                    #current_device.cache_algorithm(current_enhancement_content)
                                    current_device.cache_lru(current_enhancement_content)
                                    #current_device.cache_lfu(current_enhancement_content)
                                    #print('Secondary user enhancement content is served by D2D while base is local hit')
                                    latency_tall = latency_tall + duration
                                    break
                                else:
                                    #print('Enhancement content is dropped because no device contain the requested content')
                                    pass



                if not base_local_hit:
                    tried_channels = []
                    while(True):
                        temp = random.randint(0,9)
                        #print('Temp: {}'.format(temp))
                        #print('Frequency: {}'.format(all_channels[temp].release_time))
                        if current_time < all_channels[temp].release_time:
                            if temp not in tried_channels:
                                tried_channels.append(temp)
                                if len(tried_channels) == 10:
                                    #print('Both base and enhancement blocked')
                                    break

                        else:
                            transmitter_device_for_base = None
                            transmitter_device_for_enhancement = None
                            break_nested_loop = False
                            d2d_communication_for_base = False
                            for x in all_devices:
                                for y in x.base_cache:
                                    if current_base_content.serial_number == y.serial_number:
                                        transmitter_device_for_base = x
                                        break_nested_loop = True
                                        d2d_communication_for_base = True
                                        break
                                if break_nested_loop:
                                    break_nested_loop = False
                                    break

                            if d2d_communication_for_base:
                                count_hq_base_d2d = count_hq_base_d2d + 1
                                for x in current_device.enhancement_cache:
                                    if current_enhancement_content.serial_number == x.serial_number:
                                        #print('Enhancement local hit while base served with D2D communication')
                                        break_nested_loop = True
                                        enhancement_local_hit = True
                                        count_enh = count_enh + 1
                                        latency_tall = latency_tall + 0.05
                                        count_loc_hq_enh_base_d2d  = count_loc_hq_enh_base_d2d + 1
                                        break
                                if break_nested_loop:
                                    break_nested_loop = False
                                    break

                                if not enhancement_local_hit:
                                    break_nested_loop = False
                                    d2d_communication_for_enhancement = False
                                    for x in all_devices:
                                        for y in x.enhancement_cache:
                                            if current_enhancement_content.serial_number == y.serial_number:
                                                transmitter_device_for_enhancement = x
                                                break_nested_loop = True
                                                d2d_communication_for_enhancement = True
                                                break
                                        if break_nested_loop:
                                            break_nested_loop = False
                                            break

                                    if d2d_communication_for_enhancement:
                                        current_channel = all_channels[temp]

                                        current_base_content_size = current_base_content.size
                                        distance = calculate_distance(current_device, transmitter_device_for_base)
                                        bandwidth = calculate_bandwidth_for_secondary(current_channel.frequency, distance)
                                        duration = current_base_content_size / bandwidth
                                        current_channel.release_time = current_time + duration
                                        current_channel.owner = current_user.id
                                        #current_device.cache_algorithm(current_base_content)
                                        current_device.cache_lru(current_base_content)
                                        #current_device.cache_lfu(current_base_content)
                                        count_enh = count_enh + 1
                                        latency_tall = latency_tall + duration

                                        current_enhancement_content_size = current_enhancement_content.size
                                        distance = calculate_distance(current_device, transmitter_device_for_enhancement)
                                        bandwidth = calculate_bandwidth_for_secondary(current_channel.frequency, distance)
                                        duration = current_enhancement_content_size / bandwidth
                                        current_channel.release_time = current_channel.release_time + duration
                                        #current_device.cache_algorithm(current_enhancement_content)
                                        current_device.cache_lru(current_enhancement_content)
                                        #current_device.cache_lfu(current_enhancement_content)
                                        latency_tall = latency_tall + duration

                                        #print('Both base and enhancement content is served by D2D')

                                        break

                                    else:
                                        #print('Enhancement is dropped because no device contains requested content while base is served by d2d')
                                        break


                            else:
                                #print('Both base and enhancement is dropped because no device contains requested content')
                                break


    if current_time >= simulation_length:
        latency = latency_tall / (count_base + count_enh)
        lat_results_lru.append(latency)
        #print('Latency: {}'.format(latency))
        p_loc_sq = count_loc_sq * 1.0 / (count_sq)
        p_loc_sq_lru.append(p_loc_sq)
        #print('PlocSQ: {}'.format(p_loc_sq))
        p_loc_hq = count_loc_hq * 1.0 / (count_hq)
        p_loc_hq_lru.append(p_loc_hq)
        #print('PlocHQ: {}'.format(p_loc_hq))
        p_loc_hq_enh_base = count_loc_hq_enh * 1.0 / (count_loc_hq)
        p_loc_hq_enh_loc_base_loc_lru.append(p_loc_hq_enh_base)
        #print('PlocHQ(enh(loc)|base(loc)): {}'.format(p_loc_hq_enh_base))
        p_loc_hq_enh_base_d2d = count_loc_hq_enh_base_d2d * 1.0 / (count_hq_base_d2d)
        p_loc_hq_enh_loc_base_d2d_lru.append(p_loc_hq_enh_base_d2d)
        #print('PlocHQ(enh(loc)|base(D2D)): {}'.format(p_loc_hq_enh_base_d2d))


def start_simulation_lfu(all_devices, all_channels, all_primary_users, all_secondary_users, all_secondary_users_original):
    latency_tall = 0   ##########################################################################################
    count_base = 0     ##########################################################################################
    count_enh = 0      ##########################################################################################
    count_sq = 0       ##########################################################################################
    count_loc_sq = 0   ##########################################################################################
    count_hq = 0       ##########################################################################################
    count_loc_hq = 0   ##########################################################################################
    count_loc_hq_enh = 0    #####################################################################################
    count_hq_base_d2d = 0   #####################################################################################
    count_loc_hq_enh_base_d2d = 0  ##############################################################################

    current_time = 0    #second
    while(current_time < simulation_length):
        #print('CURRENT TIME {}'.format(current_time))
        if all_primary_users[0].request_time <= all_secondary_users[0].request_time:
            current_user = all_primary_users.pop(0)
            current_time = current_user.request_time
            current_channel = current_user.frequency_channel
            current_content = current_user.content

            if current_channel.owner == -1 and current_time < current_channel.release_time:
                #print('Primary user blocked')
                pass
            elif current_channel.owner != -1 and current_time < current_channel.release_time:
                discarded_secondary_user_id = current_channel.owner
                #print(len(all_secondary_users_original))
                #print(discarded_secondary_user_id)
                #discarded_base_content = all_secondary_users[discarded_secondary_user_id].base_content
                #discarded_secondary_user_request_time = all_secondary_users[discarded_secondary_user_id].request_time
                discarded_base_content = all_secondary_users_original[discarded_secondary_user_id].base_content
                discarded_secondary_user_request_time = all_secondary_users_original[discarded_secondary_user_id].request_time
                discarded_device_id = discarded_secondary_user_id % 500
                discarded_device = all_devices[discarded_device_id]

                #current_content = current_user.content
                content_size = current_content.size
                bandwidth = calculate_bandwidth_for_primary(current_channel.frequency)
                duration = content_size / bandwidth
                current_channel.release_time = current_time + duration
                current_channel.owner = -1
                #print("Primary user served and cut SU operation")
                ################### IMPLEMENT FINDING A NEW FREQUENCY FOR SU ###################
                tried_channels = []
                while (True):
                    temp = random.randint(0, 9)

                    if current_time < all_channels[temp].release_time:  # channel is being used by someone else
                        if temp not in tried_channels:
                            tried_channels.append(temp)  # mark used channels
                            if len(tried_channels) == 10:  # if all channels are full end loop
                                #print('Secondary user base dropped')
                                count_base = count_base - 1  ##########################################################
                                latency_tall = latency_tall - (current_time - discarded_secondary_user_request_time)
                                break

                    else:  # an idle channel is found
                        transmitter_device = None
                        break_nested_loop = False
                        for x in all_devices:
                            for y in x.base_cache:
                                if discarded_base_content.serial_number == y.serial_number:
                                    transmitter_device = x
                                    break_nested_loop = True
                                    break
                            if break_nested_loop:
                                break

                        if type(transmitter_device) is Device:
                            new_channel = all_channels[temp]
                            distance = calculate_distance(discarded_device, transmitter_device)
                            discarded_bandwidth = calculate_bandwidth_for_secondary(current_channel.frequency, distance)
                            new_content_size = discarded_base_content.size - (discarded_bandwidth * current_time - discarded_secondary_user_request_time)
                            bandwidth = calculate_bandwidth_for_secondary(new_channel.frequency, distance)
                            duration = new_content_size / bandwidth

                            new_channel.release_time = current_time + duration
                            current_channel.owner = discarded_secondary_user_id
                            #discarded_device.cache_algorithm(current_base_content)
                            #discarded_device.cache_lru(current_base_content)
                            discarded_device.cache_lfu(discarded_base_content)
                            #print('Secondary user is served by D2D communication after left its place to Primary user')
                            break
                        else:
                            break

            elif current_time >= current_channel.release_time:
                content_size = current_content.size
                bandwidth = calculate_bandwidth_for_primary(current_channel.frequency)
                duration = content_size / bandwidth
                current_channel.release_time = current_time + duration
                current_channel.owner = -1
                #print("Primary user served, channel was empty")

            else:
                #print("Shouldn't come here")
                pass


        else:   # secondary user request
            current_user = all_secondary_users.pop(0)
            current_time = current_user.request_time

            if current_user.enhancement_content is None:    #Implement 3 different scenarios. Fourth will be updated in primary user section
                local_hit = False
                device_number = current_user.id % 500
                current_device = all_devices[device_number]
                current_base_content = current_user.base_content
                count_sq = count_sq + 1     #########################################################################

                for x in current_device.base_cache:
                    if current_base_content.serial_number == x.serial_number:
                        #print('Local hit')
                        local_hit = True
                        count_base = count_base + 1  #################################################################
                        latency_tall = latency_tall + 0.25  ##########################################################
                        count_loc_sq = count_loc_sq + 1  #############################################################
                        break

                if not local_hit:
                    tried_channels = []
                    while(True):
                        temp = random.randint(0,9)
                        if current_time < all_channels[temp].release_time:  # channel is being used by someone else
                            if temp not in tried_channels:
                                tried_channels.append(temp)         # mark used channels
                                if len(tried_channels) == 10:       # if all channels are full end loop
                                    #print('Secondary user base blocked')
                                    break
                        else:       # an idle channel is found
                            transmitter_device = None
                            break_nested_loop = False
                            d2d_communication = False

                            for x in all_devices:
                                for y in x.base_cache:
                                    if current_base_content.serial_number == y.serial_number:
                                        transmitter_device = x
                                        break_nested_loop = True
                                        d2d_communication = True
                                        break
                                if break_nested_loop:
                                    break

                            if d2d_communication:
                                content_size = current_base_content.size
                                current_channel = all_channels[temp]
                                distance = calculate_distance(current_device, transmitter_device)
                                bandwidth = calculate_bandwidth_for_secondary(current_channel.frequency, distance)
                                duration = content_size / bandwidth
                                current_channel.release_time = current_time + duration
                                current_channel.owner = current_user.id
                                #current_device.cache_algorithm(current_base_content)
                                #current_device.cache_lru(current_base_content)
                                current_device.cache_lfu(current_base_content)
                                #print('Secondary user is served by D2D communication')
                                count_base = count_base + 1  ##########################################################
                                latency_tall = latency_tall + duration  ###############################################

                                break
                            else:
                                #print('Secondary user is dropped because no device contain the requested content')
                                break


            else:       #request contains an enhancement content
                base_local_hit = False
                enhancement_local_hit = False
                device_number = current_user.id % 500
                current_device = all_devices[device_number]
                current_base_content = current_user.base_content
                current_enhancement_content = current_user.enhancement_content
                count_hq = count_hq + 1

                for x in current_device.base_cache:
                    if current_base_content.serial_number == x.serial_number:
                        #print('Base local hit')
                        base_local_hit = True
                        count_enh = count_enh + 1
                        latency_tall = latency_tall + 0.25
                        count_loc_hq = count_loc_hq + 1
                        break

                if base_local_hit:
                    for x in current_device.enhancement_cache:
                        if current_enhancement_content.serial_number == x.serial_number:
                            #print('Enhancement local hit while base local hit')
                            enhancement_local_hit = True
                            latency_tall = latency_tall + 0.05
                            count_loc_hq_enh = count_loc_hq_enh + 1
                            break

                    if not enhancement_local_hit:       #base found in cache, but not enhancement
                        tried_channels = []
                        while(True):
                            temp = random.randint(0,9)
                            if current_time < all_channels[temp].release_time:
                                if temp not in tried_channels:
                                    tried_channels.append(temp)
                                    if len(tried_channels) == 10:
                                        #print('Secondary user enhancement blocked while base local hit')
                                        break
                            else:
                                transmitter_device = None
                                break_nested_loop = False
                                d2d_communication = False
                                for x in all_devices:
                                    for y in x.enhancement_cache:
                                        if current_enhancement_content.serial_number == y.serial_number:
                                            transmitter_device = x
                                            break_nested_loop = True
                                            d2d_communication = True
                                            break
                                    if break_nested_loop:
                                        break
                                if d2d_communication:
                                    current_enhancement_content_size = current_enhancement_content.size
                                    current_channel = all_channels[temp]
                                    distance = calculate_distance(current_device, transmitter_device)
                                    bandwidth = calculate_bandwidth_for_secondary(current_channel.frequency, distance)
                                    duration = current_enhancement_content_size / bandwidth
                                    current_channel.release_time = current_time + duration
                                    current_channel.owner = current_user.id
                                    #current_device.cache_algorithm(current_enhancement_content)
                                    #current_device.cache_lru(current_enhancement_content)
                                    current_device.cache_lfu(current_enhancement_content)
                                    #print('Secondary user enhancement content is served by D2D while base is local hit')
                                    latency_tall = latency_tall + duration
                                    break
                                else:
                                    #print('Enhancement content is dropped because no device contain the requested content')
                                    pass



                if not base_local_hit:
                    tried_channels = []
                    while(True):
                        temp = random.randint(0,9)
                        #print('Temp: {}'.format(temp))
                        #print('Frequency: {}'.format(all_channels[temp].release_time))
                        if current_time < all_channels[temp].release_time:
                            if temp not in tried_channels:
                                tried_channels.append(temp)
                                if len(tried_channels) == 10:
                                    #print('Both base and enhancement blocked')
                                    break

                        else:
                            transmitter_device_for_base = None
                            transmitter_device_for_enhancement = None
                            break_nested_loop = False
                            d2d_communication_for_base = False
                            for x in all_devices:
                                for y in x.base_cache:
                                    if current_base_content.serial_number == y.serial_number:
                                        transmitter_device_for_base = x
                                        break_nested_loop = True
                                        d2d_communication_for_base = True
                                        break
                                if break_nested_loop:
                                    break_nested_loop = False
                                    break

                            if d2d_communication_for_base:
                                count_hq_base_d2d = count_hq_base_d2d + 1
                                for x in current_device.enhancement_cache:
                                    if current_enhancement_content.serial_number == x.serial_number:
                                        #print('Enhancement local hit while base served with D2D communication')
                                        break_nested_loop = True
                                        enhancement_local_hit = True
                                        count_enh = count_enh + 1
                                        latency_tall = latency_tall + 0.05
                                        count_loc_hq_enh_base_d2d  = count_loc_hq_enh_base_d2d + 1
                                        break
                                if break_nested_loop:
                                    break_nested_loop = False
                                    break

                                if not enhancement_local_hit:
                                    break_nested_loop = False
                                    d2d_communication_for_enhancement = False
                                    for x in all_devices:
                                        for y in x.enhancement_cache:
                                            if current_enhancement_content.serial_number == y.serial_number:
                                                transmitter_device_for_enhancement = x
                                                break_nested_loop = True
                                                d2d_communication_for_enhancement = True
                                                break
                                        if break_nested_loop:
                                            break_nested_loop = False
                                            break

                                    if d2d_communication_for_enhancement:
                                        current_channel = all_channels[temp]

                                        current_base_content_size = current_base_content.size
                                        distance = calculate_distance(current_device, transmitter_device_for_base)
                                        bandwidth = calculate_bandwidth_for_secondary(current_channel.frequency, distance)
                                        duration = current_base_content_size / bandwidth
                                        current_channel.release_time = current_time + duration
                                        current_channel.owner = current_user.id
                                        #current_device.cache_algorithm(current_base_content)
                                        #current_device.cache_lru(current_base_content)
                                        current_device.cache_lfu(current_base_content)
                                        count_enh = count_enh + 1
                                        latency_tall = latency_tall + duration

                                        current_enhancement_content_size = current_enhancement_content.size
                                        distance = calculate_distance(current_device, transmitter_device_for_enhancement)
                                        bandwidth = calculate_bandwidth_for_secondary(current_channel.frequency, distance)
                                        duration = current_enhancement_content_size / bandwidth
                                        current_channel.release_time = current_channel.release_time + duration
                                        #current_device.cache_algorithm(current_enhancement_content)
                                        #current_device.cache_lru(current_enhancement_content)
                                        current_device.cache_lfu(current_enhancement_content)
                                        latency_tall = latency_tall + duration

                                        #print('Both base and enhancement content is served by D2D')

                                        break

                                    else:
                                        #print('Enhancement is dropped because no device contains requested content while base is served by d2d')
                                        break


                            else:
                                #print('Both base and enhancement is dropped because no device contains requested content')
                                break


    if current_time >= simulation_length:
        latency = latency_tall / (count_base + count_enh)
        lat_results_lfu.append(latency)
        #print('Latency: {}'.format(latency))
        p_loc_sq = count_loc_sq * 1.0 / count_sq
        p_loc_sq_lfu.append(p_loc_sq)
        #print('PlocSQ: {}'.format(p_loc_sq))
        p_loc_hq = count_loc_hq * 1.0 / count_hq
        p_loc_hq_lfu.append(p_loc_hq)
        #print('PlocHQ: {}'.format(p_loc_hq))
        p_loc_hq_enh_base = count_loc_hq_enh * 1.0 / count_loc_hq
        p_loc_hq_enh_loc_base_loc_lfu.append(p_loc_hq_enh_base)
        #print('PlocHQ(enh(loc)|base(loc)): {}'.format(p_loc_hq_enh_base))
        p_loc_hq_enh_base_d2d = count_loc_hq_enh_base_d2d * 1.0 / count_hq_base_d2d
        p_loc_hq_enh_loc_base_d2d_lfu.append(p_loc_hq_enh_base_d2d)
        #print('PlocHQ(enh(loc)|base(D2D)): {}'.format(p_loc_hq_enh_base_d2d))



create_devices()
create_contents()
fill_caches()
create_channels()
create_users()

start_simulation(all_devices, all_channels, all_primary_users, all_secondary_users, all_secondary_users_original)
start_simulation_lru(all_devices_lru, all_channels_lru, all_primary_users_lru, all_secondary_users_lru, all_secondary_users_original_lru)
start_simulation_lfu(all_devices_lfu, all_channels_lfu, all_primary_users_lfu, all_secondary_users_lfu, all_secondary_users_original_lfu)




def print_results():
    repeat_number = 1
    lat_avg = 0
    p_loc_sq_avg = 0
    p_loc_hq_avg = 0
    p_loc_hq_enh_base_avg = 0
    p_loc_hq_enh_base_d2d_avg = 0
    for i in range(repeat_number):
        lat_avg = lat_avg + lat_results_cache_algorithm[i]
        p_loc_sq_avg = p_loc_sq_avg + p_loc_sq_cache_algorithm[i]
        p_loc_hq_avg = p_loc_hq_avg + p_loc_hq_cache_algorithm[i]
        p_loc_hq_enh_base_avg = p_loc_hq_enh_base_avg + p_loc_hq_enh_loc_base_loc_cache_algorithm[i]
        p_loc_hq_enh_base_d2d_avg = p_loc_hq_enh_base_d2d_avg + p_loc_hq_enh_loc_base_d2d_cache_algorithm[i]
    lat_avg = lat_avg / repeat_number
    p_loc_sq_avg = p_loc_sq_avg / repeat_number
    p_loc_hq_avg = p_loc_hq_avg / repeat_number
    p_loc_hq_enh_base_avg = p_loc_hq_enh_base_avg / repeat_number
    p_loc_hq_enh_base_d2d_avg = p_loc_hq_enh_base_d2d_avg / repeat_number
    print('Latency: {}'.format(lat_avg))
    print('PlocSQ: {}'.format(p_loc_sq_avg))
    print('PlocHQ: {}'.format(p_loc_hq_avg))
    print('PlocHQ(enh(loc)|base(loc)): {}'.format(p_loc_hq_enh_base_avg))
    print('PlocHQ(enh(loc)|base(D2D)): {}'.format(p_loc_hq_enh_base_d2d_avg))



    lat_avg_lru = 0
    p_loc_sq_avg_lru = 0
    p_loc_hq_avg_lru = 0
    p_loc_hq_enh_base_avg_lru = 0
    p_loc_hq_enh_base_d2d_avg_lru = 0
    for i in range(repeat_number):
        lat_avg_lru = lat_avg_lru + lat_results_lru[i]
        p_loc_sq_avg_lru = p_loc_sq_avg_lru + p_loc_sq_lru[i]
        p_loc_hq_avg_lru = p_loc_hq_avg_lru + p_loc_hq_lru[i]
        p_loc_hq_enh_base_avg_lru = p_loc_hq_enh_base_avg_lru + p_loc_hq_enh_loc_base_loc_lru[i]
        p_loc_hq_enh_base_d2d_avg_lru = p_loc_hq_enh_base_d2d_avg_lru + p_loc_hq_enh_loc_base_d2d_lru[i]
    lat_avg_lru = lat_avg_lru  / repeat_number
    p_loc_sq_avg_lru = p_loc_sq_avg_lru / repeat_number
    p_loc_hq_avg_lru = p_loc_hq_avg_lru / repeat_number
    p_loc_hq_enh_base_avg_lru = p_loc_hq_enh_base_avg_lru / repeat_number
    p_loc_hq_enh_base_d2d_avg_lru = p_loc_hq_enh_base_d2d_avg_lru / repeat_number
    print('Latency: {}'.format(lat_avg_lru))
    print('PlocSQ: {}'.format(p_loc_sq_avg_lru))
    print('PlocHQ: {}'.format(p_loc_hq_avg_lru))
    print('PlocHQ(enh(loc)|base(loc)): {}'.format(p_loc_hq_enh_base_avg_lru))
    print('PlocHQ(enh(loc)|base(D2D)): {}'.format(p_loc_hq_enh_base_d2d_avg_lru))


    lat_avg_lfu = 0
    p_loc_sq_avg_lfu = 0
    p_loc_hq_avg_lfu = 0
    p_loc_hq_enh_base_avg_lfu = 0
    p_loc_hq_enh_base_d2d_avg_lfu = 0
    for i in range(repeat_number):
        lat_avg_lfu = lat_avg_lfu + lat_results_lfu[i]
        p_loc_sq_avg_lfu = p_loc_sq_avg_lfu + p_loc_sq_lfu[i]
        p_loc_hq_avg_lfu = p_loc_hq_avg_lfu + p_loc_hq_lfu[i]
        p_loc_hq_enh_base_avg_lfu = p_loc_hq_enh_base_avg_lfu + p_loc_hq_enh_loc_base_loc_lfu[i]
        p_loc_hq_enh_base_d2d_avg_lfu = p_loc_hq_enh_base_d2d_avg_lfu + p_loc_hq_enh_loc_base_d2d_lfu[i]
    lat_avg_lfu = lat_avg_lfu / repeat_number
    p_loc_sq_avg_lfu = p_loc_sq_avg_lfu / repeat_number
    p_loc_hq_avg_lfu = p_loc_hq_avg_lfu / repeat_number
    p_loc_hq_enh_base_avg_lfu = p_loc_hq_enh_base_avg_lfu / repeat_number
    p_loc_hq_enh_base_d2d_avg_lfu = p_loc_hq_enh_base_d2d_avg_lfu / repeat_number
    print('Latency: {}'.format(lat_avg_lfu))
    print('PlocSQ: {}'.format(p_loc_sq_avg_lfu))
    print('PlocHQ: {}'.format(p_loc_hq_avg_lfu))
    print('PlocHQ(enh(loc)|base(loc)): {}'.format(p_loc_hq_enh_base_avg_lfu))
    print('PlocHQ(enh(loc)|base(D2D)): {}'.format(p_loc_hq_enh_base_d2d_avg_lfu))

    #plt.style.use('ggplot')

    label = ['My Algorithm', 'LRU', 'LFU']
    index = np.arange(len(label))
    plt.grid(True)

    plt.bar(index, [lat_avg, lat_avg_lru, lat_avg_lfu])
    plt.xlabel('Cache Algorithms', fontsize=10)
    plt.ylabel('Average Latency(sec)', fontsize=10)
    plt.xticks(index, label, fontsize=10, rotation=0)
    plt.title('Average Latency Results')
    plt.show()

    plt.grid(True)
    plt.bar(index, [p_loc_sq_avg, p_loc_sq_avg_lru, p_loc_sq_avg_lfu])
    plt.xlabel('Cache Algorithms', fontsize=10)
    plt.ylabel('Average SQ Base Local Hit Ratio', fontsize=10)
    plt.xticks(index, label, fontsize=10, rotation=0)
    plt.title('Average Local Hit Rate of SQ Request Results')
    plt.show()

    plt.grid(True)
    plt.bar(index, [p_loc_hq_avg, p_loc_hq_avg_lru, p_loc_hq_avg_lfu])
    plt.xlabel('Cache Algorithms', fontsize=10)
    plt.ylabel('Average HQ Base Local Hit Ratio', fontsize=10)
    plt.xticks(index, label, fontsize=10, rotation=0)
    plt.title('Average Local Hit Rate of HQ Request Results')
    plt.show()

    plt.grid(True)
    plt.bar(index, [p_loc_hq_enh_base_avg, p_loc_hq_enh_base_avg_lru, p_loc_hq_enh_base_avg_lfu])
    plt.xlabel('Cache Algorithms', fontsize=10)
    plt.ylabel('PlocHQ(enh(loc)|base(loc))', fontsize=10)
    plt.xticks(index, label, fontsize=10, rotation=0)
    plt.title('Average PlocHQ(enh(loc)|base(loc))')
    plt.show()

    plt.grid(True)
    plt.bar(index, [p_loc_hq_enh_base_d2d_avg, p_loc_hq_enh_base_d2d_avg_lru, p_loc_hq_enh_base_d2d_avg_lfu])
    plt.xlabel('Cache Algorithms', fontsize=10)
    plt.ylabel('PlocHQ(enh(loc)|base(D2D))', fontsize=10)
    plt.xticks(index, label, fontsize=10, rotation=0)
    plt.title('Average PlocHQ(enh(loc)|base(D2D))')
    plt.show()



print_results()
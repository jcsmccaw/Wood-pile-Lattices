from numpy import array, linspace, floor_divide
from gcode_parsing_functions import *

bound_x = array([50, 60]) # mm
bound_y = array([50, 60]) # mm
height = 5 # mm

first_layer = 0.2 # mm
layer_height = 0.3 # mm
layers = int(floor_divide(height, layer_height))
num_trace_x = 8
num_trace_y = num_trace_x

offset = (bound_x[1] - bound_x[0])/float(num_trace_x)
traverse_height = 4 # mm
E = 0
restart_time = 0

lattice_file = 'wood_lattice.gcode'


x_index = linspace(bound_x[0], bound_x[1], num_trace_x)
y_index = linspace(bound_y[0], bound_y[1], num_trace_y)
z_index = linspace(first_layer, height, layers)

# Open file:
with open(lattice_file, 'w+') as out:
    for j in range(layers):
        if(j%2 == 0): # Even-numbered layer, so we'll do offset alignment:
            # X DIRECTION
                # Go to first corner:
            line = create_line([None, None, z_index[j]+traverse_height])
            output_line(out, line)
            line = create_line([x_index[0], y_index[0]+offset, z_index[j]+traverse_height])
            output_line(out, line)
            line = create_line([None, None, z_index[j]])
            output_line(out,line)
            for i in range(len(y_index-1)):
                if((i%2) == 0): # even-numbered line, go left-to-right
                    line= create_line([bound_x[1], y_index[i]+offset, None])
                    fan_on(out, restart_time)
                    output_line(out, line)
                    fan_off(out) # FIXME: This will need to be adjusted to connect the traces. 
                    curr_x = bound_x[1]
                else: # odd-numbered line, go right-to-left
                    fan_on(out, restart_time)
                    line = create_line([bound_x[0], y_index[i]+offset, None])
                    output_line(out,line)
                    fan_off(out)
                    curr_x = bound_x[0]
                # move up in the y if we haven't reached the last one:
                if(i != num_trace_y-1):
                    line = create_line([curr_x, y_index[i+1]+offset, None])
                    output_line(out, line)
            # Y DIRECTION
                # Go to first corner:
            line = create_line([None, None, z_index[j] + traverse_height])
            output_line(out, line)
            line = create_line([x_index[0]+offset, y_index[0], z_index[j] + traverse_height])
            output_line(out, line)
            line = create_line([None, None, z_index[j]])
            output_line(out, line)

            for i in range(len(x_index-1)):
                if((i%2) == 0): # even-numbered line, go left-to-right
                    fan_on(out, restart_time)
                    line= create_line([x_index[i]+offset, bound_y[1], None])
                    output_line(out, line)
                    fan_off(out)
                    curr_y = bound_y[1]
                else:
                    fan_on(out, restart_time)
                    line = create_line([x_index[i]+offset, bound_y[0], None])
                    output_line(out,line)
                    fan_off(out)
                    curr_y = bound_y[0]
                # move up in the y if we haven't reached the last one:
                if(i != num_trace_x-1):
                    line = create_line([x_index[i+1]+offset, curr_y, None])
                    output_line(out, line)

        else: # Original aligment:
            # X DIRECTION
                # Go to first corner:
            line = create_line([None, None, z_index[j]+traverse_height])
            output_line(out, line)
            line = create_line([x_index[0], y_index[0], z_index[j]+traverse_height])
            output_line(out, line)
            line = create_line([None, None, z_index[j]])
            output_line(out,line)
            for i in range(len(y_index)):
                if((i%2) == 0): # even-numbered line, go left-to-right
                    line= create_line([bound_x[1], y_index[i], None])
                    fan_on(out, restart_time)
                    output_line(out, line)
                    fan_off(out) # FIXME: This will need to be adjusted to connect the traces. 
                    curr_x = bound_x[1]
                else:
                    fan_on(out, restart_time)
                    line = create_line([bound_x[0], y_index[i], None])
                    output_line(out,line)
                    fan_off(out)
                    curr_x = bound_x[0]
                # move up in the y if we haven't reached the last one:
                if(i != num_trace_y-1):
                    line = create_line([curr_x, y_index[i+1], None])
                    output_line(out, line)
            # Y DIRECTION
                # Go to first corner:
            line = create_line([None, None, z_index[j] + traverse_height])
            output_line(out, line)
            line = create_line([x_index[0], y_index[0], z_index[j] + traverse_height])
            output_line(out, line)
            line = create_line([None, None, z_index[j]])
            output_line(out, line)

            for i in range(len(x_index)):
                if((i%2) == 0): # even-numbered line, go left-to-right
                    fan_on(out, restart_time)
                    line= create_line([x_index[i], bound_y[1], None])
                    output_line(out, line)
                    fan_off(out)
                    curr_y = bound_y[1]
                else:
                    fan_on(out, restart_time)
                    line = create_line([x_index[i], bound_y[0], None])
                    output_line(out,line)
                    fan_off(out)
                    curr_y = bound_y[0]
                # move up in the y if we haven't reached the last one:
                if(i != num_trace_x-1):
                    line = create_line([x_index[i+1], curr_y, None])
                    output_line(out, line)
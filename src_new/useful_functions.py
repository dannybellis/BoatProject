#Authors: Fiona Shyne and London Lowmanstone

#useful functions for the entire project

#prop is short for proportion
#prop ranges from -1 to 1
#returns a value between low and high based on prop
#-1 will give low, 1 will give high
#function is linear
def value_from_prop(prop, low, high):
    #runs the function y=mx+b where slope is m=(high-1ow)/2 and y-intercept is b=(low+high)/2
    return (((high-low)/2.0)*prop) + ((low+high)/2)
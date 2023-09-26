from skimage import io as io2
from skimage import measure



def line_intensity(file):
	image=io2.imread(file)
	horz=len(image[:,0])
	vert=len(image[0,:])
	profile_rgb=measure.profile_line(image, [int(horz/2), int(0.1*vert)],[int(horz/2), int(0.9*vert)], linewidth=int(0.8*horz))
	
	#profile_intensity=profile_rgb[:,0]*0.2126+profile_rgb[:,1]*0.7152+profile_rgb[:,2]*0.0722
	profile_intensity = profile_rgb[:,0] + profile_rgb[:,1]+profile_rgb[:,2]

	I=profile_intensity[int(0.55*len(profile_intensity)):].max()
	I0=profile_intensity[:int(0.45*len(profile_intensity))].max()
	#IdI0=np.around(I/I0, 2)
	#I_1_0 = [I, I0]

	# if I>I0:
	# 	I_1_0='✅'
	# else:
	# 	I_1_0='⛔️'

	I_1_0 = round(I/I0,2)

	return (profile_intensity, I_1_0)

# if __name__ == '__main__':
# 	file ='image.jpg'
# 	intensity=line_intensity(file)

import matplotlib.pyplot as plt
 
# create data
size=[90,10]
# Create a circle for the center of the plot
my_circle=plt.Circle( (0,0), 0.7, color='white')
plt.pie(size, colors=['red','white'],startangle=90,wedgeprops={"edgecolor":"0",'linewidth': 1,
                    'linestyle': 'dashed', 'antialiased': True})
p = plt.gcf()
p.gca().add_artist(my_circle)
plt.show()



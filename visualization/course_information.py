import matplotlib.pyplot as plt

def applicants_ratio(courses):
    args = dict(alpha = 0.5, bins = 100)

    ratios = []
    for c in courses:
        if c.capacity != 0:
            ratios.append(c.num_applicants / c.capacity)
    plt.clf()   
    plt.figure(figsize=(12,8)) 
    plt.hist(ratios, **args, color="g", label = "# of applicants / capacity")
    plt.legend()
    #plt.show()
    plt.savefig('visualization/result/applicants_capacity_ratio.png', dpi=300)

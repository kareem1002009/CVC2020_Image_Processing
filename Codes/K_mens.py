def K_means(hist,No_of_groups=10) :
    # Initialize Cetroids by dividing the range of histogram to equal size Clusters
    step = int(len(hist)/No_of_groups)
    dum = [i for i in range(0,len(hist)+1,step)]
    old_centroids = np.array(dum)
    new_centroids= np.zeros_like(old_centroids)
   
    while True :
        clusters = defaultdict(list)
        #Construct dictionary contains the Clusters by subtract each histogram value from all centroids and get index of 
        # minimum result to know each histogram value closest to each cluster and append it to the list of this cluster
        for i in range(len(hist)) :
            if hist[i] == 0:
                continue
            dis = np.abs(old_centroids-i)
            index = np.argmin(dis)
            clusters[index].append(i)

        #Calculate New Centroids by making a weighted average for each cluster 
        for i,ind in clusters.items(): 
            if np.sum(hist[ind]) == 0:
                continue
            new_centroids[i] = int(np.sum(ind*hist[ind])/np.sum(hist[ind]))
        #Break if we saturated and new_centroids eqls old_centroids
        if np.array(new_centroids-old_centroids).any() == False :
            break ;
        old_centroids = new_centroids
    return new_centroids

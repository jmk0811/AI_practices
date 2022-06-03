import numpy as np
import numpy.random as nr
import copy

class KMeans(object):
    def __init__(self, data, gt, k):
        self.data = data
        self.gt = gt
        self.k = k
        self.dim = len(self.data[0])
        
    def dist(self, a, b):
        if len(a) != len(b): return -1
        dim = len(a)
        sum = 0
        dist = 0
        for i in range(0, dim):
            sum += (a[i] - b[i]) ** 2
        dist = np.sqrt(sum)
        return dist

    def run(self):
        # Choose k random points
        clusters = []
        chosen_idx = []
        for i in range(0, self.k):
            rand = nr.randint(len(self.data))
            clusters.append([])
            clusters[i].append(self.data[rand].tolist())
            chosen_idx.append(rand)

        # print(clusters)
        # print(chosen_idx)
        
        # Calculate the distances of each point and assign them to the closest cluster
        min_cluster_idx = 0
        min_dist = float("inf")
        for idx, data in enumerate(self.data):
            data = data.tolist()
            for i in range(0, self.k):
                if idx in chosen_idx: continue
                else:
                    dist = self.dist(data, clusters[i][0])
                    if min_dist > dist:
                        min_dist = dist
                        min_cluster_idx = i
            
            if idx not in chosen_idx:
                clusters[min_cluster_idx].append(data)
           
        '''
        print("<Initial selection>")
        for i in range(0, self.k):
            print("Cluster {}: {}".format(i, len(clusters[i])))
        '''
        
        # Repeat assignment until converge
        converged = False
        cnt = 0
        while not converged:
            '''
            print("<Iteration>")
            for i in range(0, self.k):
                print("Cluster {}: {}".format(i, len(clusters[i])))
            '''
                
            # Calculate the mean of each cluster
            mean = []
            for i in range(0, self.k):
                # print(len(clusters[i]))
                mean.append([])
                sum = 0
                for j in range(0, self.dim): # dim = 10
                    for point in clusters[i]:
                        sum += point[j]
                    
                    if len(clusters[i]) == 0: mean[i].append(0)
                    else: mean[i].append(sum / len(clusters[i]))
            
            '''
            print("<mean calculation>")
            for i in range(0, self.k):
                print("mean {}: {}".format(i, len(mean[i])))
            print("mean list: {}".format(mean))
            '''
        
            # Repeat cluster assignments
            updated = False
            min_cluster_idx = 0
            min_dist = float("inf")
            for idx, data in enumerate(self.data):
                data = data.tolist()
                for i in range(0, self.k):
                    dist = self.dist(data, mean[i])
                    if min_dist > dist:
                        min_cluster_idx = i
                        min_dist = dist
                        
                if data in clusters[min_cluster_idx]:
                    continue # data not moved to another cluster
                else:
                    updated = True
                    for i in range(0, self.k):
                        if data in clusters[i]:
                            clusters[i].remove(data)
                            break
                    clusters[min_cluster_idx].append(data)
            
            # TODO: fix bug (infinite loop due to infinite cluster assignment)
            # to be removed. for now, we iterate 100 times
            if cnt >= 100:
                updated = False
            
            if not updated:
                # print("converged")
                converged = True
            cnt += 1
    
        # Evaluation
        # print("<Evaluation>")
        sil, rand = 0, 0
        
        '''
        Silhouette
        '''
        score_a = []
        score_b = []
        score_s = []
        
        # intra-cluster measure (a)
        for k in range(0, self.k):
            score_a.append([])
            for i in range(0, len(clusters[k])):
                intra_dist_sum = 0
                point_A = clusters[k][i]
                for j in range(0, len(clusters[k])):
                    if i != j:
                        point_B = clusters[k][j]
                        intra_dist_sum += self.dist(point_A, point_B)
                if len(clusters[k]) == 0: score_a[k].append(0)
                else: score_a[k].append(intra_dist_sum / len(clusters[k]) - 1) # divide dist sum by |Ck| - 1
        
        # inter-cluster measure (b)
        for k in range(0, self.k):
            score_b.append([])
            min_dist = float("inf") 
            for i in range(0, len(clusters[k])):
                inter_dist_sum = 0
                point_A = clusters[k][i]
                for l in range(0, self.k):
                    if k != l:
                        for j in range(0, len(clusters[l])):
                            point_B = clusters[l][j]
                            inter_dist_sum += self.dist(point_A, point_B)
                        if len(clusters[l]) == 0: inter_dist_avg = 0
                        else: inter_dist_avg = inter_dist_sum / len(clusters[l])
                        if min_dist > inter_dist_avg:
                            min_dist = inter_dist_avg
                score_b[k].append(min_dist)
                
        # s score
        for k in range(0, self.k):
            score_s.append([])
            for i in range(0, len(clusters[k])):
                score_s[k].append((score_b[k][i] - score_a[k][i]) / max(score_b[k][i], score_a[k][i]))
        
        final_measure = 0
        for k in range(0, self.k):
            sum_s = 0
            for i in range(0, len(score_s[k])):
                sum_s += score_s[k][i]
            if len(score_s[k]) != 0:
                final_measure += sum / len(score_s[k])
            
        sil = final_measure / self.k
        
        '''
        Rand index
        '''
        
        # TODO
        # incomplete
        
        return sil, rand
    


# Returns a numpy array of size n x d, where n is the number of samples and d is the dimensions
def read_data(filename):
    data = []
    labels = []
    with open(filename, 'r') as f:
        tmp = f.readlines()
    for line in tmp:
        toks = line.split(',')
        lbl = int(toks[0])
        dat = np.array([float(x.strip()) for x in toks[1:]])
        if len(data) == 0: data = dat
        else: data = np.vstack((data, dat))
        labels.append(lbl)
    return data, labels

def main(): 
    tr_data, tr_gt = read_data('train.csv')

    ########################## K-means clustering ######################################

    for k in [2, 3, 4]:
        kmc = KMeans(tr_data, tr_gt, k)
        silhouette, rand = kmc.run()
        print('K: {}, Silhouette: {}, Rand index: {}'.format(k, silhouette, rand))


if __name__ == '__main__':
    main()

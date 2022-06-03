import numpy as np
import numpy.random as nr
import cv2

# The size of img is w x h x channels

def conv(img, filters, stride=1, padding=0):
    (w, h, c) = img.shape
    filter = filters[0]

    ''' # blur filter
    #filter = np.ones((5, 5))
    #filter *= 0.1
    '''

    ''' # edge detection filter
    filter = [[-1, -1, -1],
              [-1, 8, -1],
              [-1, -1, -1]]
    filter = np.array(filter)
    '''

    filter_w, filter_h = filter.shape
    feat_w = ((w - filter_w + (padding * 2)) // stride ) + 1
    feat_h = ((h - filter_h + (padding * 2)) // stride ) + 1

    #padding
    img = np.pad(img, ((padding,padding),(padding,padding),(0,0)), 'constant', constant_values=0)
    #print(img.shape)

    feat = np.zeros((feat_w, feat_h, 3))
    #print(feat.shape)

    for k in range(3):  # Color channel
        for i in range(feat_w):    # feat row
            for j in range(feat_h):    # feat col
                sum = 0
                for x in range(filter_w):   # filter row
                    for y in range(filter_h):   # filter col
                        sum += filter[x][y] * img[i*stride+x][j*stride+y][k]
                feat[i][j][k] = sum

    print(feat.shape);
    return feat

def pool(img, size=2, stride=2, padding=0):
    print("pooling\n")
    (w, h, c) = img.shape
    feat_w = ((w - size + (padding * 2)) // stride ) + 1
    feat_h = ((h - size + (padding * 2)) // stride ) + 1

    print(img.shape)

    feat = np.zeros((feat_w, feat_h, 3))
    print(feat.shape)

    for k in range(3):  # Color channel
        for i in range(feat_w):    # feat row
            for j in range(feat_h):    # feat col
                max = img[i+0][j+0][k]
                for x in range(size):   # filter row
                    for y in range(size):   # filter col
                        if max < img[i*stride+x][j*stride+y][k]:
                            max = img[i*stride+x][j*stride+y][k]
                feat[i][j][k] = max

    print(feat.shape);
    return feat 

def main(imfile = '6.jpeg', outname = 'output'):
    size = 400  # Input image size (w, h)
    filter_size = 5
    num_out_maps = 10 # Number of output feature maps.
    img = cv2.imread(imfile)
    img = cv2.resize(img, (size, size))
    filters = [nr.uniform(low = -5, high = 5, size=(filter_size, filter_size)) for _ in range(num_out_maps)]

    features = np.array([])
    
    for i in range(num_out_maps): # Output each feature map to separate files
        feat = pool(conv(img, np.array([filters[i]])))
        #feat = pool(img)
        features = np.append(features, feat)
        #print(feat.shape)
        #print(features.shape)
        cv2.imwrite(outname + str(i) + '.jpeg', feat)


if __name__ == '__main__':
    main()

from skimage import feature
import numpy as np

class TextureBackground:
    """ A python implementation of a texture-based method for modelling the background.
    """
    def __init__(self, P, R, K=3, Rregion=9, Tp=0.7, Tb=1.2):
        """
        The Background models relies on adaptive LBP(local binary pattern) histograms.
        Hence, the paramters of the LBP operator must be provided.
        Additionally, proximity and background threshold are pre-setted. 
        K-means (for learning background histograms and weights) learning rates are predefined as well.
        
        Args:
            P(int): LBP parameter, Number of equaly spaced pixel on a circle of radius R around a given pixel
            R(int): LBP parameter, Radius R of a circle centered on a pixel
            Rregion(int): Radius of a circle around a pixel on which to compute a LBP histogram
            K(int): Number of model histograms
            Tp(float): Proximity Threshold
            Tb(float): Background Threshold
        """
        self.P = P
        self.R = R
        self.Rregion = Rregion
        self.K = K
        self.kmodels = np.random.rand(self.K, 2**self.P)
        # self.kweights = np.zeros(self.K)
        self.kweights = np.random.random(self.K)
        self.kweights = self.kweights/sum(self.kweights)
        self.Tp = Tp # Proximity Threshold
        self.Tb = Tb  # Background Threshold
        self.alpha_b = 0.01 # Background model learning rate
        self.alpha_w = 0.01 # Model weights learning rate
    
    def computeLBPs(self, image):
        """
        Compute Local Binary Pattern code of an image.

        Args:
            image(array): Image to process.

        Returns:
            Array with image containing the Local Binary Pattern code.
        """
        return feature.local_binary_pattern(image, self.P, self.R)
    
    @staticmethod
    def cmask(xc, yc, r, array):
        """
        Extract an approximated region containe in a circle, of center
        (xc,yc) and radius r.

        Args:
            xc(int): Abscissa of the center of the mask.
            yc(int): Oordinate of the center of the mask.
            r(int): Radius of the mask to build.
            array(array): Array from which to extract a sub array.
         Returns:
            Masked array.
        """
        nx,ny = array.shape
        y,x = np.ogrid[-xc:nx-xc,-yc:ny-yc]
        mask = x*x + y*y <= r*r

        return array[mask]
    
    @staticmethod
    def proximity(a, b):
        """
        Compute the proximity measure between two histograms.
        The histograms intersection was chosen as the core measure,
        this measure indeed calculate the common part of two histograms.

        Args:
            a(array): Histogram
            b(array): Histogram
        
        Returns:
            Measure of proximity between a and b
        """
        return sum([min(a[n], b[n]) for n in range(0, len(a))])

    def learn_kmodel(self, lbpregion, eps=1e-7):
        """
        Learn kmodel over the feature vectors of a particular region.
        Consider a region around a pixel then compute the LBP over the pixels of that region,
        then, compute the histogram over that new lbp. This histogram is the feature vector used
        to update the models and associated weights thanks to kmeans algorithm.

        Args:
            lbpregion(array): A region around a given pixel.
        
        Returns:
            (models, weights): Updated model and weights.
        """

        # Calculate histograms over the given region
        (h,_) = np.histogram(lbpregion, bins=np.arange(0, 2**self.P+1))
        h = h.astype("float")
        h /= (h.sum()+eps)

        # First stage of processing 
        # Comparison to the current k-model histograms 
        proximities = [self.proximity(h, self.kmodels[k,:]) for k in range(0, self.kmodels.shape[0])]

        # Background modelling
        if max(proximities) < self.Tp:
            # If the proximity is below Tp for all models
            # The model histogram with the lowest weight is replaced with h
            self.kmodels[self.kweights == min(self.kweights)] = h
            self.kweights[self.kweights == min(self.kweights)] = 0.01
        else:
            # Select the kmodel with the highest proximity value
            # Perform kmeans
            self.kmodels[proximities.index(max(proximities))] = self.alpha_b*h + (1 - self.alpha_b)* self.kmodels[proximities.index(max(proximities))]
            M = np.zeros(self.K)
            M[proximities.index(max(proximities))] = 1
            self.kweights = (1 - self.alpha_w)*self.kweights + self.alpha_w*M

        return (self.kmodels, self.kweights)

    def background_modelling(self, lbps):
        """
        Learn the kmodel over a whold preprocessed image

        Args:
            lbps(array): Image processed with a LBP operator
        """
        m,n = lbps.shape
        for (x,y), value in np.ndenumerate(lbps):
            if self.Rregion-1 < x <= m-self.Rregion and self.Rregion-1 < y <= n-self.Rregion:
                self.learn_kmodel(self.cmask(x, y, self.Rregion, lbps))

        print(self.kweights)
        return (self.kmodels, self.kweights)
    
    def foreground_detection(self, lbps, gray, eps=1e-7):
        """
        Labels pixels as belonging to the background or no.

        Args:
            lbps(array): Image processed with the LBP operator
            eps(float): Constant to avoid division by zero 
        
        Returns:
            Labelled image i.e in which the background region are black
        """
        imagelabelled = gray
        m,n = lbps.shape

        # Selecting background models
        # First, sort the weights in decreasing order
        idx_sorted = self.kweights.argsort()[::-1]
        weights_sorted = self.kweights[idx_sorted]
        
        # Selected the index corresponding to the B-first models
        # s.t sum(weights, k=0..B) > Tb
        b = 1
        for k in range(1, len(weights_sorted)-1):
            b = k
            if sum(weights_sorted[0:k]) > self.Tb:
                break
        
        for (x,y), value in np.ndenumerate(lbps):
            if self.Rregion-1 < x <= m-self.Rregion and self.Rregion-1 < y <= n-self.Rregion:
                (h,_) = np.histogram(self.cmask(x, y, self.Rregion, lbps),
                    bins=np.arange(0, 2**self.P+1))
                h = h.astype("float")
                h /= (h.sum()+eps)

                # First stage of processing 
                # Comparison to the current k-model histograms 
                proximities = np.array([self.proximity(h, kmodel) for kmodel in self.kmodels[idx_sorted[0:b]]])

                # Labelling pixel
                if max(proximities >= self.Tp):
                    imagelabelled[x, y] = 0

        return imagelabelled
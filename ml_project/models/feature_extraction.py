from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_array
from ml_project.models import utils
import numpy as np
import cv2

class IntensityHistogram(BaseEstimator, TransformerMixin):
    """Feature from intensity histogram of 3D images"""

    # divide 3d image into cells and make histogram per cell
    def __init__(self,
                 x_cell_number=8,
                 y_cell_number=8,
                 z_cell_number=8,
                 bin_number=45):

        # image dimension
        self.imageDimX = utils.Constants.IMAGE_DIM_X
        self.imageDimY = utils.Constants.IMAGE_DIM_Y
        self.imageDimZ = utils.Constants.IMAGE_DIM_Z
        self.histBinMax = utils.Constants.IMAGE_VALUE_MAX

        # member variables
        self.x_cell_number = x_cell_number
        self.y_cell_number = y_cell_number
        self.z_cell_number = z_cell_number
        self.bin_number = bin_number

    def fit(self, X, y=None):

        print("------------------------------------")
        print("IntensityHistogram fit")
        print("cell numbers = {}x{}x{}".format(self.x_cell_number,
                                               self.y_cell_number,
                                               self.z_cell_number))
        print("bin numbers = {}".format(self.bin_number))

        # no internal variable
        X = check_array(X)

        return self

    def transform(self, X, y=None):

        X = check_array(X)
        n_samples, n_features = np.shape(X)

        print("------------------------------------")
        print("IntensityHistogram transform")
        print("shape of X before transform : ")
        print(X.shape)

        X_3D = np.reshape(X, (-1,
                              self.imageDimX,
                              self.imageDimY,
                              self.imageDimZ))

        # cell (contains index of voxels) as bin edge
        x_cell_edges = np.linspace(0,
                                   self.imageDimX,
                                   self.x_cell_number + 1,
                                   dtype=int)
        y_cell_edges = np.linspace(0,
                                   self.imageDimY,
                                   self.y_cell_number + 1,
                                   dtype=int)
        z_cell_edges = np.linspace(0,
                                   self.imageDimZ,
                                   self.z_cell_number + 1,
                                   dtype=int)

        # histograms
        histogram = np.zeros((n_samples,
                              self.x_cell_number,
                              self.y_cell_number,
                              self.z_cell_number,
                              self.bin_number))

        for i in range(0, n_samples):
            image_3D = X_3D[i, :, :, :]

            for xi in range(0, x_cell_edges.size - 1):
                for yi in range(0, y_cell_edges.size - 1):
                    for zi in range(0, z_cell_edges.size - 1):

                        # image block for histogram
                        image_block = image_3D[x_cell_edges[xi]:x_cell_edges[xi+1],
                                      y_cell_edges[yi]:y_cell_edges[yi+1],
                                      z_cell_edges[zi]:z_cell_edges[zi+1]]

                        # histogram
                        histogram[i, xi, yi, zi, :], bins = \
                            np.histogram(image_block, bins=np.linspace(0, self.histBinMax, self.bin_number + 1))

        X_new = np.reshape(histogram, (n_samples, -1))

        print("shape of X after transform : ")
        print(X_new.shape)

        return X_new


class IntensityMean(BaseEstimator, TransformerMixin):
    """mean of each cell area"""

    def __init__(self, x_cell_number=8, y_cell_number=8, z_cell_number=8):
        # image dimension
        self.imageDimX = utils.Constants.IMAGE_DIM_X
        self.imageDimY = utils.Constants.IMAGE_DIM_Y
        self.imageDimZ = utils.Constants.IMAGE_DIM_Z

        self.x_cell_number = x_cell_number
        self.y_cell_number = y_cell_number
        self.z_cell_number = z_cell_number

    def fit(self, X, y=None):
        print("------------------------------------")
        print("IntensityMean fit")
        print("cell numbers = {}x{}x{}".format(self.x_cell_number,
                                               self.y_cell_number,
                                               self.z_cell_number))

        X = check_array(X)

        return self

    def transform(self, X, y=None):
        print(X.shape)

        print("------------------------------------")
        print("IntensityMean transform")
        print("shape of X before transform : ")

        X = check_array(X)
        n_samples, n_features = np.shape(X)

        X_3D = np.reshape(X, (-1,
                              self.imageDimX,
                              self.imageDimY,
                              self.imageDimZ))

        # cell (contains index of voxels) as bin edge
        x_cell_edges = np.linspace(0,
                                   self.imageDimX,
                                   self.x_cell_number + 1,
                                   dtype=int)
        y_cell_edges = np.linspace(0,
                                   self.imageDimY,
                                   self.y_cell_number + 1,
                                   dtype=int)
        z_cell_edges = np.linspace(0,
                                   self.imageDimZ,
                                   self.z_cell_number + 1,
                                   dtype=int)

        # histograms
        values = np.zeros((n_samples,
                           self.x_cell_number,
                           self.y_cell_number,
                           self.z_cell_number))

        for i in range(0, n_samples):
            image_3D = X_3D[i, :, :, :]

            for xi in range(0, x_cell_edges.size - 1):
                for yi in range(0, y_cell_edges.size - 1):
                    for zi in range(0, z_cell_edges.size - 1):

                        # image block for histogram
                        image_block = image_3D[x_cell_edges[xi]:x_cell_edges[xi+1],
                                      y_cell_edges[yi]:y_cell_edges[yi+1],
                                      z_cell_edges[zi]:z_cell_edges[zi+1]]

                        # mean
                        values[i, xi, yi, zi] = np.average(image_block)

        X_new = np.reshape(values, (n_samples, -1))

        print("shape of X after transform : ")
        print(X_new.shape)

        return X_new


class IntensityMedian(BaseEstimator, TransformerMixin):
    """mean of each cell area"""

    def __init__(self, x_cell_number=8, y_cell_number=8,
                 z_cell_number=8):
        # image dimension
        self.imageDimX = utils.Constants.IMAGE_DIM_X
        self.imageDimY = utils.Constants.IMAGE_DIM_Y
        self.imageDimZ = utils.Constants.IMAGE_DIM_Z

        self.x_cell_number = x_cell_number
        self.y_cell_number = y_cell_number
        self.z_cell_number = z_cell_number

    def fit(self, X, y=None):
        print("------------------------------------")
        print("IntensityMedian fit")
        print("cell numbers = {}x{}x{}".format(self.x_cell_number,
                                               self.y_cell_number,
                                               self.z_cell_number))

        X = check_array(X)

        return self

    def transform(self, X, y=None):
        print(X.shape)

        print("------------------------------------")
        print("IntensityMedian transform")
        print("shape of X before transform : ")

        X = check_array(X)
        n_samples, n_features = np.shape(X)

        X_3D = np.reshape(X, (-1,
                              self.imageDimX,
                              self.imageDimY,
                              self.imageDimZ))

        # cell (contains index of voxels) as bin edge
        x_cell_edges = np.linspace(0,
                                   self.imageDimX,
                                   self.x_cell_number + 1,
                                   dtype=int)
        y_cell_edges = np.linspace(0,
                                   self.imageDimY,
                                   self.y_cell_number + 1,
                                   dtype=int)
        z_cell_edges = np.linspace(0,
                                   self.imageDimZ,
                                   self.z_cell_number + 1,
                                   dtype=int)

        # histograms
        values = np.zeros((n_samples,
                           self.x_cell_number,
                           self.y_cell_number,
                           self.z_cell_number))

        for i in range(0, n_samples):
            image_3D = X_3D[i, :, :, :]

            for xi in range(0, x_cell_edges.size - 1):
                for yi in range(0, y_cell_edges.size - 1):
                    for zi in range(0, z_cell_edges.size - 1):
                        # image block for histogram
                        image_block = image_3D[
                                      x_cell_edges[xi]:x_cell_edges[
                                          xi + 1],
                                      y_cell_edges[yi]:y_cell_edges[
                                          yi + 1],
                                      z_cell_edges[zi]:z_cell_edges[
                                          zi + 1]]

                        # mean
                        values[i, xi, yi, zi] = np.median(image_block)

        X_new = np.reshape(values, (n_samples, -1))

        print("shape of X after transform : ")
        print(X_new.shape)

        return X_new


class IntensityMeanAndMedian(BaseEstimator, TransformerMixin):
    """Union of Mean and Median"""
    def __init__(self, x_cell_number=8, y_cell_number=8,
                 z_cell_number=8):
        # image dimension
        self.imageDimX = utils.Constants.IMAGE_DIM_X
        self.imageDimY = utils.Constants.IMAGE_DIM_Y
        self.imageDimZ = utils.Constants.IMAGE_DIM_Z

        self.x_cell_number = x_cell_number
        self.y_cell_number = y_cell_number
        self.z_cell_number = z_cell_number

        self.mean = IntensityMean(x_cell_number=x_cell_number,
                                  y_cell_number=y_cell_number,
                                  z_cell_number=z_cell_number)
        self.median = IntensityMedian(x_cell_number=x_cell_number,
                                      y_cell_number=y_cell_number,
                                      z_cell_number=z_cell_number)

    def fit(self, X, y=None):
        print("------------------------------------")
        print("IntensityMeanAndMedian fit")
        print("cell numbers = {}x{}x{}".format(self.x_cell_number,
                                               self.y_cell_number,
                                               self.z_cell_number))

        X = check_array(X)

        return self

    def transform(self, X, y=None):
        X = check_array(X)

        print("------------------------------------")
        print("IntensityMeanAndMedian transform")
        print("shape of X before transform : ")
        print(X.shape)

        X_mean = self.mean.transform(X, y)
        X_median = self.median.transform(X, y)

        X_new = np.hstack((X_mean, X_median))

        print("shape of X after transform : ")
        print(X_new.shape)

        return X_new


class MeanIntensityGradient(BaseEstimator, TransformerMixin):
    """Mean Vector of Gradient for each cells"""
    # divide 3d image into cells and make histogram per cell
    def __init__(self,
                 x_cell_number=8,
                 y_cell_number=8,
                 z_cell_number=8,
                 bin_number=8):

        # image dimension
        self.imageDimX = utils.Constants.IMAGE_DIM_X
        self.imageDimY = utils.Constants.IMAGE_DIM_Y
        self.imageDimZ = utils.Constants.IMAGE_DIM_Z
        self.histBinMax = utils.Constants.IMAGE_VALUE_MAX

        # member variables
        self.x_cell_number = x_cell_number
        self.y_cell_number = y_cell_number
        self.z_cell_number = z_cell_number
        self.bin_number = bin_number

    def fit(self, X, y=None):

        print("------------------------------------")
        print("MeanIntensityGradient fit")
        print("cell numbers = {}x{}x{}".format(self.x_cell_number,
                                               self.y_cell_number,
                                               self.z_cell_number))
        print("bin numbers = {}".format(self.bin_number))

        # no internal variable
        X = check_array(X)

        return self

    def transform(self, X, y=None):

        X = check_array(X)
        n_samples, n_features = np.shape(X)

        print("------------------------------------")
        print("MeanIntensityGradient transform")
        print("shape of X before transform : ")
        print(X.shape)

        X_3D = np.reshape(X, (-1,
                              self.imageDimX,
                              self.imageDimY,
                              self.imageDimZ))

        # cell (contains index of voxels) as bin edge
        x_cell_edges = np.linspace(0,
                                   self.imageDimX,
                                   self.x_cell_number + 1,
                                   dtype=int)
        y_cell_edges = np.linspace(0,
                                   self.imageDimY,
                                   self.y_cell_number + 1,
                                   dtype=int)
        z_cell_edges = np.linspace(0,
                                   self.imageDimZ,
                                   self.z_cell_number + 1,
                                   dtype=int)

        # gradient
        gradient = np.zeros((n_samples,
                             self.x_cell_number,
                             self.y_cell_number,
                             self.z_cell_number, 3))

        histogram_bins = np.linspace(0, self.histBinMax, self.bin_number + 1)

        for i in range(0, n_samples):
            image_3D = X_3D[i, :, :, :]

            for xi in range(0, x_cell_edges.size - 1):
                for yi in range(0, y_cell_edges.size - 1):
                    for zi in range(0, z_cell_edges.size - 1):

                        # image block for histogram
                        image_block = image_3D[x_cell_edges[xi]:x_cell_edges[xi+1],
                                      y_cell_edges[yi]:y_cell_edges[yi+1],
                                      z_cell_edges[zi]:z_cell_edges[zi+1]]

                        # block gradient
                        image_gradient = np.gradient(image_block)

                        gradient[i, xi, yi, zi, 0] = np.mean(image_gradient[0])
                        gradient[i, xi, yi, zi, 1] = np.mean(image_gradient[1])
                        gradient[i, xi, yi, zi, 2] = np.mean(image_gradient[2])

        X_new = np.reshape(gradient, (n_samples, -1))

        print("shape of X after transform : ")
        print(X_new.shape)

        return X_new


class SiftDetectorXY(BaseEstimator, TransformerMixin):
    """Sift feature for each cut (plane // XY)"""

    # divide 3d image into cells and make histogram per cell
    def __init__(self, featureNumPerLayer=50):

        # image dimension
        self.imageDimX = utils.Constants.IMAGE_DIM_X
        self.imageDimY = utils.Constants.IMAGE_DIM_Y
        self.imageDimZ = utils.Constants.IMAGE_DIM_Z

        # sift
        self.sift = cv2.xfeatures2d.SIFT_create()
        self.featureNumPerLayer = featureNumPerLayer


    def fit(self, X, y=None):
        X = check_array(X)
        n_samples, n_features = np.shape(X)

        print("------------------------------------")
        print("SiftDetector fit")
        print("shape of X before transform : ")
        print(X.shape)

        # no internal variable
        X = check_array(X)

        return self

    def transform(self, X, y=None):

        X = check_array(X)
        n_samples, n_features = np.shape(X)

        print("------------------------------------")
        print("SiftDetector transform")
        print("shape of X before transform : ")
        print(X.shape)

        X_3D = np.reshape(X, (-1,
                              self.imageDimX,
                              self.imageDimY,
                              self.imageDimZ))

        X_new = np.zeros((n_samples,
                          self.imageDimZ,
                          self.featureNumPerLayer,
                          2))

        for i in range(0, n_samples):
            image_3D = X_3D[i, :, :, :]

            for zi in range(0, self.imageDimZ):
                # image block for histogram
                image_block = image_3D[:,:,zi]

                # normalize for feature
                image_block = image_block / \
                              utils.Constants.IMAGE_VALUE_MAX
                image_block = np.array(image_block * 255,
                                       dtype=np.uint8)

                kp = self.sift.detect(image_block, None)
                # kp, des = self.sift.detectAndCalculate(image_block, None)

                if len(kp) > self.featureNumPerLayer:
                    X_new[i, zi, 0:self.featureNumPerLayer, :] = \
                        np.array([keyPoint.pt for keyPoint in kp[0:self.featureNumPerLayer]])
                elif len(kp) > 0:
                    X_new[i, zi, 0:len(kp), :] = \
                        np.array([keyPoint.pt for keyPoint in kp])

        print("shape of X after transform : ")
        print(X_new.shape)

        return X_new



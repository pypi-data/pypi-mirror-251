import cv2
import numpy as np

from ._eb import *

class ebsynth:
    """
    EBSynth class provides a wrapper around the ebsynth style transfer method.

    Usage:
        ebsynth = ebsynth.ebsynth(style='style.png', guides=[('source1.png', 'target1.png'), 1.0])
        result_img = ebsynth.run()
    """
    
    def __init__(self, style, guides=[], uniformity=3500.0, 
             patchsize=5, pyramidlevels=6, searchvoteiters=12, 
             patchmatchiters=6, extrapass3x3=True, backend='cuda'):

        """
        Initialize the EBSynth wrapper.      
        :param style: path to the style image, or a numpy array.
        :param guides: list of tuples containing source and target guide images, as file paths or as numpy arrays.
        :param weight: weights for each guide pair. Defaults to 1.0 for each pair.
        :param uniformity: uniformity weight for the style transfer. Defaults to 3500.0.
        :param patchsize: size of the patches. Must be an odd number. Defaults to 5. [5x5 patches]
        :param pyramidlevels: number of pyramid levels. Larger Values useful for things like color transfer. Defaults to 6.
        :param searchvoteiters: number of search/vote iterations. Defaults to 12.
        :param patchmatchiters: number of Patch-Match iterations. Defaults to 6.
        :param extrapass3x3: whether to perform an extra pass with 3x3 patches. Defaults to False.
        :param backend: backend to use ('cpu', 'cuda', or 'auto'). Defaults to 'auto'.
        """
        #self.lock = threading.Lock()
        # Handling the style image
        if isinstance(style, (np.ndarray)):
            self.style = style
        elif isinstance(style, (str)):
            self.style = cv2.imread(style)
        elif style is None:
            print("[INFO] No Style Image Provided. Remember to add a style image to the run() method.")
        else:
            print(type(style))
            raise ValueError("style should be either a file path or a numpy array.")

        # Handling the guide images
        self.guides = []
        #self.eb = LoadDLL()
        self.runner = EbsynthRunner()
        # Store the arguments
        self.style = style
        self.guides = guides
        self.uniformity = uniformity
        self.patchsize = patchsize
        self.pyramidlevels = pyramidlevels
        self.searchvoteiters = searchvoteiters
        self.patchmatchiters = patchmatchiters
        self.extrapass3x3 = extrapass3x3

        # Define backend constants
        self.backends = {
            'cpu': EbsynthRunner.EBSYNTH_BACKEND_CPU,
            'cuda': EbsynthRunner.EBSYNTH_BACKEND_CUDA,
            'auto': EbsynthRunner.EBSYNTH_BACKEND_AUTO
        }
        self.backend = self.backends[backend]


    def clear_guide(self):
        """
        Clear all the guides.
        """
      
        self.guides = []
        
    def add_guide(self, source, target, weight=None):
        """
        Add a new guide pair.
        
        :param source: Path to the source guide image or a numpy array.
        :param target: Path to the target guide image or a numpy array.
        :param weight: Weight for the guide pair. Defaults to 1.0.
        """

    
        if not isinstance(source, (str, np.ndarray)):
            raise ValueError("source should be either a file path or a numpy array.")
        if not isinstance(target, (str, np.ndarray)):
            raise ValueError("target should be either a file path or a numpy array.")
        if not isinstance(weight, (float, int)):
            raise ValueError("weight should be a float or an integer.")
        
        weight = weight if weight is not None else 1.0
        self.guides.append((source, target, weight))

            
    def run(self):
        """
        Run the style transfer and return the result image.
        
        :return: styled image as a numpy array.
        """

        #with self.lock:
        if isinstance(self.style, np.ndarray):
            style = self.style
        else:
            style = cv2.imread(self.style)

        # Prepare the guides
        guides_processed = []
        for idx, (source, target, weight) in enumerate(self.guides):
            if isinstance(source, np.ndarray):
                source_img = source
            else:
                source_img = cv2.imread(source)
            if isinstance(target, np.ndarray):
                target_img = target
            else:
                target_img = cv2.imread(target)
            guides_processed.append((source_img, target_img, weight))
            
        # Call the run function with the provided arguments
        img, err = self.runner.run(style, guides_processed, 
                    patch_size=self.patchsize,
                    num_pyramid_levels=self.pyramidlevels,
                    num_search_vote_iters=self.searchvoteiters,
                    num_patch_match_iters=self.patchmatchiters,
                    uniformity_weight=self.uniformity,
                    extraPass3x3=self.extrapass3x3
                    )

        return img, err

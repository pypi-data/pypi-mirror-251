
import cv2

class Sequence:
    def __init__(self, begFrame, endFrame, style_start=None, style_end=None):
        self.begFrame = begFrame
        self.endFrame = endFrame

        # Check explicitly for None
        self.style_start = style_start if style_start is not None else None
        self.style_end = style_end if style_end is not None else None

        self.init = begFrame
        self.final = endFrame

        # Check if both style_start and style_end are None
        if self.style_start is None and self.style_end is None:
            raise ValueError("At least one style attribute should be provided.")

    def __str__(self):
        # Use a more informative string representation
        start_info = str(self.style_start) if self.style_start is not None else "None"
        end_info = str(self.style_end) if self.style_end is not None else "None"
        return f"Sequence: {self.begFrame} - {self.endFrame} | Style Start: {start_info} - Style End: {end_info}"

class Subsequence:
    def __init__(self, init, final, begFrame, endFrame,
                 style_start = None, style_end = None):
        self.init = init
        self.final = final
        self.begFrame = begFrame
        self.endFrame = endFrame
        self.style_start = style_start if style_start else None
        self.style_end = style_end if style_end else None
        if self.style_start is None and self.style_end is None:
                raise ValueError("At least one style attribute should be provided.")
            
    def __str__(self):
        return f"Subsequence: Init: {self.init} - {self.final} | Range: {self.begFrame} - {self.endFrame} | Styles: {self.style_start} - {self.style_end}"

class SequenceManager:
    def __init__(self, begFrame, endFrame, styles, style_indexes, imgindexes):
        self.begFrame = begFrame
        self.endFrame = endFrame
        self.styles = styles
        self.style_indexes = style_indexes
        self.imgindexes = imgindexes
        self.num_styles = len(styles)

    def _set_sequence(self):
        """
        Setup Sequence Information.
        Compares the style indexes with the image indexes to determine the sequence information.
        """
        sequences = []
        if self.num_styles == 1 and self.begFrame == self.style_indexes[0]:

            sequences.append(
                Sequence(begFrame= self.begFrame, endFrame= self.endFrame ,style_start = cv2.imread(self.styles[0])))

            return sequences
        
        if self.style_indexes[0] == self.endFrame and self.num_styles == 1:

            sequences.append(
                Sequence(begFrame= self.begFrame , endFrame= self.endFrame, style_end = self.styles[0]))
        
            return sequences
        
        for i in range(self.num_styles-1):

            # If both style indexes are not None
            if self.style_indexes[i] is not None and self.style_indexes[i+1] is not None:
                if self.style_indexes[i] == self.begFrame and self.style_indexes[i+1] == self.endFrame:
                    sequences.append(
                        Sequence(self.begFrame, self.endFrame, self.styles[i], self.styles[i+1]))

                # If the first style index is the first frame in the sequence
                elif self.style_indexes[i] == self.begFrame and self.style_indexes[i+1] != self.endFrame:
                    sequences.append(Sequence(
                        self.begFrame, self.style_indexes[i+1], self.styles[i], self.styles[i+1]))

                # If the second style index is the last frame in the sequence
                elif self.style_indexes[i] != self.begFrame and self.style_indexes[i+1] == self.endFrame:
                    sequences.append(Sequence(
                        self.style_indexes[i], self.endFrame, self.styles[i], self.styles[i+1]))

                elif self.style_indexes[i] != self.begFrame and self.style_indexes[i+1] != self.endFrame and self.style_indexes[i] in self.imgindexes and self.style_indexes[i+1] in self.imgindexes:
                    sequences.append(Sequence(
                        self.style_indexes[i], self.style_indexes[i+1], self.styles[i], self.styles[i+1]))

        return sequences
    
    @staticmethod
    def generate_subsequences(sequence, chunk_size = 10, overlap = 1):
        subsequences = []
        init = sequence.begFrame
        final = sequence.endFrame
        begFrame = init
        last_endFrame = None  # Keep track of the last endFrame
        
        while begFrame < final:
            endFrame = min(begFrame + chunk_size + overlap, final)
            
            # If remaining frames are less than chunk size and already covered by previous subsequence
            if (final - begFrame < chunk_size) and (last_endFrame is not None and last_endFrame >= final):
                break

            # Create a subsequence
            subseq = Subsequence(init, final, begFrame, endFrame,
                                sequence.style_start if sequence.style_start else None,
                                sequence.style_end if sequence.style_end else None)
            subsequences.append(subseq)
            last_endFrame = endFrame  # Update last_endFrame

            # Update begFrame for the next iteration
            new_begFrame = endFrame - overlap

            # Check to prevent infinite loop
            if new_begFrame <= begFrame:
                break

            begFrame = new_begFrame

        return subsequences

    def __call__(self, chunk_size = 10, overlap = 1):
        sequences = self._set_sequence()
        subsequences = []
        for sequence in sequences:
            subsequences += self.generate_subsequences(sequence, chunk_size, overlap)
        return subsequences
    
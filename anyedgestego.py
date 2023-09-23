import math
import numpy as np
from PIL import Image, ImageFilter
from binaryFunc import text2binary, binary2text


class EdgeStego:
    def __init__(self, operation, input_filename, input_text=None, bits_to_decode=None, output_filename=None):
        """
        Initializes the object with the given operation and filename.

        :param operation: A string representing the operation to be performed. Must be either "encode" or "decode".
        :param input_filename: A string representing the path to the image file.
        """
        if operation == "encode":
            self.input_filename = input_filename
            self.output_path = output_filename
            self.base_image = self.read_image(input_filename)
            self.base_image_binary = self.image_to_binary(self.base_image)
            self.edges = self.edge_detector(self.base_image_binary)
            self.list_of_indices = self.list_edge_indices(self.edges)
            self.num_of_chars_possible = self.num_of_chars_possible(self.list_of_indices)
            self.blue_channel_array = self.get_blue_channel_array(self.base_image)
            self.r, self.g, self.b = self.get_all_ch_vector(self.base_image)
            self.blue_channel_values_binary = self.get_blue_channel_values_binary(self.list_of_indices,
                                                                                  self.blue_channel_array)
            self.textInputString = input_text

            self.textInputString_binary = self.text_input_to_binary(self.textInputString)
            self.hiddenTextBitLength = len(self.textInputString_binary)
            self.new_blue_channel_values_binary = self.change_pixel_vals(self.textInputString_binary,
                                                                         self.blue_channel_values_binary)
            self.b_channel_copy = np.copy(self.blue_channel_array)
            self.newBlueChannel = self.new_blue_channel_array(self.new_blue_channel_values_binary, self.b_channel_copy)
        elif operation == "decode":
            self.bits_to_decode = bits_to_decode
            self.input_filename = input_filename
            self.base_image = self.read_image(input_filename)
            self.base_image_binary = self.image_to_binary(self.base_image)
            self.edges = self.edge_detector(self.base_image_binary)
            self.list_of_indices = self.list_edge_indices(self.edges)
            self.num_of_chars_possible = self.num_of_chars_possible(self.list_of_indices)
            self.blue_channel_array = self.get_blue_channel_array(self.base_image)
            self.blue_channel_values_binary = self.get_blue_channel_values_binary(self.list_of_indices,
                                                                                  self.blue_channel_array)

        elif operation == "inspect":
            self.input_filename = input_filename
            self.output_path = output_filename
            self.base_image = self.read_image(input_filename)
            self.base_image_binary = self.image_to_binary(self.base_image)
            self.edges = self.edge_detector(self.base_image_binary)
            self.list_of_indices = self.list_edge_indices(self.edges)
            self.num_of_chars_possible = self.num_of_chars_possible(self.list_of_indices)

        else:
            pass


    @staticmethod
    def edge_detector(binary):
        """Detect Edges in given image"""
        edges = np.array(binary.filter(ImageFilter.FIND_EDGES))
        return edges

    @staticmethod
    def read_image(filename):
        """Read Image"""
        image = Image.open(filename)
        image = image.convert("RGB")
        return image

    @staticmethod
    def image_to_binary(image):
        """Convert given Image to Binary"""
        gray = image.convert('L')
        # binarize the grayscale image
        threshold = 128
        binary = gray.point(lambda x: 0 if x < threshold else 255, '1')
        return binary

    @staticmethod
    def list_edge_indices(edges):
        """Get indices where pixel = 1"""
        true_indices = np.where(edges)
        list_of_indices = []
        # print the ordered list of indices
        for i in range(len(true_indices[0])):
            list_of_indices.append((true_indices[0][i], true_indices[1][i]))

        return list_of_indices

    @staticmethod
    def num_of_chars_possible(list_of_indices):
        """Get number of chars that can be encoded in a given image"""
        number_of_chars_possible = math.floor(len(list_of_indices) / 8)
        return number_of_chars_possible

    @staticmethod
    def get_blue_channel_array(image):
        """Get Blue channel"""
        r, g, b = image.split()
        b_array = np.asarray(b)
        return b_array

    @staticmethod
    def get_all_ch_vector(image):
        """Get RGB channels"""
        r, g, b = image.split()
        return r, g, b

    @staticmethod
    def get_blue_channel_values_binary(true_indices, blu_channel):
        """Get Blue channel intensity values in binary format"""
        results = []

        for idx in true_indices:
            x, y = idx
            value = blu_channel[x][y]
            value_bin = text2binary(str(value))
            results.append((idx, value, value_bin))

        return results

    @staticmethod
    def get_text_input(text_input=None):
        """Gets user input for the text to be hidden"""

        if text_input is None:
            return input("Enter text to encode into image: ")
        else:
            return text_input

    @staticmethod
    def text_input_to_binary(text):
        """Converts the input text to binary format"""
        xx = text2binary(text)
        return xx

    @staticmethod
    def change_pixel_vals(text_bin, b_val_bin):
        """Changes the pixel values in the blue channel based on the binary text"""
        new_ds_list = []

        for i in range(len(text_bin)):
            temp = b_val_bin[i]

            new_string = temp[2][:-1]
            new_string = new_string + text_bin[i]

            new_val = binary2text(new_string)
            new_ds = [temp[0], new_val, new_string]
            new_ds_list.append(new_ds)

        return new_ds_list

    @staticmethod
    def new_blue_channel_array(new_pixel_ds, blu_channel2):
        """Creates a new blue channel array with modified pixel values"""
        for x, y, z in new_pixel_ds:
            # print(x, y)
            blu_channel2[x[0]][x[1]] = y
        # print(blu_channel2)
        return blu_channel2

    def encode_image(self):
        """Encodes the hidden text in the blue channel and saves the modified image"""
        b_image_final = Image.fromarray(self.b_channel_copy)
        merged_image = Image.merge('RGB', (self.r, self.g, b_image_final))
        merged_image.save(self.output_path)

    def decode_image(self):
        """Decodes the hidden text from the blue channel of the merged image"""
        actual_ans_bin = ""
        text_length = self.bits_to_decode

        for i in range(min(len(self.blue_channel_values_binary), text_length)):
            ans = self.blue_channel_values_binary[i]
            bin_ans = ans[2][-1]
            actual_ans_bin += bin_ans
        # print(actual_ans_bin)
        actual_ans = binary2text(actual_ans_bin)
        # print(actual_ans)
        return actual_ans

    def inspect_image(self):
        return self.num_of_chars_possible

